# Project Detailed Architecture Explanation

## 🏗️ Enterprise RAG System Architecture

**Version:** 1.0.0  
**Last Updated:** 2026-08-20  
**Repository:** https://github.com/vasanthakumarkannathasan/RAG_CHATBOT

---

## 📑 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Layered Architecture](#layered-architecture)
3. [Core RAG Pipeline](#core-rag-pipeline)
4. [Key Components](#key-components)
5. [Data Flow Architecture](#data-flow-architecture)
6. [Design Patterns](#design-patterns)
7. [Technology Stack](#technology-stack)
8. [Scalability Considerations](#scalability-considerations)
9. [API Endpoints](#api-endpoints)

---

## Architecture Overview

This Enterprise RAG (Retrieval-Augmented Generation) system follows a **clean 3-tier layered architecture** with service-oriented design principles. The system enables intelligent question-answering over documents with conversation memory and multi-format document support.

### Architecture Pattern: **Layered + Service-Oriented**

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│  • FastAPI REST API (main.py)                                   │
│  • Static HTML UI (static/index.html)                           │
│  • 12 RESTful endpoints with standardized responses             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (src/api/v1/)                    │
│  • chat.py         → Chat with conversation memory              │
│  • health.py       → System health checks                       │
│  • index.py        → Document indexing trigger                  │
│  • database.py     → Database management                        │
│  • documents.py    → Document CRUD operations                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   SERVICE LAYER (src/services/)                 │
│  Core RAG: chat_service, retrieval, prompt_builder, llm         │
│  Document Processing: loader, chunking, embedding, indexing     │
│  Data Management: database, memory, document_registry           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
│  • ChromaDB (vector_db/)    → Vector embeddings                 │
│  • File System (data/)      → Source documents                  │
│  • In-Memory (sessions)     → Conversation state                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layered Architecture

### 1. **Presentation Layer**

**Components:**
- `main.py` - FastAPI application entry point
- `static/index.html` - Web-based UI
- CORS middleware for browser access
- Graceful shutdown endpoint

**Responsibilities:**
- HTTP request handling
- Static file serving
- Middleware configuration
- Application lifecycle management

---

### 2. **API Layer** (`src/api/v1/`)

**Version:** v1 (versioned API for future compatibility)

#### Components:

**`chat.py`** - Chat API
- Handles chat requests
- Manages conversation sessions (in-memory)
- Integrates ConversationMemory for multi-turn dialogs
- Formats responses with sources

**`health.py`** - Health Check API
- System status monitoring
- Database connectivity check
- Returns collection info

**`index.py`** - Indexing API
- Triggers document indexing
- Returns detailed statistics (file count, chunk count, duplicates)

**`database.py`** - Database Management API
- Get database information
- Clear/reset database

**`documents.py`** - Document Management API
- Upload documents (with/without auto-indexing)
- List indexed documents
- Delete documents
- Sync database with data folder

**Responsibilities:**
- Request validation (Pydantic models)
- Session management
- Response formatting (standardized `{success, message, data}`)
- HTTP exception handling

---

### 3. **Service Layer** (`src/services/`)

The core business logic layer organized into three functional groups:

#### **A. Core RAG Pipeline**

**`chat_service.py`** - RAG Orchestrator
```python
def chat(question, source, session_id, conversation_history):
    # 1. Retrieve relevant documents
    documents = retrieve_documents(question, source)
    
    # 2. Build context-aware prompt
    prompt = build_prompt(question, documents, conversation_history)
    
    # 3. Generate answer
    answer = generate_answer(prompt)
    
    # 4. Extract & format sources
    return {answer, sources}
```

**`retrieval.py`** - Document Retrieval
- Vector similarity search
- Source filtering capability
- Top-k document selection (default k=2)

**`prompt_builder.py`** - Prompt Construction
- Builds structured prompts with:
  - System instructions
  - Conversation history
  - Retrieved context documents
  - Current question

**`llm.py`** - LLM Integration
- Ollama client management (cached)
- Answer generation
- Streaming support (optional)

#### **B. Document Processing**

**`loader.py`** - Multi-Format Document Loading
- **PDF**: PyPDFLoader
- **Word**: Docx2txtLoader (.docx, .doc)
- **PowerPoint**: UnstructuredPowerPointLoader (.pptx, .ppt)
- Metadata extraction (source, page/slide)

**`chunking.py`** - Text Splitting & Deduplication
- RecursiveCharacterTextSplitter
  - chunk_size: 500 characters
  - chunk_overlap: 100 characters
- SHA256 hash generation per chunk
- Enables deduplication

**`embedding.py`** - Embedding Generation
- HuggingFace Embeddings
- Model caching (@lru_cache)
- 768-dimensional vectors

**`indexing.py`** - Indexing Orchestration
- Full indexing pipeline coordinator
- Orphan cleanup (sync with data folder)
- Deduplication checking
- Statistics reporting

#### **C. Data Management**

**`database.py`** - ChromaDB Operations
- Vector database initialization
- CRUD operations (create, read, delete)
- Collection management
- Metadata filtering
- Hash-based deduplication queries

**`database_service.py`** - High-Level DB Utilities
- Database information retrieval
- Database reset/clear operations

**`memory.py`** - Conversation Memory
- Session-based conversation history
- Auto-trimming (keeps last 6 messages = 3 Q&A pairs)
- Message management (add, get, clear)

**`document_registry.py`** - Document Tracking
- Document metadata management
- File tracking

---

### 4. **Data Layer**

**ChromaDB** (`vector_db/`)
- Persistent vector storage
- Cosine similarity search
- Metadata storage (source, page, chunk_hash)

**File System** (`data/`)
- Source document storage
- Supports PDF, DOCX, DOC, PPTX, PPT

**In-Memory** (session_sessions dict)
- Conversation state per session_id
- Fast access for active conversations
- (Note: Not persistent across restarts)

---

## Core RAG Pipeline

### **Phase 1: Document Ingestion & Indexing**

```
PDF/DOCX/PPTX Files (data/)
        ↓
    loader.py
    ├─→ Detects format (PDF/Word/PowerPoint)
    ├─→ Uses appropriate loader
    └─→ Extracts text + metadata (source, page)
        ↓
    chunking.py
    ├─→ RecursiveCharacterTextSplitter (500 chars, 100 overlap)
    ├─→ Generates SHA256 hash per chunk
    └─→ Enables deduplication
        ↓
    embedding.py
    ├─→ HuggingFace Embeddings Model
    ├─→ Converts text to 768-dim vectors
    └─→ Cached with @lru_cache
        ↓
    database.py (ChromaDB)
    ├─→ Filters duplicate chunks by hash
    ├─→ Stores: vectors + text + metadata
    └─→ Persistent storage (vector_db/)
```

**Indexing Statistics Returned:**
```json
{
  "file_count": 5,
  "document_count": 25,
  "chunk_count": 150,
  "skipped_duplicates": 10,
  "orphaned_cleaned": 2
}
```

---

### **Phase 2: Query & Retrieval (RAG Pipeline)**

```
User Question
        ↓
    API Layer (chat.py)
    ├─→ Get/Create ConversationMemory(session_id)
    ├─→ Add user message to history
    └─→ Retrieve conversation_history
        ↓
    chat_service.py (Orchestrator)
    └─→ Passes conversation_history to downstream
        ↓
    retrieval.py
    ├─→ Embed query using same model
    ├─→ Vector similarity search (cosine)
    ├─→ Apply source filter (optional)
    └─→ Return top-k documents (k=2)
        ↓
    prompt_builder.py
    └─→ Build structured prompt:
        ┌───────────────────────────────┐
        │ System Instructions           │
        ├───────────────────────────────┤
        │ Conversation History          │
        │   User: previous question     │
        │   Assistant: previous answer  │
        ├───────────────────────────────┤
        │ Retrieved Context Documents   │
        ├───────────────────────────────┤
        │ Current Question              │
        └───────────────────────────────┘
        ↓
    llm.py (Ollama)
    ├─→ Send prompt to Ollama
    ├─→ Generate context-aware answer
    └─→ Support streaming (optional)
        ↓
    chat_service.py
    ├─→ Extract source citations
    └─→ Format with page numbers
        ↓
    API Layer (chat.py)
    ├─→ Add assistant response to memory
    └─→ Return {answer, sources, session_id}
```

**Response Format:**
```json
{
  "success": true,
  "message": "Chat response generated successfully",
  "data": {
    "answer": "Machine learning is...",
    "session_id": "abc123",
    "sources": [
      "document1.pdf (Page 5)",
      "document2.docx (Page 12)"
    ]
  }
}
```

---

## Key Components

### 1. **chat_service.py** - RAG Orchestrator

The central coordinator that orchestrates the entire RAG pipeline:

**Flow:**
1. Retrieve relevant documents (vector search)
2. Build context-aware prompt (with history)
3. Generate answer via LLM
4. Extract and format source citations

**Key Feature:** Now properly accepts and passes `conversation_history` throughout the pipeline.

---

### 2. **prompt_builder.py** - Context Manager

Constructs structured prompts with all necessary context:

**Prompt Structure:**
- **System Instructions**: Role and behavior definition
- **Conversation History**: Previous Q&A pairs for context
- **Retrieved Documents**: RAG context from vector search
- **Current Question**: User's current query

**Why This Matters:** Enables multi-turn conversations where the LLM understands follow-up questions in context.

---

### 3. **ConversationMemory** - Session Manager

Manages conversational state per session:

**Features:**
- Stores last 6 messages (3 Q&A pairs) per session
- Auto-trims older messages (rolling window)
- Isolated per session_id (multi-user support)
- In-memory storage (fast access)

**API:**
```python
memory.add_user_message(question)
memory.add_assistant_message(answer)
history = memory.get_messages()
memory.clear()
```

---

### 4. **database.py** - Vector Store Manager

ChromaDB operations and management:

**Capabilities:**
- Vector storage & retrieval
- Metadata filtering (e.g., by source filename)
- Deduplication checking (via chunk_hash)
- Document deletion by source
- Collection management

**Key Functions:**
- `get_vector_db()` - Initialize/get ChromaDB instance
- `get_existing_hashes()` - Fetch all chunk hashes
- `delete_document_by_source()` - Remove document
- `sync_database_with_files()` - Cleanup orphans

---

### 5. **indexing.py** - Pipeline Manager

End-to-end indexing orchestration:

**Process:**
1. Sync database with data folder (cleanup orphans)
2. Find all supported files (PDF/Word/PowerPoint)
3. Load each document
4. Split into chunks with SHA256 hashing
5. Check for existing chunks (deduplication)
6. Generate embeddings for new chunks
7. Store in vector database
8. Return detailed statistics

---

## Data Flow Architecture

### **Indexing Data Flow**

```
Documents → Loader → Chunks → Embeddings → Vector DB
             ↓         ↓         ↓           ↓
          Metadata   SHA256   768-dim    ChromaDB
          (source,    Hash    Vector    Collection
           page)                         (persistent)
```

### **Query Data Flow**

```
Question → Embedding → Similarity Search → Top-k Docs → Context
             ↓              ↓                  ↓           ↓
         768-dim        Cosine             Retrieved   Prompt
         Vector        Distance            Chunks
                                                         ↓
                                                    LLM → Answer
```

### **Conversation Memory Data Flow**

```
User Message → Memory.add_user() → Storage
                                      ↓
                              get_messages() → Prompt Builder
                                      ↓
Answer ← LLM ← Prompt          Auto-trim (keep last 6)
  ↓
Memory.add_assistant() → Storage
```

---

## Design Patterns

### 1. **Service Layer Pattern**
- API layer delegates to service layer
- Services contain business logic
- Clean separation of concerns

**Example:**
```python
# API Layer
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    result = chat_service.chat(...)  # Delegates to service
    return format_response(result)

# Service Layer
def chat(question, ...):
    documents = retrieve_documents(...)
    prompt = build_prompt(...)
    return generate_answer(...)
```

---

### 2. **Repository Pattern**
- `database.py` abstracts vector DB access
- Services don't know about ChromaDB internals
- Easy to swap vector DB implementations

**Benefit:** Can replace ChromaDB with Pinecone/Weaviate without changing service code.

---

### 3. **Strategy Pattern**
- Multiple document loaders (PDF/Word/PowerPoint)
- Selected dynamically based on file extension
- Easy to add new formats

```python
if file_ext == '.pdf':
    loader = PyPDFLoader(file_path)
elif file_ext in ['.docx', '.doc']:
    loader = Docx2txtLoader(file_path)
elif file_ext in ['.pptx', '.ppt']:
    loader = UnstructuredPowerPointLoader(file_path)
```

---

### 4. **Decorator Pattern**
- `@measure_performance` for monitoring
- `@lru_cache` for caching
- Non-invasive functionality addition

```python
@measure_performance("Document Loading")
@lru_cache(maxsize=1)
def get_embedding_model():
    return HuggingFaceEmbeddings(...)
```

---

### 5. **Factory Pattern**
- Single instance creation via caching
- Lazy initialization

```python
@lru_cache(maxsize=1)
def get_vector_db():
    return Chroma(...)  # Singleton-like behavior
```

---

## Technology Stack

### **Backend Framework**
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### **RAG & LLM**
- **LangChain** - RAG orchestration framework
- **Ollama** - Local LLM inference
- **HuggingFace** - Embedding models

### **Vector Database**
- **ChromaDB** - Open-source vector database
- Persistent storage
- Cosine similarity search

### **Document Processing**
- **PyPDFLoader** - PDF processing
- **Docx2txtLoader** - Word documents
- **UnstructuredPowerPointLoader** - PowerPoint presentations
- **RecursiveCharacterTextSplitter** - Text chunking

### **Utilities**
- **Python 3.11+** - Modern Python features
- **Logging** - Comprehensive logging system
- **Performance Monitoring** - Custom decorator-based tracking

---

## Scalability Considerations

### **Current Design:**
- **Vector DB**: ChromaDB (local, persistent)
- **Sessions**: In-memory dict
- **Embeddings**: Cached (@lru_cache)
- **LLM**: Local Ollama instance
- **Web Server**: Single Uvicorn instance

### **Scaling Path:**

#### **Horizontal Scaling:**
1. **Load Balancer** → Multiple FastAPI instances
2. **Session Store** → Redis/PostgreSQL (distributed state)
3. **Vector DB** → Cloud-based (Pinecone/Weaviate) or scaled ChromaDB
4. **LLM** → API-based (OpenAI/Anthropic) or clustered Ollama

#### **Vertical Scaling:**
1. **Increase Resources** → More RAM for embeddings cache
2. **GPU Support** → For local embeddings/LLM
3. **SSD Storage** → Faster vector DB access

#### **Optimization:**
1. **Caching Layer** → Redis for frequent queries
2. **Response Caching** → Cache common Q&A pairs
3. **Batch Processing** → Bulk document indexing
4. **Async Processing** → Background indexing tasks

---

## API Endpoints

### **Chat Module** (3 endpoints)

```
POST   /api/v1/chat/
Request:  {question, session_id?, source?, stream?}
Response: {success, message, data: {answer, sources, session_id}}

DELETE /api/v1/chat/session/{session_id}
Response: {success, message, data: {cleared}}

GET    /api/v1/chat/sessions
Response: {success, message, data: {sessions[]}}
```

---

### **Health Module** (1 endpoint)

```
GET    /api/v1/health
Response: {success, message, data: {status, database: {collection, documents}}}
```

---

### **Index Module** (1 endpoint)

```
POST   /api/v1/index
Response: {success, message, data: {file_count, chunk_count, skipped_duplicates}}
```

---

### **Database Module** (2 endpoints)

```
GET    /api/v1/database
Response: {success, message, data: {collection, documents}}

DELETE /api/v1/database
Response: {success, message, data: {cleared}}
```

---

### **Documents Module** (5 endpoints)

```
POST   /api/v1/documents/upload
Request:  multipart/form-data (file)
Response: {success, message, data: {filename, uploaded}}

POST   /api/v1/documents/upload-and-index
Request:  multipart/form-data (file)
Response: {success, message, data: {filename, indexed}}

GET    /api/v1/documents/list
Response: {success, message, data: {documents: [{filename, chunk_count, page_count}]}}

DELETE /api/v1/documents/{filename}
Response: {success, message, data: {deleted, chunks_deleted}}

POST   /api/v1/documents/sync
Response: {success, message, data: {orphaned_documents, chunks_deleted}}
```

---

## Key Architectural Decisions

### **1. Multi-Format Document Support**
**Decision:** Support PDF, Word, and PowerPoint  
**Rationale:** Enterprise environments use diverse document types  
**Implementation:** Strategy pattern with format-specific loaders

---

### **2. SHA256-Based Deduplication**
**Decision:** Hash chunks using SHA256(content + source + page)  
**Rationale:** Prevent duplicate content in vector DB  
**Benefit:** Reduced storage, improved search quality

---

### **3. Conversation Memory System**
**Decision:** Rolling window of 6 messages (3 Q&A pairs)  
**Rationale:** Balance context vs. token limits  
**Implementation:** Session-based, auto-trimming

---

### **4. Orphan Cleanup System**
**Decision:** Auto-sync DB with data folder before indexing  
**Rationale:** Keep embeddings in sync with source files  
**Implementation:** `sync_database_with_files()` runs before each index

---

### **5. Source Filtering**
**Decision:** Enable querying specific documents  
**Rationale:** Users often want to query specific sources  
**Implementation:** ChromaDB metadata filtering

---

### **6. Performance Monitoring**
**Decision:** Decorator-based performance tracking  
**Rationale:** Non-invasive monitoring of critical operations  
**Implementation:** `@measure_performance` decorator

---

### **7. Custom Exception Hierarchy**
**Decision:** Specialized exceptions for each component  
**Rationale:** Fine-grained error handling and debugging  
**Hierarchy:**
```
EnterpriseRAGException (base)
├── DatabaseException
├── EmbeddingException
├── LLMException
└── PDFException
```

---

## Error Handling Architecture

### **3-Level Error Strategy**

**1. Service Level** (Business Logic)
```python
try:
    documents = load_document(filename)
except Exception as ex:
    logger.exception(f"Failed to load: {ex}")
    raise PDFException(f"Failed to load: {ex}")
```

**2. API Level** (HTTP Errors)
```python
try:
    result = chat_service.chat(...)
except EnterpriseRAGException as ex:
    logger.error(f"Chat error: {ex}")
    raise HTTPException(status_code=500, detail=str(ex))
```

**3. Client Level** (Standardized Responses)
```json
{
  "success": false,
  "message": "Error message here",
  "data": {}
}
```

---

## Architecture Strengths

### ✅ **Modularity**
Each component has a single, well-defined responsibility.

### ✅ **Extensibility**
Easy to add:
- New document types (add loader)
- New vector DBs (swap repository)
- New LLMs (swap llm.py)

### ✅ **Testability**
16 test modules cover all components independently.

### ✅ **Observability**
- Logging throughout
- Performance monitoring
- Detailed error messages

### ✅ **Maintainability**
- Clear structure
- Good naming conventions
- Comprehensive documentation

### ✅ **Production-Ready**
- Error handling
- Deduplication
- Orphan cleanup
- Session management

---

## Future Enhancements

### **High Priority**
1. **Persistent Session Storage** - Redis/PostgreSQL for sessions
2. **Authentication & Authorization** - JWT/OAuth2
3. **Rate Limiting** - Prevent API abuse
4. **Streaming Implementation** - Real-time response streaming

### **Medium Priority**
5. **Environment Configuration** - Dev/Staging/Prod configs
6. **Monitoring & Observability** - Prometheus, OpenTelemetry
7. **Advanced Search** - Hybrid search (keyword + semantic)

### **Low Priority**
8. **Document Versioning** - Track document changes
9. **Analytics Dashboard** - Usage statistics
10. **Export Conversations** - Download chat history

---

## Summary

This Enterprise RAG system demonstrates a **well-architected, production-ready** implementation with:

- ✅ **Clean 3-tier architecture** (Presentation → API → Service → Data)
- ✅ **Service-oriented design** (Single responsibility per service)
- ✅ **Well-defined data flows** (Indexing, querying, memory management)
- ✅ **Production features** (Deduplication, cleanup, multi-format)
- ✅ **Proper abstractions** (Repository, Strategy, Factory patterns)
- ✅ **Best practices** (Error handling, logging, monitoring)

The architecture is designed for **maintainability**, **scalability**, and **extensibility**, making it suitable for enterprise deployments.

---

**Repository:** https://github.com/vasanthakumarkannathasan/RAG_CHATBOT  
**License:** MIT  
**Author:** Vasanthakumar Kannathasan  
**Last Updated:** 2026-08-20
