import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import fetch_cve_documents
from app.embeddingd import get_embedding
from app.vectorstore import create_collection, insert_documents


def load_to_qdrant():
    create_collection()
    docs = fetch_cve_documents()

    embedded_docs = []
    for doc in docs:
        embedded_docs.append({
            "id": doc["id"],
            "cve_id": doc["cve_id"],
            "description": doc["description"],
            "problem_types": doc["problem_types"],
            "cvss_metrics": doc["cvss_metrics"],
            "severity": doc["severity"],
            "vuln_status": doc["vuln_status"],
            "embedding": get_embedding(doc["description"])
        })

    insert_documents(embedded_docs)