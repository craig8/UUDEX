from __future__ import annotations

from pathlib import Path

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from pydantic import BaseModel
from uudex_web.settings import UUDEXSettings
from typing import Optional
from functools import lru_cache

from .sessions import SessionId


class Certificate(BaseModel):
    key_path: Path
    crt_path: Path
    name: str


certificate_by_session: dict[SessionId, Certificate] = {}

# This should only have the crt_path specified in it.
ca_certificate: Path

certificates: list[Certificate] = []

CertificateCommonName = str


def set_session_certificate(session_id: SessionId,
                            certificate: Certificate | CertificateCommonName):
    if isinstance(certificate, CertificateCommonName):
        certificate = get_certificate_by_name(certificate)
    certificate_by_session[session_id] = certificate


def get_session_certificate(session_id: SessionId) -> Certificate:
    return certificate_by_session[session_id]


def get_ca_certificate_path() -> Path:
    return ca_certificate


def get_certificate_by_name(name: CertificateCommonName) -> Optional[Certificate]:
    return next(filter(lambda x: x.name == name, certificates))


def get_certificates(cert_dir: Optional[Path] = None) -> list[Certificate]:
    global ca_certificate
    if certificates:
        return certificates

    if cert_dir is None:
        cert_dir = Path(UUDEXSettings.client_cert_dir)
    certs = []
    for cert in cert_dir.glob('**/*'):
        if cert.is_file() and cert.suffix in (".crt", ".pem"):
            with cert.open("rb") as f:
                pem_data = f.read()
                cert_obj = load_pem_x509_certificate(pem_data, default_backend())
                name = cert_obj.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
                key_path = Path(cert.as_posix()[:-len(cert.suffix) + 1] + 'key')
                if 'UUDEX CA' not in name:
                    certs.append(
                        Certificate(crt_path=cert,
                                    key_path=key_path,
                                    name=name.decode() if isinstance(name, bytes) else name))
                else:
                    ca_certificate = cert
    certs = sorted(certs, key=lambda k: k.name)

    certificates.extend(certs)
    return certs
