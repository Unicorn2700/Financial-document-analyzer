import sys
import os
sys.path.append(os.getcwd())
from celery import Celery

# celery -A celery_worker.celery_app worker --loglevel=info --pool=solo -Q financial_queue
celery_app = Celery(
    "financial_tasks",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

celery_app.conf.task_routes = {
    "celery_worker.run_analysis": {"queue": "financial_queue"}
}

@celery_app.task(name="celery_worker.run_analysis")
def run_analysis(query, file_path):
    from tools import FinancialDocumentTool

    document_text = FinancialDocumentTool.read_data_tool(file_path)
    document_text = document_text[:3000]  # keep limit

    return {
        "status": "processed",
        "query": query,
        "document_preview": document_text[:800],
        "note": "Full AI analysis available via synchronous endpoint."
    }