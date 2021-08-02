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

import argparse
import base64
import logging
import pathlib
import sys

import ngus


def eprint(*arg, **kwargs):
    """stdderr print wrapper"""
    print(*arg, file=sys.stderr, flush=True, **kwargs)


def main(inargs=None):
    """main entry point"""
    parser = argparse.ArgumentParser(
        description='The following options are available')
    parser.add_argument(
        '-b', '--basic-auth',
        metavar='<username:password>',
        type=str,
        dest='basic_auth',
        default='',
        help=('Require Basic auth from the client in order to POST a file '
              '(default: No basic auth required)'))
    parser.add_argument(
        '-H', '--hostname',
        metavar='<hostname>',
        type=str,
        dest='hostname',
        default='127.0.0.1',
        help='ngus server IP / hostname (default: 127.0.0.1)')
    parser.add_argument(
        '-i', '--input-name',
        metavar='<name>',
        type=str,
        dest='input_name',
        default='ufile',
        help='The name of the form input field (default: "ufile")')
    parser.add_argument(
        '-p', '--port',
        metavar='<port>',
        type=int,
        dest='port',
        default=8080,
        help='ngus server port (default: 8080)')
    parser.add_argument(
        '-u', '--upload-dir',
        metavar='<dir>',
        type=pathlib.Path,
        dest='upload_dir',
        default=pathlib.Path.cwd(),
        help='ngus server upload dir (default: CWD)')
    parser.add_argument(
        '-U', '--upload-page',
        metavar='<filename>',
        type=argparse.FileType('rb'),
        dest='upload_page',
        default=None,
        help='Alternative upload page (form) to display (default: None)')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {ngus.__version__}',
        help='Display program-version and exit')
    args = parser.parse_args(inargs)
    try:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        logger = logging.getLogger('ngus')
        logger.info('ngus starting')
        server_params = {
            'input_name': args.input_name,
            'upload_dir': args.upload_dir
        }
        if args.upload_page is not None:
            server_params['upload_page'] = args.upload_page.read()
        if args.basic_auth and len(args.basic_auth.split(':')) == 2:
            server_params['basic_auth'] = base64.b64encode(
                args.basic_auth.strip().encode('utf-8')).decode()
            logger.info('Requiring basic-auth')
        ngus_server = ngus.NgusHTTPServer((args.hostname, args.port),
                                          ngus.NgusBaseHTTPRequestHandler,
                                          **server_params)
        logger.info(f'Listening on {args.hostname}:{args.port}')
        logger.info('Done!')
        ngus_server.serve_forever()
    except KeyboardInterrupt:
        print('\n\nTerminating...')
    except Exception as e:
        eprint(f'ngus critical error: {e}')
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
