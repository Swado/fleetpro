import http.server
import socketserver
import os

# Set the port
PORT = 5001

# Set up the directory to serve files from
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)

# Custom handler to serve specific file types
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve preview.html for root requests
        if self.path == '/' or self.path == '/index.html':
            self.path = '/preview.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def guess_type(self, path):
        # Add appropriate MIME types
        base, ext = os.path.splitext(path)
        if ext == '.css':
            return 'text/css'
        elif ext == '.html':
            return 'text/html'
        elif ext == '.js':
            return 'application/javascript'
        elif ext == '.svg':
            return 'image/svg+xml'
        elif ext == '.png':
            return 'image/png'
        elif ext == '.jpg' or ext == '.jpeg':
            return 'image/jpeg'
        else:
            return super().guess_type(path)

# Set up and start the server
Handler = CustomHTTPRequestHandler
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Server running at http://0.0.0.0:{PORT}/")
    httpd.serve_forever()