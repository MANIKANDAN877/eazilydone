# Fintech Q&A Chatbot

A beginner-friendly fintech chatbot project built with React, FastAPI, and PostgreSQL for local internship demo use.

## What this project does

- React frontend sends user questions to a Python FastAPI backend
- FastAPI matches the question against a PostgreSQL knowledge base
- The app returns the best answer, source URL, and confidence score
- If no match is found, the chatbot shows a safe fallback message
- The project is educational and explicitly states it is not an official Indian Overseas Bank service

## Project structure

- frontend/: Vite + React UI
- backend/: FastAPI app and environment variables
- database/: PostgreSQL schema and seed data
- README.md: project instructions

## Technology stack

- Frontend: React + Vite
- Backend: Python + FastAPI
- Database: PostgreSQL 17
- Communication: REST API with JSON

## Local setup

### 1) Check the environment

```powershell
python --version
node --version
npm --version
psql --version
```

### 2) Create the PostgreSQL database

```powershell
$env:Path += ';C:\Program Files\PostgreSQL\17\bin'
psql -U postgres -c "CREATE DATABASE fintech_chatbot;"
psql -U postgres -d fintech_chatbot -f D:\newassign\fintech-chatbot\database\schema.sql
psql -U postgres -d fintech_chatbot -f D:\newassign\fintech-chatbot\database\seed.sql
```

### 3) Start the backend

```powershell
Set-Location 'D:\newassign\fintech-chatbot\backend'
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 4) Start the frontend

```powershell
Set-Location 'D:\newassign\fintech-chatbot\frontend'
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Test the app

### Backend health

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected output:

```json
{ "status": "ok", "service": "Fintech Chatbot API" }
```

### Chat test

```powershell
$body = @{ question = 'What is the repayment period for a personal loan?' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/chat -ContentType 'application/json' -Body $body
```

Expected result:

```json
{
  "question": "What is the repayment period for a personal loan?",
  "answer": "The official IOB personal loan information states the maximum repayment period is 84 months...",
  "category": "personal_loan_repayment",
  "match_found": true
}
```

## Files to know

- [backend/app/main.py](backend/app/main.py): FastAPI endpoints
- [backend/app/chatbot.py](backend/app/chatbot.py): score and match logic
- [backend/app/database.py](backend/app/database.py): PostgreSQL queries
- [backend/app/schemas.py](backend/app/schemas.py): request/response models
- [database/schema.sql](database/schema.sql): table definition
- [database/seed.sql](database/seed.sql): sample questions and answers
- [frontend/src/App.jsx](frontend/src/App.jsx): chatbot interface

## Important notes

- This is a prototype for educational use only.
- It does not use ChatGPT, an LLM, or paid APIs.
- Financial facts should be verified against official bank information before use.
- The app is designed for local development and demonstration only.
