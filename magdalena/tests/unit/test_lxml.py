# SPDX-FileCopyrightText: 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import pytest

from ... import methodshub


class TestMethodsHubExtractHtml:
    def test_text(self):
        raw_html = b"""<html>
  <body>
    <main>
      Lorem ipsum.
    </main>
  </body>
</html>"""

        expected_html = b"""<div>
      Lorem ipsum.
    </div>"""

        html = methodshub.extract_content_from_html(raw_html)

        assert html == expected_html

    def test_header(self):
        raw_html = b"""<html>
  <body>
    <main>
      <header>Title</header>
      Lorem ipsum.
    </main>
  </body>
</html>"""

        expected_html = b"""<div>
      
      Lorem ipsum.
    </div>"""

        html = methodshub.extract_content_from_html(raw_html)

        assert html == expected_html

    def test_empty_link(self):
        raw_html = b"""<html>
  <body>
    <main>
      Lorem <a href="#cb1-1" aria-hidden="true" tabindex="-1"></a> ipsum.
    </main>
  </body>
</html>"""

        expected_html = b"""<div>
      Lorem <a href="#cb1-1" aria-hidden="true" tabindex="-1"></a> ipsum.
    </div>"""

        html = methodshub.extract_content_from_html(raw_html)

        assert html == expected_html
