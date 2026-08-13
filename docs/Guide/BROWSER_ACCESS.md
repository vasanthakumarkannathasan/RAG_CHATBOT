# 🌐 Browser Access Guide

## ✅ Your RAG Application is Now Running!

The server is accessible from your browser at multiple URLs:

---

## 📍 Access Points

### 1. **Web Chat Interface** (Recommended for Users)
```
http://127.0.0.1:8000/static/index.html
```
or
```
http://localhost:8000/static/index.html
```

**Features:**
- ✨ Beautiful, modern chat interface
- 💬 Real-time conversation with your RAG system
- 📚 Source citations displayed automatically
- 🎨 Gradient design with smooth animations
- 📱 Responsive layout

---

### 2. **Interactive API Documentation** (For Developers)
```
http://127.0.0.1:8000/docs
```

**Features:**
- 📖 Complete API documentation
- 🧪 Test endpoints directly in browser
- 📝 Request/response examples
- ✅ Swagger UI interface

---

### 3. **Alternative API Documentation**
```
http://127.0.0.1:8000/redoc
```

**Features:**
- 📚 ReDoc interface
- 📄 Clean, readable documentation
- 🔍 Search functionality

---

### 4. **API Root Endpoint**
```
http://127.0.0.1:8000/
```

**Returns:**
```json
{
    "success": true,
    "message": "Enterprise RAG API is running successfully.",
    "data": {
        "version": "1.0.0",
        "status": "UP"
    }
}
```

---

## 🚀 Quick Start

### Step 1: Server is Running
The terminal shows:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Open Your Browser
Click on any of these links:

1. **Chat Interface**: http://127.0.0.1:8000/static/index.html
2. **API Docs**: http://127.0.0.1:8000/docs

### Step 3: Start Chatting!
Type your question in the chat interface and press Enter or click Send.

---

## 🎯 Example Questions to Try

In the web chat interface, try these questions:

- "What is machine learning?"
- "Explain neural networks"
- "What is deep learning?"
- "Tell me about artificial intelligence"
- "What are the types of machine learning?"

---

## 📊 All Available Endpoints

### Chat Endpoints
- `POST /api/v1/chat/` - Send a question
- `GET /api/v1/chat/sessions` - List all sessions
- `DELETE /api/v1/chat/session/{id}` - Clear a session

### System Endpoints
- `GET /api/v1/health` - Check system health
- `GET /api/v1/database` - Database information
- `DELETE /api/v1/database` - Clear database
- `POST /api/v1/index` - Index documents

---

## 🔧 Using the API Directly

### Using cURL:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "session_id": "test-session",
    "source": null
  }'
```

### Using JavaScript (Fetch):
```javascript
fetch('http://127.0.0.1:8000/api/v1/chat/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        question: 'What is machine learning?',
        session_id: 'web-user-123',
        source: null
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Using Python (requests):
```python
import requests

response = requests.post(
    'http://127.0.0.1:8000/api/v1/chat/',
    json={
        'question': 'What is machine learning?',
        'session_id': 'python-client',
        'source': None
    }
)
print(response.json())
```

---

## 📱 Access from Mobile/Other Devices

If you want to access from another device on the same network:

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. Access from other device:
   ```
   http://YOUR_IP_ADDRESS:8000/static/index.html
   ```
   Example: `http://192.168.1.100:8000/static/index.html`

---

## 🛑 Stop the Server

To stop the server, go to the terminal and press:
```
CTRL + C
```

---

## 🔄 Restart the Server

If you need to restart:
```bash
c:/Personal/AI_Roadmap/RAG/Projects/Enterprise-RAG/.venv/Scripts/python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚡ Response Format

All API responses follow this standardized format:

```json
{
    "success": true,
    "message": "Chat response generated successfully",
    "data": {
        "answer": "Your answer here...",
        "session_id": "web-abc123",
        "sources": ["document.pdf (Page 1)", "document.pdf (Page 3)"]
    }
}
```

---

## 🎨 Web Interface Features

The web chat interface includes:

✅ **Modern Design**
- Gradient backgrounds
- Smooth animations
- Responsive layout

✅ **User Experience**
- Real-time message display
- Loading indicators
- Error handling
- Source citations

✅ **Functionality**
- Session management
- Quick question buttons
- Keyboard shortcuts (Enter to send)
- Connection status indicator

---

## 🐛 Troubleshooting

### "Cannot connect" or "API not reachable"
- Check if server is running (terminal should show `Uvicorn running`)
- Make sure you're using the correct URL
- Check firewall settings

### Page doesn't load
- Try http://localhost:8000/static/index.html instead of 127.0.0.1
- Clear browser cache (Ctrl+Shift+Delete)
- Try a different browser

### Slow responses
- First request initializes models (~10 seconds)
- Subsequent requests are faster
- LLM generation takes 8-20 seconds normally

---

## 📚 More Information

- **API Documentation**: See [Guide/GUIDE_API.py](Guide/GUIDE_API.py)
- **Code Flow**: See [Guide/COMPLETE_CODE_FLOW_VERIFICATION.py](Guide/COMPLETE_CODE_FLOW_VERIFICATION.py)
- **Tests**: See [tests/README.md](tests/README.md)

---

**🎉 Enjoy using your Enterprise RAG Application!**
