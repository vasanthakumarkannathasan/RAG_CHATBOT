# 📦 Installation & Setup Guide - Enterprise RAG Chatbot

**Complete step-by-step guide for new users**

---

## 🎯 Overview

This guide will help you install and run the Enterprise RAG Chatbot on your local machine. No prior experience required!

**What you'll be able to do:**
- Upload your PDF, Word, and PowerPoint documents
- Ask questions and get AI-powered answers from your documents
- Manage your document library through a web interface
- Get source citations showing where answers came from

**Time to complete:** 15-30 minutes (including downloads)

---

## 📋 Before You Start

### System Requirements

- **Operating System:** Windows 10/11, macOS, or Linux
- **RAM:** Minimum 8GB (16GB recommended)
- **Disk Space:** At least 5GB free space
- **Internet:** Required for initial setup and downloads

### What You'll Install

1. **Python 3.14+** - Programming language runtime
2. **Ollama** - Local AI model runner (includes tinyllama model)
3. **Git** (optional) - For cloning the repository
4. **Enterprise RAG Application** - This application!

---

## 🚀 Step-by-Step Installation

### Step 1: Install Python

#### Windows:
1. Download Python 3.14+ from: https://www.python.org/downloads/
2. Run the installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation:
   ```powershell
   python --version
   ```
   Should show: `Python 3.14.0` or higher

#### macOS:
```bash
# Using Homebrew (install Homebrew first if needed)
brew install python@3.14
python3 --version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.14 python3.14-venv python3-pip
python3 --version
```

---

### Step 2: Install Ollama (AI Model)

Ollama runs the AI model locally on your computer.

#### Windows:
1. Download from: https://ollama.com/download/windows
2. Run the installer (`OllamaSetup.exe`)
3. Follow the installation wizard
4. Open Command Prompt or PowerShell and verify:
   ```powershell
   ollama --version
   ```

#### macOS:
1. Download from: https://ollama.com/download/mac
2. Open the downloaded `.dmg` file
3. Drag Ollama to Applications
4. Open Ollama from Applications
5. Verify in Terminal:
   ```bash
   ollama --version
   ```

#### Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

#### Download the AI Model:
After installing Ollama, download the tinyllama model:
```bash
ollama pull tinyllama
```
**Note:** This downloads ~637MB. Wait for completion.

---

### Step 3: Get the Application

You have two options:

#### Option A: Using Git (Recommended)

1. **Install Git** (if not already installed):
   - Windows: https://git-scm.com/download/win
   - macOS: `brew install git`
   - Linux: `sudo apt install git`

2. **Clone the repository:**
   ```bash
   git clone https://github.com/vasanthakumarkannathasan/RAG_CHATBOT.git
   cd RAG_CHATBOT
   ```

#### Option B: Manual Download

1. Go to: https://github.com/vasanthakumarkannathasan/RAG_CHATBOT
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your preferred location
5. Open terminal/command prompt in the extracted folder

---

### Step 4: Create Virtual Environment

A virtual environment keeps the application's dependencies isolated.

#### Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Confirmation:** Your prompt should now show `(.venv)` at the beginning.

---

### Step 5: Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

**This will install:**
- FastAPI (Web framework)
- LangChain (AI framework)
- ChromaDB (Vector database)
- HuggingFace Transformers (Embeddings)
- And other required packages

**Note:** First-time installation takes 3-5 minutes. Wait for completion.

---

### Step 6: Configure the Application

#### Create environment file:

**Windows:**
```powershell
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

#### (Optional) Edit configuration:

Open `.env` file in a text editor if you want to customize:

```env
# AI Model Settings
MODEL_NAME=tinyllama                    # Ollama model to use
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5  # HuggingFace embedding model

# Database Settings
COLLECTION_NAME=enterprise_rag          # ChromaDB collection name
VECTOR_DB_PATH=vector_db                # Vector database storage path

# Application Settings
PDF_DIRECTORY=data                      # Document upload directory
LOG_LEVEL=INFO                          # Logging level (DEBUG, INFO, WARNING, ERROR)
```

**For beginners:** You can skip editing this file. Defaults work great!

---

### Step 7: Start the Application

#### Windows:
```powershell
.\START_SERVER.ps1
```

#### macOS/Linux:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**What you should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Success!** The server is now running.

---

### Step 8: Open the Application

1. Open your web browser (Chrome, Firefox, Edge, Safari)
2. Go to: **http://localhost:8000/static/index.html**
3. You should see the Enterprise RAG Chatbot interface! 🎉

---

## 📚 Using the Application

### First Time: Add Your Documents

1. **Click the "📚 Documents" button** in the top-right corner
2. **Upload a document:**
   - Click the upload area or drag & drop
   - Supported formats: PDF, Word (.docx, .doc), PowerPoint (.pptx, .ppt)
   - Select your file
3. **Click "Upload & Index"**
4. **Wait for processing** (10-30 seconds depending on file size)
5. **Return to chat:** Click "✕ Back to Chat"

### Ask Questions

1. Type your question in the input box
2. Press Enter or click the Send button
3. Wait for the AI to generate an answer (2-15 seconds)
4. See the answer with source citations!

**Example questions:**
- "What is this document about?"
- "Summarize the main points"
- "What does it say about [topic]?"
- "Can you explain [concept] from the document?"

### Manage Documents

- **View documents:** Click "📚 Documents"
- **See statistics:** View chunk count and page count for each file
- **Delete documents:** Remove files from `data/` folder, system auto-syncs

---

## 🛑 Stopping the Application

### Windows:
1. In PowerShell window, press `Ctrl + C`
2. Or use the shutdown button in the web interface

### macOS/Linux:
1. In Terminal, press `Ctrl + C`

---

## 🔄 Starting Again Later

### Quick Start:

#### Windows:
```powershell
cd path\to\RAG_CHATBOT
.\.venv\Scripts\Activate.ps1
.\START_SERVER.ps1
```

#### macOS/Linux:
```bash
cd path/to/RAG_CHATBOT
source .venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open: http://localhost:8000/static/index.html

---

## ❓ Troubleshooting

### Problem: "Python is not recognized"

**Solution:** Python not in PATH.
- Reinstall Python and check "Add Python to PATH"
- Or add manually to system environment variables

### Problem: "Port 8000 already in use"

**Solution:** Another application is using port 8000.

**Windows:**
```powershell
netstat -ano | findstr :8000
taskkill /F /PID <process_id>
```

**macOS/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Problem: "No module named 'fastapi'"

**Solution:** Virtual environment not activated or dependencies not installed.
```bash
# Activate virtual environment first
pip install -r requirements.txt
```

### Problem: "Cannot connect to Ollama"

**Solution:** Ollama not running.
- **Windows:** Start Ollama from Start Menu
- **macOS:** Open Ollama from Applications
- **Linux:** Run `ollama serve` in a separate terminal

### Problem: "Model 'tinyllama' not found"

**Solution:** Model not downloaded.
```bash
ollama pull tinyllama
```

### Problem: "Embedding model download slow"

**Solution:** Set HuggingFace token for faster downloads.
1. Get free token from: https://huggingface.co/settings/tokens
2. Set environment variable:
   ```bash
   # Windows
   $env:HF_TOKEN="your_token_here"
   
   # macOS/Linux
   export HF_TOKEN="your_token_here"
   ```

### Problem: PowerShell script execution error

**Solution:** Execution policy restriction.
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: "No such file or directory: 'data'"

**Solution:** Data folder doesn't exist (normal for first run).
- The folder is created automatically when you upload your first document
- Or create manually: `mkdir data`

---

## 📊 What Gets Created

When you run the application, these folders are created:

```
RAG_CHATBOT/
├── .venv/           # Virtual environment (don't commit to Git)
├── data/            # Your uploaded documents (don't commit to Git)
├── vector_db/       # Vector database storage (don't commit to Git)
├── logs/            # Application logs (don't commit to Git)
│   └── application.log
└── __pycache__/     # Python cache files (don't commit to Git)
```

**Note:** These folders are in `.gitignore` to protect your privacy.

---

## 🔒 Privacy & Security

### Your Data Stays Local

- ✅ All documents stay on your computer
- ✅ AI runs locally (Ollama)
- ✅ No data sent to external services (except HuggingFace for initial model download)
- ✅ Vector database stored locally

### Safe to Delete

You can safely delete these folders to reset the application:
- `vector_db/` - Deletes all indexed documents (you'll need to re-index)
- `logs/` - Deletes application logs
- `data/` - Deletes uploaded documents (backup first!)

**Don't delete:**
- `.venv/` - You'll need to reinstall dependencies
- `src/` - Application code

---

## 🎓 Next Steps

### Learn More

- **📖 Full Documentation:** See [docs/README.md](docs/README.md)
- **🧪 Run Tests:** `python tests/run_all_tests.py`
- **📊 Check Logs:** View `logs/application.log`
- **⚙️ Advanced Config:** Edit `.env` file

### Explore Features

- Upload multiple documents
- Ask follow-up questions
- Try different document formats (PDF, Word, PowerPoint)
- View source citations
- Check document statistics

### Get Help

- **GitHub Issues:** https://github.com/vasanthakumarkannathasan/RAG_CHATBOT/issues
- **Documentation:** [docs/Guide/](docs/Guide/)
- **API Docs:** http://localhost:8000/docs (when server is running)

---

## 🎉 You're All Set!

Your Enterprise RAG Chatbot is ready to use!

**Quick Reference:**
1. Activate virtual environment
2. Start server: `.\START_SERVER.ps1` (Windows) or `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000` (Mac/Linux)
3. Open: http://localhost:8000/static/index.html
4. Upload documents and start asking questions!

**Enjoy using your AI-powered document assistant!** 🚀

---

## 📞 Support

Need help? Check these resources:

1. **Troubleshooting Section** (above)
2. **Documentation:** [docs/](docs/)
3. **GitHub Issues:** Report bugs or ask questions
4. **README.md:** Quick reference guide

---

**Version:** 1.0.0  
**Last Updated:** 2026-08-13  
**Tested On:** Windows 11, macOS Sonoma, Ubuntu 22.04
