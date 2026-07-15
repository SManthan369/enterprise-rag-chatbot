import json
import os
from dotenv import load_dotenv

load_dotenv()
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

from langchain_groq import ChatGroq
from ragas.llms import LangchainLLMWrapper


def main():

    with open(
        "evaluation/results.json",
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    dataset = Dataset.from_list(data)

    # Groq model for RAG evaluation
    groq_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    evaluator_llm = LangchainLLMWrapper(groq_llm)

    result = evaluate(
        dataset=dataset,
        metrics=[
            Faithfulness(),
            AnswerRelevancy(),
            ContextPrecision(),
            ContextRecall(),
        ],
        llm=evaluator_llm,
    )

    print("\n========== RAGAS RESULTS ==========\n")
    print(result)

    df = result.to_pandas()

    df.to_csv(
        "evaluation/ragas_results.csv",
        index=False
    )

    print("\nSaved to evaluation/ragas_results.csv")


if __name__ == "__main__":
    main()