import os
import sqlite3
import pickle
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types



load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )



client = genai.Client(api_key=API_KEY)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "vector_store.db"
)



def create_query_embedding(query):
    """
    Convert the user's question into a Gemini embedding vector.
    """

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[query],
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    embedding = np.array(
        response.embeddings[0].values,
        dtype=np.float32
    )

    return embedding



def cosine_similarity(vector1, vector2):
    """
    Calculate cosine similarity between two vectors.
    """

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(
        np.dot(vector1, vector2)
        / (norm1 * norm2)
    )



def retrieve_documents(
    query,
    top_k=5,
    source_keyword=None
):
    """
    Retrieve the most relevant document chunks.

    Parameters:
        query:
            User's question.

        top_k:
            Number of results to return.

        source_keyword:
            Optional company/source filter.

            Examples:
                "Infosys"
                "Maruti"

            If None, search the complete database.
    """


    query_embedding = create_query_embedding(
        query
    )




    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()




    if source_keyword:

        cursor.execute(
            """
            SELECT id, source, file_type,
                   chunk_text, embedding
            FROM documents
            WHERE source LIKE ?
            """,
            (f"%{source_keyword}%",)
        )

    else:

        cursor.execute(
            """
            SELECT id, source, file_type,
                   chunk_text, embedding
            FROM documents
            """
        )


    rows = cursor.fetchall()

    connection.close()


 

    results = []

    for row in rows:

        document_id = row[0]
        source = row[1]
        file_type = row[2]
        chunk_text = row[3]
        embedding_blob = row[4]

        # Convert BLOB back to numpy array
        document_embedding = pickle.loads(
            embedding_blob
        )

        # Calculate cosine similarity
        score = cosine_similarity(
            query_embedding,
            document_embedding
        )

        results.append(
            {
                "id": document_id,
                "source": source,
                "file_type": file_type,
                "chunk_text": chunk_text,
                "score": score
            }
        )


    
    # Sort by similarity
   
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


  
    # Return top K


    return results[:top_k]



# 7. Test retrieval from terminal


def main():

    print("=" * 60)
    print("HDFC AMC RAG - Document Retrieval Test")
    print("=" * 60)

    print()

    question = input(
        "Enter your question: "
    ).strip()

    if not question:

        print(
            "Please enter a question."
        )

        return

    print()

    print(
        "Searching documents..."
    )

    print()

    try:

        results = retrieve_documents(
            question,
            top_k=5
        )


        if not results:

            print(
                "No documents found."
            )

            return


        print("=" * 60)
        print("TOP RELEVANT DOCUMENT CHUNKS")
        print("=" * 60)


        for index, result in enumerate(
            results,
            start=1
        ):

            print()

            print(
                f"Result {index}"
            )

            print(
                "-" * 60
            )

            print(
                f"Similarity Score: "
                f"{result['score']:.4f}"
            )

            print(
                f"Source: "
                f"{result['source']}"
            )

            print(
                f"File Type: "
                f"{result['file_type']}"
            )

            print()

            print(
                result["chunk_text"]
            )

            print(
                "-" * 60
            )


    except Exception as error:

        print()

        print(
            "Error while retrieving documents:"
        )

        print(error)



# 8. Run retrieval test


if __name__ == "__main__":

    main()