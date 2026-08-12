class ConversationMemory:
    """
    Manages conversation history for the RAG chat system.
    Keeps the last 6 messages (3 Q&A pairs) to provide context
    while avoiding token limit issues.
    """

    def __init__(self, max_messages: int = 6):
        self.messages = []
        self.max_messages = max_messages

    def add_user_message(self, message: str):
        """Add a user message to the conversation history."""
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        self._trim_messages()

    def add_assistant_message(self, message: str):
        """Add an assistant message to the conversation history."""
        self.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )
        self._trim_messages()

    def get_messages(self):
        """Get the recent conversation history (up to max_messages)."""
        return self.messages[-self.max_messages:]

    def _trim_messages(self):
        """Trim messages to keep only the most recent ones."""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def clear(self):
        """Clear all conversation history."""
        self.messages.clear()

    def get_message_count(self) -> int:
        """Get the total number of messages in history."""
        return len(self.messages)

    def is_empty(self) -> bool:
        """Check if conversation history is empty."""
        return len(self.messages) == 0