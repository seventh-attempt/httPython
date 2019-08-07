from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from sys import argv
from os import path, sep

# TODO:
#  fix:
#   console cookies update only after second refresh, though in browser updates are visible right after changes applied
#   make cookies visible in browser at /charge
#  add:
#   get cookies in post to allow/ban charge operation

HOST = '127.0.0.1'
PORT = 8001

if len(argv) > 1:
    PORT = int(argv[1])


class Handler(BaseHTTPRequestHandler):

    def _charge(self):
        pass

    def _form(self):
        pass

    def _log_in(self):
        cookies = SimpleCookie()
        cookies['auth'] = True
        # cookies['auth']['expires'] = None
        self.send_header('Set-Cookie', cookies.output(header='', sep=''))

    def _log_out(self):
        cookies = SimpleCookie()
        cookies['auth'] = False
        # cookies['auth']['expires'] = None
        self.send_header('Set-Cookie', cookies.output(header='', sep=''))

    PAGES = {
        'charge.html': _charge,
        'form.html': _form,
        'logIn.html': _log_in,
        'logOut.html': _log_out,
    }

    def _set_headers(self, page=None):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')

        if page is not None:
            self.PAGES[page](self)

        self.end_headers()

    def do_GET(self):
        page = self.path[1:] + '.html'
        self._set_headers(page)

        print(self.headers)

        if page not in self.PAGES.keys():
            page = 'error.html'
        with open(sep.join((path.dirname(__file__), 'templates', page)), "rb") as f:
            self.wfile.write(f.read())

    def do_POST(self):
        self.do_GET()


server = HTTPServer((HOST, PORT), Handler)

try:
    print("Serving at {0}:{1}".format(HOST, PORT))
    server.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    server.server_close()
