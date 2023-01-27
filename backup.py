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

# setting default messages for each httpcode
HTTPCODE = {"200":"OK",
            "301":"Moved Permanently",
            "404":"Paths Not Found",
            "405":"Method Not Allowed"}


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()

        # this parse the data into interpratable string
        self.addr = self.parse(self.data)
        print ("Got a request of: %s\n" % self.data)
        print("Address to request is %s" % self.addr[1])

        # initialize empty respond code
        self.respondcode = ""

        # check if the HTTP command is getting GET or not; proceed if it is GET
        if "GET" in self.addr[0]:
            # retrieve file path from parsed input
            self.filepath = self.addr[1]
            print("Received filepath as", self.filepath)

            # strip the first character for the filepath to be readable
            if self.filepath[0] == "/":
                self.filepath = self.filepath[1:]
            print("Path without first / is now: ", self.filepath)

            # if user requests local folder with no file specified, serve index.html
            if len(self.filepath) == 0:
                print("Path is empty now, add on 'index.html'")
                self.filepath = "index.html"
            print("If need to append index.html, now is the new address:", self.filepath)

            # call function get to send requests
            print("Call get function to retrieve full path...")
            self.get(self.filepath)
        # if command is not GET then return 405 where command is invalid
        else:
            print("Command is not get")
            self.respondcode = "405"
            self.get(self.respondcode)

    def parse(self, data):
        self.parsed = []
        self.parsed = str(data).split(" ")

        return self.parsed

    # get function gets the request to return data from given path
    def get(self, path):
        print("Within get function")

        # if path fully exist then return 200 code
        if os.path.isfile(path):
            print("file path pre-exists")
            # if path is too long or command to go back up in directories is given return 404
            if len(path)>30 and ".." in path:
                self.respondcode = "404"
                self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))
            else:
                # open the file at the openable path and return code 200
                with open(path, 'rb') as file:
                    print("Path fully exists and no forbidden path is given")
                    self.respondcode = "200"
                    self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))
                    self.request.sendall(file.read())

        # if the HTTP request is not GET, then return 405 Method Not allowed
        # the 405 comes from handle function where it filters out non-GET requests and send code 405 as path into the get function
        elif path == "405":
            print("Command other than HTTP GET is given")
            self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\n\n", 'utf-8'))

        # if path is not a full address and also a GET request
        else:
            print("Path doesn't exist")
            # call find file to retrieve full path from the local folder
            # i.e.= /index.html -> /www/index.html
            index_html_path = self.find_file(path, ".")
            print("index_html_path returned to get funtion at: ", index_html_path)
            contentType = "\n\n"

            try:
                # returns any invalid paths
                if index_html_path == None:
                    print("inside here")
                    # try to see if path cant be found try adding www in front of it
                    try:
                        index_html_path = "www/" + path
                        open(index_html_path, 'rb')
                    except IsADirectoryError:
                        index_html_path = path+"/"

                    print(index_html_path)

                # if a html file is returned set content type to html
                if ".html" in index_html_path:
                    contentType = "\r\nContent-Type: text/html\r\n\r\n"

                # if a css file is returned set content type to css
                elif ".css" in index_html_path:
                    contentType = "\r\nContent-Type: text/css\r\n\r\n"

                # if path returned is not empty
                if index_html_path:
                    # try to open the file
                    try:
                        with open(index_html_path, 'rb') as file:
                            self.respondcode = "200"
                            self.request.send(bytearray(
                                "HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + contentType,'utf-8'))
                            self.request.sendall(file.read())
                    except IsADirectoryError:
                        # rn if its a valid path to directory with index, append index.html to it and open it ; open it wiht
                        # ---------------------------------------------------------------------------------------------------------------------------
                        print("Reached inadirError with file path", index_html_path)

                        self.respondcode = "301"
                        self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + "\r\nLocation: " + index_html_path + "\r\n\r\n", 'utf-8'))
                        self.get(index_html_path+"index.html")
                else:
                    print("Paths not found")
                    # paths not found
                    self.respondcode = "404"
                    self.request.send(
                        bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + contentType,'utf-8'))
            except FileNotFoundError:
                print("filenotfound error")
                self.respondcode = "404"
                self.request.send(bytearray("HTTP/1.1 " + self.respondcode + " " + HTTPCODE[self.respondcode] + contentType, 'utf-8'))





    # # find_file returns the full path to a given file_name, else None if can't find it in the directory
    # def find_file(self, file_name, directory):
    #     print ("Called find_file to find full path")
    #     # if the path ends in / indicating its a directory
    #     if file_name[-1] == "/":
    #         file_name = file_name[:-1]
    #     # if path doesn't end in / means its not a directory but a file
    #         for root, dirs, files in os.walk(directory):
    #             if file_name in files:
    #                 print("files", files)
    #                 print("fixed file path", os.path.join(root, file_name))
    #                 if "www" not in root:
    #                     return None
    #                 else:
    #                     return os.path.join(root, file_name)
    #             elif file_name in root:
    #                 print("fixed file path", os.path.join(root) + "/")
    #                 if "www" not in root:
    #                     return None
    #                 else:
    #                     return os.path.join(root)
    #         return None

    # find_file returns the full path to a given file_name, else None if can't find it in the directory
    def find_file(self, file_name, directory):
        print ("Called find_file to find full path")
    # if path doesn't end in / means its not a directory but a file
        if file_name[-1] == "/":
            file_name = file_name[:-1]
        for root, dirs, files in os.walk(directory):
            # if path leads to a file
            if file_name in files:
                #print("fixed file path", os.path.join(root, file_name), ";filename = ", file_name)
                if "www" not in root:
                    return None
                else:
                    full_path = os.path.join(root, file_name)
                    print("find_file returns: ", os.path.join(root, file_name))
                    if full_path.count("/") >= 2:
                        return None
                    else:
                        return full_path





            # if path leads to a directory
            elif file_name in root:
                #print("fixed file path", os.path.join(root) + "/" + ";filename = ", file_name)
                file_name += "/"
                print("filename is now======", file_name)
                if "www" not in root:
                    return None
                else:
                    print("2 find_file returns: ", os.path.join(root)+"/")
                    return (os.path.join(root)+"/")
        return None





if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


# handle 301
# if 301 occurs, should we output the correct page or just 301