#!/bin/bash
#
# Convert Jupyter Notebook to Jupyter Notebook
#
# Syntax:
#
# ipynb2md.sh

set -o errexit

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.ipynb

mkdir --parents $output_dirname

cp $file2render $output_dirname/$output_basename
