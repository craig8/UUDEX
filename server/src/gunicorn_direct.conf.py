# this setup is for using gunicorn facing directly to outside and handling ssl (no nginx involved)

import ssl

bind = "0.0.0.0:3546"
worker_class = "server_handlers.gunicorn_handler.CustomWorker"

#### Site specific - change these parameters
ca_certs = "/home/d3m614/repos/UUDEX/example_ssl_certs/ca.pem"
certfile = "/home/d3m614/repos/UUDEX/example_ssl_certs/server/server.crt"
keyfile = "/home/d3m614/repos/UUDEX/example_ssl_certs/server/server.key"
####

cert_reqs = ssl.CERT_REQUIRED
do_handshake_on_connect = True
