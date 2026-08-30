# 🤖 RepoMind AI

### AI-Powered GitHub Repository RAG Assistant

RepoMind AI is a code-aware Retrieval-Augmented Generation (RAG) assistant that allows users to connect a GitHub repository and ask natural-language questions about its source code.

Instead of sending an entire repository directly to an LLM, RepoMind parses the repository, extracts functions and classes, creates semantic embeddings, stores them in Qdrant, retrieves the most relevant code, reranks the results, and generates a grounded answer using Mistral.

---

## ✨ Features

- 🔗 GitHub repository ingestion
- 🐍 Python source-code parsing using Tree-sitter
- 🧩 Function and class-level code chunking
- 🧠 Semantic code embeddings using Sentence Transformers
- 🔎 Vector similarity search using Qdrant
- 🎯 Retrieval reranking for better source selection
- 🚫 Reduces irrelevant test/example results for definition questions
- 🤖 Mistral-powered answer generation
- 📚 Source-aware answers with file paths and line numbers
- 🖥️ Interactive Streamlit interface
- 💻 CLI interface through `ask.py`
- 🔐 Environment-variable based API key configuration

---

## 🏗️ Architecture

```text
                GitHub Repository
                       │
                       ▼
                ┌──────────────┐
                │ Repo Loader  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ File Scanner │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Tree-sitter  │
                │    Parser    │
                └──────┬───────┘
                       │
                Functions / Classes
                       │
                       ▼
                ┌──────────────┐
                │ Code Chunker │
                └──────┬───────┘
                       │
                       ▼
             ┌─────────────────────┐
             │ Sentence Transformer│
             │    Embeddings       │
             └──────────┬──────────┘
                        │
                        ▼
                 ┌────────────┐
                 │   Qdrant   │
                 │ Vector DB  │
                 └─────┬──────┘
                       │
                 User Question
                       │
                       ▼
                Query Embedding
                       │
                       ▼
              Retrieve Top Candidates
                       │
                       ▼
                   Reranking
                       │
                       ▼
                 Top 3 Results
                       │
                       ▼
                 RAG Prompt
                       │
                       ▼
                   Mistral LLM
                       │
                       ▼
              Answer + Code Sources
```
🔄 How RepoMind Works
1. Clone Repository

The user provides a GitHub repository URL.

RepoMind downloads the repository locally.

2. Scan Source Files

The file scanner identifies supported source files from the repository.

3. Parse Code

Tree-sitter analyzes Python source files and extracts:

Classes
Functions
Methods
Source locations
4. Create Code Chunks

RepoMind creates semantic chunks around classes and functions.

Each chunk contains metadata such as:

File path
Symbol name
Symbol type
Start line
End line
Source code
5. Generate Embeddings

Each code chunk is converted into a vector representation using Sentence Transformers.

6. Store in Qdrant

The vectors and metadata are stored in the local Qdrant vector database.

The project uses:

Collection: repomind_code
Vector size: 384
Distance: Cosine
7. Retrieve Relevant Code

When a user asks a question, the question is converted into an embedding.

RepoMind retrieves multiple candidate chunks from Qdrant.

The system retrieves more candidates than the final answer needs so that relevant production code is not lost during the initial similarity search.

8. Rerank Results

RepoMind applies additional ranking logic.

For definition-style questions, production source code is preferred over:

tests/
test/
examples/
example/

It also boosts:

/src/ source files
Exact symbol-name matches
9. Generate Answer

The highest-ranked code chunks are inserted into a RAG prompt.

Mistral generates the final answer using the retrieved repository context.

10. Display Sources

RepoMind displays the relevant:

File
Symbol
Line numbers
Similarity score
Retrieved source code
🧠 Example

Question:

What does the Flask class inherit from?

RepoMind retrieves the relevant source:

class Flask(App):

and produces:

The Flask class inherits from the App class.

File: src/flask/app.py
Line: 110

This allows the answer to be traced back to the repository source.

🛠️ Tech Stack
Technology	Purpose
Python	Core application
Streamlit	Web interface
Tree-sitter	Source-code parsing
Sentence Transformers	Code embeddings
Qdrant	Vector database
Mistral	LLM generation
LangChain	LLM integration
GitPython	GitHub repository cloning
📁 Project Structure
REPOMIND-AI/
│
├── app.py
├── ask.py
├── check_qdrant.py
├── reset_qdrant.py
│
├── requirements.txt
├── .env.example
├── .gitignore
│
├── backend/
│   │
│   ├── chunking/
│   │   └── code_chunker.py
│   │
│   ├── embeddings/
│   │   └── embedding_model.py
│   │
│   ├── ingestion/
│   │   ├── file_scanner.py
│   │   └── repo_loader.py
│   │
│   ├── llm/
│   │   └── mistral_model.py
│   │
│   ├── parser/
│   │   └── code_parser.py
│   │
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   └── rag_prompt.py
│   │
│   └── vectorstore/
│       └── qdrant_store.py
│
├── tests/
│   ├── test_llm.py
│   ├── test_prompt.py
│   ├── test_qdrant.py
│   ├── test_qdrant_search.py
│   ├── test_reindex.py
│   ├── test_repo_chunking.py
│   ├── test_repo_embeddings.py
│   ├── test_repo_loader.py
│   ├── test_repo_parser.py
│   ├── test_repo_qdrant.py
│   ├── test_repo_scan.py
│   ├── test_repo_search.py
│   └── test_single_file.py
│
└── data/
⚙️ Installation
1. Clone the repository
git clone https://github.com/Shaiksyed097/repomind-ai.git
cd repomind-ai
2. Create a virtual environment

Windows:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Configure the API key

Create a .env file in the project root:

MISTRAL_API_KEY="your-mistral-api-key"

Never commit the .env file.

▶️ Run RepoMind

Start the Streamlit application:

python -m streamlit run app.py

The application will open in your browser.

Enter a GitHub repository URL such as:

https://github.com/pallets/flask

Then index the repository and start asking questions.

💬 Example Questions

You can ask questions such as:

What does the Flask class inherit from?
Where is the Flask class defined?
How is register_blueprint implemented?
What does this function do?
Where is the application initialized?
How does this repository handle requests?
💻 CLI Usage

RepoMind also includes a command-line interface.

Run:

python ask.py

Then enter a question:

Ask RepoMind a question:
What does the Flask class inherit from?

The CLI displays the generated answer and retrieved source locations.

🔎 Qdrant Utilities

Check the contents of the local Qdrant database:

python check_qdrant.py

Reset the local Qdrant database when a completely fresh index is required:

python reset_qdrant.py

reset_qdrant.py is a development utility. Do not run it unless you intentionally want to remove the local vector index.

🧪 Testing

The repository contains individual tests for major components including:

Repository loading
File scanning
Python parsing
Code chunking
Embedding generation
Qdrant storage
Vector search
RAG pipeline
LLM integration

Tests are located in:

tests/
🔐 Security

RepoMind uses environment variables for API credentials.

Create:

.env

locally and store:

MISTRAL_API_KEY="your-mistral-api-key"

The .env file is excluded through .gitignore.

Use .env.example as the public configuration template.

Never commit API keys, tokens, or other secrets.

🚧 Current Limitations

The current version primarily focuses on Python repositories.

Future versions can expand support for:

JavaScript / TypeScript
Java
C / C++
Go
Rust

Additional improvements could include:

Hybrid keyword + vector search
Cross-file dependency analysis
Repository-level call graphs
AST-aware chunking improvements
Better reranking models
GitHub URL metadata
Multi-repository sessions
Conversation memory
Cloud deployment
🚀 Future Improvements
Code Intelligence
Function call graph generation
Import/dependency analysis
Class inheritance graphs
Cross-file symbol resolution
Retrieval
Hybrid BM25 + vector retrieval
Dedicated code reranking models
Metadata-aware filtering
Query expansion
User Experience
Syntax-highlighted source viewer
Clickable source locations
Repository statistics
Search history
Chat history
Deployment
Docker support
Cloud Qdrant
Production API
Authentication
Hosted Streamlit deployment
🎯 Why RepoMind?

Large repositories can contain thousands of files and millions of lines of code.

Traditional keyword search can find text, but it does not understand the semantic relationship between a question and the code.

RepoMind combines:

Code Parsing
      +
Semantic Embeddings
      +
Vector Search
      +
Retrieval Reranking
      +
LLM Generation

to create a source-aware code understanding assistant.

📌 Project Status

Status: Working Prototype / Portfolio Project

The core GitHub repository ingestion, code parsing, semantic retrieval, reranking, Qdrant storage, and Mistral-based RAG pipeline are implemented.
👨‍💻 Author

Syed Shaik

GitHub: [RepoMind AI](https://github.com/Shaiksyed097/repomind-ai)
```
