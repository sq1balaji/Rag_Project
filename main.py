from app.rag_pipeline import run_rag_pipeline
from data_loader.load_data import load_to_qdrant

if __name__ == "__main__":
     load_to_qdrant()
     query = input("Enter your query: ")
     answer = run_rag_pipeline(query)
     print(f"\nAnswer:\n{answer}")


    
