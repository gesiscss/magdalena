#!/bin/bash
#
# Convert Markdown to Jupyter Notebook
#
# Syntax:
#
# md2ipynb.sh

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.ipynb

mkdir --parents $output_dirname

cd $dirname2render

quarto \
    convert ${basename2render} \
    --output index.ipynb && \
    cp index.ipynb $output_dirname/$output_basename
