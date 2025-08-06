from sqlalchemy import create_engine, text
from app.config import Config
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(Config.DATABASE_URL)

def fetch_cve_documents(limit=100):
    print("Connecting with the postgres db...")
    with engine.connect() as conn:
        print("Connected with thw postgres db.")
        query = text("""
            SELECT 
                id,
                cve_id, 
                description, 
                problem_types, 
                cvss_metrics, 
                severity, 
                vuln_status 
            FROM cves
            LIMIT :limit
        """)
        result = conn.execute(query, {"limit": limit})
        print(f"Fetched {limit} no of data....")
        return [
            {
                "id" : row["id"],
                "cve_id": row["cve_id"],
                "description": row["description"],
                "problem_types": row["problem_types"],
                "cvss_metrics": row["cvss_metrics"],
                "severity": row["severity"],
                "vuln_status": row["vuln_status"]
            }
            for row in result.mappings()
            
        ]
