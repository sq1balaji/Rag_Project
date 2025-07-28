from app.retriever import retrieve_similar_docs
from app.llm import generate_answer

def run_rag_pipeline(query: str) -> tuple[str, str]:
    relevant_docs = retrieve_similar_docs(query)
    if relevant_docs is None:
        raise ValueError("No relevant documents found.")

    context = str(relevant_docs)

    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQ: {query}\nA:"
    answer = generate_answer(prompt)

    return answer, context
