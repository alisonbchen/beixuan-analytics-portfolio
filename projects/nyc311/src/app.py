"""Local dashboard and read-only JSON API; no third-party dependencies."""
import argparse
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from pipeline import borough_totals, top_issues


def handler_for(database):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlparse(self.path)
            try:
                params = parse_qs(url.query)
                if url.path == "/":
                    body = Path(__file__).with_name("dashboard.html").read_bytes()
                    return self.respond(200, body, "text/html; charset=utf-8")
                if url.path == "/api/boroughs":
                    result = borough_totals(database, params.get("month", [""])[0])
                elif url.path == "/api/top-issues":
                    result = top_issues(database, params.get("month", [""])[0], params.get("borough", [""])[0], int(params.get("limit", ["3"])[0]))
                elif url.path == "/api/quality":
                    with sqlite3.connect(database) as con:
                        result = json.loads(con.execute("SELECT report_json FROM run_metadata").fetchone()[0])
                else:
                    return self.respond(404, b'{"error":"route not found"}')
                self.respond(200, json.dumps(result).encode())
            except (ValueError, TypeError) as error:
                self.respond(400, json.dumps({"error": str(error)}).encode())

        def respond(self, status, body, content_type="application/json; charset=utf-8"):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass
    return Handler


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="build/nyc311.sqlite")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not Path(args.db).is_file():
        parser.error("build the database with pipeline.py first")
    print(f"Open http://127.0.0.1:{args.port}; Ctrl-C to stop")
    ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(args.db)).serve_forever()
