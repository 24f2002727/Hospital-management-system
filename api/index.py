import sys
import os

# Ensure the root project directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel serverless function entrypoint
app = app
