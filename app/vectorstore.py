from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import Config
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(url=Config.QDRANT_HOST)

def create_collection():
    if not client.collection_exists(Config.COLLECTION_NAME):
        client.recreate_collection(
            collection_name=Config.COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

def insert_documents(docs):
    if not docs:
        print("No document insert into the Qdrant...")
        return
    
    vectors = [doc["embedding"] for doc in docs]
    ids = [doc["id"] for doc in docs]

    payloads = [
        {
            "cve_id": doc["cve_id"],
            "description": doc["description"],
            "problem_types": doc["problem_types"],
            "cvss_metrics": doc["cvss_metrics"],
            "severity": doc["severity"],
            "vuln_status": doc["vuln_status"]
        }
        for doc in docs
    ]

    print(f"Inserting {len(docs)} documents into Qdrant")


    client.upsert(
        collection_name=Config.COLLECTION_NAME,
        points=[
            {"id": ids[i], "vector": vectors[i], "payload": payloads[i]}
            for i in range(len(docs))
        ]
    )
