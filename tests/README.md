# 🧪 Enterprise RAG - Comprehensive Test Suite

This directory contains a comprehensive, well-organized test suite that provides detailed insights into every stage of the RAG pipeline.

## 📋 Test Organization

### **INDEXING TESTS** (Tests 1-6)

#### Test 1: Document Loading
- **File:** `test_1_document_loading.py`
- **Purpose:** Tests document loading for all formats (PDF, Word, PowerPoint)
- **Shows:** Document count, page count, loading time, file statistics

#### Test 2: Document Chunking
- **File:** `test_2_chunking.py`
- **Purpose:** Tests chunking process with detailed chunk analysis
- **Shows:** Chunk count, chunk IDs (hash), chunk text, metadata, chunking strategy

#### Test 3: Embedding Tokenization
- **File:** `test_3_embedding_tokenization.py`
- **Purpose:** Tests tokenization process
- **Shows:** Tokenizer model, token count, token IDs, tokenization method

#### Test 4: Embedding Transformation
- **File:** `test_4_embedding_transformation.py`
- **Purpose:** Tests embedding model transformation
- **Shows:** Model details, embedding dimensions, embedding vectors, transformation process

#### Test 5: Embedding Pooling
- **File:** `test_5_embedding_pooling.py`
- **Purpose:** Tests pooling operation (multi-token → single vector)
- **Shows:** Before/after comparison, pooling method, vector consolidation

#### Test 6: Vector Database Storage
- **File:** `test_6_vector_storage.py`
- **Purpose:** Tests vector database storage
- **Shows:** Storage count, memory usage, chunk details with embeddings

---

### **RETRIEVAL TESTS** (Tests 7-11)

#### Test 7: User Query to Embedding
- **File:** `test_7_query_embedding.py`
- **Purpose:** Tests query conversion to embedding
- **Shows:** Query tokenization, embedding transformation, query vector details

#### Test 8: Metadata Filtering
- **File:** `test_8_metadata_filtering.py`
- **Purpose:** Tests metadata filtering before search
- **Shows:** Filter configuration, search scope reduction, filter benefits

#### Test 9: Search Operation
- **File:** `test_9_search.py`
- **Purpose:** Tests similarity search operation
- **Shows:** Search type (cosine similarity), timing, top-k retrieval, relevance scores

#### Test 10: Prompt Builder
- **File:** `test_10_prompt_builder.py`
- **Purpose:** Tests RAG prompt construction
- **Shows:** System prompt, context, user query, metadata, prompt structure

#### Test 11: LLM Generation & Activity
- **File:** `test_11_llm_generation.py`
- **Purpose:** Tests LLM generation process
- **Shows:** Model info, tokenization, generation process, timing, output analysis

---

### **SYSTEM TESTS** (Tests 12-15)

#### Test 12: Duplicate Chunk Detection
- **File:** `test_12_duplicate_check.py`
- **Purpose:** Tests SHA-256 deduplication system
- **Shows:** Hash analysis, duplicate detection, hash generation demo

#### Test 13: LLM Health Check
- **File:** `test_13_llm_health.py`
- **Purpose:** Tests LLM model availability and health
- **Shows:** Ollama status, model availability, response test, performance

#### Test 14: Overall Indexing Flow
- **File:** `test_14_indexing_flow.py`
- **Purpose:** Tests complete indexing pipeline end-to-end
- **Shows:** All indexing stages with timing breakdown

#### Test 15: Overall Retrieval Flow
- **File:** `test_15_retrieval_flow.py`
- **Purpose:** Tests complete retrieval pipeline end-to-end
- **Shows:** All retrieval stages with timing breakdown

---

## 🚀 Running Tests

### Run Individual Test
```bash
# Run specific test by number
python tests/test_1_document_loading.py
python tests/test_2_chunking.py
# ... and so on
```

### Run All Indexing Tests (1-6)
```bash
python tests/test_1_document_loading.py
python tests/test_2_chunking.py
python tests/test_3_embedding_tokenization.py
python tests/test_4_embedding_transformation.py
python tests/test_5_embedding_pooling.py
python tests/test_6_vector_storage.py
```

### Run All Retrieval Tests (7-11)
```bash
python tests/test_7_query_embedding.py
python tests/test_8_metadata_filtering.py
python tests/test_9_search.py
python tests/test_10_prompt_builder.py
python tests/test_11_llm_generation.py
```

### Run System Tests (12-15)
```bash
python tests/test_12_duplicate_check.py
python tests/test_13_llm_health.py
python tests/test_14_indexing_flow.py
python tests/test_15_retrieval_flow.py
```

### Run Master Test Suite
```bash
python tests/run_all_tests.py
```

---

## 📊 Test Output Features

Each test provides:
- ✅ **Detailed step-by-step execution**
- ⏱️ **Precise timing measurements**
- 📊 **Statistics and metrics**
- 📝 **Sample data visualization**
- 🎯 **Performance analysis**
- ✅/❌ **Pass/fail status**

---

## 🎯 Test Purpose

These tests serve multiple purposes:

1. **Learning:** Understand how each RAG component works
2. **Debugging:** Identify issues at each pipeline stage
3. **Performance:** Measure timing and efficiency
4. **Validation:** Ensure system correctness
5. **Documentation:** Living documentation of system behavior

---

## 📁 Test Data Requirements

- **Documents:** Tests use documents from `data/` folder
- **Vector DB:** Tests connect to existing ChromaDB
- **LLM Model:** Requires Ollama with configured model running
- **Embeddings:** Uses HuggingFace embedding model

---

## 🔧 Prerequisites

Before running tests, ensure:

1. ✅ Virtual environment activated
2. ✅ All dependencies installed (`pip install -r requirements.txt`)
3. ✅ Documents in `data/` folder (for indexing tests)
4. ✅ Vector DB populated (for retrieval tests)
5. ✅ Ollama running with configured model (for LLM tests)

---

## 📈 Recommended Testing Order

**For New Users:**
1. Start with Test 13 (LLM Health) - Verify system readiness
2. Run Test 14 (Indexing Flow) - Understand indexing
3. Run Test 15 (Retrieval Flow) - Understand retrieval
4. Explore individual tests for deep dives

**For Developers:**
1. Run relevant tests when modifying components
2. Use individual tests for targeted debugging
3. Run overall flow tests after major changes

---

## 💡 Tips

- Tests are **non-destructive** (most are read-only or use simulation)
- Test 6 (Vector Storage) shows current DB state
- Test 14 (Indexing) simulates without storing
- Each test is **standalone** and can run independently
- Tests produce **rich, formatted output** for easy reading

---

## 📞 Support

If tests fail:
1. Check prerequisites above
2. Verify system configuration in `.env`
3. Check logs in `logs/application.log`
4. Ensure all services (Ollama, etc.) are running

---

**Happy Testing! 🎉**

## Test Categories

1. **Unit Tests** - Test individual components (services, utils)
2. **Integration Tests** - Test component interactions (API + services)
3. **End-to-End Tests** - Test complete user flows (chat, indexing)
4. **System Tests** - Test system health and configuration

## Notes

- Tests use the virtual environment at `.venv/`
- Database tests use the ChromaDB at `vector_db/`
- Test logs are written to `logs/application.log`
- Some tests require the server to be running (e.g., test_standardized_format.py)
