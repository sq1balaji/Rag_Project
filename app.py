import os
import streamlit as st
# from app.rag_pipeline import run_rag_pipeline
from app.llm import respond_with_relevancy_check
from app.rag_pipeline import retrieve_similar_docs
from evaluation.evaluate import log_evaluation
from app.vectorstore import create_collection
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

create_collection()
qdrant_url = os.getenv("QDRANT_URL")
client = QdrantClient(url=qdrant_url)
st.set_page_config(page_title="CVE RAG System", layout="centered")

st.title("🔍 CVE RAG Query Interface")
st.markdown("Search for CVE-related information using RAG")

query = st.text_input("Enter your query:", placeholder="e.g., CVE-2016-4777")

if st.button("Submit"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        try:
            answer = respond_with_relevancy_check(query)
            # context = retrieve_similar_docs(query)
            st.markdown("**Answer:**")
            st.markdown(answer)

            # ✅ Log to MLflow
            # log_evaluation(query, answer, context)

        except Exception as e:
            st.error(f"❌ Error: {e}")



