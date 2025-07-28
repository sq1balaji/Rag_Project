import mlflow

def log_evaluation(query, answer, context):
    mlflow.set_experiment("task-1")

    with mlflow.start_run():
        mlflow.log_param("query", query)
        mlflow.log_param("context_used", context)
        mlflow.log_text(answer, "response.txt")
