#!/bin/bash

# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

#
# Convert Markdown to HTML
#
# Syntax:
#
# md2html.sh

set -o errexit

md2render=${file2render}
qmd2render=${file2render/.md/.qmd}

cp ${md2render} ${qmd2render}

export file2render=${qmd2render}

$( dirname -- "${BASH_SOURCE[0]}" )/qmd2html.sh
