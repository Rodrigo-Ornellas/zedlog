import http.server
import socketserver

# handler = http.server.SimpleHTTPRequestHandler
# with socketserver.TCPServer(("", PORT), handler) as httpd:
#     print("Server started at localhost:" + str(PORT))
#     httpd.serve_forever()

PORT = 9003


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = './DPVesselSchedule4.pdf'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# Create an object of the above class
handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
print('Server is forever in Port {}'.format(PORT))
my_server.serve_forever()
