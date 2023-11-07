#!/bin/bash
#
# Convert Quarto to Jupyter Notebook
#
# Syntax:
#
# ipynb2md.sh

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.ipynb

mkdir --parents $output_dirname

quarto \
    convert ${basename2render} \
    --output index.ipynb && \
    cp index.ipynb $output_dirname/$output_basename
