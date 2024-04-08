#!/bin/bash

# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

#
# Convert Quarto to Quarto
#
# Syntax:
#
# ipynb2md.sh

set -o errexit

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.qmd

mkdir --parents $output_dirname

cp $file2render $output_dirname/$output_basename
