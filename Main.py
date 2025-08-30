from http.server import HTTPServer, BaseHTTPRequestHandler
from Logging import LOGGER
import HTTPHandler

PORT = 5247

LOGGER.name = "Lairs"

class Server(BaseHTTPRequestHandler):
    with open('./http/404/index.html') as file_in: index = file_in.buffer.read()
    fourohfour = 404, [], index

    def do_GET(self) -> None:
        url, pairs = self.path.removeprefix('/').removesuffix('/').split('?') + [""]
        parameters = {}
        for pair in pairs.split('&'):
            pair = pair.split('=') + [True]
            parameters[pair[0]] = pair[1]

        status, headers, data = HTTPHandler.handle_GET_request(url.lower().split('/'), parameters)

        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        for header in headers: self.send_header(*header)
        self.end_headers()
        if not isinstance(data, (bytes, bytearray)): data = bytes(data, 'utf-8')
        self.wfile.write(data)

    def do_POST(self) -> None:
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        status, headers, data = HTTPHandler.handle_POST_request(body)

        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        for header in headers: self.send_header(*header)
        self.end_headers()
        if not isinstance(data, (bytes, bytearray)): data = bytes(data, 'utf-8')
        self.wfile.write(data)
    
    def log_message(self, format, *args): pass

if __name__ == "__main__":
    LOGGER.info("Opening HTTP Server and REST API")
    server = HTTPServer(("0.0.0.0", 5247), Server)
    try: server.serve_forever()
    except Exception as e: print(e)
    LOGGER.warning("Closed Server")

# ////.:•,,•:.\\\\