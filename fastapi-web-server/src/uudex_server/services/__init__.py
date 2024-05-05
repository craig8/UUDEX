from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from uudex_server.core.settings import Settings
from uudex_server.services.authentication_service import AuthenticationService
from uudex_server.services.authorization_service import AuthorizationService
#from uudex_server.services.database_service import DatabaseService
from uudex_server.services.database_service import get_db_session

__services__: Services = None


class Services:
    """Services class holds a reference to the services available on the server.

    Each service will be available through a property and created during instantiation
    of the services.  This class should not be instantiated other than through the
    fuctions `get_services` and `create_services`.
    """

    def __init__(self, settings: Settings):
        """Initialize all of the services available on the server.

        :param config: A dictionary of configuration elements to create the services from.
        :type config: Dict
        """
        ...
        #self.db_service: DatabaseService = DatabaseService.create(settings)
        #self.auth_service: AuthenticationService = AuthenticationService.create(settings)
#        self.authz_service: AuthorizationService = AuthorizationService.create(config, self.auth_service)


def get_services() -> Services:
    """Retrieve a `Services` object to gain access to server services.

    :raises RuntimeError: If create_services hasn't been calle dirst
    :return:
    :rtype: Services
    """
    if not __services__:
        raise RuntimeError(
            f"Services have not be initialized call create_services first!")
    return __services__


def create_services(config: Dict) -> Services:
    """Create a services object and returns it

    :param config: A configuration dictionary of key/value pairs.
    :type config: Dict
    :return:
    :rtype: Services
    """
    global __services__
    if __services__ is None:
        __services__ = Services(config)
    return get_services()


__all__: List[str] = ["get_services", "create_services"]
