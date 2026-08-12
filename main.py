from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import signal
import os
from src.api.v1.chat import router as chat_router
from src.api.v1.health import router as health_router
from src.api.v1.index import router as index_router
from src.api.v1.database import router as database_router
from src.api.v1.documents import router as documents_router

from src.config.settings import (
    APP_NAME,
    APP_DESCRIPTION,
    APP_VERSION,
)

app = FastAPI(
    title="Enterprise RAG API",
    description="Production-ready Enterprise RAG Application",
    version="1.0.0"
)

# Add CORS middleware to allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (HTML interface)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint
@app.get("/")
def root():
    return {
        "success": True,
        "message": "Enterprise RAG API is running successfully.",
        "data": {
            "version": "1.0.0",
            "status": "UP"
        }
    }

# Shutdown endpoint
@app.post("/api/v1/shutdown")
def shutdown():
    """
    Shutdown the server gracefully.
    This endpoint allows the UI to stop the server.
    """
    def stop_server():
        # Give time for response to be sent
        import time
        time.sleep(1)
        # Send SIGTERM to current process
        os.kill(os.getpid(), signal.SIGTERM)
    
    # Run shutdown in background
    import threading
    threading.Thread(target=stop_server, daemon=True).start()
    
    return {
        "success": True,
        "message": "Server is shutting down...",
        "data": {
            "status": "SHUTTING_DOWN"
        }
    }

# Register API Routers
app.include_router(
    chat_router,
    prefix="/api/v1"
)

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    index_router,
    prefix="/api/v1"
)

app.include_router(
    database_router,
    prefix="/api/v1"
)

app.include_router(
    documents_router,
    prefix="/api/v1"
)