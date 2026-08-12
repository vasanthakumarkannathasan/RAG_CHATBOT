from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="User question"
    )

    source: str | None = Field(
        default=None,
        description="Optional document filter"
    )

    session_id: str | None = Field(
        default=None,
        description="Conversation session id"
    )