
# Financial Document Analyzer

Financial Document Analyzer is an AI-powered system for processing financial PDF reports and generating structured financial insights using multi-agent reasoning.

This project was built to explore how modern LLM orchestration frameworks can be combined with scalable backend systems to analyze complex financial documents efficiently.

The system integrates:

- FastAPI — REST API framework  
- CrewAI — Multi-agent orchestration  
- Ollama — Local LLM inference  
- Celery + Redis — Asynchronous background task execution  

It combines production-style backend architecture with AI agent collaboration for financial report analysis.

---

## System Architecture

The application is designed with clear separation between asynchronous task execution and AI reasoning.

### Asynchronous Background Processing (`/analyze`)

Implements non-blocking document submission using Celery and Redis.

**Flow:**  
Client → FastAPI → Redis Broker → Celery Worker → Redis Result Backend → Client Polling

**Purpose:**

- Prevent API blocking during document uploads  
- Support concurrent task execution  
- Simulate queue-based scalable backend architecture  

---

### Multi-Agent Financial Analysis (`/analyze-ai`)

Runs a full CrewAI pipeline for structured financial reasoning.

**Agents involved:**

- Financial Document Verifier  
- Financial Analyst  
- Risk Assessor  
- Investment Advisor  

**Flow:**  
Client → FastAPI → CrewAI → Ollama → Structured Financial Report  

**Purpose:**

- Extract key financial insights  
- Generate risk assessment  
- Provide investment-oriented observations  
- Explore collaborative multi-agent reasoning with local LLMs  

---

## Implementation Highlights

### CrewAI Integration

Configured CrewAI agents using proper initialization patterns and modular task definitions.

```python
from crewai import Agent
````

### Structured Agent Prompt Design

Designed prompts to improve output reliability by enforcing:

* Document-grounded reasoning
* Structured financial summaries
* Controlled recommendation style

### FastAPI Service Layer

Built FastAPI endpoints for both queued processing and synchronous AI analysis.

```python
app = FastAPI()
```

### LLM Context Optimization

To maintain stable inference speed, document input is truncated before sending to the model.

```python
document_text = document_text[:4000]
```

This prevents long-context slowdowns during local inference.

### Queue Routing with Celery

Configured dedicated task routing for background financial analysis jobs.

```python
celery_app.conf.task_routes = {
    "celery_worker.run_analysis": {"queue": "financial_queue"}
}
```

### Redis-Based Task Orchestration

Redis is used as:

* Message broker
* Result backend

This enables asynchronous task execution and polling-based result retrieval.

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/Unicorn2700/Financial-document-analyzer
cd financial-document-analyzer
```

### Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Redis (Docker)

```bash
docker run -d -p 6379:6379 --name redis-server redis
```

If container already exists:

```bash
docker start redis-server
```

### Start Celery Worker

```bash
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo -Q financial_queue
```

Wait until:

```bash
ready.
```

### Launch FastAPI Server

```bash
uvicorn main:app --reload
```

Server runs at:

```bash
http://127.0.0.1:8000
```

---

## API Documentation

Interactive API docs available at:

```bash
http://127.0.0.1:8000/docs
```

### POST `/analyze`

Submit document for background processing.

**Request:**

* `query` (string)
* `file` (PDF)

**Response:**

```json
{
  "status": "queued",
  "task_id": "uuid"
}
```

### GET `/result/{task_id}`

Retrieve background task result.

**Response:**

```json
{
  "status": "SUCCESS",
  "result": {...}
}
```

### POST `/analyze-ai`

Run full multi-agent financial analysis.

**Output includes:**

* Executive Summary
* Key Financial Metrics
* Risk Assessment
* Investment Outlook

---

## Design Decisions

* Separated AI inference from queue execution for stability
* Added input-size safeguards for local LLM responsiveness
* Modularized backend and AI layers independently
* Used Redis + Celery to simulate scalable task architecture
* Designed the project to explore production-style AI service patterns

---

## Tech Stack

* FastAPI
* CrewAI
* Ollama
* Celery
* Redis
* Docker
* Python

```
```
