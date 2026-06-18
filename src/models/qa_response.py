from pydantic import BaseModel
from pydantic import Field

from typing import List


class QAResponse(BaseModel):

    answer: str = Field(
        description="Answer to the user"
    )

    confidence: str = Field(
        description="high medium low"
    )

    reasoning: str = Field(
        description="Reasoning"
    )

    follow_up_questions: List[str] = Field(
        default_factory=list
    )

    sources_needed: bool = Field(
        default=False
    )