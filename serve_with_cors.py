from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import socket

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/events/stream':
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            import time
            try:
                while True:
                    self.wfile.write(b"data: updated\n\n")
                    self.wfile.flush()
                    time.sleep(10)  # Send update every 10 seconds (demo)
            except Exception:
                pass
        else:
            super().do_GET()
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    local_ip = get_local_ip()
    server = HTTPServer((local_ip, 8000), CORSRequestHandler)
    print(f'Serving with CORS at http://{local_ip}:8000')
    server.serve_forever()