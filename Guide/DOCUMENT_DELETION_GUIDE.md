# 🗑️ DOCUMENT DELETION & AUTO-SYNC FEATURE

## ✨ NEW CAPABILITY

Your RAG system now automatically cleans up vector database embeddings when documents are deleted from the `data/` folder!

---

## 🎯 PROBLEM SOLVED

**Before**: If you deleted a document from `data/`, the embeddings stayed in the vector database → stale data, wasted space

**After**: System automatically detects deleted files and removes their embeddings → always in sync!

---

## 🔄 HOW IT WORKS

### **Automatic Sync** (Recommended)

The system **automatically syncs** during indexing:

1. You delete a file from `data/` folder
2. Run indexing (upload new document OR call index endpoint)
3. System detects missing file
4. Removes orphaned embeddings automatically
5. Indexes new documents

**Example:**
```bash
# 1. Delete a file
rm data/old_document.pdf

# 2. Upload any new document (triggers auto-sync)
# UI: Click "Upload & Index"
# OR API: POST /api/v1/documents/upload-and-index

# Result: old_document.pdf embeddings removed automatically!
```

---

## 🛠️ MANUAL SYNC OPTIONS

### **Option 1: Manual Sync API Endpoint**

If you delete files manually and want to clean up immediately:

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/documents/sync
```

**Response:**
```json
{
    "success": true,
    "message": "Sync completed: Removed 2 orphaned documents (156 chunks)",
    "data": {
        "orphaned_documents": 2,
        "chunks_deleted": 156,
        "deleted_files": [
            {
                "filename": "old_report.pdf",
                "chunks_deleted": 89
            },
            {
                "filename": "outdated_notes.docx",
                "chunks_deleted": 67
            }
        ],
        "remaining_files": 5
    }
}
```

---

### **Option 2: Delete via API**

Delete both file and embeddings in one API call:

**Request:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/documents/sample.pdf
```

**Response:**
```json
{
    "success": true,
    "message": "Document 'sample.pdf' deleted successfully",
    "data": {
        "filename": "sample.pdf",
        "file_deleted": true,
        "chunks_deleted": 21
    }
}
```

---

## 📋 USAGE SCENARIOS

### **Scenario 1: Clean Up Old Documents**

```bash
# 1. Manually delete files from data folder
cd data/
rm old_report_2023.pdf
rm outdated_presentation.pptx

# 2. Sync database
curl -X POST http://127.0.0.1:8000/api/v1/documents/sync

# Result:
# ✅ Removed 2 orphaned documents (234 chunks)
```

---

### **Scenario 2: Replace Document**

```bash
# 1. Delete old version
curl -X DELETE http://127.0.0.1:8000/api/v1/documents/project_plan_v1.docx

# 2. Upload new version
# UI: Upload project_plan_v2.docx

# Result:
# ✅ Old version removed: 89 chunks deleted
# ✅ New version indexed: 102 chunks added
```

---

### **Scenario 3: Automatic Cleanup**

```bash
# 1. Delete files from data folder
rm data/temp_file.pdf

# 2. Upload ANY new document (triggers auto-sync)
# UI: Upload new_document.pdf

# Behind the scenes:
# - System detects temp_file.pdf is missing
# - Removes temp_file.pdf embeddings automatically
# - Indexes new_document.pdf

# Result: Zero manual work needed!
```

---

## 🔧 TECHNICAL IMPLEMENTATION

### **New Functions in database.py**

#### **1. delete_document_by_source(filename: str)**

Deletes all chunks of a specific document from vector database.

```python
# Delete by filename
chunks_deleted = delete_document_by_source("sample.pdf")
# Returns: 21 (number of chunks deleted)
```

**How it works:**
- Queries ChromaDB for all chunks with `source == filename`
- Deletes all matching chunks
- Returns count of deleted chunks

---

#### **2. sync_database_with_files()**

Syncs vector database with data folder (removes orphaned embeddings).

```python
# Run sync
result = sync_database_with_files()

# Returns:
{
    'orphaned_documents': 2,
    'chunks_deleted': 156,
    'deleted_files': [
        {'filename': 'old.pdf', 'chunks_deleted': 89},
        {'filename': 'temp.docx', 'chunks_deleted': 67}
    ],
    'remaining_files': 5
}
```

**How it works:**
1. Gets list of indexed documents from vector DB
2. Gets list of actual files in `data/` folder
3. Compares: finds documents in DB but not in folder
4. Deletes orphaned documents
5. Returns statistics

---

### **Modified Services**

#### **indexing.py - Auto-Sync Before Indexing**

```python
@measure_performance("Directory Indexing")
def index_directory():
    # Step 1: Auto-sync (NEW!)
    sync_result = sync_database_with_files()
    if sync_result['orphaned_documents'] > 0:
        logger.info(f"Cleaned up {sync_result['orphaned_documents']} orphaned documents")
    
    # Step 2: Index new documents
    # ... existing indexing code ...
    
    # Return includes sync info
    return {
        "chunk_count": total_chunks,
        "skipped_duplicates": total_skipped,
        "orphaned_cleaned": sync_result['orphaned_documents']  # NEW!
    }
```

**Result**: Every indexing operation automatically cleans up deleted files!

---

## 🌐 API ENDPOINTS

### **DELETE /api/v1/documents/{filename}**

Delete a specific document (file + embeddings).

**URL:** `http://127.0.0.1:8000/api/v1/documents/{filename}`

**Method:** DELETE

**Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/documents/report.pdf
```

**Response:**
```json
{
    "success": true,
    "message": "Document 'report.pdf' deleted successfully",
    "data": {
        "filename": "report.pdf",
        "file_deleted": true,
        "chunks_deleted": 89
    }
}
```

**Use Case:** Clean deletion of a specific document

---

### **POST /api/v1/documents/sync**

Sync database with data folder (remove orphaned embeddings).

**URL:** `http://127.0.0.1:8000/api/v1/documents/sync`

**Method:** POST

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/documents/sync
```

**Response (documents were deleted):**
```json
{
    "success": true,
    "message": "Sync completed: Removed 2 orphaned documents (156 chunks)",
    "data": {
        "orphaned_documents": 2,
        "chunks_deleted": 156,
        "deleted_files": [
            {"filename": "old.pdf", "chunks_deleted": 89},
            {"filename": "temp.docx", "chunks_deleted": 67}
        ],
        "remaining_files": 5
    }
}
```

**Response (already in sync):**
```json
{
    "success": true,
    "message": "Sync completed: Database is already in sync with data folder",
    "data": {
        "orphaned_documents": 0,
        "chunks_deleted": 0,
        "deleted_files": [],
        "remaining_files": 5
    }
}
```

**Use Case:** Manual cleanup after deleting files from `data/` folder

---

## 🧪 TESTING

### **Test 1: Manual File Deletion + Auto-Sync**

```bash
# 1. Check current documents
curl http://127.0.0.1:8000/api/v1/documents/list
# Result: 5 documents

# 2. Delete a file manually
rm data/old_document.pdf

# 3. Upload any new document (triggers auto-sync)
curl -X POST http://127.0.0.1:8000/api/v1/documents/upload-and-index \
  -F "file=@new_document.pdf"

# 4. Check logs
# You'll see: "Cleaned up 1 orphaned documents"

# 5. Verify
curl http://127.0.0.1:8000/api/v1/documents/list
# Result: 5 documents (old_document.pdf gone, new_document.pdf added)
```

✅ **Expected**: old_document.pdf embeddings automatically removed

---

### **Test 2: API Delete**

```bash
# 1. Upload a test document
curl -X POST http://127.0.0.1:8000/api/v1/documents/upload-and-index \
  -F "file=@test.pdf"

# Result: 45 chunks added

# 2. Delete via API
curl -X DELETE http://127.0.0.1:8000/api/v1/documents/test.pdf

# Result: 45 chunks deleted

# 3. Verify file is gone
ls data/ | grep test.pdf
# Result: (no output - file deleted)

# 4. Verify embeddings are gone
curl http://127.0.0.1:8000/api/v1/documents/list
# Result: test.pdf not in list
```

✅ **Expected**: Both file and embeddings removed

---

### **Test 3: Manual Sync**

```bash
# 1. Delete 3 files from data folder
rm data/file1.pdf data/file2.docx data/file3.pptx

# 2. Call sync endpoint
curl -X POST http://127.0.0.1:8000/api/v1/documents/sync

# Response:
{
    "orphaned_documents": 3,
    "chunks_deleted": 234,
    "deleted_files": [
        {"filename": "file1.pdf", "chunks_deleted": 89},
        {"filename": "file2.docx", "chunks_deleted": 67},
        {"filename": "file3.pptx", "chunks_deleted": 78}
    ]
}
```

✅ **Expected**: All 3 documents' embeddings removed

---

## 📊 WORKFLOW DIAGRAM

```
USER ACTION              →  SYSTEM BEHAVIOR
═══════════════════════════════════════════════════════════

Delete file from data/   →  File removed from disk
                         →  Embeddings still in DB (orphaned)
                            ⚠️ Out of sync

Upload new document      →  🔄 AUTO-SYNC TRIGGERED
                         →  ✅ Detects orphaned embeddings
                         →  ✅ Removes orphaned chunks
                         →  ✅ Indexes new document
                         →  ✅ Database clean!

OR

Call /documents/sync     →  🔄 MANUAL SYNC TRIGGERED
                         →  ✅ Detects orphaned embeddings
                         →  ✅ Removes orphaned chunks
                         →  ✅ Database clean!

OR

DELETE /documents/file   →  ✅ Deletes file from disk
                         →  ✅ Removes embeddings from DB
                         →  ✅ All in one step!
```

---

## ✨ BENEFITS

### **1. Automatic Cleanup**
- No manual intervention needed
- Database stays in sync automatically
- Works every time you index

### **2. Space Savings**
- Removes unused embeddings
- Keeps vector database lean
- Faster queries

### **3. Data Accuracy**
- No stale results from deleted files
- Always shows current documents
- Clean document list

### **4. Flexibility**
- Auto-sync during indexing (recommended)
- Manual sync when needed
- API delete for programmatic use

---

## 🚀 RECOMMENDED WORKFLOW

### **Daily Use:**

```bash
# Just delete files and upload new ones
# System handles cleanup automatically!

1. Delete old files from data/
2. Upload new documents via UI
3. Done! System auto-syncs ✅
```

### **Batch Cleanup:**

```bash
# Delete many files, then sync once

1. Delete multiple files from data/
2. Call: POST /api/v1/documents/sync
3. Done! All orphans removed ✅
```

### **Programmatic Delete:**

```bash
# API-driven deletion

1. Call: DELETE /api/v1/documents/{filename}
2. Done! File + embeddings removed ✅
```

---

## 🔍 LOGGING

All operations are logged for audit trail:

```log
2026-08-12 13:42:01 | INFO | Syncing database with data folder...
2026-08-12 13:42:02 | INFO | Deleted 89 chunks for document: old_report.pdf
2026-08-12 13:42:02 | INFO | Deleted 67 chunks for document: temp_notes.docx
2026-08-12 13:42:02 | INFO | Cleaned up 2 orphaned documents (156 chunks)
2026-08-12 13:42:03 | INFO | Added 102 chunks from new_document.pdf
```

Check logs at: `logs/application.log`

---

## 🎯 SUMMARY

### **What You Requested:**

> "If I remove document from data then it remove respective embedding data from vector db"

### **What We Delivered:**

✅ **Auto-Sync**: Automatic cleanup during indexing  
✅ **Manual Sync**: POST /documents/sync endpoint  
✅ **API Delete**: DELETE /documents/{filename} endpoint  
✅ **Logging**: Full audit trail  
✅ **Statistics**: Detailed deletion reports  
✅ **No UI needed**: Works via code/API as requested  

---

## 🚀 GET STARTED

**Try it now:**

1. **Delete a file:**
   ```bash
   rm data/sample.pdf
   ```

2. **Upload new document** (via UI or API) - triggers auto-sync

3. **Check logs:**
   ```bash
   tail -f logs/application.log
   # You'll see: "Cleaned up 1 orphaned documents"
   ```

4. **Verify:**
   ```bash
   curl http://127.0.0.1:8000/api/v1/documents/list
   # sample.pdf is gone!
   ```

---

**🎊 Your vector database now stays perfectly in sync with your data folder!**

Delete files anytime - the system automatically cleans up orphaned embeddings! 🗑️✨
