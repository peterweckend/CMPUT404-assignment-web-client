#!/usr/bin/env python
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
import urllib
from urlparse import urlparse


def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    BUFF_SIZE = 4096

    client_socket = None

    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        return None

    def get_code(self, data):
        # print "CODE", data.split(" ")[1], "END"
        return data.split(" ")[1]

    def get_headers(self,data):

        return None

    def get_body(self, data):
        # print "BODY", data.split("\r\n\r\n")[1], "END"
        return data.split("\r\n\r\n")[1]

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
        return str(buffer)

    def GET(self, url, args=None):

        parsed_url = urlparse(url)

        # assuming http and not https
        if parsed_url.port is None:
            line1 = "GET " + parsed_url.path + " HTTP/1.1\r\n"
            line2 = "Host: " + parsed_url.hostname + "\r\n"
            line3 = "Accept: */*\r\n"
            line4 = "Connection: close\r\n\r\n"
            port = 80
        else:
            line1 = "GET " + parsed_url.path + " HTTP/1.1\r\n"
            line2 = "Host: " + parsed_url.hostname + ":" + str(parsed_url.port) + "\r\n"
            line3 = "Accept: */*\r\n"
            line4 = "Connection: close\r\n\r\n"
            port = parsed_url.port

        request = line1 + line2 + line3 + line4

        self.connect(parsed_url.hostname, port)

        self.client_socket.send(request)

        received = b""

        while True:
            print "in while"
            data = self.client_socket.recv(self.BUFF_SIZE)
            if not data: break
            received += data

        # received = self.client_socket.recv(self.BUFF_SIZE)

        print "sent:", request, "end"
        print "received:", received, "end"

        code = self.get_code(received)
        body = self.get_body(received)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
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
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
