from sys import argv
from os import path, sep

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from cgi import FieldStorage
from urllib.parse import urlparse

# TODO:
#   add: handler for external js files


HOST = '127.0.0.1'
PORT = 8001

if len(argv) > 1:
    PORT = int(argv[1])


class Handler(BaseHTTPRequestHandler):

    def _charge(self):
        pass

    def _error(self):
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
        'error': _error,
    }

    if PORT == 8001:
        PAGES.update({
            'form': _form,
        })
    elif PORT == 8002:
        PAGES.update({
            'charge': _charge,
            'logIn': _log_in,
            'logOut': _log_out,
        })

    def _set_headers(self, page=None, response_code=200, content_type='text/html'):
        self.send_response(response_code)
        self.send_header('Content-type', content_type)

        if page is not None:
            self.PAGES[page](self)

        self.end_headers()

    def do_GET(self):
        page = urlparse(self.path).path[1:]

        if page not in self.PAGES.keys():
            page = 'error'

        self._set_headers(page)

        with open(sep.join((path.dirname(__file__), 'templates', '.'.join((page, 'html')))), "rb") as f:
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


if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), Handler)

    try:
        print("Serving at {0}:{1}".format(HOST, PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        server.server_close()
