import logging
import os
from pathlib import Path
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

#from uudex_server.core.config import load_config
from .core import get_settings, get_logger
from uudex_server.services import get_services, create_services
from uudex_server.endpoints import add_routers

logger = get_logger("uudex_server.main")
logger.debug("Starting UUDEX Server")

# config = load_config(Path(".env-develop"))
# create_services(config)
#settings = get_settings(".env-develop")
settings = get_settings(".env")
#create_services(settings)
app = FastAPI(title="UUDEX API")

# Adds the endpoint routers to the FastAPI app
add_routers(app)

############################################################################
# Middleware functions
# These are loaded in reverse order.  So the first one listed is the last
# one called.  As they are chained together, the first one called is the
# last one listed. And will finish after all of the others have finished.
############################################################################


@app.middleware("http")
async def check_ssl_cert(request: Request, call_next):
    """
    This middleware method usese the request to determine whether or not a user
    is authorized.

    The certificate passed in the header x-ssl-cert (assumed to be passed from nginx)
    is interrogated.  If not present, then a 401 is returned.  If present, but
    the common name of the certificate is not found in the database, then a 401
    is returned.

    If the user is successfully looked up from the endpoints databases table, then
    it is stored in the request.state.endpoint variable for later use and validation.

    call_next is only called if the request is able to lookup the user.

    :param request: The http request used.
    :type request: Request
    :param call_next: The next request to call after this one.
    :type call_next: request function
    :return: The value returned from call_next
    :rtype: Response
    """

    logger.debug("Checking SSL Cert")
    if not request.headers.get('x-ssl-cert'):
        return JSONResponse(content=dict(error="Not Authorized"), status_code=403)


    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.backends import default_backend
    from urllib.parse import unquote
    from uudex_server.repos import endpoint_repository as er
    from uudex_server.services import get_db_session

    pem_data = request.headers.get('x-ssl-cert')
    if not pem_data:
        return JSONResponse(status_code=401, content="Missing x-ssl-cert from headers")

    pem_data = unquote(pem_data)

    cert = load_pem_x509_certificate(pem_data.encode('utf-8'))

    cn = str(cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value)


    endpoint = er.select_endpoint_by_certificate_dn(session=get_db_session(),
                                                    certificate_dn=cn)

    if not endpoint:
        return JSONResponse(status_code=401, content="Unauthorized certificate detected.")

    # Modify the request state adding the endpoint before continuing.
    request.state.endpoint = endpoint

    return await call_next(request)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"Process time: {process_time}")
    return response


@app.get("/")
async def root(request: Request):
    return {"message": "Hello World", "headers": request.headers}
