from dataclasses import dataclass
from datetime import date


@dataclass
class QuestionRecord:
    id: int
    question: str
    answer: str
    category: str
    keywords: str
    source_url: str | None
    last_verified_at: date
