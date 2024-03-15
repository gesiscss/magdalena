from bs4 import BeautifulSoup, NavigableString


def test_get_index(client):
    response = client.get("/")
    response_html = BeautifulSoup(response.data, "html.parser")

    assert response_html.find(id="source_url") is not None
    assert response_html.find(id="filename") is not None
