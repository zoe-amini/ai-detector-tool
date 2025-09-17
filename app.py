#!/usr/bin/env python3
"""
A minimal HTTP server that allows users to upload job candidate submissions and
automatically analyses the contents.  The server uses only the Python
standard library so it can run in environments without access to external
packages.  Uploaded files are stored in a dedicated directory and passed
through simple readability and AI‑detection heuristics defined in
``utils.py``.  For Python submissions, a basic autopilot grading stub
demonstrates how automated testing might work.
"""

import os
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from string import Template

from utils import analyse_file


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Ensure necessary directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


def load_template(name: str) -> str:
    """Read an HTML template file from the templates directory."""
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


class CandidateHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the candidate submission tool."""

    def log_message(self, format: str, *args) -> None:
        """Override to silence default console logging."""
        return

    def do_GET(self):
        """Serve static files and the upload form."""
        # Normalise path and strip query parameters
        path = unquote(self.path.split('?', 1)[0])
        if path in ('/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = load_template('index.html')
            self.wfile.write(html.encode('utf-8'))
        elif path.startswith('/static/'):
            # Serve static files (e.g. CSS)
            file_path = os.path.join(BASE_DIR, path.lstrip('/'))
            if os.path.isfile(file_path):
                # Determine content type based on extension
                ext = os.path.splitext(file_path)[1].lower()
                if ext == '.css':
                    content_type = 'text/css'
                elif ext == '.js':
                    content_type = 'application/javascript'
                elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg'}:
                    content_type = f"image/{ext.lstrip('.')}"
                else:
                    content_type = 'application/octet-stream'
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'File not found')
        elif path.startswith('/uploads/'):
            # Allow downloading of uploaded files (optional)
            file_path = os.path.join(BASE_DIR, path.lstrip('/'))
            if os.path.isfile(file_path):
                self.send_response(200)
                ext = os.path.splitext(file_path)[1].lower()
                content_type = 'application/octet-stream'
                if ext == '.txt':
                    content_type = 'text/plain; charset=utf-8'
                self.send_header('Content-Type', content_type)
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'File not found')
        else:
            self.send_error(404, 'Page not found')

    def do_POST(self):
        """Handle file uploads and return analysis results."""
        path = unquote(self.path)
        if path != '/upload':
            self.send_error(404, 'Invalid endpoint')
            return
        # Parse form data using cgi.FieldStorage
        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={
                                    'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE': self.headers.get('Content-Type', '')
                                })
        fileitem = form.getfirst('submission') if 'submission' in form else None
        # Due to limitations of FieldStorage with file uploads, we must access file object differently
        file_field = form['submission'] if 'submission' in form else None
        if (file_field is None or 
            not hasattr(file_field, 'file') or 
            file_field.file is None or 
            not hasattr(file_field, 'filename') or 
            not file_field.filename):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No file uploaded.")
            return
        filename = os.path.basename(file_field.filename)
        safe_filename = filename.replace('/', '_').replace('..', '')
        saved_path = os.path.join(UPLOAD_DIR, safe_filename)
        try:
            with open(saved_path, 'wb') as f:
                # Read file data in chunks to avoid memory overhead
                while True:
                    chunk = file_field.file.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        except Exception as exc:
            self.send_response(500)
            self.end_headers()
            msg = f"Failed to save uploaded file: {exc}".encode('utf-8')
            self.wfile.write(msg)
            return
        # Perform analysis
        analysis, autopilot_result = analyse_file(saved_path)
        # Prepare result page
        template_str = load_template('result.html')
        template = Template(template_str)
        html = template.safe_substitute(
            filename=safe_filename,
            word_count=analysis['word_count'],
            unique_words=analysis['unique_word_count'],
            unique_ratio=f"{analysis['unique_ratio']:.2f}",
            sentence_count=analysis['sentence_count'],
            avg_sentence_length=f"{analysis['avg_sentence_length']:.2f}",
            syllable_count=analysis['syllable_count'],
            flesch_score=f"{analysis['flesch_reading_ease']:.2f}",
            ai_likelihood=f"{analysis['ai_likelihood']:.2f}",
            ai_rigorous=f"{analysis.get('ai_rigorous_score', 0.0):.2f}",
            autopilot_result=autopilot_result.replace('\n', '<br/>')
        )
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


def run_server(host: str = '0.0.0.0', port: int = 8000) -> None:
    """Start the HTTP server on the specified host and port."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, CandidateHandler)
    print(f"Serving on http://{host}:{port} ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == '__main__':
    # Run the server if executed as a script
    run_server()