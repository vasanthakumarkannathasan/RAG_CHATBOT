# Tests Directory

This folder contains all test files for the Enterprise RAG system.

## Test Files

### Core Functionality Tests
- **test_indexing_retrival.py** - Tests document indexing and retrieval
- **test_simplified_chat.py** - Tests simplified chat service
- **test_code_flow.py** - Tests overall code flow
- **test_flow_after_standardization.py** - Comprehensive flow verification after API standardization

### API Tests
- **test_api.py** - Basic API tests
- **test_api_endpoints.py** - API endpoint tests
- **test_standardized_format.py** - Tests standardized API response format

### Memory Tests
- **test_conversation_memory.py** - Tests conversation memory functionality
- **test_memory_flow.py** - Tests memory flow

### Feature Tests
- **test_source_citation.py** - Tests source citation functionality
- **test_citation_edge_cases.py** - Tests edge cases in citation
- **test_metadata_filtering.py** - Tests metadata filtering
- **test_streaming.py** - Tests streaming functionality

### Integration Tests
- **test_updated_flow.py** - Tests updated flow
- **test_inspect_database.py** - Database inspection tests

### System Tests
- **system_check.py** - System health and configuration check

## Running Tests

### Run All Tests
```bash
python -m pytest tests/
```

### Run Specific Test File
```bash
python tests/test_standardized_format.py
```

### Run Individual Test
```bash
python -m pytest tests/test_api.py::test_function_name
```

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
