from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        session_id = self.get_session_id()
        print(f"Session ID is: {session_id}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
        self.end_headers()
        self.wfile.write(b"""
        <html><body>
        <form action="/" method="post">
            <textarea name="ip_list" rows="10" cols="30">8.8.8.8\n1.1.1.1</textarea><br>
            <input type="submit" value="Submit">
        </form>
        </body></html>
        """)
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length',0))
        post_data = self.rfile.read(content_length)
        post_data_str = post_data.decode('utf-8')

        form_data = urllib.parse.parse_qs(post_data_str)
        ip_list_raw = form_data.get('ip_list', [''])[0]
        session_id = self.get_session_id()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
        self.end_headers()
        self.wfile.write(b"Received IPs:\n")
        self.wfile.write(f"{ip_list_raw}".encode())
        #use ip_list to create a separate folder for each user
        ip_list=ip_list_raw.splitlines()
        base_dir = 'users'
        user_dir = os.path.join(base_dir,session_id)
        #exist_ok =True -> if directory already exist, don't raise exception
        os.makedirs(user_dir, exist_ok=True)
        ips_file_path = os.path.join(user_dir, 'ips.txt')
        with open(ips_file_path, 'w') as f:
            for ip in ip_list:
                f.write(ip + '\n')

        print(ip_list)
    def get_session_id(self):
        cookie_header = self.headers.get('Cookie')
        session_id = None
        
        if cookie_header:
            cookies = cookie_header.split(';')
            for cookie in cookies:
                cookie = cookie.strip()
                if cookie.startswith('session_id='):
                    session_id = cookie[len('session_id='):]
                    break
        
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
        
        return session_id


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MyHandler)
    print("Running on http://localhost:8080")
    server.serve_forever()