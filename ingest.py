import os
import sqlite3
import pickle
import time
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from google.genai import types




load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "hdfc_rag" / "data"

DB_PATH = BASE_DIR / "vector_store.db"

EMBEDDING_MODEL = "gemini-embedding-001"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

BATCH_SIZE = 50



def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            file_type TEXT NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding BLOB NOT NULL
        )
    """)

    conn.commit()

    return conn




def extract_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)



# Extract TXT Text


def extract_txt_text(txt_path):

    return txt_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )



# Create Chunks


def create_chunks(text):

    text = text.replace("\x00", " ")

    text = " ".join(text.split())

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks



# Generate Embeddings with Retry


def generate_embeddings(texts):

    max_retries = 5

    for attempt in range(max_retries):

        try:

            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=texts,
                config=types.EmbedContentConfig(
                    output_dimensionality=768
                )
            )

            return [
                embedding.values
                for embedding in response.embeddings
            ]

        except Exception as e:

            error_message = str(e)

            if "429" in error_message:

                wait_time = 65

                print(
                    f"\n  Gemini quota reached."
                    f" Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

                print("  Retrying embedding request...\n")

            else:

                raise e

    raise RuntimeError(
        "Gemini embedding failed after multiple retries."
    )



# Main Ingestion


def main():

    print("\nStarting document ingestion...\n")

    conn = create_database()

    cursor = conn.cursor()

    # Clear old data before fresh ingestion
    cursor.execute("DELETE FROM documents")

    conn.commit()

    
    # Find PDFs
    

    all_files = []

    for file in DATA_DIR.glob("*.pdf"):

        all_files.append(file)

    
    # Find YouTube transcripts
    

    transcript_dir = DATA_DIR / "transcripts"

    if transcript_dir.exists():

        for file in transcript_dir.glob("*.txt"):

            all_files.append(file)

    print(f"Found {len(all_files)} source files.\n")

    total_chunks = 0

    
    # Process Files
    

    for file_path in all_files:

        print(f"Processing: {file_path.name}")

        
        # Extract text
        

        if file_path.suffix.lower() == ".pdf":

            text = extract_pdf_text(file_path)

            file_type = "PDF"

        elif file_path.suffix.lower() == ".txt":

            text = extract_txt_text(file_path)

            file_type = "YouTube Transcript"

        else:

            continue

        
        # Check text
        

        if not text.strip():

            print("  WARNING: No text found.\n")

            continue

        
        # Create chunks
        

        chunks = create_chunks(text)

        print(f"  Created {len(chunks)} chunks")

        
        # Process chunks in batches
        

        for i in range(
            0,
            len(chunks),
            BATCH_SIZE
        ):

            batch = chunks[
                i:i + BATCH_SIZE
            ]

            embeddings = generate_embeddings(batch)

            
            # Save embeddings
            

            for chunk, embedding in zip(
                batch,
                embeddings
            ):

                embedding_array = np.array(
                    embedding,
                    dtype=np.float32
                )

                cursor.execute(
                    """
                    INSERT INTO documents
                    (
                        source,
                        file_type,
                        chunk_text,
                        embedding
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        file_path.name,
                        file_type,
                        chunk,
                        pickle.dumps(
                            embedding_array
                        )
                    )
                )

                total_chunks += 1

            conn.commit()

            processed = min(
                i + BATCH_SIZE,
                len(chunks)
            )

            print(
                f"  Embedded "
                f"{processed}/{len(chunks)} chunks"
            )

            
            # Wait between batches
            

            if processed < len(chunks):

                print(
                    "  Waiting 65 seconds "
                    "before next batch..."
                )

                time.sleep(65)

        print()

    
    # Finish
    

    conn.close()

    print("=" * 50)
    print("INGESTION COMPLETE")
    print("=" * 50)

    print(
        f"Files processed : {len(all_files)}"
    )

    print(
        f"Total chunks    : {total_chunks}"
    )

    print(
        f"Database        : {DB_PATH}"
    )

    print("=" * 50)



# Run


if __name__ == "__main__":

    main()