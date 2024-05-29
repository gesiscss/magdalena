# SPDX-FileCopyrightText: 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import filecmp
import os.path
import re

from ... import methodshub
from ...mybinder import MYBINDER_URL

from ..util.methodshub import expected_mybinder_build_response


class TestMinimalExamples:
    def test_render_qmd_to_html_with_quarto(self, requests_mock):
        requests_mock.real_http = True

        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units.git",
            filename="index.qmd",
            git_commit_id="e07674b52239e67f41813ee9487258f740cf4719",
        )

        mybinder_build_matcher = re.compile(f"^{MYBINDER_URL}/build")
        requests_mock.get(
            mybinder_build_matcher,
            text=expected_mybinder_build_response(
                "gesiscss/binder-r2d-g5b5b759-gesis-2dmethods-2dhub-2dminimal-2dexample-2dqmd-2drstats-2dunits-06c93c",
                methods_hub_content.repository_name,
                methods_hub_content.git_commit_id,
            ),
        )

        mybinder_status_matcher = re.compile(f"^{MYBINDER_URL}/jupyter/user/.*/api$")
        requests_mock.get(mybinder_status_matcher, json={"version": "mock"})

        mybinder_shutdown_matcher = re.compile(
            f"^{MYBINDER_URL}/jupyter/user/.*/api/shutdown$"
        )
        requests_mock.post(mybinder_shutdown_matcher)

        methods_hub_content.create_container()
        methods_hub_content._render_format("html")

        file_path = methods_hub_content.rendered_file("html")
        expected_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../expected_files/minimal-example-qmd-rstats-units.html",
        )
        print(expected_file_path)
        assert filecmp.cmp(file_path, expected_file_path), "%s != %s" % (
            file_path,
            expected_file_path,
        )
