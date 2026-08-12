from functools import lru_cache
import ollama
import src.config.settings as settings

from src.exceptions.llm_exception import (
    LLMException,
)
from src.utils.logger import logger
from src.utils.performance import measure_performance

@lru_cache(maxsize=1)
@measure_performance("Ollama Client Initialization")
def get_ollama_client():
    try:
        return ollama.Client()
    except Exception as ex:
        logger.exception(f"Failed to initialize Ollama client: {ex}")
        raise LLMException(f"Failed to initialize Ollama client: {ex}") from ex 

@measure_performance("LLM Response Generation")
def generate_answer(prompt: str, stream: bool = False):
    """
    Generate answer from LLM.
    
    Args:
        prompt: The prompt to send to the LLM
        stream: If True, returns a generator that yields chunks.
                If False, returns the complete answer as a string.
    
    Returns:
        str if stream=False, or generator if stream=True
    """
    try:
        client = get_ollama_client()
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        if stream:
            # Return generator for streaming
            return _stream_response(client, messages)
        else:
            # Return complete response
            response = client.chat(
                model=settings.MODEL_NAME,
                messages=messages
            )
            return response["message"]["content"]
    
    except Exception as ex:
        logger.exception(f"Failed to generate response from Ollama: {ex}")
        raise LLMException(f"Failed to generate response from Ollama: {ex}") from ex

def _stream_response(client, messages):
    """
    Internal generator function for streaming responses.
    """
    try:
        stream = client.chat(
            model=settings.MODEL_NAME,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            content = chunk["message"]["content"]
            if content:  # Only yield non-empty content
                yield content
    
    except Exception as ex:
        logger.exception(f"Streaming error: {ex}")
        raise LLMException(f"Streaming failed: {ex}") from ex

    