#!/bin/bash
#
# Convert R Markdown to Jupyter Notebook
#
# Syntax:
#
# Rmd2md.sh

set -o errexit

Rmd_file=$file2render
file2render=${Rmd_file/Rmd/qmd}

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.ipynb

mkdir --parents $output_dirname

cp $Rmd_file $file2render

sed -i -e '/^output: rmarkdown/d' $file2render

cd $dirname2render

quarto \
    convert ${basename2render} \
    --output index.ipynb && \
    cp index.ipynb ${output_dirname}/${output_basename}
