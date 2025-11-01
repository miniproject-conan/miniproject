#!/bin/bash
echo "FastAPI 서버 실행"
poetry run uvicorn app.main:app --reload