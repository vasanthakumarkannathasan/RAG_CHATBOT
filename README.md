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
- 📊 **Comprehensive Logging** - 67+ log points across all services with performance tracking
- 🧪 **Complete Test Suite** - 15 pipeline tests covering indexing, retrieval, and system checks
- 📖 **Organized Documentation** - Centralized docs with technical reports and user guides

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
│   ├── services/                # Core business logic (11 services with logging)
│   │   ├── chat_service.py      # Chat orchestration
│   │   ├── loader.py            # Multi-format document loading
│   │   ├── chunking.py          # Text splitting with SHA-256 hashing
│   │   ├── embedding.py         # HuggingFace embeddings
│   │   ├── database.py          # ChromaDB operations
│   │   ├── database_service.py  # Database utilities
│   │   ├── retrieval.py         # Document search
│   │   ├── llm.py               # Ollama LLM integration
│   │   ├── indexing.py          # Directory indexing with auto-sync
│   │   ├── prompt_builder.py    # RAG prompt construction
│   │   └── memory.py            # Conversation memory management
│   ├── api/v1/                  # REST API endpoints
│   │   ├── chat.py              # Chat endpoints
│   │   ├── documents.py         # Document management endpoints
│   │   ├── health.py            # Health check
│   │   ├── index.py             # Indexing endpoints
│   │   └── database.py          # Database operations
│   ├── exceptions/              # Custom exception classes
│   └── utils/                   # Utility functions
│       ├── logger.py            # Logging configuration
│       └── performance.py       # Performance tracking decorator
├── static/
│   └── index.html               # Web UI
├── data/                        # Document storage (gitignored)
├── vector_db/                   # ChromaDB storage (gitignored)
├── logs/                        # Application logs (gitignored)
│   └── application.log          # Main log file with 67+ log points
├── tests/                       # Comprehensive test suite (15 tests)
│   ├── test_1_document_loading.py      # Document loading test
│   ├── test_2_chunking.py              # Chunking test
│   ├── test_3-6_embedding_*.py         # Embedding pipeline tests
│   ├── test_7-9_*.py                   # Retrieval pipeline tests
│   ├── test_10-11_*.py                 # Prompt & LLM tests
│   ├── test_12-15_*.py                 # System & flow tests
│   ├── run_all_tests.py                # Batch test runner
│   ├── system_check.py                 # System validation
│   └── README.md                       # Test documentation
└── docs/                        # Documentation
    ├── README.md                # Documentation index
    ├── BUILD_REPORT.md          # Complete build verification
    ├── SERVICE_VALIDATION_REPORT.md  # Service validation results
    ├── LOGGING_SUMMARY.md       # Logging implementation details
    ├── TEST_REDESIGN_SUMMARY.md # Test suite organization
    ├── CLEANUP_SUMMARY.md       # Project cleanup history
    └── Guide/                   # User and developer guides (7 files)
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
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

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

### Comprehensive Test Suite (15 Tests)

The application includes a complete test suite organized by pipeline:

#### Run All Tests

```bash
# Run all 15 tests in sequence
python tests/run_all_tests.py
```

#### Test Categories

**Indexing Pipeline Tests (1-6):**
- `test_1_document_loading.py` - Multi-format document loading
- `test_2_chunking.py` - Text splitting and hashing
- `test_3_embedding_tokenization.py` - Token generation
- `test_4_embedding_transformation.py` - Vector transformation
- `test_5_embedding_pooling.py` - Mean pooling
- `test_6_vector_storage.py` - ChromaDB storage

**Retrieval Pipeline Tests (7-11):**
- `test_7_query_embedding.py` - Query vectorization
- `test_8_metadata_filtering.py` - Source filtering
- `test_9_search.py` - Similarity search
- `test_10_prompt_builder.py` - RAG prompt construction
- `test_11_llm_generation.py` - Answer generation

**System Tests (12-15):**
- `test_12_duplicate_check.py` - SHA-256 deduplication
- `test_13_llm_health.py` - Ollama connectivity
- `test_14_indexing_flow.py` - Complete indexing flow
- `test_15_retrieval_flow.py` - Complete retrieval flow

#### System Check

```bash
# Quick system validation
python tests/system_check.py
```

#### Individual Tests

```bash
# Run specific test
python tests/test_1_document_loading.py
python tests/test_14_indexing_flow.py
```

---

## � Logging & Monitoring

### Comprehensive Logging System

All services include production-ready logging:

- **Log File:** `logs/application.log`
- **Log Points:** 67+ across all services
- **Log Levels:** INFO, DEBUG, WARNING, EXCEPTION
- **Performance Tracking:** `@measure_performance` decorator on key operations
- **Coverage:** 100% of active service files (11/11)

### View Logs

**Real-time monitoring:**
```powershell
# Windows
Get-Content logs\application.log -Wait -Tail 50
```

**Filter logs:**
```powershell
# Show errors only
Get-Content logs\application.log | Select-String "ERROR|EXCEPTION"

# Show performance metrics
Get-Content logs\application.log | Select-String "completed in"
```

### Log Example

```
2026-08-13 14:30:45,123 | INFO | Chat request - Question: 'What is Docker?...'
2026-08-13 14:30:45,234 | INFO | Retrieved 3 documents for query
2026-08-13 14:30:45,345 | INFO | Built prompt with 2456 characters
2026-08-13 14:30:52,456 | INFO | Generated answer with 342 characters
2026-08-13 14:30:52,567 | INFO | Chat completed - 2 unique sources cited
2026-08-13 14:30:52,670 | INFO | Chat Service completed in 7.54 sec
```

---

## �📖 Documentation

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
| First embedding load | ~8-15 sec | Downloads model (~133MB) |
| Subsequent loads | <1 sec | Uses cache |
| PDF upload (10 pages) | ~10 sec | Includes chunking & indexing |
| Word upload | ~5 sec | Faster than PDF |
| PowerPoint upload | ~5 sec | Per slide processing |
| Chat query | ~2-15 sec | Depends on LLM & context size |
| Document retrieval | ~100-200 ms | Vector search with metadata filter |
| Chunk deduplication | <1 sec | SHA-256 hash comparison |

### Optimization Tips

- Use SSD for vector database storage
- Increase RAM for larger models (8GB+ recommended)
- Use GPU for faster embeddings (if available)
- Adjust chunk size in `chunking.py` (default: 500 chars)
- Use different Ollama models (e.g., `llama2`, `mistral`, `phi3`)
- Enable logging at INFO level in production (DEBUG for troubleshooting)
- Monitor `logs/application.log` for performance metrics

---

## 🆕 Recent Updates

### Version 1.0.0 (2026-08-13)

**Major Enhancements:**

1. **📊 Comprehensive Logging System**
   - Added logging to all 11 active service files
   - 67+ strategic log points across the codebase
   - INFO, DEBUG, WARNING, EXCEPTION log levels
   - Performance tracking with `@measure_performance` decorator
   - Centralized logging to `logs/application.log`

2. **📖 Documentation Reorganization**
   - Created centralized `docs/` folder
   - 5 technical reports (Build, Service Validation, Logging, Test Redesign, Cleanup)
   - 7 user guides (Browser Access, Multi-Format Support, Document Management, etc.)
   - Documentation index at `docs/README.md`
   - Updated all documentation links in main README

3. **🧪 Test Suite Redesign**
   - Redesigned test folder with 15 comprehensive tests
   - Organized by pipeline: Indexing (1-6), Retrieval (7-11), System (12-15)
   - Added `run_all_tests.py` for batch execution
   - Each test focuses on specific component with detailed validation
   - Updated `tests/README.md` with complete documentation

4. **🧹 Code Cleanup**
   - Removed obsolete files (app.py, api/ folder, Notes.txt)
   - Removed 15 outdated test files
   - Fixed all import statements and dependencies
   - 100% syntax validation across all service files
   - Zero errors in production code

5. **✅ Build & Validation**
   - All 13 service files validated
   - All 5 API routers operational
   - Complete build verification (BUILD_REPORT.md)
   - Service validation report (SERVICE_VALIDATION_REPORT.md)
   - Production-ready status confirmed

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
