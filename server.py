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
        self.respondcode = ""

        # check if the HTTP command is getting GET or not; if it is using GET
        if "GET" in self.addr[0]:
            self.filepath = self.addr[1]
            print("first", self.filepath)

            # strip the first character for the filepath to be readable
            if self.filepath[0] == "/":
                self.filepath = self.filepath[1:]
            if len(self.filepath)==0:
                self.filepath = "index.html"
            print("second", self.filepath)


            self.get(self.filepath)
        # if command is not GET then return 405 where command is invalid
        else:
            print("command not get")
            self.respondcode = "405"
            self.get(self.respondcode)

    def parse(self, data):
        self.parsed = []
        self.parsed = str(data).split(" ")

        return self.parsed

    # get function gets the request to return data from given path
    def get(self, path):
        print("get function")
        # if path fully exist then return 200 code
        if os.path.isfile(path):
            print("file path exists")
            # if path is too long or command to go back up in directories is given return 404
            if len(path)>20 and ".." in path:
                self.respondcode = "404"
                self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))
            else:
                # open the file at the openable path and return code 200
                with open(path, 'rb') as file:
                    self.respondcode = "200"
                    self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))
                    self.request.sendall(file.read())

        # if the HTTP request is not GET, then return 405 Method Not allowed
        # the 405 comes from handle function where it filters out non-GET requests and send code 405 as path into the get function
        elif path == "405":
            self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))

        # if path is not a full address and also a GET request
        else:
            print("path doesn't exist")
            # call find file to retrieve full path from the local folder
            # i.e.= /index.html -> /www/index.html
            index_html_path = self.find_file(path, ".")
            print(index_html_path)
            contentType = "\n\n"

            try:
                # if path cant be found try adding www in front of it
                if index_html_path == None:
                    print("inside here")
                    index_html_path = "www/"+path
                    print("trying path", index_html_path)
                    open(index_html_path, 'rb')

                if ".html" in index_html_path:
                    contentType = "\r\nContent-Type: text/html\r\n\r\n"

                elif ".css" in index_html_path:
                    contentType = "\r\nContent-Type: text/css\r\n\r\n"

                if index_html_path:
                    try:
                        with open(index_html_path, 'rb') as file:
                            self.respondcode = "200"
                            self.request.send(bytearray(
                                "HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + contentType,
                                'utf-8'))
                            self.request.sendall(file.read())
                    except IsADirectoryError:
                        index_html_path += "/index.html"
                        with open(index_html_path, 'rb') as file:
                            self.respondcode = "200"
                            self.request.send(bytearray(
                                "HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + contentType,
                                'utf-8'))
                            self.request.sendall(file.read())
                else:
                    print("Paths not found")
                    # paths not found
                    self.respondcode = "404"
                    self.request.send(
                        bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + contentType,
                                  'utf-8'))


            except FileNotFoundError:
                print("filenotfound error")
                self.respondcode = "404"
                self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + contentType, 'utf-8'))





    # find_file returns the full path to a given file_name, else None if can't find it in the directory
    def find_file(self, file_name, directory):
        if file_name[-1] == "/":
            file_name = file_name[:-1]
        print("find file", file_name)
        for root, dirs, files in os.walk(directory):
            if file_name in files:
                print("fixed file path", os.path.join(root, file_name))
                return os.path.join(root, file_name)
            elif file_name in root:
                print("fixed file path", os.path.join(root) + "/")
                return os.path.join(root)
        return None







if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


# if its http://127.0.0.1:8080/ should it just return www/index.html
# what is mime type stuff
# BASEURL = "http://127.0.0.1:8080/deep.css"
# if 301 occurs, should we output the correct page or just 301