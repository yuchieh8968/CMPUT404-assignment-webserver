#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

HTTPCODE = {"200":"OK",
            "301": "Paths Moved",
            "404":"Paths Not Found",
            "405": "Method Not Allowed"}


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.addr = self.parse(self.data)
        print ("Got a request of: %s\n" % self.data)
        self.respondcode = ""
        if "GET" in self.addr[0]:
            self.respondcode = "200"
        else:
            self.respondcode = "405"

        self.request.send(bytearray("HTTP/1.1 200 OK\n\n", 'utf-8'))
        self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))

    def parse(self, data):
        self.parsed = []
        print(self.data)
        # b'GET /index.html HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.79.1\r\nAccept: */*'
        # ["b'GET", '/index.html', 'HTTP/1.1\\r\\nHost:', 'localhost:8080\\r\\nUser-Agent:', 'curl/7.79.1\\r\\nAccept:', "*/*'"]
        self.parsed = str(data).split(" ")

        return self.parsed

    def send_request(self, host, port, request_data):
        pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()



# wsl ubuntu
# only show html and css
# reject png
#
# 1. curl get familiar with
# 2. how to parsh; \n\n cut out
# 3. index.html assumed the end pt of addr if not specified
#
# after parse; give proper http responce


