#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust, Peter Weckend
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POSTa
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
# from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    # BUFF_SIZE = 4096

    # client_socket = None

    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        return None

    def get_code(self, data):
        # print "CODE", data.split(" ")[1], "END"
        return data.split(" ")[1]

    def get_headers(self,data):
        # todo: add to this
        return None

    def get_body(self, data):
        # print "BODY", data.split("\r\n\r\n")[1], "END"
        return data.split("\r\n\r\n")[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):

        parsed_url = urllib.parse.urlparse(url)

        if parsed_url.path == "":
            path = "/"
        else:
            path = parsed_url.path

        try:
            potential_port = parsed_url.port
        except Exception:
            potential_port = None

        # assuming http and not https
        if parsed_url.port is None:
            line1 = "GET " + path + " HTTP/1.1\r\n"
            line2 = "Host: " + parsed_url.hostname + "\r\n"
            line3 = "Accept: */*\r\n"
            line4 = "Connection: close\r\n\r\n"
            port = 80
        else:
            line1 = "GET " + path + " HTTP/1.1\r\n"
            line2 = "Host: " + parsed_url.hostname + ":" + str(parsed_url.port) + "\r\n"
            line3 = "Accept: */*\r\n"
            line4 = "Connection: close\r\n\r\n"
            port = potential_port

        request = line1 + line2 + line3 + line4

        self.connect(parsed_url.hostname, port)
        self.sendall(request)

        # received = b""
        #
        # while True:
        #     data = self.socket.recv(self.BUFF_SIZE)
        #     if not data: break
        #     received += data

        # received = self.socket.recv(self.BUFF_SIZE)

        received = self.recvall(self.socket)

        # print("sent:", request, "end")
        # print("received:", received, "end")

        code = self.get_code(received)
        body = self.get_body(received)

        self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        parsed_url = urllib.parse.urlparse(url)

        if parsed_url.path == "":
            path = "/"
        else:
            path = parsed_url.path

        try:
            potential_port = parsed_url.port
        except Exception:
            potential_port = None

        if args is None:
            content = ""
            content_length = "0"
        else:
            content = urllib.parse.urlencode(args)
            content_length = str(len(content))

        # assuming http and not https
        if potential_port is None:
            line1 = "POST " + path + " HTTP/1.1\r\n"
            line2 = "Host: " + parsed_url.hostname + "\r\n"
            line3 = "Accept: */*\r\n"
            line4 = "Connection: close\r\n"
            line5 = "Content-Type: application/x-www-form-urlencoded\r\n"
            line6 = "Content-Length: " + content_length + "\r\n\r\n"
            port = 80
        else:
            line1 = "POST " + path + " HTTP/1.1\r\n"
            line2 = "Host: " + parsed_url.hostname + ":" + str(potential_port) + "\r\n"
            line3 = "Accept: */*\r\n"
            line4 = "Connection: close\r\n"
            line5 = "Content-Type: application/x-www-form-urlencoded\r\n"
            line6 = "Content-Length: " + content_length + "\r\n\r\n"
            port = potential_port

        request = line1 + line2 + line3 + line4 + line5 + line6 + content

        self.connect(parsed_url.hostname, port)
        self.sendall(request)

        # received = b""
        # while True:
        #     # print "in while"
        #     data = self.client_socket.recv(self.BUFF_SIZE)
        #     if not data: break
        #     received += data

        received = self.recvall(self.socket)

        code = self.get_code(received)
        body = self.get_body(received)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))

