#!/bin/bash
#
# Convert Markdown to HTML
#
# Syntax:
#
# md2html.sh

md2render=${file2render}
qmd2render=${file2render/.md/.qmd}

mv ${md2render} ${qmd2render}

export file2render=${qmd2render}

./qmd2html.sh
