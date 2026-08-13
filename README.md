# 🤖 Enterprise RAG Chatbot

AI-powered document Q&A system with multi-format support (PDF, Word, PowerPoint).

## ✨ Features

- 🤖 **Intelligent Document Q&A** - Ask questions and get answers from your documents
- 📄 **Multi-Format Support** - PDF, Word (.docx, .doc), PowerPoint (.pptx, .ppt)
- 🔒 **SHA-256 Deduplication** - Prevents duplicate content in vector database
- 🗑️ **Automatic Sync** - Auto-cleanup of orphaned embeddings when files are deleted
- 🌐 **Web Interface** - Beautiful, responsive browser-based UI
- 📚 **Document Management** - Upload, index, and manage documents from the UI
- 🔄 **Real-time Updates** - Instant indexing and search
- 🎯 **Source Citations** - See which documents answers come from

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.14+** installed
- **Ollama** installed with `tinyllama` model
- **Git** (for cloning the repository)

### Install Ollama

1. Download from: https://ollama.com
2. Install and run: `ollama pull tinyllama`

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/vasanthakumarkannathasan/RAG_CHATBOT.git
cd RAG_CHATBOT
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` if you need to change any settings (optional).

### 5. Start the Server

**Windows:**
```bash
.\START_SERVER.ps1
```

**Mac/Linux:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open Your Browser

```
http://127.0.0.1:8000/static/index.html
```

---

## 📚 Usage

### Upload Documents

1. Click **"📚 Documents"** button in the top-right
2. Click the upload area or drag & drop
3. Select PDF, Word, or PowerPoint file
4. Click **"Upload & Index"**
5. Wait for processing (shows progress)
6. Click **"✕ Back to Chat"** to return

### Ask Questions

1. Type your question in the input box
2. Press Enter or click Send
3. Get AI-powered answers with source citations
4. See which documents were used

### Manage Documents

- **View indexed files**: Click "📚 Documents"
- **See statistics**: Chunk count and page count per file
- **Auto-cleanup**: Delete files from `data/` folder, system auto-syncs on next index

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Web Browser (UI)                   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         FastAPI REST API                     │
│  ┌──────────┬──────────┬──────────┐        │
│  │  Chat    │Documents │ Health   │        │
│  │Endpoints │Endpoints │Endpoints │        │
│  └──────────┴──────────┴──────────┘        │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Services Layer                     │
│  ┌──────────────────────────────────────┐  │
│  │ Loader → Chunker → Embeddings        │  │
│  │    ↓         ↓          ↓            │  │
│  │ Vector DB ← Retrieval ← LLM         │  │
│  └──────────────────────────────────────┘  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Storage & Models                   │
│  ┌────────────┬─────────────┬────────────┐ │
│  │ ChromaDB   │ HuggingFace │  Ollama    │ │
│  │(Vectors)   │(Embeddings) │  (LLM)     │ │
│  └────────────┴─────────────┴────────────┘ │
└─────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
RAG_CHATBOT/
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Configuration template
├── START_SERVER.ps1             # Windows server startup script
├── STOP_SERVER.ps1              # Windows server stop script
├── src/
│   ├── config/                  # Configuration settings
│   ├── services/                # Core business logic
│   │   ├── chat_service.py      # Chat orchestration
│   │   ├── loader.py            # Multi-format document loading
│   │   ├── chunking.py          # Text splitting with SHA-256 hashing
│   │   ├── embedding.py         # HuggingFace embeddings
│   │   ├── database.py          # ChromaDB operations
│   │   ├── retrieval.py         # Document search
│   │   ├── llm.py               # Ollama LLM integration
│   │   └── indexing.py          # Directory indexing with auto-sync
│   ├── api/v1/                  # REST API endpoints
│   │   ├── chat.py              # Chat endpoints
│   │   ├── documents.py         # Document management endpoints
│   │   ├── health.py            # Health check
│   │   └── database.py          # Database operations
│   ├── exceptions/              # Custom exception classes
│   └── utils/                   # Utility functions
├── static/
│   └── index.html               # Web UI
├── data/                        # Document storage (gitignored)
├── vector_db/                   # ChromaDB storage (gitignored)
├── logs/                        # Application logs (gitignored)
├── tests/                       # Test files
└── docs/                        # Documentation
    ├── README.md                # Documentation index
    ├── Technical Reports/       # Build, validation, and system reports
    └── Guide/                   # User and developer guides
```

---

## 🔧 Configuration

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `tinyllama` | Ollama model name |
| `EMBEDDING_MODEL` | `BAAI/bge-small-en-v1.5` | HuggingFace embedding model |
| `COLLECTION_NAME` | `enterprise_rag` | ChromaDB collection name |
| `VECTOR_DB_PATH` | `vector_db` | Vector database storage path |
| `PDF_DIRECTORY` | `data` | Document upload directory |
| `LOG_LEVEL` | `INFO` | Logging level |

---

## 📊 API Endpoints

### Chat Endpoints

- `POST /api/v1/chat/` - Send a question and get AI response
- `GET /api/v1/chat/sessions` - List all chat sessions
- `DELETE /api/v1/chat/session/{id}` - Delete a chat session

### Document Endpoints

- `POST /api/v1/documents/upload-and-index` - Upload and index a document
- `GET /api/v1/documents/list` - List all indexed documents
- `DELETE /api/v1/documents/{filename}` - Delete document and embeddings
- `POST /api/v1/documents/sync` - Manually sync database with files

### System Endpoints

- `GET /api/v1/health` - Health check with system status
- `POST /api/v1/index` - Index all documents in data folder
- `GET /api/v1/database` - Get database statistics
- `DELETE /api/v1/database` - Delete entire database

---

## 🧪 Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Test Specific Components

```bash
# Test chat flow
python tests/test_code_flow.py

# Test standardized API format
python tests/test_standardized_format.py

# System check
python system_check.py
```

---

## 📖 Documentation

📚 **[Complete Documentation](docs/README.md)** - All documentation organized in one place

### User Guides

- **[Browser Access](docs/Guide/BROWSER_ACCESS.md)** - How to use the web interface
- **[Multi-Format Support](docs/Guide/MULTI_FORMAT_SUPPORT.md)** - PDF, Word, PowerPoint support
- **[How to Add Documents](docs/Guide/HOW_TO_ADD_DOCUMENTS.md)** - Document upload and indexing
- **[Document Deletion Guide](docs/Guide/DOCUMENT_DELETION_GUIDE.md)** - Managing documents and auto-sync
- **[New Features Guide](docs/Guide/NEW_FEATURES_GUIDE.md)** - Upload UI, document list, deduplication
- **[Shutdown Button Guide](docs/Guide/SHUTDOWN_BUTTON_GUIDE.md)** - Server control from UI

### Technical Reports

- **[Build Report](docs/BUILD_REPORT.md)** - Complete build verification and component validation
- **[Service Validation](docs/SERVICE_VALIDATION_REPORT.md)** - Service files validation results
- **[Logging Summary](docs/LOGGING_SUMMARY.md)** - Logging implementation details
- **[Test Redesign](docs/TEST_REDESIGN_SUMMARY.md)** - Test suite organization
- **[Cleanup Summary](docs/CLEANUP_SUMMARY.md)** - Project optimization history

---

## 🛠️ Troubleshooting

### Common Issues

**1. "No module named 'docx2txt'"**
```bash
pip install python-docx python-pptx docx2txt
```

**2. "Port 8000 already in use"**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <process_id>

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

**3. "Ollama connection error"**
```bash
# Make sure Ollama is running
ollama serve

# Pull the model
ollama pull tinyllama
```

**4. "Embedding model not found"**
- First run downloads the model from HuggingFace (~133MB)
- Subsequent runs use cached model
- Set `HF_TOKEN` environment variable for faster downloads

---

## 🔒 Security Notes

### Before Deploying

- ⚠️ **Never commit** `.env` file (contains local paths)
- ⚠️ **Never commit** `vector_db/` (contains indexed content)
- ⚠️ **Never commit** `data/` folder with documents (may contain sensitive info)
- ✅ **Always use** `.env.example` as template
- ✅ **Always add** proper `.gitignore`

### Production Recommendations

- Use environment-specific `.env` files
- Enable authentication for API endpoints
- Use HTTPS in production
- Implement rate limiting
- Add input validation
- Regular security audits
- Backup vector database periodically

---

## 📈 Performance

### Expected Performance

| Operation | Time | Notes |
|-----------|------|-------|
| First embedding load | ~8 sec | Downloads model |
| Subsequent loads | <1 sec | Uses cache |
| PDF upload (10 pages) | ~10 sec | Includes chunking & indexing |
| Word upload | ~5 sec | Faster than PDF |
| PowerPoint upload | ~5 sec | Per slide processing |
| Chat query | ~2-15 sec | Depends on LLM |

### Optimization Tips

- Use SSD for vector database
- Increase RAM for larger models
- Use GPU for faster embeddings (if available)
- Adjust chunk size in `chunking.py`
- Use different Ollama models (e.g., `llama2`, `mistral`)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📝 License

This project is open source. Feel free to use and modify as needed.

---

## 👨‍💻 Author

**Vasanthakumar Kannathasan**

GitHub: [@vasanthakumarkannathasan](https://github.com/vasanthakumarkannathasan)

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [LangChain](https://python.langchain.com/) - LLM application framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Ollama](https://ollama.com/) - Local LLM runner
- [HuggingFace](https://huggingface.co/) - Embeddings models

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check documentation in the [`docs/`](docs/) folder
- Review troubleshooting section above

---

**⭐ If you find this project helpful, please give it a star!**
