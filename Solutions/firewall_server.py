# www.theforage.com - Telstra Cyber Task 3
# Firewall Server Handler

from http.server import BaseHTTPRequestHandler, HTTPServer

host = "localhost"
port = 8000

#########
# Handle the response here 
def block_request(self):
    print("Potential Spring4Shell exploit detected! Blocking request.")
    # Send a 403 Forbidden response
    self.send_response(403)
    self.end_headers()
    self.wfile.write(b"Forbidden: Potential Exploit Attempt")

def handle_request(self):
    if self.path == '/tomcatwar.jsp' and self.command == 'POST':
        block_request(self)
        return
    elif "Content-Type" in self.headers and "application/x-www-form-urlencoded" in self.headers.get("Content-Type"):
        block_request(self)
        return

    # If the request does not meet the criteria for blocking, send a 200 OK response
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(b"Request processed successfully.")

#########

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
