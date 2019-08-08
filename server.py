from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from cgi import FieldStorage
from sys import argv
from os import path, sep


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
        cookies['auth'] = 100
        self.send_header('Set-Cookie', cookies.output(header='', sep=''))

    def _log_out(self):
        cookies = SimpleCookie()
        cookies['auth'] = 0
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

        if page not in self.PAGES.keys():
            page = 'error.html'

        with open(sep.join((path.dirname(__file__), 'templates', page)), "rb") as f:
            self.wfile.write(f.read())

    def do_POST(self):
        self._set_headers()

        cookies = SimpleCookie(self.headers.get('Cookie'))

        if len(cookies) > 0 and int(cookies['auth'].value) > 0:
            form = FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            ans = f'Charged {form.getvalue("cake")}$'
            self.wfile.write(ans.encode('UTF-8'))
        else:
            self.wfile.write('Can\'t charge, you need to authorise yourself'.encode('UTF-8'))


server = HTTPServer((HOST, PORT), Handler)

try:
    print("Serving at {0}:{1}".format(HOST, PORT))
    server.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    server.server_close()
