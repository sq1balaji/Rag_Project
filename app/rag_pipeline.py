from app.embeddingd import get_embedding
from app.retriever import retrieve_similar_docs
from app.llm import generate_answer

def run_rag_pipeline(query: str) -> str:
    relevant_docs = retrieve_similar_docs(query)
    context = relevant_docs
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQ: {query}\nA:"
    return generate_answer(prompt)
