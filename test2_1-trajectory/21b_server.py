from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HTTPHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        self._set_response()
        data = json.loads(post_data)
        if "lat" in data and "long" in data:
            self.wfile.write(("Lat: " + str(data["lat"]) + ", Long: " + str(data["long"])).encode('utf-8'))
        else:
            self.wfile.write("Incorrect data format".encode('utf-8'))

server_address = ("localhost", 8000)
httpd = HTTPServer(server_address, HTTPHandler)

print(f"Starting httpd server on {server_address[0]}:{server_address[1]}")
httpd.serve_forever()
