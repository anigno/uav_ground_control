from http.server import BaseHTTPRequestHandler, HTTPServer

from common.meta_classes.no_instance_meta import NoInstanceMeta
from common.utils.generic_event import GenericEvent

class Http2Server(metaclass=NoInstanceMeta):
    """receive data bytes over http2 POST request and raise an event"""
    on_request_post_received = GenericEvent(bytes)

    @staticmethod
    def start(local_ip, local_port):
        server_address = (local_ip, local_port)
        httpd = HTTPServer(server_address, Http2Server._RequestHandler)
        httpd.serve_forever()

    class _RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            # sender_ip, sender_port = self.client_address
            Http2Server.on_request_post_received.raise_event(post_data_bytes)
            # Send a response (optional)
            self.send_response(200)
            self.end_headers()

if __name__ == '__main__':
    def on_request_post_received(data_dict: dict):
        print(data_dict)

    Http2Server.on_request_post_received += on_request_post_received
    Http2Server.start('localhost', 1000)
