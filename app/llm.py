import json
import requests
import time
from dotenv import load_dotenv
from app.config import Config
# from app.rag_pipeline import relevant_docs
from app.retriever import retrieve_similar_docs

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional

load_dotenv()

# --- Step 1: Keep your existing generate_answer function ---
# def generate_answer(prompt: str) -> str:
#     headers = {"Content-Type": "application/json"}
#     for attempt in range(10):
#         try:
#             response = requests.post(f"{Config.OLLAMA_API}/api/generate", json={
#                 "model": "llama3.2:1b",
#                 "prompt": prompt,
#                 "stream": False
#             }, headers=headers)
#             response.raise_for_status()
#             return response.json()["response"]
#         except requests.exceptions.RequestException as e:
#             print(f"[Generate Retry {attempt+1}/10] Ollama not ready yet: {e}")
#             time.sleep(2)
#     raise RuntimeError("Failed to connect to Ollama generate API after 10 retries.")

def generate_answer(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}

    for attempt in range(10):
        try:
            print(f"\n🔁 Attempt {attempt + 1}: Sending prompt to Ollama:\n{prompt}\n", flush=True)

            response = requests.post(
                f"{Config.OLLAMA_API}/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False
                },
                headers=headers
            )
            response.raise_for_status()

            # Debug: print raw JSON response
            print("📝 Raw response from Ollama:", response.text, flush=True)

            data = response.json()
            answer = data.get("response", "").strip()

            if not answer:
                print("⚠️ Empty response received from LLM!", flush=True)
            else:
                print("✅ LLM Response:", answer, flush=True)

            return answer

        except requests.exceptions.RequestException as e:
            print(f"[Generate Retry {attempt+1}/10] Ollama not ready yet: {e}", flush=True)
            time.sleep(2)

    raise RuntimeError("❌ Failed to connect to Ollama generate API after 10 retries.")


# --- Step 2: LangGraph Nodes ---
def check_relevancy(state):
    query = state["query"].strip().upper()
    docs = retrieve_similar_docs(query)
    if not docs or len(docs) == 0:
        return {"query": query, "relevant": False}
    return {"query": query, "relevant": True, "docs": docs}

def get_response(state):
    query = state["query"]
    docs = state["docs"]

    if not docs:
        return {"response": "Sorry, I couldn’t retrieve any relevant document."}

    doc = docs[0]

    # Extract context fields
    description = doc.get('description', 'No description available.')
    severity = doc.get('severity', 'Unknown')
    vuln_status = doc.get('vuln_status', 'Unknown')

    cvss_score = "Not available"
    cvss_vector = "Not available"
    cvss_severity = "Not available"

    if 'cvss_metrics' in doc and 'v2' in doc['cvss_metrics']:
        cvss = doc['cvss_metrics']['v2']
        cvss_score = cvss.get('baseScore', 'N/A')
        cvss_vector = cvss.get('vectorString', 'N/A')
        cvss_severity = cvss.get('severity', 'N/A')

    # Context for display (from Qdrant)
    context_display = (
        f"🛡️ **CVE ID:** {doc.get('cve_id')}\n"
        f"📝 **Description:** {description}\n"
        f"📛 **Severity:** {severity}\n"
        f"📊 **CVSS Score:** {cvss_score} ({cvss_vector}) - {cvss_severity}\n"
        f"🔄 **Status:** {vuln_status}\n\n"
    )

    # Prompt to LLM - generate solution/mitigation based only on description
    prompt = (
        "You are a cybersecurity assistant. Based on the following CVE description, suggest potential mitigations, patches, or best practices to address the issue.\n\n"
        f"Description:\n{description}\n\n"
        f"Question: What are the possible solutions or mitigations for {query}?\n"
        "Answer:"
    )

    print("📋 CVE Metadata:\n", context_display)
    print("🧠 Prompt to LLM:\n", prompt, flush=True)

    llm_response = generate_answer(prompt)

    return {
        "response": f"{context_display}\n💡 **Suggested Solution:**\n{llm_response}"
    }


def get_polite_message(state):
    return {"response": "Sorry, I couldn’t find relevant information. Could you please rephrase your query?"}


class GraphState(TypedDict):
    query: str
    relevant: Optional[bool]
    docs: Optional[List[str]]
    response: Optional[str]

# --- Step 3: Build LangGraph ---
def build_relevancy_graph():
    graph = StateGraph(GraphState)
    graph.add_node("check_relevancy", check_relevancy)
    graph.add_node("llm_response", get_response)
    graph.add_node("polite_message", get_polite_message)

    graph.set_entry_point("check_relevancy")
    graph.add_conditional_edges(
        "check_relevancy",
        lambda state: "llm_response" if state["relevant"] else "polite_message"
    )
    graph.add_edge("llm_response", END)
    graph.add_edge("polite_message", END)

    return graph.compile()

# --- Step 4: Final function to expose ---
def respond_with_relevancy_check(query: str) -> str:
    graph = build_relevancy_graph()
    result = graph.invoke({"query": query})
    return result["response"]
