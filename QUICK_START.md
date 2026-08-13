# ⚡ Quick Start Guide - Enterprise RAG Chatbot

**Get started in 5 minutes!**

---

## 🎯 For Users Who Just Downloaded

### Prerequisites (Install First)

1. **Python 3.14+** → https://www.python.org/downloads/
2. **Ollama + tinyllama** → https://ollama.com/

---

## 🚀 Installation Commands

### Windows (PowerShell):

```powershell
# 1. Navigate to downloaded folder
cd path\to\RAG_CHATBOT

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create environment file
copy .env.example .env

# 6. Download AI model (one-time, ~637MB)
ollama pull tinyllama

# 7. Start the application
.\START_SERVER.ps1
```

### macOS/Linux (Terminal):

```bash
# 1. Navigate to downloaded folder
cd path/to/RAG_CHATBOT

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create environment file
cp .env.example .env

# 6. Download AI model (one-time, ~637MB)
ollama pull tinyllama

# 7. Start the application
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 Open the Application

**In your browser, go to:**

```
http://localhost:8000/static/index.html
```

---

## 📚 First Steps

### 1. Upload a Document

1. Click **"📚 Documents"** button (top-right)
2. Drag & drop or click to select a file
3. Supported: PDF, Word (.docx), PowerPoint (.pptx)
4. Click **"Upload & Index"**
5. Wait for processing (~10-30 seconds)

### 2. Ask Questions

1. Type your question in the input box
2. Press Enter or click Send
3. Get AI-powered answers with sources!

---

## 🛑 Stop the Server

- Press `Ctrl + C` in terminal
- Or use shutdown button in web interface

---

## 🔄 Run Again Later

### Windows:
```powershell
cd path\to\RAG_CHATBOT
.\.venv\Scripts\Activate.ps1
.\START_SERVER.ps1
```

### macOS/Linux:
```bash
cd path/to/RAG_CHATBOT
source .venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ❓ Common Issues

### "Python not recognized"
→ Reinstall Python and check "Add Python to PATH"

### "Port 8000 already in use"
→ Another app using port 8000. Kill the process or use different port.

### "Cannot connect to Ollama"
→ Start Ollama application first

### "PowerShell script error"
→ Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 📖 Need More Help?

- **Detailed Guide:** See [INSTALLATION.md](INSTALLATION.md)
- **Full Documentation:** See [docs/README.md](docs/README.md)
- **Troubleshooting:** Check [INSTALLATION.md](INSTALLATION.md#-troubleshooting)

---

**Ready to start using your AI document assistant!** 🎉

**Repository:** https://github.com/vasanthakumarkannathasan/RAG_CHATBOT
