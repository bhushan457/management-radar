# Development Notes

## Project

**HDFC AMC Management Radar RAG Assistant**

This project was developed for the HDFC AMC Management Radar — Intern Build Challenge.

## AI-Assisted Development

AI tools were used during development for:

- Understanding the assignment requirements
- Planning the RAG workflow
- Designing the SQLite storage approach
- Writing and improving Python code
- Debugging API and dependency issues
- Improving retrieval quality
- Designing the Streamlit interface
- Preparing project documentation

AI suggestions were reviewed, tested, and modified where required.

## Key AI Prompts Used

### 1. RAG Architecture

**Prompt:**  
"Design a simple end-to-end RAG application for company research using Python, SQLite, Gemini embeddings, cosine similarity retrieval, and Streamlit."

**Decision:**  
Accepted the overall architecture because it was simple enough to implement reliably within the assessment time.

### 2. Database Design

**Prompt:**  
"Suggest a lightweight SQLite schema for storing document chunks and embeddings for a RAG application."

**Decision:**  
Used SQLite with a `documents` table containing source, file type, chunk text, and embedding data.

### 3. Grounded Answers

**Prompt:**  
"Create a prompt for an LLM that answers only from retrieved document context and clearly says when the information is not available."

**Decision:**  
Accepted and implemented the grounding approach to reduce unsupported answers.

### 4. Comparison Retrieval

**Prompt:**  
"Improve RAG retrieval when a question compares Infosys and Maruti Suzuki so that evidence from both companies is retrieved."

**Decision:**  
Implemented company-aware retrieval. Infosys and Maruti Suzuki evidence is retrieved separately for comparison questions before being sent to the LLM.

## Important Engineering Decisions

### SQLite

SQLite was selected because the assignment requires a real database and SQLite provides a simple, portable solution for this prototype.

### Gemini Embeddings

`gemini-embedding-001` was selected for document and query embeddings.

Embeddings are stored in SQLite and compared using cosine similarity.

### Gemini LLM

`gemini-3.6-flash` is used for grounded answer generation.

### Streamlit

Streamlit was selected to build the working research interface quickly while keeping the application simple and readable.

## Debugging and Fixes

### Gemini Embedding Rate Limit

During ingestion, the Gemini embedding API reached a free-tier request limit.

**Fix:**  
Added retry/wait handling and processed embeddings in smaller batches.

The final ingestion completed successfully with **231 document chunks**.

### LLM Model Issue

The initial LLM model configuration was not available for the project.

**Fix:**  
Updated the application to use `gemini-3.6-flash`.

### Comparison Retrieval Issue

Initial comparison retrieval could return stronger evidence from only one company.

**Fix:**  
Added company-specific retrieval for Infosys and Maruti Suzuki and combined the retrieved evidence before generation.

## Accepted Suggestions

The following AI-assisted suggestions were implemented:

- RAG-based document retrieval
- SQLite database storage
- Gemini embeddings
- Cosine similarity search
- Company-aware comparison retrieval
- Grounded LLM responses
- Streamlit interface
- Environment-variable API key management
- `.gitignore` for secrets and local files
- README and development documentation

## Rejected / Not Implemented

Some features were considered but were not implemented because the priority was to deliver a working end-to-end prototype within the assessment time:

- PDF page-number citations
- YouTube timestamp citations
- Automated topic tagging
- Separate AI summary storage
- Advanced vector database infrastructure
- Automated live-source fetching
- Raw video storage

These are documented as limitations rather than being claimed as implemented features.

## Data Issue

One supplied Maruti Suzuki Q4 FY26 BSE PDF could not be downloaded successfully.

Rather than using an unreliable or fabricated source, it was excluded from the current indexed dataset.

The remaining available sources were processed successfully.

## Security

The Gemini API key is stored in `.env` and is not hard-coded.

`.env` is excluded from Git.

Raw videos are not stored in the repository.

Retrieved document content is treated as untrusted data and is provided to the LLM as context rather than as executable instructions.

## Git Development

Git is being used as the development diary.

Changes are committed as the project progresses so the repository history reflects the development process and major fixes.

The `.git` history is retained for submission.

## Current Dataset

- 2 companies
- 9 available/indexed sources
- 6 PDFs
- 3 transcript TXT files
- 231 indexed chunks

Companies:

- Infosys
- Maruti Suzuki

## Deliberate Scope Cut

The main priority was a working end-to-end pipeline:

**data → database → retrieval → grounded answer → frontend**

Advanced features such as page/timestamp citations and automated summaries/tags were left out rather than risking an unstable implementation within the assessment time.

## Final Verification

Before submission:

- [ ] Application runs successfully
- [ ] SQLite database is populated
- [ ] Cached PDFs/transcripts are included
- [ ] README is complete
- [ ] NOTES.md is included
- [ ] `.env` is not committed
- [ ] No API key is exposed
- [ ] Git history is preserved
- [ ] Demo recording/link is added
- [ ] Repository is made public only at final submission

---