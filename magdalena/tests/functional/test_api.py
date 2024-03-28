import os
import datetime
import time

import jwt

from lxml import etree
from lxml.cssselect import CSSSelector


def generate_jwt():
    private_key = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

    now = datetime.datetime.now()
    authentication_time = now - datetime.timedelta(minutes=10)
    issue_time = now - datetime.timedelta(minutes=5)
    expiration_time = now + datetime.timedelta(minutes=30)

    payload = {
        "exp": int(time.mktime(expiration_time.timetuple())),
        "iat": int(time.mktime(issue_time.timetuple())),
        "auth_time": int(time.mktime(authentication_time.timetuple())),
        "jti": "995ad816-d8e6-4c5d-9dfc-64ad71b77342",
        "iss": os.getenv("JWT_ISSUER"),
        "aud": ["realm-management", "account"],
        "sub": "12345678-abcd-abcd-abcd-123456789012",
        "typ": "Bearer",
        "azp": "gesis-methodshub-ember-client",
        "nonce": "9dd3ed6f-35a2-419a-a547-32052225fc43",
        "session_state": "0b4b7e0c-0329-4050-9bf0-50d966a0b872",
        "acr": "1",
        "allowed-origins": ["http://localhost:4200"],
        "resource_access": {
            "realm-management": {
                "roles": [
                    "view-realm",
                    "view-identity-providers",
                    "manage-identity-providers",
                    "impersonation",
                    "realm-admin",
                    "create-client",
                    "manage-users",
                    "query-realms",
                    "view-authorization",
                    "query-clients",
                    "query-users",
                    "manage-events",
                    "manage-realm",
                    "view-events",
                    "view-users",
                    "view-clients",
                    "manage-authorization",
                    "manage-clients",
                    "query-groups",
                ]
            },
            "account": {"roles": ["manage-account", "manage-account-links"]},
        },
        "scope": "openid profile email",
        "sid": "0b4b7e0c-0329-4050-9bf0-50d966a0b872",
        "email_verified": True,
        "name": "Methods Hub",
        "preferred_username": "methodshub",
        "given_name": "Methods",
        "family_name": "Hub",
        "email": "methods@hub.localhost",
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


def test_post_ipynb_to_html(client):
    response = client.post(
        "/",
        headers={
            "Authorization": f"Bearer {generate_jwt()}",
        },
        json={
            "source_url": "https://github.com/GESIS-Methods-Hub/minimal-example-ipynb-python",
            "filename": "index.ipynb",
            "target_format": ["html"],
            "response": "download",
        },
    )

    assert response.status_code == 201, "New document was not created!"


def test_post_docx_to_html(client):
    response = client.post(
        "/",
        headers={
            "Authorization": f"Bearer {generate_jwt()}",
        },
        json={
            "source_url": "https://gesisbox.gesis.org/index.php/s/tPbi9bXiHfXAHR4",
            "target_format": ["html"],
            "response": "download",
        },
    )

    assert response.status_code == 201, "New document was not created!"
