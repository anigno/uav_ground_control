import http.client
from http.client import HTTPResponse

from python.common.meta_classes.no_instance_meta import NoInstanceMeta

class Http2Client(metaclass=NoInstanceMeta):
    """sends data bytes over http2 POST request"""

    @staticmethod
    def send_data_request(data_bytes: bytes, ip, port) -> HTTPResponse:
        conn = http.client.HTTPConnection(ip, port)
        headers = {
            'Content-Type': 'application/octet-stream',
            'Connection': 'Upgrade',
            'Upgrade': 'h2c',
        }
        conn.request('POST', '/', body=data_bytes, headers=headers)
        response = conn.getresponse()
        conn.close()
        return response

if __name__ == '__main__':
    # message1 = StatusUpdateMessage()
    data = b'12345678'
    r = Http2Client.send_data_request(data, 'localhost', 1000)
    print(r.read().decode('utf-8'))
