#!/bin/bash
#
# Convert Markdown to HTML
#
# Syntax:
#
# md2html.sh

md2render=${file2render}
qmd2render=${file2render/.md/.qmd}

cp ${md2render} ${qmd2render}

export file2render=${qmd2render}

$( dirname -- "${BASH_SOURCE[0]}" )/qmd2html.sh
