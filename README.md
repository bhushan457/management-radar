# HDFC AMC RAG Assistant

AI-powered Retrieval-Augmented Generation (RAG) assistant for researching public company information from **Infosys** and **Maruti Suzuki** documents.

Built for the **HDFC AMC Management Radar — Intern Build Challenge**.

## Overview

This application allows users to ask natural-language questions about company financial results, announcements, and management discussions.

It retrieves relevant document chunks from a SQLite vector database and uses Gemini to generate a grounded answer based on the retrieved information.

## Features

- PDF and TXT document extraction
- Text chunking
- Gemini embeddings
- SQLite vector database
- Cosine-similarity retrieval
- Company-aware retrieval for Infosys and Maruti Suzuki comparisons
- Grounded Gemini answers
- Source and relevance-score display
- Streamlit web interface
- API error handling

## RAG Architecture

```text
Company Documents
       ↓
PDF / TXT Extraction
       ↓
Text Chunking
       ↓
Gemini Embeddings
       ↓
SQLite Vector Database
       ↓
User Question
       ↓
Query Embedding
       ↓
Cosine Similarity Retrieval
       ↓
Relevant Chunks
       ↓
Gemini LLM
       ↓
Grounded Answer + Sources

For comparison questions, Infosys and Maruti Suzuki documents are retrieved separately before generating the answer.

Data Sources

Current dataset:

2 companies
9 sources
6 PDF files
3 transcript TXT files
231 indexed chunks
Infosys
Q1 FY27 results / earnings material
CEO succession announcement
Collaboration announcement
Management interview transcripts
Maruti Suzuki
Q1 FY27 results
e-VITARA announcement
August 2026 production report
Management interview transcript

One Maruti Suzuki Q4 FY26 BSE PDF could not be downloaded successfully and is not included.

Technology Stack
Component	Technology
Language	Python
Frontend	Streamlit
Database	SQLite
Embeddings	Gemini gemini-embedding-001
LLM	Gemini gemini-3.6-flash
PDF Processing	pypdf
Vector Operations	NumPy
Configuration	python-dotenv
Project Structure
HDFC AMC/
│
├── app.py
├── ingest.py
├── retrieve.py
├── requirements.txt
├── README.md
├── NOTES.md
├── .gitignore
├── vector_store.db
│
└── hdfc_rag/
    └── data/
        ├── Infosys- 1.pdf
        ├── Infosys- 2.pdf
        ├── Infosys- 3.pdf
        ├── Maruti Suzuki- 1.pdf
        ├── Maruti Suzuki- 2.pdf
        ├── Maruti Suzuki- 3.pdf
        └── transcripts/
            ├── infosys_salil_parekh_1.txt
            ├── infosys_salil_parekh_2.txt
            └── maruti_rc_bhargava.txt
Database

SQLite is used to store document chunks and embeddings.

Current documents table:

Column	Description
id	Unique chunk ID
source	Source filename
file_type	File type
chunk_text	Document text chunk
embedding	Stored embedding vector

Retrieval uses cosine similarity between the user's question embedding and stored document embeddings.

Setup
1. Clone the repository
git clone https://github.com/bhushan457/management-radar.git
cd management-radar
2. Create virtual environment
python -m venv venv

Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure Gemini API key

Create .env in the project root:

GEMINI_API_KEY=your_api_key_here

Never commit .env or expose the API key.

5. Run the application

The populated vector_store.db is included.

streamlit run app.py

Open:

http://localhost:8501
Rebuild Database

If required, rebuild the vector database from the cached documents:

python ingest.py

This performs:

PDF / TXT
   ↓
Text Extraction
   ↓
Chunking
   ↓
Gemini Embeddings
   ↓
SQLite Vector Database
Example Questions
What was Infosys revenue growth in Q1 FY27?
What was Infosys operating margin in Q1 FY27?
What percentage of Infosys revenue came from AI services?
Who is the successor to Salil Parekh as Infosys CEO?
What was Maruti Suzuki's total production in August 2026?
What was the introductory price of the e VITARA under BaaS?
Compare Infosys Q1 FY27 performance with Maruti Suzuki August 2026 production.
Grounded Answers

The application instructs Gemini to:

Use retrieved document content only
Avoid inventing facts or numbers
Provide exact numbers when available
State when information is unavailable
Handle Infosys and Maruti Suzuki comparison questions separately

The UI displays the retrieved sources and relevance scores.

Security
API keys are stored in .env
.env is excluded using .gitignore
API keys are not hard-coded
venv/ and Python cache files are excluded
Retrieved document content is treated as data rather than instructions
Known Limitations

This is a focused 24-hour prototype.

Current SQLite schema focuses on document chunks and embeddings.
Source display currently uses filenames and relevance scores.
PDF page-number and YouTube timestamp citations are not implemented.
Automated summaries and topic tags are not implemented as a separate database/UI feature.
One supplied Maruti Suzuki Q4 FY26 PDF could not be downloaded and is not included.
Gemini free-tier quota limits can affect repeated API testing.
AI-Assisted Development

AI assistance was used for architecture, implementation, debugging, retrieval logic, prompt design, UI development, and documentation.

Important prompts, decisions, accepted/rejected suggestions, and fixes are documented in NOTES.md.

Demo

3-minute screen recording:

TODO: Add demo video link before final submission.
Future Improvements
Add document metadata such as dates and URLs
Add PDF page-number citations
Add transcript timestamp citations
Add summaries and topic tags
Add company timeline
Add management promise tracking
Add management consistency analysis
Add latest-data fetching