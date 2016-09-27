#!/usr/bin/env python

## Small HTTP server that responds to POSTs containing OSF node IDs.
## It contacts the RMap server, which creates DiSCO data for the node.
## The DiSCO ID is returned to the caller.
import BaseHTTPServer
import CGIHTTPServer
import cgi
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
import requests

## Must modify the standard CGO request handler to
## allow access control from other servers and to perform the functionality.
class CORSRequestHandler (CGIHTTPServer.CGIHTTPRequestHandler):

    ## Allow access control from other servers.
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        CGIHTTPServer.CGIHTTPRequestHandler.end_headers(self)

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        ## Get the RMap URL from the POST parameters.
        length = int(self.headers.getheader('content-length'))
        postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        url = postvars['url'][0]

        ## Add credentials to the URL and POST to the RMap server.
        user_pass = "1CQXJEwFFkPpm:HEQQlPZ7Fms6x1"
        postUrl = "http://" + user_pass + "@" + url
        response = requests.post(postUrl)

        ## Return the discoId (from RMap) to the caller
        self.wfile.write(response.text)


## Start the server on port 7000.
server = BaseHTTPServer.HTTPServer
server_address = ("", 7000)

handler = CORSRequestHandler
handler.cgi_directories = ["/"]
 
httpd = server(server_address, handler)
httpd.serve_forever()
