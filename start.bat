@echo off
REM Run Alembic migrations
alembic upgrade head

REM Start FastAPI
uvicorn app.main:app --reload
pause