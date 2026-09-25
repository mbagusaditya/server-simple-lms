import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def index(self):
        self.send_json({"message": "Simple LMS Backend"})

    def health(self):
        self.send_json({"status": "ok"})

    def courses(self):
        self.send_json(
            {
                "courses": [
                    {"id": 1, "name": "Pemrograman Sisi Server"},
                    {"id": 2, "name": "Basis Data"},
                ]
            }
        )

    def students(self):
        self.send_json(
            {"students": [{"id": 1, "name": "Andi"}, {"id": 2, "name": "Siti"}]}
        )

    def assignments(self):
        self.send_json({"assignments": [{"id": 1, "title": "Backend Fundamentals"}]})

    def fallback(self):
        self.send_json({"detail": "Not Found"}, 404)

    def getRoutes(self):
        path = self.path

        routes = {
            "/": self.index,
            "/health": self.health,
            "/courses": self.courses,
            "/students": self.students,
            "/assignments": self.assignments,
        }

        return routes.setdefault(path, self.fallback)

    def do_GET(self):
        self.getRoutes()()


server = HTTPServer(("localhost", 8000), SimpleHandler)
print("Server running at http://localhost:8000")

server.serve_forever()
