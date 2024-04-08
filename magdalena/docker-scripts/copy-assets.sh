#!/bin/bash

# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

#
# Copy assets
#
# Syntax:
# copy-assets.sh output_dirname

set -o errexit

output_dirname=$1

find . \
    \( \
    \( -type f -iname '*.bib' \) \
    -o \( -type f -iname '*.csl' \) \
    -o \( -type f -iname '*.jpg' \) \
    -o \( -type f -iname '*.jpeg' \) \
    -o \( -type f -iname '*.png' \) \
    -o \( -type f -iname '*.webp' \) \
    -o \( -type f -iname '*.gif' \) \
    -o \( -type f -iname '*.tif' \) \
    -o \( -type f -iname '*.tiff' \) \
    -o \( -type f -iname '*.svg' \) \
    -o \( -type f -iname '*.pdf' \) \
    -o \( -type f -iname '*.eps' \) \
    \) | \
    xargs -I {} cp --parents {} $output_dirname
