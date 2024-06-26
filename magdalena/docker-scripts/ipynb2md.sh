#!/bin/bash

# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

#
# Convert Jupyter Notebook to Markdown
#
# Syntax:
#
# ipynb2md.sh

set -o errexit

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.md

mkdir --parents $output_dirname

quarto_version=$(quarto --version)

cd $dirname2render

quarto \
    render ${basename2render} \
    --execute \
    --to markdown \
    --output index.md \
    --wrap=none \
    --metadata "method:true" \
    --metadata "citation:true" \
    --metadata "github_https:${github_https}" \
    --metadata "github_user_name:${github_user_name}" \
    --metadata "github_repository_name:${github_repository_name}" \
    --metadata "docker_image:${docker_image}" \
    --metadata "info_quarto_version:${quarto_version}" \
    --metadata "source_filename:${file2render}" && \
    cp index.md $output_dirname/$output_basename && \
    ${docker_script_root}/copy-assets.sh $output_dirname
