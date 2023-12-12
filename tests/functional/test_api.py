def test_post_ipynb_to_md(client):
    response = client.post(
        "/",
        json={
            "source_url": "https://github.com/GESIS-Methods-Hub/minimal-example-ipynb-python",
            "filename": "index.ipynb",
            "target_format": ["md"],
            "response": "download",
        },
    )

def test_post_docx_to_md(client):
    response = client.post(
        "/",
        json={
            "source_url": "https://gesisbox.gesis.org/index.php/s/tPbi9bXiHfXAHR4",
            "target_format": ["md"],
            "response": "download",
        },
    )

    expected_markdown = b"""---
citation: true
guide: true
info_pandoc_version: 3.1.2
keywords: {}
source_filename: lorem-ipsum.docx
---

Lorem ipsum.
"""
    assert response.data == expected_markdown

def test_post_docx_to_md_with_filename(client):
    response = client.post(
        "/",
        json={
            "source_url": "https://gesisbox.gesis.org/index.php/s/tPbi9bXiHfXAHR4",
            "filename": "minimal.docx",
            "target_format": ["md"],
            "response": "download",
        },
    )

    expected_markdown = b"""---
citation: true
guide: true
info_pandoc_version: 3.1.2
keywords: {}
source_filename: minimal.docx
---

Lorem ipsum.
"""
    assert response.data == expected_markdown
