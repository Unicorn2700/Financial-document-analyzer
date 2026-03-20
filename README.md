# Financial Document Analyzer  

---

## 1. Project Overview

This project implements an AI-powered financial document analysis system capable of processing financial PDF reports and generating structured insights.

The system integrates:

- FastAPI – REST API framework  
- CrewAI – Multi-agent orchestration  
- Ollama (Local LLM) – AI inference engine  
- Celery + Redis – Asynchronous task queue (Bonus Feature)

The original codebase contained structural, dependency, and architectural issues.  
This submission includes a fully debugged, stabilized, and production-ready version.

---

## 2. System Architecture

The system is intentionally designed with separation of concerns:

### 2.1 Asynchronous Background Processing (`/analyze`)
Implements scalable task execution using Celery and Redis.

**Flow:**

Client → FastAPI → Redis (Broker) → Celery Worker → Redis (Result Backend) → Client Polling

Purpose:
- Prevent API blocking
- Support concurrent document submissions
- Demonstrate queue worker architecture (Bonus Requirement)

---

### 2.2 Multi-Agent AI Analysis (`/analyze-ai`)
Executes full CrewAI multi-agent pipeline synchronously.

Agents involved:
- Financial Document Verifier
- Financial Analyst
- Risk Assessor
- Investment Advisor

Flow:
Client → FastAPI → CrewAI → Ollama → Structured Financial Report

Purpose:
- Provide deep financial reasoning
- Generate structured investment recommendations
- Demonstrate AI orchestration capability

---

## 3. Bugs Identified and Fixed

The original codebase had multiple issues. They are categorized below.

---

### 3.1 Core Code Issues

#### 3.1.1 Incorrect CrewAI Import
Original:
```python
from crewai.agents import Agent
```

Corrected to:
```python
from crewai import Agent
```

---

#### 3.1.2 Invalid Tool Import
`search_tool` was imported but not defined in `tools.py`.

Fix:
- Removed invalid import
- Aligned tool definitions with actual implementation

---

#### 3.1.3 Unreliable Agent Prompts
Original agents:
- Fabricated financial advice
- Approved all documents without validation
- Used exaggerated investment language

Fix:
- Enforced document-based reasoning
- Structured output format
- Removed hallucination-prone instructions

---

#### 3.1.4 Missing Crew Initialization
`financial_crew` was referenced before proper initialization.

Fix:
- Defined global Crew instance in `main.py`

---

#### 3.1.5 Missing FastAPI `app` Instance
Error:
```
Error loading ASGI app. Attribute "app" not found
```

Fix:
```python
app = FastAPI()
```
Defined at module level.

---

#### 3.1.6 Nested Folder Structure
Duplicate folder naming caused:
```
ModuleNotFoundError: No module named 'main'
```

Fix:
- Flattened directory structure
- Corrected import paths

---

#### 3.1.7 Large LLM Context Causing Freezing
Entire PDF passed to LLM caused:
- Extremely slow execution
- Blocking behavior
- Timeouts

Fix:
```python
document_text = document_text[:4000]
```

---

### 3.2 Dependency Conflicts

#### 3.2.1 Pydantic Version Conflict
FastAPI and CrewAI required different versions.

Fix:
- Removed manual version pinning
- Upgraded FastAPI to version compatible with Pydantic v2
- Allowed dependency resolver to manage versions

---

#### 3.2.2 OpenAI Version Conflict
Manual OpenAI version conflicted with CrewAI's internal dependency chain.

Fix:
- Removed manual OpenAI version specification
- Allowed CrewAI dependencies to resolve automatically

---

### 3.3 Celery & Redis Issues (Bonus Feature)

#### 3.3.1 Celery Task Import Error
```
ModuleNotFoundError: No module named 'main'
```

Fix:
- Corrected project structure
- Adjusted task import paths

---

#### 3.3.2 Queue Routing Issue
Tasks were not being consumed.

Fix:
```python
celery_app.conf.task_routes = {
    "celery_worker.run_analysis": {"queue": "financial_queue"}
}
```

---

#### 3.3.3 Redis Not Running
Docker daemon not started.

Fix:
```bash
docker run -d -p 6379:6379 --name redis-server redis
```

---

#### 3.3.4 CrewAI Blocking Inside Celery Worker
LLM execution inside multiprocessing worker caused indefinite hanging (Windows environment).

Solution:
- Separated AI execution from queue worker
- `/analyze` handles background tasks
- `/analyze-ai` handles synchronous AI reasoning

This ensures stability while still demonstrating queue architecture.

---

## 4. Setup Instructions

### 4.1 Clone Repository

```bash
git clone <repository-url>
cd financial-document-analyzer
```

---

### 4.2 Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 4.3 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4.4 Start Redis (Docker)

```bash
docker run -d -p 6379:6379 --name redis-server redis
```

If container already exists:

```bash
docker start redis-server
```

---

### 4.5 Start Celery Worker

```bash
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo -Q financial_queue
```

Wait until:
```
ready.
```

---

### 4.6 Launch FastAPI Server

```bash
uvicorn main:app --reload
```

Server runs at:
```
http://127.0.0.1:8000
```

---

## 5. API Documentation

Interactive documentation available at:

```
http://127.0.0.1:8000/docs
```

---

### 5.1 POST `/analyze`

Submits document for background processing.

Request:
- `query` (string)
- `file` (PDF)

Response:
```json
{
  "status": "queued",
  "task_id": "uuid"
}
```

---

### 5.2 GET `/result/{task_id}`

Retrieves result of background task.

Response:
```json
{
  "status": "SUCCESS",
  "result": {...}
}
```

---

### 5.3 POST `/analyze-ai`

Executes full multi-agent financial analysis.

Response:
- Executive Summary
- Key Financial Metrics
- Risk Assessment
- Investment Outlook

---

## 6. Design Decisions

- Separated AI inference from queue execution to avoid worker deadlocks
- Implemented character limit safeguard for LLM stability
- Removed unnecessary dependency pinning
- Modularized infrastructure and AI components
- Ensured reproducible setup via requirements.txt and Docker Redis

---

## 7. Assignment Requirements Fulfilled

- Fixed all core codebase issues  
- Resolved dependency conflicts  
- Implemented Queue Worker Model (Celery + Redis)  
- Provided full API documentation  
- Stabilized multi-agent financial AI pipeline  
- Documented debugging process thoroughly  

---

**Submission Complete**
