# 📚 How to Add New PDF Documents to Your RAG System

## ✅ Quick Summary

**3 Simple Steps:**
1. **Copy** your PDF files to the `data/` folder
2. **Trigger indexing** (using UI, API, or CLI)
3. **Start asking questions** about your new documents!

---

## 📁 Step 1: Add PDF Files

### **Method 1: Using Windows Explorer (Easiest)**

1. Open File Explorer
2. Navigate to:
   ```
   C:\Personal\AI_Roadmap\RAG\Projects\Enterprise-RAG\data\
   ```
3. **Copy or drag-and-drop** your PDF files into this folder
4. Done! Your files are ready to be indexed.

### **Method 2: Using PowerShell**

```powershell
# Copy a single PDF
Copy-Item "C:\path\to\your\document.pdf" -Destination "C:\Personal\AI_Roadmap\RAG\Projects\Enterprise-RAG\data\"

# Copy multiple PDFs from a folder
Copy-Item "C:\path\to\your\pdfs\*.pdf" -Destination "C:\Personal\AI_Roadmap\RAG\Projects\Enterprise-RAG\data\"
```

### **Current Data Folder Location:**
```
C:\Personal\AI_Roadmap\RAG\Projects\Enterprise-RAG\data\
```

**Currently contains:** `sample.pdf`

---

## 🚀 Step 2: Index the Documents

After adding PDFs, you need to **index** them so the RAG system can search through them.

### **Method 1: Using the Web Interface (Easiest)** 🌐

1. **Make sure server is running**
   ```powershell
   .\START_SERVER.ps1
   ```

2. **Open API Documentation**
   ```
   http://127.0.0.1:8000/docs
   ```

3. **Find the `/api/v1/index` endpoint**
   - Click on **POST /api/v1/index**
   - Click **"Try it out"**
   - Click **"Execute"**

4. **Wait for indexing to complete**
   - You'll see a success message with document counts

---

### **Method 2: Using cURL (Terminal)** 💻

With server running, open PowerShell and run:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/index
```

**Response:**
```json
{
    "success": true,
    "message": "Documents indexed successfully",
    "data": {
        "indexed": true
    }
}
```

---

### **Method 3: Using Python Script** 🐍

Create a file `index_new_documents.py`:

```python
import requests

response = requests.post('http://127.0.0.1:8000/api/v1/index')
data = response.json()

if data['success']:
    print("✅ Documents indexed successfully!")
else:
    print(f"❌ Error: {data['message']}")
```

Run it:
```powershell
python index_new_documents.py
```

---

### **Method 4: Direct Python (No Server Needed)** ⚡

If server is NOT running, you can index directly:

Create `index_direct.py`:
```python
from src.services.indexing import index_directory

print("🔄 Indexing documents...")
result = index_directory()

print(f"✅ Indexed {result['pdf_count']} PDF files")
print(f"📄 Total documents: {result['document_count']}")
print(f"🧩 Total chunks: {result['chunk_count']}")
```

Run it:
```powershell
c:/Personal/AI_Roadmap/RAG/Projects/Enterprise-RAG/.venv/Scripts/python.exe index_direct.py
```

---

## 🔍 Step 3: Verify Indexing

### **Check Database Info**

#### **Option 1: Use Web Interface**
```
http://127.0.0.1:8000/docs
```
- Find **GET /api/v1/database**
- Click "Try it out" → "Execute"
- You'll see document count

#### **Option 2: Use API**
```powershell
curl http://127.0.0.1:8000/api/v1/database
```

#### **Option 3: Use Inspection Script**
```powershell
python inspect_database.py
```

**Expected Output:**
```
Collection: enterprise_rag
Documents: 21 (or your new count)
```

---

## 📝 Complete Example Workflow

### **Example: Adding a Machine Learning Book**

1. **Add the PDF:**
   ```powershell
   Copy-Item "C:\Downloads\machine_learning_book.pdf" -Destination "data\"
   ```

2. **Start Server (if not running):**
   ```powershell
   .\START_SERVER.ps1
   ```

3. **Trigger Indexing:**
   ```powershell
   curl -X POST http://127.0.0.1:8000/api/v1/index
   ```

4. **Verify:**
   ```powershell
   curl http://127.0.0.1:8000/api/v1/database
   ```

5. **Ask Questions:**
   - Open: http://127.0.0.1:8000/static/index.html
   - Ask: "What is supervised learning?"
   - Get answers from your new book! 🎉

---

## 🔄 What Happens During Indexing?

```
1. 📂 LOAD PDFs
   └─> Reads all .pdf files from data/ folder
   
2. 📄 EXTRACT TEXT
   └─> Extracts text content from each PDF page
   
3. 🧩 CHUNK TEXT
   └─> Splits text into smaller, manageable chunks
   └─> Default: RecursiveCharacterTextSplitter
   
4. 🔢 CREATE EMBEDDINGS
   └─> Converts chunks to 384-dimensional vectors
   └─> Model: BAAI/bge-small-en-v1.5
   
5. 💾 STORE IN CHROMADB
   └─> Saves vectors + metadata to vector_db/
   └─> Collection: enterprise_rag
   
6. ✅ READY!
   └─> Documents are now searchable!
```

---

## ⚙️ Configuration

Your current settings (from `.env`):

```env
PDF_DIRECTORY=data                    # Where to put PDFs
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5  # Embedding model
COLLECTION_NAME=enterprise_rag        # Vector DB collection
VECTOR_DB_PATH=vector_db             # Where vectors are stored
```

---

## 🎯 Supported File Types

Currently supported:
- ✅ **PDF files** (`.pdf`)

**Note:** Only PDF files are indexed. Other file types in the `data/` folder will be ignored.

---

## 🔧 Advanced: Re-index vs. Add New

### **Current Behavior:**
- **Indexing adds new documents** to the existing collection
- **Does NOT remove old documents**
- **May create duplicates** if you index the same files again

### **To Start Fresh (Clear Database):**

#### **Option 1: Via Web UI**
```
http://127.0.0.1:8000/docs
```
- Find **DELETE /api/v1/database**
- Click "Try it out" → "Execute"

#### **Option 2: Via Script**
```powershell
python reset_database.py
```

#### **Option 3: Manual**
```powershell
# Delete the vector database folder
Remove-Item -Recurse -Force vector_db/

# Re-run indexing
curl -X POST http://127.0.0.1:8000/api/v1/index
```

---

## 📊 Performance Tips

### **Indexing Speed:**
- First-time: ~10-15 seconds (loading models)
- Subsequent: ~2-5 seconds per PDF
- Depends on PDF size and number of pages

### **Optimize:**
- ✅ Index during off-hours for large collections
- ✅ Use SSD for faster I/O
- ✅ Ensure PDFs are text-based (not scanned images)

---

## ❓ Troubleshooting

### **Problem: "No PDFs found"**
**Solution:**
- Check PDFs are in `data/` folder
- Verify file extension is `.pdf` (lowercase)
- Check file permissions

### **Problem: "Indexing fails"**
**Solution:**
- Check PDF is not corrupted
- Ensure PDF contains extractable text
- Check logs at `logs/application.log`

### **Problem: "Can't find my document in search"**
**Solution:**
- Verify indexing completed successfully
- Check database count matches expected
- Try more specific questions
- Ensure PDF text was extracted properly

### **Problem: "Duplicates in search results"**
**Solution:**
- Clear database and re-index
- Use `reset_database.py` first
- Then re-index all documents

---

## 📋 Quick Reference Commands

```powershell
# Add PDFs to data folder
Copy-Item "C:\path\to\*.pdf" -Destination "data\"

# Start server
.\START_SERVER.ps1

# Index documents (API)
curl -X POST http://127.0.0.1:8000/api/v1/index

# Check database
curl http://127.0.0.1:8000/api/v1/database

# Clear database
curl -X DELETE http://127.0.0.1:8000/api/v1/database

# Direct inspection
python inspect_database.py

# Reset everything
python reset_database.py
```

---

## 🎉 Example: Add Your Company Documents

1. **Gather PDFs:**
   - Annual reports
   - Technical documentation
   - Product manuals
   - Research papers

2. **Copy to data folder:**
   ```powershell
   Copy-Item "C:\Company\Documents\*.pdf" -Destination "data\"
   ```

3. **Index:**
   ```powershell
   curl -X POST http://127.0.0.1:8000/api/v1/index
   ```

4. **Ask questions:**
   - "What was our Q3 revenue?"
   - "How do I configure the XYZ feature?"
   - "What are the system requirements?"

**Your AI assistant now knows your company documents!** 🚀

---

## 📚 Summary

| Step | Action | Command/Location |
|------|--------|------------------|
| 1️⃣ | Add PDFs | Copy to `data/` folder |
| 2️⃣ | Index | `curl -X POST http://127.0.0.1:8000/api/v1/index` |
| 3️⃣ | Verify | `curl http://127.0.0.1:8000/api/v1/database` |
| 4️⃣ | Use | http://127.0.0.1:8000/static/index.html |

---

**🎯 That's it! You're ready to add and index new documents!**
