# import socket
# import http
# host , port = "0.0.0.0",9000
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind((host, port))    
# server_socket.listen(1)
# print('Listening on port %s ...' % port)

# while True:    
#     # Wait for client connections
#     client_connection, client_address = server_socket.accept()

#     # Get the client request
#     request = client_connection.recv(1024).decode()
#     print(request)

#     # Send HTTP response
#     response = 'HTTP/1.0 200 OK\n\nHello World'
#     client_connection.sendall(response.encode())
#     client_connection.close()

# # Close socket
# server_socket.close()

from main import search

import http.server
import json

class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        # Get the length of the incoming request data
        content_length = int(self.headers['Content-Length'])

        # Read the incoming request data
        post_data = self.rfile.read(content_length)

        # Decode the incoming request data from bytes to string
        post_data = post_data.decode()
        rank=search(post_data)
        # Parse the incoming JSON data
        # data = json.loads(post_data)

        # Do something with the data (e.g. save to a database)
        # print(data)

        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        print(rank)
        self.wfile.write((json.dumps(rank).encode()))

# Create an HTTP server on port 9000
server_address = ('', 9000)
httpd = http.server.HTTPServer(server_address, MyHandler)

# Start the server
print('Server listening on port 9000...')
httpd.serve_forever()