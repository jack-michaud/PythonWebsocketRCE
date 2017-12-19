class Request:

    def __init__(self, raw):
        request_parts = raw.split('\n')
        request_parts = [part.replace('\r','') for part in request_parts]
        self.header = request_parts.pop(0)

        self.data = {part.split(': ')[0]: part.split(': ')[1]
                     for part in request_parts if part is not ''}

    def keys(self):
        return self.data.keys()

    def is_valid_websocket(self):
        keys = self.keys()

        return "Host" in keys and\
               "Upgrade" in keys and\
               "Connection" in keys and\
               "Sec-WebSocket-Key" in keys and\
               "Sec-WebSocket-Version" in keys and\
               "Origin" in keys

    def generate_accept_value(self):
        key = self.data['Sec-WebSocket-Key']
        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

        decoded = key + GUID
        sha_decoded = hashlib.sha1(decoded).digest()
        return base64.b64encode(sha_decoded)

    def generate_websocket_response(self):
        return ["HTTP/1.1 101 Switching Protocols\r",
               "Upgrade: websocket\r" + \
               "Connection: Upgrade\r" + \
               "Sec-WebSocket-Protocol: chat\r" + \
               "Sec-WebSocket-Accept: " + self.generate_accept_value() + "\r\n\n"]
