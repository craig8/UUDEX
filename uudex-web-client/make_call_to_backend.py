# from http.client import HTTPSConnection
# import ssl

# key_file = 'certs/0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client.key'
# cert_file = 'certs/0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client.crt'
# ca_file = 'certs/ca.crt'

# context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
# context.load_cert_chain(keyfile=key_file,
#                         certfile=cert_file)
# context.load_verify_locations(cafile=ca_file)

# conn = HTTPSConnection("localhost", port=443, context=context)
# conn.request('GET', '/api/participants/')
# resp = conn.getresponse()
# print(resp.status, resp.reason)
# data = resp.read()
# print(data.decode('utf-8'))

import httpx
import ssl

key_file = 'certs/0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client.key'
cert_file = 'certs/0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client.crt'
ca_file = 'certs/ca.crt'

context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(keyfile=key_file, certfile=cert_file)
context.load_verify_locations(cafile=ca_file)

client = httpx.Client(verify=context)

participants = client.get('https://localhost/api/participants/')
print(participants)
