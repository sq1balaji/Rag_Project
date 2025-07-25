
from qdrant_client.http import models as rest_models
from app.vectorstore import client
from app.config import Config
from app.embeddingd import get_embedding

def retrieve_similar_docs(cve_id):
    # Build filter to match exact cve_id in payload
    filter = rest_models.Filter(
        must=[
            rest_models.FieldCondition(
                key="cve_id",
                match= rest_models.MatchValue(value=cve_id)
            )
        ]
    )
    results = client.search(
        collection_name=Config.COLLECTION_NAME,
        query_vector=get_embedding(cve_id),
        query_filter = filter,
        limit=1                # only one result expected per unique CVE ID
    )
    
    # results is a list of hits, extract payloads
    if not results:
        return None  # or [] or raise error, as needed
    
    # Return payload dict for the first matched doc
    return results[0].payload


