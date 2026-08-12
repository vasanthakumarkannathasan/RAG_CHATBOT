from pathlib import Path
import ollama

from src.config.settings import (
    MODEL_NAME,
    EMBEDDING_MODEL,
    PDF_DIRECTORY,
    VECTOR_DB_PATH,
)
from src.services.database import get_vector_db
from src.services.embedding import get_embedding_model


def check_ollama():
    print("\n========== OLLAMA ==========")
    try:
        client = ollama.Client()
        models = client.list()
        model_names = [
            model.model
            for model in models.models
        ]

        if MODEL_NAME in model_names:
            print(f"✅ Ollama is running")
            print(f"✅ Model found : {MODEL_NAME}")
        else:
            print(f"❌ Model not found : {MODEL_NAME}")

    except Exception as ex:
        print(f"❌ Ollama Error : {ex}")


def check_embedding():
    print("\n========== EMBEDDING ==========")
    try:
        get_embedding_model()
        print(f"✅ Embedding Model : {EMBEDDING_MODEL}")
    except Exception as ex:
        print(ex)


def check_vector_db():
    print("\n========== CHROMADB ==========")
    try:
        get_vector_db()
        print(f"✅ Vector DB : {VECTOR_DB_PATH}")
    except Exception as ex:
        print(ex)


def check_pdf_folder():
    print("\n========== DATA ==========")
    if not PDF_DIRECTORY.exists():
        print("❌ data folder not found")
        return

    pdf_files = list(PDF_DIRECTORY.glob("*.pdf"))
    print(f"PDF Folder : {PDF_DIRECTORY}")
    print(f"PDF Count : {len(pdf_files)}")
    for pdf in pdf_files:
        print(f"   📄 {pdf.name}")


if __name__ == "__main__":
    print("=" * 60)
    print("Enterprise RAG - System Check")
    print("=" * 60)
    check_ollama()
    check_embedding()
    check_vector_db()
    check_pdf_folder()
    print("\nSystem Check Completed")