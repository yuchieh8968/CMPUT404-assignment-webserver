#  coding: utf-8 
import socketserver, os

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
        print(self.addr)
        self.respondcode = ""

        # check if the HTTP command is getting GET or not; if it is using GET
        if "GET" in self.addr[0]:
            print('first if')

            self.filepath = self.addr[1]
            # strip the last character for the filepath to be readable
            if self.filepath[0] == "/":
                print('second if')
                self.filepath = self.filepath[1:]

            # remove first / character for the path to be readable
            if self.filepath[-1] == "/":
                self.filepath = self.filepath[:-1]

            print(self.filepath)
            # check if file is applicable to opening
            if self.filepath.endswith('.html') or self.filepath.endswith('.css'):
                print('third if')

                self.get(self.filepath)
        # if command is not GET then return 405 where command is invalid
        else:
            self.respondcode = "405"
            self.get(self.respondcode)

    def parse(self, data):
        self.parsed = []
        print(self.data)
        # b'GET /www/index.html HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.79.1\r\nAccept: */*'
        # ["b'GET", '/www/index.html', 'HTTP/1.1\\r\\nHost:', 'localhost:8080\\r\\nUser-Agent:', 'curl/7.79.1\\r\\nAccept:', "*/*'"]
        self.parsed = str(data).split(" ")

        return self.parsed

    # this function gets the data if its a valid command (GET) and check if file exists
    def get(self, path):
        if os.path.isfile(path):
            print("200 return")

            with open(path, 'rb') as file:
                self.respondcode = "200"
                self.request.send( bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))
                self.request.sendall(file.read())
        elif path == "405":
            print("405 code returned")
            self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))
            self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))

        else:
            # paths not found
            print("404 return")
            self.respondcode = "404"
            self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
