from sys import argv
from os import path, sep

from urllib.parse import urlparse
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

    def _get_auth_cookies(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        is_exist = False

        try:
            if int(cookies['auth'].value) > 0:
                is_exist = True
        except KeyError:
            print('There is no entity with \'auth\' key')

        return is_exist

    def _set_template(self, page, **kwargs):
        file_loader = FileSystemLoader(sep.join((path.dirname(path.abspath(__file__)), 'templates')))
        env = Environment(loader=file_loader)
        template = env.get_template(page)
        output = template.render(kwargs)
        self.wfile.write(output.encode('UTF-8'))

    def _set_auth_cookies(self, value):
        cookies = SimpleCookie()

        cookies['auth'] = value

        if value == 0:
            cookies['auth']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'

        self.send_header('Set-Cookie', cookies.output(header='', sep=''))

    def _charge_handler(self):
        pass

    def _error_handler(self):
        pass

    def _form_handler(self):
        pass

    def _log_in_handler(self):
        self._set_auth_cookies(100)

    def _log_out_handler(self):
        self._set_auth_cookies(0)

    HANDLERS = {
        'error.html': _error_handler,
    }

    if PORT == 8001:
        HANDLERS.update({
            'form.html': _form_handler,
        })
    elif PORT == 8002:
        HANDLERS.update({
            'charge.html': _charge_handler,
            'logIn.html': _log_in_handler,
            'logOut.html': _log_out_handler,
        })

    def _set_headers(self, page=None, content_type='text/html'):
        response_code = 200

        if page == 'error.html':
            response_code = 404

        self.send_response(response_code)
        self.send_header('Content-type', content_type)

        if page is not None:
            self.HANDLERS[page](self)

        self.end_headers()

    def do_GET(self):
        page = urlparse(self.path).path[1:] + '.html'

        if 'favicon.ico' in self.path or page not in self.HANDLERS.keys():
            page = 'error.html'

        self._set_headers(page)
        port_1, port_2 = 8001, 8002

        if self._get_auth_cookies():
            auth = f'<form action="http://{ HOST }:{ port_2 }/logOut"><input type="submit" value="Log Out"></form>'
        else:
            auth = f'<form action="http://{ HOST }:{ port_2 }/logIn"><input type="submit" value="Log In"></form>'

        self._set_template(page, auth=auth, host=HOST, port_1=port_1, port_2=port_2)

    def do_POST(self):
        self._set_headers()
        page = urlparse(self.path).path[1:] + '.html'

        if self._get_auth_cookies():
            form = FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            output = f'{form.getvalue("cake")}$ charged'
        else:
            output = 'Can\'t charge, you need to authorise yourself'

        self._set_template(page, output=output)


if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), Handler)

    try:
        print("Serving at {0}:{1}".format(HOST, PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        server.server_close()
