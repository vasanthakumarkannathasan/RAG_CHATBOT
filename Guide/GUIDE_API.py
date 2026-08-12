"""
FastAPI Enterprise RAG - Quick Start Guide
===========================================

Your FastAPI application is now ready to run!

┌─────────────────────────────────────────────────────────────────┐
│                    HOW TO RUN THE API                            │
└─────────────────────────────────────────────────────────────────┘

Step 1: Start the FastAPI Server
─────────────────────────────────
Open a terminal and run:

    uvicorn main:app --reload

Or:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

The API will start at: http://localhost:8000


Step 2: Access the API Documentation
─────────────────────────────────────
FastAPI provides automatic interactive documentation!

Open in your browser:
  • Swagger UI:  http://localhost:8000/docs
  • ReDoc:       http://localhost:8000/redoc


┌─────────────────────────────────────────────────────────────────┐
│                    API ENDPOINTS                                 │
└─────────────────────────────────────────────────────────────────┘

1. Root Endpoint
   GET /
   Returns: {"message": "Enterprise RAG API is running successfully."}

2. Chat Endpoint
   POST /api/v1/chat/
   Body: {
     "question": "What is machine learning?",
     "session_id": "optional-session-id",
     "source": null,
     "stream": false
   }
   Returns: {
     "answer": "Machine learning is...",
     "session_id": "optional-session-id",
     "sources": ["sample.pdf (Page 1)"]
   }

3. List Sessions
   GET /api/v1/chat/sessions
   Returns: List of active conversation sessions

4. Clear Session
   DELETE /api/v1/chat/session/{session_id}
   Returns: Success message


┌─────────────────────────────────────────────────────────────────┐
│                 TESTING THE API                                  │
└─────────────────────────────────────────────────────────────────┘

Option 1: Using the Test Script
────────────────────────────────
1. Start the API: uvicorn main:app --reload
2. In another terminal: python test_api.py

Option 2: Using cURL
────────────────────
curl -X POST "http://localhost:8000/api/v1/chat/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "What is machine learning?",
    "session_id": "my-session"
  }'

Option 3: Using the Swagger UI
───────────────────────────────
1. Open http://localhost:8000/docs
2. Click on "POST /api/v1/chat/"
3. Click "Try it out"
4. Enter your request
5. Click "Execute"

Option 4: Using Python requests
────────────────────────────────
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat/",
    json={
        "question": "What is machine learning?",
        "session_id": "my-session"
    }
)

print(response.json())


┌─────────────────────────────────────────────────────────────────┐
│                    FEATURES                                      │
└─────────────────────────────────────────────────────────────────┘

✓ RESTful API with FastAPI
✓ Automatic interactive documentation (Swagger UI)
✓ Conversation memory with session management
✓ Source citations in responses
✓ Document filtering support
✓ Error handling and logging
✓ Pydantic models for request/response validation
✓ Production-ready structure


┌─────────────────────────────────────────────────────────────────┐
│                PRODUCTION CONSIDERATIONS                         │
└─────────────────────────────────────────────────────────────────┘

For production deployment:

1. Session Storage
   Replace in-memory sessions with Redis or database:
   
   from redis import Redis
   redis_client = Redis(host='localhost', port=6379)

2. Add Authentication
   Use JWT tokens or API keys:
   
   from fastapi.security import HTTPBearer
   security = HTTPBearer()

3. Add Rate Limiting
   Prevent API abuse:
   
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)

4. Add CORS if needed
   For web frontend:
   
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(CORSMiddleware, ...)

5. Use Production Server
   Replace uvicorn with gunicorn:
   
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

6. Add Health Checks
   For monitoring:
   
   @app.get("/health")
   def health_check():
       return {"status": "healthy"}


┌─────────────────────────────────────────────────────────────────┐
│                    TROUBLESHOOTING                               │
└─────────────────────────────────────────────────────────────────┘

Issue: ModuleNotFoundError
Solution: Make sure you're in the correct directory and venv is activated

Issue: Port already in use
Solution: Use a different port: uvicorn main:app --port 8001 --reload

Issue: No documents indexed
Solution: Run test_indexing_retrival.py first to index documents

Issue: Ollama not running
Solution: Start Ollama service before running the API
"""

print(__doc__)
