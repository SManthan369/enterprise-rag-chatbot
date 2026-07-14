from fastapi import FastAPI
from pydantic import BaseModel

from src.rag import RAGChatbot


app = FastAPI(
    title="Enterprise RAG API",
    description="AI Document Assistant API"
)


# Load chatbot once

bot = RAGChatbot()



class QuestionRequest(BaseModel):

    question: str



@app.get("/")
def home():

    return {
        "message": "Enterprise RAG API running"
    }



@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    answer, docs = bot.ask(
        request.question
    )


    sources = []


    for doc in docs:

        sources.append(
            {
                "page": doc.metadata.get(
                    "page",
                    0
                ) + 1,

                "source": doc.metadata.get(
                    "source",
                    "unknown"
                )
            }
        )


    return {

        "answer": answer,

        "sources": sources

    }