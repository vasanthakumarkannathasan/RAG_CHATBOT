from src.utils.logger import logger


class ConversationMemory:
    """
    Manages conversation history for the RAG chat system.
    Keeps the last 6 messages (3 Q&A pairs) to provide context
    while avoiding token limit issues.
    """

    def __init__(self, max_messages: int = 6):
        self.messages = []
        self.max_messages = max_messages
        logger.info(f"Initialized ConversationMemory with max_messages={max_messages}")

    def add_user_message(self, message: str):
        """Add a user message to the conversation history."""
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        self._trim_messages()
        logger.debug(f"Added user message (total messages: {len(self.messages)})")

    def add_assistant_message(self, message: str):
        """Add an assistant message to the conversation history."""
        self.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )
        self._trim_messages()
        logger.debug(f"Added assistant message (total messages: {len(self.messages)})")

    def get_messages(self):
        """Get the recent conversation history (up to max_messages)."""
        recent_messages = self.messages[-self.max_messages:]
        logger.debug(f"Retrieved {len(recent_messages)} recent messages")
        return recent_messages

    def _trim_messages(self):
        """Trim messages to keep only the most recent ones."""
        if len(self.messages) > self.max_messages:
            trimmed_count = len(self.messages) - self.max_messages
            self.messages = self.messages[-self.max_messages:]
            logger.debug(f"Trimmed {trimmed_count} old messages")

    def clear(self):
        """Clear all conversation history."""
        message_count = len(self.messages)
        self.messages.clear()
        logger.info(f"Cleared conversation history ({message_count} messages removed)")

    def get_message_count(self) -> int:
        """Get the total number of messages in history."""
        return len(self.messages)

    def is_empty(self) -> bool:
        """Check if conversation history is empty."""
        return len(self.messages) == 0