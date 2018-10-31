import socketserver
from http.server import BaseHTTPRequestHandler
from swiftweet_packer import pack_tweets

class TweetsFeeder(BaseHTTPRequestHandler):
    def do_GET(self):
        print("<----- Request Start ----->")
        print("request_path :", self.path)
        print("self.headers :", self.headers)
        print("<----- Request End ------->\n")

        if self.path == '/feed/start':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            print("sending a pack of tweets")
            self.wfile.write(pack_tweets().encode())

httpd = socketserver.TCPServer(("", 8080), TweetsFeeder)
httpd.serve_forever()