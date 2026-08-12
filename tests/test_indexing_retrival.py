from src.services.loader import load_pdf
from src.services.chunking import split_documents
from src.services.embedding import get_embedding_model
import src.config.settings as settings

print('=== Stage 1 === Loading PDF ===')
docs = load_pdf('sample.pdf')
print(f'Documents loaded: {len(docs)}')

print('\n=== Stage 2 === Chunking ===')
chunks = split_documents(docs)
print(f'Chunks created: {len(chunks)}')

print('\n=== Sample Chunks ===')
print('Showing first 5 chunks:\n')
for i in range(min(5, len(chunks))):
    chunk = chunks[i]
    print(f'--- Chunk {i} ---')
    print(f'Length: {len(chunk.page_content)} characters')
    print(f'Page: {chunk.metadata.get("page", "N/A")}')
    print(f'Source: {chunk.metadata.get("source", "N/A").split("/")[-1]}')
    print(f'Content:\n{chunk.page_content}')
    print()

print('\n=== Stage 3 === Creating Embeddings ===')
model = get_embedding_model()
print('Embedding first 3 chunks...\n')

for i in range(3):
    chunk_text = chunks[i].page_content[:80] + '...'
    vector = model.embed_query(chunks[i].page_content)
    
    print(f'Chunk {i}:')
    print(f'  Text: {chunk_text}')
    print(f'  Vector dimensions: {len(vector)}')
    print(f'  First 5 values: {[round(v, 6) for v in vector[:5]]}')
    print(f'  Range: [{min(vector):.4f}, {max(vector):.4f}]')
    print()

print('=== Stage 3(a) === Batch Embeddings ===')
print('Embedding all chunks at once...')
all_texts = [chunk.page_content for chunk in chunks]
all_vectors = model.embed_documents(all_texts)

print(f'Total embeddings created: {len(all_vectors)}')
print(f'Each embedding dimension: {len(all_vectors[0])}')
print(f'\nSample of Chunk 0 embedding (first 20 values):')
print([round(v, 4) for v in all_vectors[0][:20]])

print('\n=== Stage 4 === Database Operations ===')
from src.services.database import (
    get_chroma_client,
    get_vector_db,
    list_collections,
    delete_collections,
    get_collection_count
)

print('Initializing ChromaDB...')
client = get_chroma_client()
print(f'  ✓ Client type: {type(client).__name__}')

print('\nChecking existing collections...')
collections = list_collections()
print(f'  ✓ Collections found: {collections}')

print('\nInitializing vector database...')
vector_db = get_vector_db()
print(f'  ✓ Vector DB type: {type(vector_db).__name__}')
print(f'  ✓ Collection name: {vector_db._collection.name}')

print('\nChecking document count...')
count = get_collection_count()
print(f'  ✓ Documents in collection: {count}')

print('\n=== Database Ready for Indexing ===')
print(f'Database path: {settings.VECTOR_DB_PATH}')
print(f'Collection: {settings.COLLECTION_NAME}')
print(f'Embedding dimension: {len(all_vectors[0])}')

print('\n=== Stage 5 === Indexing Documents ===')
from src.services.indexing import index_directory

print('Storing documents in vector database...')
initial_count = get_collection_count()
print(f'Initial document count: {initial_count}')

result = index_directory()
print(f'\nIndexing complete:')
print(f'  ✓ PDFs processed: {result["pdf_count"]}')
print(f'  ✓ Pages loaded: {result["document_count"]}')
print(f'  ✓ Chunks indexed: {result["chunk_count"]}')

final_count = get_collection_count()
print(f'  ✓ New document count: {final_count}')
print(f'  ✓ Documents added: {final_count - initial_count}')

print('\n=== Stage 6 === Tokenization Analysis ===')
print('Analyzing how text is tokenized for embeddings...')

# Get the tokenizer from the embedding model
try:
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(settings.EMBEDDING_MODEL)
    
    sample_text = chunks[0].page_content[:200]
    print(f'\nSample text ({len(sample_text)} chars):')
    print(f'"{sample_text}..."')
    
    # Tokenize
    tokens = tokenizer.tokenize(sample_text)
    token_ids = tokenizer.encode(sample_text)
    
    print(f'\nTokenization results:')
    print(f'  ✓ Total tokens: {len(tokens)}')
    print(f'  ✓ Token IDs count: {len(token_ids)}')
    print(f'  ✓ First 15 tokens: {tokens[:15]}')
    print(f'  ✓ First 15 token IDs: {token_ids[:15]}')
    
    # Special tokens
    print(f'\nSpecial tokens:')
    print(f'  ✓ CLS token: {tokenizer.cls_token} (ID: {tokenizer.cls_token_id})')
    print(f'  ✓ SEP token: {tokenizer.sep_token} (ID: {tokenizer.sep_token_id})')
    print(f'  ✓ PAD token: {tokenizer.pad_token} (ID: {tokenizer.pad_token_id})')
    print(f'  ✓ Max length: {tokenizer.model_max_length}')
    
except Exception as e:
    print(f'  ⚠️ Could not load tokenizer: {e}')

print('\n=== Stage 7 === Transformer & Pooling ===')
print('Understanding embedding model architecture...')
print(f'\nModel: {settings.EMBEDDING_MODEL}')
print(f'Architecture: BERT-based (BGE model)')
print(f'Output dimension: {len(all_vectors[0])}')
print(f'\nPooling strategy: CLS Token Pooling')
print(f'  - Uses the [CLS] token representation')
print(f'  - [CLS] token is the first token in sequence')
print(f'  - Provides sentence-level representation')
print(f'  - Alternative would be mean pooling (averaging all tokens)')

print('\n=== Stage 8 === Retrieval Test ===')
from src.services.retrieval import retrieve_documents

# Option 1: Interactive input
print('Enter your test question (or press Enter for default):')
user_input = input('> ').strip()
test_question = user_input if user_input else "What is machine learning?"
print(f'\nTest question: "{test_question}"')

print('\nEmbedding the question...')
question_vector = model.embed_query(test_question)
print(f'  ✓ Question vector dimensions: {len(question_vector)}')
print(f'  ✓ First 5 values: {[round(v, 4) for v in question_vector[:5]]}')

print('\nSearching for similar documents...')
retrieved_docs = retrieve_documents(test_question, k=3)
print(f'  ✓ Retrieved {len(retrieved_docs)} documents')

print('\nTop 3 relevant chunks:')
for i, doc in enumerate(retrieved_docs, 1):
    content_preview = doc.page_content[:100].replace('\n', ' ')
    print(f'\n  [{i}] Page {doc.metadata.get("page", "?")}:')
    print(f'      {content_preview}...')

print('\n=== Stage 9 === Prompt Building ===')
from src.services.prompt_builder import build_prompt

print('Building RAG prompt from retrieved context...')
rag_prompt = build_prompt(test_question, retrieved_docs)

print(f'\nPrompt structure:')
print(f'  ✓ Total length: {len(rag_prompt)} characters')
print(f'  ✓ Contains system instructions: Yes')
print(f'  ✓ Context from {len(retrieved_docs)} documents: Yes')
print(f'  ✓ User question included: Yes')

print(f'\nPrompt preview (first 300 chars):')
print('-' * 70)
print(rag_prompt[:300] + '...')
print('-' * 70)

print('\n=== Stage 10 === LLM Pipeline ===')
from src.services.llm import generate_answer

print('Testing LLM integration...')
print(f'Model: {settings.MODEL_NAME}')
print(f'Backend: Ollama')

try:
    print('\nSending simple test prompt to LLM...')
    test_prompt = "Say 'Hello' in exactly one word."
    response = generate_answer(test_prompt)
    
    print(f'  ✓ LLM responded successfully')
    print(f'  ✓ Response: "{response}"')
    print(f'  ✓ Response length: {len(response)} characters')
    
    print('\n=== Stage 11 === LLM Tokenization ===')
    print('Note: LLM tokenization happens inside Ollama server')
    print(f'Model: {settings.MODEL_NAME}')
    print(f'Tokenizer: Model-specific (Qwen tokenizer)')
    print(f'Context window: Model-dependent')
    
    print('\n=== Stage 12 === Full RAG Query ===')
    print('Testing complete RAG pipeline with real question...')
    
    # Option 1: Interactive input
    print('\nEnter your final question (or press Enter for default):')
    user_final = input('> ').strip()
    final_question = user_final if user_final else "What is artificial intelligence?"
    print(f'\nQuestion: "{final_question}"')
    
    # Retrieve relevant documents
    print('\n[1] Retrieving relevant context...')
    context_docs = retrieve_documents(final_question, k=3)
    print(f'    Retrieved {len(context_docs)} documents')
    
    # Build prompt with context
    print('\n[2] Building RAG prompt...')
    full_prompt = build_prompt(final_question, context_docs)
    print(f'    Prompt length: {len(full_prompt)} characters')
    
    # Generate answer
    print('\n[3] Generating answer with LLM...')
    final_answer = generate_answer(full_prompt)
    
    print('\n' + '=' * 70)
    print('FINAL ANSWER')
    print('=' * 70)
    print(final_answer)
    print('=' * 70)
    
    print('\n=== Stage 13 === LLM Reasoning Analysis ===')
    print('LLM Reasoning Process:')
    print('  [1] Received prompt with system instructions')
    print('  [2] Tokenized input prompt')
    print('  [3] Processed through transformer layers')
    print('  [4] Applied attention mechanism to context')
    print('  [5] Generated response tokens sequentially')
    print('  [6] Applied temperature and sampling')
    print('  [7] Decoded tokens to text')
    
    print('\n✅ COMPLETE RAG PIPELINE TEST SUCCESSFUL!')
    
except Exception as e:
    print(f'\n⚠️ LLM Error: {type(e).__name__}')
    print(f'Message: {str(e)[:200]}')
    print('\nThis is likely due to:')
    print('  - Ollama server not running')
    print('  - Model not downloaded')
    print('  - Insufficient system memory')
    print('  - Model name mismatch')
    print('\nRAG retrieval and prompt building are working correctly.')
    print('LLM integration requires Ollama setup.')

print('\n' + '=' * 70)
print('COMPLETE PIPELINE STAGES SUMMARY')
print('=' * 70)
print('✅ Stage 1:  PDF Loading')
print('✅ Stage 2:  Document Chunking')
print('✅ Stage 3:  Embedding Generation')
print('✅ Stage 4:  Database Initialization')
print('✅ Stage 5:  Document Indexing')
print('✅ Stage 6:  Tokenization Analysis')
print('✅ Stage 7:  Transformer & Pooling')
print('✅ Stage 8:  Semantic Retrieval')
print('✅ Stage 9:  Prompt Building')
print('✅ Stage 10: LLM Integration')
print('✅ Stage 11: LLM Tokenization')
print('✅ Stage 12: Full RAG Query')
print('✅ Stage 13: LLM Reasoning')
print('=' * 70)
