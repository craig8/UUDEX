class BaseConfig():
    # PROPAGATE_EXCEPTIONS = True
    API_PREFIX = '/v1/uudex'
    DEBUG = False
    INCLUDE_RESPONSE_META_DATA = False
    PEER_CERT_KEY_NAME = "X_PEER_CERT_COMMON_NAME"
    SQLALCHEMY_DATABASE_URI = 'postgresql://uudex_user:uudex@localhost/uudex?options=-c+timezone%3Dutc'  # options parm: options=-c timezone=utc
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class DevConfig(BaseConfig):
    APP_SERVER_HOST = "weurkzieg"
    DEBUG = True
    FLASK_ENV = 'development'
    MESSAGE_BROKER_URL = "rabbitmq://localhost:15672?username=uudex&password=uudex"
    PROPAGATE_EXCEPTIONS = False
    SQLALCHEMY_ECHO = True

    # For weurkzieg dev server only (not gunicorn)
    SERVER_CERT_KEY = r"/home/d3m614/repos/UUDEX/example_ssl_certs/server/server.key"
    SERVER_CERT = r"/home/d3m614/repos/UUDEX/example_ssl_certs/server/server.crt"
    CA_CERT = r"/home/d3m614/repos/UUDEX/example_ssl_certs/ca.pem"
    #

# unproxied server option
# starts gunicorn so it's directly facing client and gunicron handles all ssl
class GunicornConfig(BaseConfig):
    APP_SERVER_HOST = "gunicorn"
    DEBUG = True
    FLASK_ENV = 'development'
    MESSAGE_BROKER_URL = "rabbitmq://localhost:15672?username=uudex&password=<password>"
    PROPAGATE_EXCEPTIONS = False
    SQLALCHEMY_ECHO = True

# proxied server - production mode
# expect nginx to forward requests over http. nginx handles ssl and passes client cert info in http header
class GunicornProxiedConfig(BaseConfig):
    APP_SERVER_HOST = "gunicorn_proxied"
    PEER_CERT_KEY_NAME = "X_SSL_CLIENT_S_DN"  # the header key nginx sends us
    DEBUG = True
    FLASK_ENV = 'development'
    MESSAGE_BROKER_URL = "rabbitmq://localhost:15672?username=uudex&password=<password>"
    PROPAGATE_EXCEPTIONS = False
    SQLALCHEMY_ECHO = True
