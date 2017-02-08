"""
To use WSGI server from Gevent, run app like this

    python -m scorer.run

To see supported options:

    python -m scorer.run --help

To use Python's default WSGI, specify --debug option:

    python -m scorer.run --debug

"""
from gevent.wsgi import WSGIServer
import logging
import sys
from demo.main import app, parse_args

args = parse_args()

gevent_server = WSGIServer((args.host, args.port), app)
try:
    gevent_server.serve_forever()
except Exception as exc:
    logging.exception(exc)
    sys.exit(1)
