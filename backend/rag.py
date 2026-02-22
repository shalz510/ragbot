from langchain_openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

MIN_CONTEXT_LENGTH = 200  # characters


def get_answer(db, question):
    # Retrieve top-k documents
    docs = db.similarity_search(question, k=6)

    # Combine context
    context = "\n\n".join(doc.page_content for doc in docs).strip()

    # 🚨 Hallucination Guard
    if len(context) < MIN_CONTEXT_LENGTH:
        return (
            "❌ The answer to this question is not available in the uploaded document.\n\n"
            "Please ask a question related to the provided content."
        )

    prompt = f"""
You are a document-based AI assistant.

Answer STRICTLY using the context below.
If the answer is not present, say:
"The information is not available in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    llm = OpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    return llm.invoke(prompt).strip()
