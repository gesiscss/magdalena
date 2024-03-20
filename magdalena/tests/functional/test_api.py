from lxml import etree
from lxml.cssselect import CSSSelector


def test_post_ipynb_to_md(client):
    response = client.post(
        "/",
        json={
            "source_url": "https://github.com/GESIS-Methods-Hub/minimal-example-ipynb-python",
            "filename": "index.ipynb",
            "target_format": ["html"],
            "response": "download",
        },
    )

    response_html = etree.fromstring(response.data, etree.HTMLParser())

    selector = CSSSelector("main")
    selection = selector(response_html)

    assert len(selection) > 0, "HTML document does NOT have <main>!"


def test_post_docx_to_md(client):
    response = client.post(
        "/",
        json={
            "source_url": "https://gesisbox.gesis.org/index.php/s/tPbi9bXiHfXAHR4",
            "target_format": ["html"],
            "response": "download",
        },
    )

    response_html = etree.fromstring(response.data, etree.HTMLParser())

    selector = CSSSelector("main")
    selection = selector(response_html)

    assert len(selection) > 0, "HTML document does NOT have <main>!"


def test_post_docx_to_md_with_filename(client):
    response = client.post(
        "/",
        json={
            "source_url": "https://gesisbox.gesis.org/index.php/s/tPbi9bXiHfXAHR4",
            "filename": "minimal.docx",
            "target_format": ["html"],
            "response": "download",
        },
    )

    response_html = etree.fromstring(response.data, etree.HTMLParser())

    selector = CSSSelector("main")
    selection = selector(response_html)

    assert len(selection) > 0, "HTML document does NOT have <main>!"
