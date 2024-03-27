import os
import os.path

import requests

KEYCLOAK_SCHEME = os.getenv("KEYCLOAK_SCHEME", "https")
KEYCLOAK_DOMAIN = os.getenv("KEYCLOAK_DOMAIN", None)
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", None)

assert KEYCLOAK_DOMAIN is not None, "KEYCLOAK_DOMAIN can't be None"
assert KEYCLOAK_REALM is not None, "KEYCLOAK_REALM can't be None"

KEYCLOAK_ISSUER = f"{KEYCLOAK_SCHEME}://{KEYCLOAK_DOMAIN}/realms/{KEYCLOAK_REALM}"

def retrieve_public_key():
    request = requests.get(KEYCLOAK_ISSUER)

    assert request.status_code == 200, "Keycloak answer must be 200"

    request_as_json = request.json()

    public_key = request_as_json['public_key']

    # Documented at https://www.rfc-editor.org/rfc/rfc7468
    pem_public_key = "-----BEGIN RSA PUBLIC KEY-----\n"
    # 16 groups of 4 chars, which means exactly 64 chars per; line, except the final line
    for i in range(len(public_key) // 64):
        begin = i * 64
        end = (i + 1) * 64
        pem_public_key += f"{public_key[begin:end]}\n"
    pem_public_key += f"{public_key[end:]}\n"
    pem_public_key += "-----END RSA PUBLIC KEY-----\n"

    return pem_public_key
