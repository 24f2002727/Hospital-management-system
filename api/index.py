import sys
import os

# Ensure project root directory is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

CWD = os.getcwd()
if CWD not in sys.path:
    sys.path.insert(0, CWD)

try:
    from app import app
    application = app
except Exception as e:
    import traceback
    err_trace = traceback.format_exc()
    from flask import Flask, Response
    app = Flask(__name__)
    application = app

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def error_page(path):
        return Response(
            f"<h2>Hospital Management System - Deployment Error</h2><pre>{err_trace}</pre>",
            status=500,
            mimetype="text/html"
        )
