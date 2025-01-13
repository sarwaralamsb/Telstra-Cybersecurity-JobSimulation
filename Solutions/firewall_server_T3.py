# www.theforage.com - Telstra Cyber Task 3
# Model Work Example
# Firewall Server Handler

from http.server import BaseHTTPRequestHandler, HTTPServer

host = "localhost"
port = 8000

def block_request(self):
    self.send_error(403, "Request blocked due to firewall")

def handle_request(self):
    # List of bad headers from the proof of concept payload
    bad_headers = {
        "suffix": "%>//",
        "c1": "Runtime",
        "c2": "<%",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    bad_header_keys = bad_headers.keys()

    # If a request is on the Spring Framework path
    if self.path == "/tomcatwar.jsp":
        # Iterate through bad headers
        for bad_header_key in bad_header_keys:
            # If we find a bad header that matches the malicious payload
            if bad_header_key in self.headers and self.headers[bad_header_key] == bad_headers[bad_header_key]:
                # Block request and throw 403 error
                return block_request(self)

    # Return successful response
    self.send_response(200)
    self.send_header("content-type", "application/json")
    self.end_headers()

    self.wfile.write({ "success": True })

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)

    def do_POST(self):
        handle_request(self)


if __name__ == "__main__":        
    server = HTTPServer((host, port), ServerHandler)
    print("[+] Firewall Server")
    print("[+] HTTP Web Server running on: %s:%s" % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("[+] Server terminated. Exiting...")
    exit(0)