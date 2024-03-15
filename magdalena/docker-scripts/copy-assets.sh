#!/bin/bash
#
# Copy assets
#
# Syntax:
# copy-assets.sh output_dirname

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
