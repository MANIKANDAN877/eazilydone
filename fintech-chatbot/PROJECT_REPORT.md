# Eazily Done — Fintech Account Assistant

## 1. Overview

Eazily Done is a fintech assistant for account insights, loan FAQ guidance, and business-finance education. The system combines a React frontend, a FastAPI backend, and a database-backed knowledge layer to answer questions related to account analysis, expense breakdowns, fees, savings guidance, and official Indian Overseas Bank (IOB) loan information.

## 2. Business objective

The project is designed to help users:

- understand account activity through debit/credit percentages and fee explanations,
- ask finance questions in natural language,
- review MSME and business-loan FAQs,
- access official IOB information about loans, eligibility, documents, and scheme guidance,
- receive a professional, user-friendly response experience.

## 3. System architecture

The application follows a simple three-layer architecture:

1. Frontend layer
   - React + Vite
   - Chat interface with suggestion chips and message rendering
   - Chart panel for account-activity breakdowns

2. API layer
   - FastAPI service in the backend
   - Routes for health checks, suggested questions, and chat handling
   - CORS support for local frontend development

3. Knowledge layer
   - Structured question/answer records in the SQL seed data
   - Smart fallback knowledge in the Python chatbot logic
   - Official IOB references for MSME and business-loan guidance

## 4. Features implemented

- Business-loan FAQs
- MSME loan guidance
- Eligibility checks and application readiness guidance
- Required document explanations
- Interest-rate awareness with source-based disclaimers
- Account breakdown analysis for debits, credits, fees, and penalties
- Fee and penalty explanation for common account-related charges
- Savings recommendations and account-product guidance
- Professional response formatting
- DB-safe fallback responses when the database is unavailable

## 5. Technology stack

- Frontend: React, Vite, JavaScript, CSS
- Backend: Python, FastAPI, Uvicorn
- Database: PostgreSQL with psycopg2
- Validation: Python unittest / pytest
- Deployment mode: local full-stack development environment

## 6. Implementation notes

The main issue with the original chatbot was that it relied on shallow keyword matching, which caused generic answers for finance questions that needed specific product and scheme context. The improved solution adds:

- explicit official IOB answer mapping for business loans, MSME loans, and documents,
- account-breakdown detection for percentage-based financial requests,
- fee and savings guidance for common user questions,
- graceful fallback when the database is unavailable,
- source-aware answers so users are directed to official IOB materials when policy details require verification.

## 7. Official IOB sources used

- https://www.iob.bank.in/en/
- https://www.iob.bank.in/en/msme
- https://www.iob.bank.in/en/iob-msme-easy

## 8. Data and security considerations

This assistant provides educational and informational support, not an official bank application channel. Loan eligibility, rate information, fees, and documentation requirements can change, so final verification should always happen on the official IOB website or with the bank branch.

## 9. Outcome

The project now provides a working fintech assistant with a chat UI, more professional answer quality, official source references, and stronger financial-topic handling than the original prototype.
