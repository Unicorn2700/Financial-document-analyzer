from fastapi import FastAPI, UploadFile, File
from celery_worker import run_analysis
from tools import FinancialDocumentTool
from crewai import Crew, Process
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from task import verification_task, analysis_task, risk_task, investment_task
import shutil

app = FastAPI()

# Create Crew globally
financial_crew = Crew(
    agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
    tasks=[verification_task, analysis_task, risk_task, investment_task],
    process=Process.sequential
)

def generate_report(query, file_path):
    document_text = FinancialDocumentTool.read_data_tool(file_path)
    document_text = document_text[:4000]
    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path,
        "document_text": document_text
    })
    return result

@app.post("/analyze")
async def analyze(query: str, file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Queue background task
    task = run_analysis.delay(query, file_path)

    return {
        "status": "queued",
        "task_id": task.id,
        "message": "Document submitted for background processing."
    }

@app.post("/analyze-ai")
async def analyze_ai(query: str, file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    document_text = FinancialDocumentTool.read_data_tool(file_path)
    document_text = document_text[:4000]

    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path,
        "document_text": document_text
    })

    return {"result": result}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    from celery.result import AsyncResult
    from celery_worker import celery_app

    result = AsyncResult(task_id, app=celery_app)

    return {
        "status": result.status,
        "result": result.result
    }