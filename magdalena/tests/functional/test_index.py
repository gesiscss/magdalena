# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from bs4 import BeautifulSoup, NavigableString


def test_get_index(client):
    response = client.get("/")
    response_html = BeautifulSoup(response.data, "html.parser")

    assert response_html.find(id="source_url") is not None
    assert response_html.find(id="filename") is not None
