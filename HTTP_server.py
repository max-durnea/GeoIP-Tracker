from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import subprocess
import mimetypes

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith('/downloads/'):
            parts = parsed_path.path.split('/')
            if len(parts) >= 4:
                _, _, session_id, filename = parts[:4]
                filename = urllib.parse.unquote(filename)
                file_path = os.path.join('downloads', session_id, filename)
                if os.path.isfile(file_path):
                    mime_type, _ = mimetypes.guess_type(file_path)
                    mime_type = None
                    if mime_type is None:
                        mime_type = 'application/octet-stream'

                    self.send_response(200)
                    self.send_header('Content-Type', mime_type)
                    self.end_headers()

                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    return
            self.send_error(404, "File not found")
            return
        session_id = self.get_session_id()
        print(f"Session ID is: {session_id}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <head>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                background-color: #f0f2f5;
                color: #333;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                padding: 20px;
            }
            h1 {
                margin-bottom: 20px;
                color: #0078d7;
            }
            form {
                background: white;
                padding: 20px 30px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 350px;
                box-sizing: border-box;
            }
            textarea {
                width: 100%;
                font-family: monospace;
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                resize: vertical;
                box-sizing: border-box;
            }
            input[type="submit"] {
                margin-top: 15px;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                background-color: #0078d7;
                color: white;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                width: 100%;
            }
            input[type="submit"]:hover {
                background-color: #005fa3;
            }
        </style>
        </head>
        <body>
            <h1>Geo IP Tracker</h1>
            <form action="/" method="post">
                <textarea name="ip_list" rows="10" cols="30">8.8.8.8\n1.1.1.1</textarea><br>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        post_data_str = post_data.decode('utf-8')

        form_data = urllib.parse.parse_qs(post_data_str)
        ip_list_raw = form_data.get('ip_list', [''])[0]
        session_id = self.get_session_id()

        # Create user directory and save IPs
        ip_list = ip_list_raw.splitlines()
        base_dir = 'users'
        user_dir = os.path.join(base_dir, session_id)
        os.makedirs(user_dir, exist_ok=True)
        ips_file_path = os.path.join(user_dir, 'ips.txt')
        user_ip = self.client_address[0]
        print(f"User IP address: {user_ip}")
        with open(ips_file_path, 'w') as f:
            f.write(user_ip+ '\n')
            for ip in ip_list:
                f.write(ip + '\n')

        print(ip_list)

        # Run the geo_ip_tracker.py script
        subprocess.run(
            ["python3", "geo_ip_tracker.py", ips_file_path, session_id],
            capture_output=True,
            text=True
        )

        # After processing, list files in user_dir
        user_dir = os.path.join("downloads",session_id)
        files = os.listdir(user_dir)

        # Build HTML links to files
        links_html = ""
        for filename in files:
            # URL encode filename for safety
            file_url = f"/downloads/{session_id}/{urllib.parse.quote(filename)}"
            links_html += f'<li><a href="{file_url}" target="_blank">{filename}</a></li>'

        # Send response with links
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
        self.end_headers()

        response_html = f"""
            <html>
            <head>
            <style>
                html, body {{
                    height: 100%;
                    margin: 0;
                    background-color: #f0f2f5;
                    color: #333;
                }}
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    padding: 20px;
                }}
                h1 {{
                    margin-bottom: 20px;
                    color: #0078d7;
                }}
                form {{
                    background: white;
                    padding: 20px 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    margin-bottom: 30px;
                    width: 350px;
                    box-sizing: border-box;
                }}
                textarea {{
                    width: 100%;
                    font-family: monospace;
                    font-size: 14px;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    resize: vertical;
                    box-sizing: border-box;
                }}
                input[type="submit"] {{
                    margin-top: 15px;
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    background-color: #0078d7;
                    color: white;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                    width: 100%;
                }}
                input[type="submit"]:hover {{
                    background-color: #005fa3;
                }}
                h3 {{
                    margin-bottom: 10px;
                }}
                ul {{
                    list-style-type: none;
                    padding-left: 0;
                    width: 350px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                ul li {{
                    padding: 10px 15px;
                    border-bottom: 1px solid #eee;
                }}
                ul li:last-child {{
                    border-bottom: none;
                }}
                ul li a {{
                    text-decoration: none;
                    color: #0078d7;
                    font-weight: 600;
                }}
                ul li a:hover {{
                    text-decoration: underline;
                }}
            </style>
            </head>
            <body>
                <h1>Geo IP Tracker</h1>
                <form action="/" method="post">
                    <textarea name="ip_list" rows="10" cols="30">8.8.8.8\n1.1.1.1</textarea><br>
                    <input type="submit" value="Submit">
                </form>
                <h3>Your generated files:</h3>
                <ul>
                    {links_html}
                </ul>
            </body>
            </html>
            """


        self.wfile.write(response_html.encode('utf-8'))
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