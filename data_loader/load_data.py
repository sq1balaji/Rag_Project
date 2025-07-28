import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import fetch_cve_documents
from app.embeddings import get_embedding
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
    print(f"Loaded {len(embedded_docs)} documents into Qdrant.")
    insert_documents(embedded_docs)
    print("Documents successfully inserted into Qdrant.")   


if __name__ == "__main__":
    load_to_qdrant()
