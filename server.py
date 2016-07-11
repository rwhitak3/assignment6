import re
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import logging
import logging.config
import json
import measures

logging.config.fileConfig("logging.config", disable_existing_loggers=False)
logger = logging.getLogger("server")

logger.info("Starting Server")
server_port = 8080


class RestHandler(BaseHTTPRequestHandler):

    def send_json(self, data):
        data_msg = json.dumps(data)
        logger.debug("Sending Data {}".format(data_msg))
        self.send_response(200)
        self.send_header("content-type", "application/json")
        msg = data_msg.encode()
        self.send_header('content-length', len(msg))
        self.end_headers()
        self.wfile.write(msg)

    def error(self, code, message=None):
        if message is None:
            message = "Unknown Error"
        self.send_error(code, message);

    def do_GET(self):
        logger.info("Received Request from {}".format(self.client_address))
        logger.info("Path = {}".format(self.path))
        if re.fullmatch('/area', self.path):
            areas = measures.get_areas()
            self.send_json(areas)
        else:
            self.error(404, "Not Found")





if __name__ == '__main__':
    server_address = ('', server_port)
    http_server = HTTPServer(server_address, RestHandler)
    http_server.serve_forever()
