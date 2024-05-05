from __future__ import annotations
from dataclasses import dataclass
import os
from pathlib import Path
from typing import List, Optional


@dataclass
class ClientCert:
    name: str
    key_path: str
    cert_path: str

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def load_all(path: Path) -> List[ClientCert]:
        """Load the key and pem from the client certificats.
        
        The path should be to the client directories where 
        certificates and keys are located.  The clients should
        be in the following directory structure.

        clients/
            client1/
                client1.key
                client1.pem
            client2/
                client2.key
                client2.pem
        
        Args:
            path: Path to the root client certificate directory.

        Returns:
            A list of CertContainer objects, one for each client 
            in the client certificate directory.

        Raises:
            ValueError if one of the certificate directories does
            not contain a .key and .pem file within them.
        """
        certs: List[ClientCert] = []

        # For all dirs in the clients certificate directory
        for dir in path.iterdir():
            name = dir.name
            key = ""
            cert = ""

            # we expect the ca to be in the client's directory as well.
            if not dir.is_dir():
                continue

            # For files in the specific client's directory.
            for pth in dir.iterdir():
                if pth.suffix == '.pem':
                    cert = dir / pth.name
                if pth.suffix == '.key':
                    key = dir / pth.name
            
            if key == "" or cert == "":
                raise ValueError(f"key or pem cert not found in {pth.as_posix()}")

            certs.append(ClientCert(name,
                                       key,
                                       cert))
        return certs
    

class State:

    def __init__(self, client_certs_path: Path) -> None:
        self._client_cert = None
        self._client_certs = ClientCert.load_all(client_certs_path)
    
    def get_client_certs(self) -> List[ClientCert]:
        return self._client_certs
    
    def get_client_cert(self, index: int) -> Optional[ClientCert]:
        try:
            return self._client_certs[index]
        except IndexError:
            return None
        
    def set_client_cert(self, value: int):
        self._client_cert = [x for x in self._client_certs if x.name == value][0]

    def selected_client_cert(self) -> ClientCert:
        if self._client_cert is None:
            raise ValueError("Client cert has not been properly set.")

        return self._client_cert
