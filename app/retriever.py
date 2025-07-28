from qdrant_client.http import models as rest_models
from app.vectorstore import client, create_collection
from app.config import Config
from app.embeddings import get_embedding  

def retrieve_similar_docs(cve_id):
    create_collection()
    embedding = get_embedding(cve_id)

    filter = rest_models.Filter(
        must=[
            rest_models.FieldCondition(
                key="cve_id",
                match=rest_models.MatchValue(value=cve_id)
            )
        ]
    )

    results = client.search(
        collection_name=Config.COLLECTION_NAME,
        query_vector=embedding,  
        query_filter=filter,
        limit=1
    )

    if not results:
        return None
    
    return results[0].payload