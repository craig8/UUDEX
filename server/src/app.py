"""

UUDEX

Copyright © 2021, Battelle Memorial Institute

1. Battelle Memorial Institute (hereinafter Battelle) hereby grants
permission to any person or entity lawfully obtaining a copy of this
software and associated documentation files (hereinafter “the Software”)
to redistribute and use the Software in source and binary forms, with or
without modification.  Such person or entity may use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and
may permit others to do so, subject to the following conditions:

   - Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimers.
   - Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.
   - Other than as used herein, neither the name Battelle Memorial Institute
     or Battelle may be used in any form whatsoever without the express
     written consent of Battelle.

2. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

#########################################################
#
#    _    _   _    _   _____    ______  __   __
#   | |  | | | |  | | |  __ \  |  ____| \ \ / /
#   | |  | | | |  | | | |  | | | |__     \ V /
#   | |  | | | |  | | | |  | | |  __|     > <
#   | |__| | | |__| | | |__| | | |____   / . \
#    \____/   \____/  |_____/  |______| /_/ \_\
#
#
#########################################################

import os
import logging
from logging.handlers import RotatingFileHandler
import ssl
#
from flask import Flask, g, json
from werkzeug.serving import WSGIRequestHandler
#
import api
from api import setup
import common
import config
from models import db
from server_handlers.werkzeug_handler import PeerCertWSGIRequestHandler

# Create the app instance
from app_container import app
#

logger = logging.getLogger(__name__)

def setup_logger():

    LOG_FORMAT = ('%(levelname) -9s %(asctime)s  %(name) -55s %(funcName)  -35s %(lineno) -4d: %(message)s')
    DATE_FMT = '%Y-%m-%d %H:%M:%S'

    ch = logging.StreamHandler()
    ch.formatter = logging.Formatter(fmt=LOG_FORMAT)
    logger.parent.addHandler(ch)
    logger.parent.setLevel(logging.DEBUG)

    # numeric_level = getattr(logging, config.LOG_LEVEL.upper(), None)
    # logger = logging.getLogger(__name__)
    # logger.setLevel(numeric_level)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    fh = RotatingFileHandler(os.path.join(dir_path, "logs", "uudex.log"), maxBytes=1024 * 1024, backupCount=10)
    if config.APP_ENV == 'Dev':
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt="")
    fh.setFormatter(formatter)
    app.logger.parent.addHandler(fh)

    logger.info("    _    _   _    _   _____    ______  __   __")
    logger.info("   | |  | | | |  | | |  __ \  |  ____| \ \ / /")
    logger.info("   | |  | | | |  | | | |  | | | |__     \ V /")
    logger.info("   | |  | | | |  | | | |  | | |  __|     > <")
    logger.info("   | |__| | | |__| | | |__| | | |____   / . \\")
    logger.info("    \____/   \____/  |_____/  |______| /_/ \_\\")

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FMT)
    fh.setFormatter(formatter)
    #

    # app.logger.parent.addHandler(fh)


def setup_ssl_context():
    #
    # For development, setup SSL for built-in werkzeug dev server. In production,
    # it's assumed the app will be fronted by NGINX or Apache which will handle
    # SSL negotiation and simply pass the user cert to us or have  gunicorn
    # face clients directly.
    #

    # to establish an SSL socket we need the private key and certificate that
    # we want to serve to users.
    server_cert_key = config.SERVER_CERT_KEY
    server_cert = config.SERVER_CERT
    server_cert_key_password = ""

    # in order to verify client certificates we need the certificate of the
    # CA that issued the client's certificate.
    ca_cert = config.CA_CERT

    # create_default_context establishes a new SSLContext object that
    # aligns with the purpose we provide as an argument. Here we provide
    # Purpose.CLIENT_AUTH, so the SSLContext is set up to handle validation
    # of client certificates.
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=ca_cert)

    # load in the certificate and private key for our server to provide to clients.
    # force the client to provide a certificate.
    ssl_context.load_cert_chain(certfile=server_cert, keyfile=server_cert_key, password=server_cert_key_password)
    #  Required for client cert auth, see https://docs.python.org/3/library/ssl.html#ssl.CERT_REQUIRED
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    return ssl_context


@app.errorhandler(404)
def handle_404_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()

    # replace the body with JSON
    message = common.extract_attr_from_exception(e, e.name + " :: " + e.description)

    response.data = json.dumps({
        "code": e.code,
        "message": message})

    response.content_type = "application/json"
    return response

########################################################################################################################

app.config.from_object('config')
setup_logger()
logger.info('******************************************************')
logger.info(f'Starting UUDEX server in {config.APP_ENV} environment')
logger.info('******************************************************')
#
#
api.setup.add_routes()
api.uudex_api.init_app(app)
db.init_app(app)
#
#

if __name__ == '__main__':
    # keep-alive for flask built-in dev server (werkzeug)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"

    ssl_context = setup_ssl_context()

    # app.run(port=5000, debug=True)
    app.run(ssl_context=ssl_context, request_handler=PeerCertWSGIRequestHandler, port=5000)
    # app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
