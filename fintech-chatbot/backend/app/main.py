from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .chatbot import find_best_answer
from .config import settings
from .database import fetch_questions, fetch_suggested_questions
from .schemas import ChatRequest, ChatResponse

app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.APP_TITLE}


@app.get("/questions")
def get_questions():
    try:
        rows = fetch_suggested_questions(limit=10)
        return {"questions": rows}
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}") from exc


@app.post("/chat", response_model=ChatResponse)
def chat_with_bot(payload: ChatRequest):
    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result = find_best_answer(question)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}") from exc

    if result is None:
        return ChatResponse(
            question=question,
            answer=(
                "I could not find a strong match in the current knowledge base. "
                "This chatbot is an educational prototype and is not an official Indian Overseas Bank service. "
                "Please check the official IOB website for the latest policy, eligibility, rates, and documents."
            ),
            category="unmatched",
            source_url="https://www.iob.bank.in/en/",
            confidence=0,
            match_found=False,
        )

    return ChatResponse(
        question=question,
        answer=result["answer"],
        category=result["category"],
        source_url=result.get("source_url"),
        confidence=result.get("confidence", 0),
        match_found=True,
        chart=result.get("chart"),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
