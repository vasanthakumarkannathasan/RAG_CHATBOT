from src.config.settings import COLLECTION_NAME
from src.services.database import (
    get_chroma_client,
    get_vector_db,
)


def reset_database():

    print("=" * 60)
    print("Enterprise RAG - Reset Database")
    print("=" * 60)
    print(f"\nCollection : {COLLECTION_NAME}")

    confirm = input(
        "\n⚠️ This will permanently delete all indexed documents.\n"
        "Type 'yes' to continue: "
    ).strip().lower()

    if confirm != "yes":
        print("\n❌ Operation cancelled.")
        return

    client = get_chroma_client()

    try:

        existing = [c.name for c in client.list_collections()]
        if COLLECTION_NAME in existing:
            print(f"\nDeleting collection '{COLLECTION_NAME}'...")
            client.delete_collection(COLLECTION_NAME)
            print("✅ Collection deleted successfully.")

            # Clear cached Chroma instance
            get_vector_db.cache_clear()

        else:
            print(f"\nCollection '{COLLECTION_NAME}' does not exist.")
        print("\nCreating new collection...")

        vector_db = get_vector_db()

        count = vector_db._collection.count()

        print("\n✅ Database reset completed successfully.")
        print(f"Collection Name : {COLLECTION_NAME}")
        print(f"Document Count  : {count}")

    except Exception as ex:

        print(f"\n❌ Error : {ex}")


if __name__ == "__main__":
    reset_database()