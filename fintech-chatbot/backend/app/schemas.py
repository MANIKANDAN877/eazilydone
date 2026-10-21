from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)


class ChartItem(BaseModel):
    label: str
    value: int
    color: str


class ChartData(BaseModel):
    title: str
    items: list[ChartItem]


class ChatResponse(BaseModel):
    question: str
    answer: str
    category: str
    source_url: str | None = None
    confidence: int = 0
    match_found: bool = True
    chart: ChartData | None = None
