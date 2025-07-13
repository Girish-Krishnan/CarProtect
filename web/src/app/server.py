import os
from wsgiref.simple_server import make_server
from . import create_app


def main():
    app = create_app()
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', '6000'))
    server = make_server(host, port, app)
    server.serve_forever()


if __name__ == '__main__':
    main()
