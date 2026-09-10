
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

# HDFC AMC RAG Assistant

AI-powered Retrieval-Augmented Generation (RAG) assistant for researching public company information from **Infosys** and **Maruti Suzuki** documents.

Built for the **HDFC AMC Management Radar — Intern Build Challenge**.

## Overview

This application allows users to ask natural-language questions about company financial results, announcements, and management discussions.

It retrieves relevant document chunks from a SQLite vector database and uses Gemini to generate a grounded answer based on the retrieved information.

Questions with Answers-
1. What was Infosys revenue growth in Q1 FY27?
Infosys reported 2.4% year-on-year revenue growth in constant currency terms in Q1 FY27.

2. What was Infosys operating margin in Q1 FY27?
Infosys reported an operating margin of 21.1% in Q1 FY27.

3. What percentage of Infosys revenue came from AI services?
AI services contributed 8.2% of Infosys' overall revenue in Q1 FY27.

4. Who is the successor to Salil Parekh as Infosys CEO?
Ashiss Dash is the successor to Salil Parekh as Infosys CEO.

5. What was Maruti Suzuki's total production in August 2026?
Maruti Suzuki produced 221,613 vehicles in August 2026.

6. What was the introductory price of the e VITARA under BaaS?
The introductory price was ₹10.99 lakh plus a battery EMI of ₹3.99 per kilometre.

7. Compare Infosys Q1 FY27 performance with Maruti Suzuki August 2026 production.
Infosys reported 2.4% year-on-year revenue growth with a 21.1% operating margin, while Maruti Suzuki's August 2026 production increased by approximately 40.1% year-on-year to 221,613 vehicles.

8. What was Infosys' exact revenue from AI agents in Q1 FY27?
The information is not found in the provided documents.