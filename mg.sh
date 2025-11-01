#!/bin/bash
echo "[1/4] 초기화"
poetry run aerich init -t app.db.config.TORTOISE_ORM || true

echo "[2/4] DB 초기화"
poetry run aerich init-db || true

echo "[3/4] 마이그레이션 파일 생성"
poetry run aerich migrate --name "auto_$(date +%Y%m%d_%H%M%S)" || true

echo "[4/4] DB에 반영"
poetry run aerich upgrade || true