#!/bin/bash
#
# Convert Jupyter Notebook to Quarto
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

cd $dirname2render

quarto \
    convert ${basename2render} \
    --output index.qmd && \
    cp index.qmd $output_dirname/$output_basename
