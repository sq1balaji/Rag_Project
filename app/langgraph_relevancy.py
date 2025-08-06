from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from app.rag_pipeline import retrieve_documents
from app.llm import generate_answer

# --- Step 1: Define relevance checker node ---
def check_relevancy(state):
    query = state["query"]
    docs = retrieve_documents(query)
    if not docs or len(docs) == 0:
        return {"query": query, "relevant": False}
    return {"query": query, "relevant": True, "docs": docs}

# --- Step 2: Define LLM response node ---
def get_response(state):
    return {"response": generate_answer(state["query"])}

# --- Step 3: Define fallback polite response ---
def get_polite_message(state):
    return {"response": "Sorry, I couldn’t find relevant information. Could you please rephrase your query?"}

# --- Step 4: Build the LangGraph ---
def build_relevancy_graph() -> Runnable:
    graph = StateGraph()

    graph.add_node("check_relevancy", check_relevancy)
    graph.add_node("llm_response", get_response)
    graph.add_node("polite_message", get_polite_message)

    # Transitions
    graph.set_entry_point("check_relevancy")
    graph.add_conditional_edges(
        "check_relevancy",
        lambda state: "llm_response" if state["relevant"] else "polite_message"
    )
    graph.add_edge("llm_response", END)
    graph.add_edge("polite_message", END)

    return graph.compile()
