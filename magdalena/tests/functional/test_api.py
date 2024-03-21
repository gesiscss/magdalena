from lxml import etree
from lxml.cssselect import CSSSelector


def test_post_ipynb_to_html(client):
    response = client.post(
        "/",
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
        json={
            "source_url": "https://gesisbox.gesis.org/index.php/s/tPbi9bXiHfXAHR4",
            "target_format": ["html"],
            "response": "download",
        },
    )

    assert response.status_code == 201, "New document was not created!"
