
import json
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from kms_server import Get_Key, _load_and_validate, KMS_POOL_DIR

HOST = "127.0.0.1"
PORT = 8000

API_TOKEN = os.environ.get("KMS_API_TOKEN")
if not API_TOKEN:
    raise SystemExit("Set KMS_API_TOKEN before starting the server.")


class KMSHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            return self.send_json(200, {"status": "ok"})

        if self.headers.get("Authorization") != f"Bearer {API_TOKEN}":
            return self.send_json(401, {"error": "Unauthorized"})

        match = re.fullmatch(r"/keys/([A-Za-z0-9_-]+)", path)
        if not match:
            return self.send_json(404, {"error": "Not found"})

        block_id = match.group(1)

        try:
            key = Get_Key(block_id)
            return self.send_json(200, {
                "blockId": block_id,
                "key": key,
                "keyBits": len(bytes.fromhex(key)) * 8
            })
        except FileNotFoundError:
            return self.send_json(404, {"error": "Key block not found"})
        except (ValueError, json.JSONDecodeError):
            return self.send_json(400, {"error": "Invalid key block"})

    def log_message(self, format, *args):
        # Avoid logging request details.
        pass


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), KMSHandler)
    print(f"KMS API listening on http://{HOST}:{PORT}")
    print("Local testing only; do not expose this HTTP service to a network.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping KMS API...")
    finally:
        server.server_close()
