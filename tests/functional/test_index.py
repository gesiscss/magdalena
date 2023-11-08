from bs4 import BeautifulSoup, NavigableString

def test_index(client):
    response = client.get("/")
    response_html = BeautifulSoup(response.data, 'html.parser')

    assert response_html.find(id="git_repository_url") is not None
    assert response_html.find(id="filename") is not None
