# Python DevContainer

Drop-in development container for Python projects (FastAPI, Django, Flask, etc).

## Features
- Python 3.12
- PostgreSQL 16
- Redis 7
- VS Code Python extensions (Pylance, Black, Ruff)
- Oh-My-Zsh terminal

## Quick Start
1. Copy `.devcontainer` folder to Python project root
2. Ensure `requirements.txt` exists
3. Open in VS Code
4. `Cmd+Shift+P` → "Dev Containers: Reopen in Container"

## Services
- Python App: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Framework Examples

### FastAPI
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Django
```bash
django-admin startproject myproject .
python manage.py runserver 0.0.0.0:8000
```

### Flask
```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

# Run: flask run --host=0.0.0.0 --port=8000
```

## Requirements Template
```txt
# Web Framework (choose one)
fastapi==0.109.0
uvicorn[standard]==0.27.0
# django==5.0
# flask==3.0.0

# Database
psycopg2-binary==2.9.9
sqlalchemy==2.0.25

# Redis
redis==5.0.1

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3

# Code Quality
black==23.12.1
ruff==0.1.11
```

## Commands
```bash
# Run app
python main.py
uvicorn main:app --reload --host 0.0.0.0
python manage.py runserver 0.0.0.0:8000

# Testing
pytest
pytest -v

# Formatting
black .
ruff check .
```
