#!/bin/bash
#
# Convert Quarto to Quarto
#
# Syntax:
#
# ipynb2md.sh

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.qmd

mkdir --parents $output_dirname

cp $file2render $output_dirname/$output_basename
