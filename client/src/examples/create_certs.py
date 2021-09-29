import os
import subprocess


def create_client_certs(cert_name):
    cwd = f"{os.path.expanduser('~')}/easyrsa"
    easyrsa_path = f"{cwd}/easyrsa"
    cmd = [easyrsa_path, 'build-client-full', cert_name, 'nopass']
    results = subprocess.run(cmd, cwd=cwd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if results.returncode != 0:
        raise RuntimeError(f"Error executing command: {cmd}")
    else:
        print(f"{results.stdout.decode('utf-8')}")