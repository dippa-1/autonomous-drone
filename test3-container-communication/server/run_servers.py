import threading

# http
from http.server import HTTPServer, BaseHTTPRequestHandler

# turbo gear 2
from wsgiref.simple_server import make_server
from tg import MinimalApplicationConfigurator
from tg import expose, TGController

# bottle
from bottle import route, run

# websocket
import asyncio
import websockets

async def websocket_response(websocket):
    async for _ in websocket:
        await websocket.send(RETURN_MESSAGE)

async def main():
    async with websockets.serve(websocket_response, "", 8010):
        await asyncio.Future()  # run forever


RETURN_MESSAGE = "hello world!" # TODO: replace with byte array that has the size of the actual sensor data


def serve_http():
    class HTTPHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(RETURN_MESSAGE.encode("utf8"))

    server_address = ("", 8000)
    httpd = HTTPServer(server_address, HTTPHandler)

    print(f"Starting httpd server on {server_address[0]}:{server_address[1]}")
    httpd.serve_forever()

def serve_turboGear():
    # RootController of our web app, in charge of serving content for /
    class RootController(TGController):
     @expose(content_type="text/plain")
     def index(self):
         return RETURN_MESSAGE

    # Configure a new minimal application with our root controller.
    config = MinimalApplicationConfigurator()
    config.update_blueprint({
     'root_controller': RootController()
    })

    # Serve the newly configured web application.
    httpd = make_server('', 8003, config.make_wsgi_app())
    httpd.serve_forever()


def serve_bottle():
    @route('/')
    def index():
        return RETURN_MESSAGE
    run(host='', port=8007)


def run_asyncio():
    asyncio.run(main())


if __name__ == "__main__":

    threads = [
        threading.Thread(target=serve_http),
        threading.Thread(target=serve_turboGear),
        threading.Thread(target=serve_bottle),
        threading.Thread(target=run_asyncio),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

