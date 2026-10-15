"""
TRACE × X — Vercel Serverless Function Entry Point
Department of Computer Science & Engineering | T.J.S. Engineering College

Provides serverless API compatibility for Vercel deployment.
Routes incoming /api/* requests to TraceXRequestHandler with SQLite /tmp support.
"""

import os
import sys

# Add repository root to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Set environment flag for serverless runtime
os.environ['VERCEL'] = '1'

import server

# Initialize database schema and initial cases/admins on cold start
try:
    server.init_database()
except Exception as _init_err:
    print(f"[TRACE × X] Serverless cold-start DB init note: {_init_err}")

# Vercel's Python runtime invokes the 'handler' class inheriting from BaseHTTPRequestHandler
class handler(server.TraceXRequestHandler):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('directory', ROOT_DIR)
        super().__init__(*args, **kwargs)
