import os
from pathlib import Path
from dotenv import load_dotenv 

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

MODEL_NAME = os.getenv("MODEL_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
LOG_LEVEL = os.getenv("LOG_LEVEL")
VECTOR_DB_PATH = BASE_DIR / os.getenv("VECTOR_DB_PATH")
PDF_DIRECTORY = BASE_DIR / os.getenv("PDF_DIRECTORY")

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION")