"""
index.py — Ponto de entrada Serverless da Vercel para o FastAPI.
"""
import sys
import os

# Adiciona o diretório backend ao sys.path para carregar routers, services e models
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
