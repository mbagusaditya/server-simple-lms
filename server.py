import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from modules import get_assignments, get_courses, get_enrollments, get_students


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
        self.send_json({"courses": get_courses()})

    def students(self):
        self.send_json({"students": get_students()})

    def assignments(self):
        self.send_json({"assignments": get_assignments()})

    def enrollments(self):
        self.send_json({"enrollments": get_enrollments()})

    def fallback(self):
        self.send_json({"detail": "Not Found"}, 404)

    def get_routes(self):
        path = self.path

        routes = {
            "/": self.index,
            "/health": self.health,
            "/courses": self.courses,
            "/students": self.students,
            "/assignments": self.assignments,
            "/enrollments": self.enrollments,
        }

        return routes.setdefault(path, self.fallback)

    def do_GET(self):
        func = self.get_routes()

        func()


server = HTTPServer(("localhost", 8000), SimpleHandler)
print("Server running at http://localhost:8000")

server.serve_forever()
