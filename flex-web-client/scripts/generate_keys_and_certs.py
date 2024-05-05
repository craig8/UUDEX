
"""
This module generates private keys and certificates for UUDEX common names.

Usage:
    python generate_private_keys.py <easyrsa_dir>

Arguments:
    easyrsa_dir (str): Path to EasyRSA directory.

Steps:
1. Parse the command-line arguments.
2. Check if the specified EasyRSA directory exists.
3. Define a list of common names for the private keys.
4. Generate private keys and certificate signing requests (CSRs) for each common name in the current directory.
5. Initialize EasyRSA and build the certificate authority (CA).
6. Import the CSRs and sign the requests using EasyRSA.
7. Copy the generated certificates and CA file to the current directory.

"""

import argparse
import subprocess
from subprocess import PIPE
import os
import sys
import shutil
from pathlib import Path

# Rest of the code...
import argparse
import subprocess
from subprocess import PIPE
import os
import sys
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description='Generate private keys for UUDEX')
parser.add_argument('easyrsa_dir', type=str, help='Path to EasyRSA directory')

opts = parser.parse_args()

if not Path(opts.easyrsa_dir).exists():
    print(f"Path {opts.easyrsa_dir} does not exist")
    sys.exit(1)

opts.easyrsa_dir = Path(opts.easyrsa_dir).expanduser()

key_common_names = (
    '4b3b819e-94bd-4adf-b461-17ccb58ac870__app_rt_1',
    '0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client',
    '3fa9be8b-a0f9-40a5-ab3d-51d580d4797e_alice',
    '7ef06c20-1937-4492-b697-122d07fc72e8_subj_pol_demo',
    '8f026ebe-c71e-4fa1-8d66-82d3d85b72a4-mitre-client',
    '58c728dc-bb26-4d13-a670-348f8821057e_carol',
    '8487799e-237b-4c26-8d25-c50665ac909a-oati-client',
    'b24c1e2b-5c00-41ce-b196-630e69428d29_bob',
    'mitre-uudex.mitre.org',
    'oati-uudex.oati.com',
    'uudex-demo.pnl.gov',
    'localhost'
)

server_key = 'localhost'

cmd_create_key = "openssl genrsa -out {key}.key 2048"
cmd_generate_csr = 'openssl req -new -key {key}.key -out {key}.csr -subj /C=US/ST=Washington/L=Richland/O=UUDEX/OU=UUDEX/CN={key}'

for key in key_common_names:
    print(f"Create key: {cmd_generate_csr}".format(key=key))
    try:
        subprocess.check_call(f"{cmd_create_key}".format(key=key).split(), stderr=PIPE, stdout=PIPE)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())

    print(f"Create csr: {cmd_generate_csr}".format(key=key))
    try:
        subprocess.check_call(f"{cmd_generate_csr}".format(key=key).split(),
                              stderr=PIPE,
                              stdout=PIPE)
    except subprocess.CalledProcessError as e:
        print(e)

easyrsa_dir = opts.easyrsa_dir
easyrsa = f"{easyrsa_dir}/easyrsa"
easyrsa_init = f"{easyrsa} init-pki"
easyrsa_build_ca = f"{easyrsa} build-ca nopass"

print("Initializing EasyRSA: ", easyrsa_init)
p = subprocess.run(easyrsa_init.split(),
                   stderr=PIPE,
                   stdout=PIPE,
                   input="yes\n",
                   encoding='ascii',
                   cwd=easyrsa_dir,
                   text=True)
print(p.returncode)
assert p.returncode == 0
p = subprocess.run(easyrsa_build_ca.split(),
                   stderr=PIPE,
                   stdout=PIPE,
                   input="UUDEX CA\n",
                   encoding='ascii',
                   cwd=easyrsa_dir,
                   text=True)
print(p.returncode)
assert p.returncode == 0

for key in key_common_names:
    easy_rsa_import = f"{easyrsa} import-req {os.getcwd()}/{key}.csr {key}"
    keytype = 'client'
    if key == server_key:
        keytype = 'server'
    easy_rsa_sign = f"{easyrsa} sign-req {keytype} {key}"

    try:
        print("Importing csr: ", easy_rsa_import)
        subprocess.check_call(easy_rsa_import.split(), stderr=PIPE, stdout=PIPE, cwd=easyrsa_dir)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())


    print("Signing Client: ", easy_rsa_sign)
    p = subprocess.run(easy_rsa_sign.split(), stderr=PIPE, stdout=PIPE, cwd=easyrsa_dir, input="yes\n", encoding='ascii', text=True)
    assert p.returncode == 0

print("Copying certs")
[shutil.copy(f"{easyrsa_dir}/pki/issued/{key}.crt", ".") for key in key_common_names]

print("Copying ca")
shutil.copy(f"{easyrsa_dir}/pki/private/ca.key", ".")
shutil.copy(f"{easyrsa_dir}/pki/ca.crt", ".")
