import os
import streamlit as st
from app.rag_pipeline import run_rag_pipeline
from qdrant_client import QdrantClient



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
        st.text("Started embedding...")
        try:
            answer = run_rag_pipeline(query)
            st.text("Finished Embedding\n")
            st.markdown("**Answer:**")
            print(answer)
            st.markdown(answer)
        except Exception as e:
            st.error(f"❌ Error: {e}")
