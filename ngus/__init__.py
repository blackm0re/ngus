# ngus v1.0
# Copyright (C) 2021 Simeon Simeonov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cgi
import http.server
import pathlib

__author__ = 'Simeon Simeonov'
__version__ = '1.0'
__license__ = 'GPL3'

DEFAULT_UPLOAD_PAGE = bytes('''<!DOCTYPE html>
<html>
<head>
<title>File Upload</title>
<meta name="viewport" content="width=device-width, user-scalable=no" />
<style type="text/css">
@media (prefers-color-scheme: dark) {
  body {
    background-color: #000;
    color: #fff;
  }
}
</style>
</head>
<body>
<h1>File Upload</h1>
<form method="POST" enctype="multipart/form-data">
<input name="ufile" type="file" />
<br/>
<br/>
<input type="submit" />
</form>
</body>
</html>''', 'utf-8')


class NgusBaseHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    A custom http.server.SimpleHTTPRequestHandler that handles POST uploads
    """
    def do_GET(self):
        """GET requests will load the upload page"""
        self._send_upload_page()

    def do_POST(self):
        """POST requests will be handled according to the settings"""
        if self.server.basic_auth is not None:
            if (
                'Authorization' not in self.headers
                or len(self.headers['Authorization'].split()) != 2
                or self.headers['Authorization'].split()[0].lower() != 'basic'
                or self.headers[
                    'Authorization'
                ].split()[1] != self.server.basic_auth
            ):
                self.send_response(http.HTTPStatus.UNAUTHORIZED)
                self.send_header('WWW-Authenticate',
                                 'Basic realm="ngus", charset="UTF-8"')
                self.end_headers()
                return None
        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD': 'POST'})
        if not (upload_dir := self.server.upload_dir).is_dir():
            raise ValueError('upload_dir is not a directory')
        i_name = self.server.input_name
        if i_name in form and form[i_name].file and form[i_name].filename:
            with open(
                upload_dir / pathlib.Path(form[i_name].filename).name,
                'wb'
            ) as f:
                f.write(form[i_name].file.read())
        self._send_upload_page()
        return None

    def _send_upload_page(self):
        """Renders an upload page (form)"""
        self.send_response(http.HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(self.server.upload_page))
        self.end_headers()
        self.wfile.write(self.server.upload_page)


class NgusHTTPServer(http.server.HTTPServer):
    """A custom http.server.HTTPServer"""
    def __init__(self, *arg, **kwargs):
        """
        """
        self._basic_auth = kwargs.pop('basic_auth', None)
        self._input_name = kwargs.pop('input_name', 'ufile')
        self._upload_dir = kwargs.pop('upload_dir', pathlib.Path.cwd())
        self._upload_page = kwargs.pop('upload_page', DEFAULT_UPLOAD_PAGE)
        super().__init__(*arg, **kwargs)

    @property
    def basic_auth(self):
        """basic_auth-property"""
        return self._basic_auth

    @property
    def input_name(self):
        """input_name-property"""
        return self._input_name

    @property
    def upload_dir(self):
        """upload_dir-property"""
        return self._upload_dir

    @property
    def upload_page(self):
        """upload_page-property"""
        return self._upload_page
