from sys import argv
from os import path, sep

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from cgi import FieldStorage
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader


HOST = '127.0.0.1'
PORT = 8001

if len(argv) > 1:
    PORT = int(argv[1])


class Handler(BaseHTTPRequestHandler):

    def _get_cookies(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        is_exist = False

        try:
            if int(cookies['auth'].value) > 0:
                is_exist = True
        except KeyError:
            print('There is no entity with \'auth\' key')

        return is_exist

    def _get_template(self, page):
        file_loader = FileSystemLoader(sep.join((path.dirname(path.abspath(__file__)), 'templates')))
        env = Environment(loader=file_loader)
        return env.get_template(page)

    def _set_cookies(self, value):
        cookies = SimpleCookie()
        cookies['auth'] = value
        self.send_header('Set-Cookie', cookies.output(header='', sep=''))

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
        'error.html': _error,
    }

    if PORT == 8001:
        PAGES.update({
            'form.html': _form,
        })
    elif PORT == 8002:
        PAGES.update({
            'charge.html': _charge,
            'logIn.html': _log_in,
            'logOut.html': _log_out,
        })

    def _set_headers(self, page=None, response_code=200, content_type='text/html'):
        self.send_response(response_code)
        self.send_header('Content-type', content_type)

        if page is not None:
            self.PAGES[page](self)

        self.end_headers()

    def do_GET(self):

        if 'favicon.ico' in self.path:
            return

        page = urlparse(self.path).path[1:] + '.html'

        if page not in self.PAGES.keys():
            page = 'error.html'

        self._set_headers(page)

        if self._get_cookies():
            auth = '<form action="http://127.0.0.1:8002/logOut"><input type="submit" value="Log Out"></form>'
        else:
            auth = '<form action="http://127.0.0.1:8002/logIn"><input type="submit" value="Log In"></form>'

        template = self._get_template(page)
        output = template.render(auth=auth)
        self.wfile.write(output.encode('UTF-8'))

    def do_POST(self):
        self._set_headers()
        page = urlparse(self.path).path[1:] + '.html'
        template = self._get_template(page)

        if self._get_cookies():
            form = FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            output = template.render(output=f'{form.getvalue("cake")}$ charged')
        else:
            output = template.render(output='Can\'t charge, you need to authorise yourself')

        self.wfile.write(output.encode('UTF-8'))


if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), Handler)

    try:
        print("Serving at {0}:{1}".format(HOST, PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        server.server_close()
