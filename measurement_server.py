import re
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import logging
import logging.config
import json
import measures

logging.config.fileConfig("logging.config", disable_existing_loggers=False)
logger = logging.getLogger("server")

logger.info("Starting Server")
server_port = 12345


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
        self.send_error(code, message)

    def do_GET(self):
        logger.info("Received Request from {}".format(self.client_address))
        logger.info("Path = {}".format(self.path))
        if re.fullmatch('/area', self.path):
            result = measures.get_areas()
            if result is not None:
                return self.send_json(result)
        elif re.fullmatch("/area/(\\d+)/location", self.path):
            match = re.fullmatch("/area/(\\d+)/location", self.path)
            area_id = match.group(1)
            logger.debug("Area id passed in {}".format(area_id))
            result = measures.get_locations_by_area_id(area_id)
            if result is not None:
                return self.send_json(result)
        elif re.fullmatch("/location/(\\d+)/measurement", self.path):
            match = re.fullmatch("/location/(\\d+)/measurement", self.path)
            location_id = match.group(1)
            logger.debug("Location id passed in {}".format(location_id))
            result = measures.get_measures_by_location_id(location_id)
            if result is not None:
                return self.send_json(result)
        elif re.fullmatch("/area/(\\d+)/category", self.path):
            match = re.fullmatch("/area/(\\d+)/category", self.path)
            area_id = match.group(1)
            logger.debug("Area id passed in {}".format(area_id))
            result = measures.get_categories_by_area_id(area_id)
            if result is not None:
                return self.send_json(result)
        elif re.fullmatch("/area/(\\d+)/average_measurement", self.path):
            match = re.fullmatch("/area/(\\d+)/average_measurement", self.path)
            area_id = match.group(1)
            logger.debug("Area id passed in {}".format(area_id))
            result = measures.get_avg_measurement_by_area_id(area_id)
            if result is not None:
                return self.send_json(result)

        elif re.fullmatch("/area/(\\d+)/number_locations", self.path):
            match = re.fullmatch("/area/(\\d+)/number_locations", self.path)
            area_id = match.group(1)
            logger.debug("Area id passed in {}".format(area_id))
            result = measures.get_locations_count_by_area_id(area_id)
            if result is not None:
                return self.send_json(result)
        else:
            self.error(404, "Not Found")

        self.error(500, "Error processing request")






if __name__ == '__main__':
    server_address = ('', server_port)
    http_server = HTTPServer(server_address, RestHandler)
    http_server.serve_forever()
