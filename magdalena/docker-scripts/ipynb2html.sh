#!/bin/bash
#
# Convert Jupyter Notebook to HTML
#
# Syntax:
#
# ipynb2html.sh

set -o errexit

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.html

mkdir --parents $output_dirname

git --version

git_hash=$(git rev-parse HEAD)

# If git > 2.25
# git_date=$(git log -1 --format="%as")
# else
git_date=$(git log -1 --format=format:%ad --date=format:%Y-%m-%d)

quarto_version=$(quarto --version)

cd $dirname2render

quarto \
    render ${basename2render} \
    --execute \
    --to html \
    --self-contained \
    --output ${output_basename} \
    --wrap=none \
    --metadata "method:true" \
    --metadata "citation:true" \
    --metadata "github_https:${github_https}" \
    --metadata "github_user_name:${github_user_name}" \
    --metadata "github_repository_name:${github_repository_name}" \
    --metadata "docker_image:${docker_image}" \
    --metadata "git_hash:${git_hash}" \
    --metadata "git_date:${git_date}" \
    --metadata "date:${git_date}" \
    --metadata "info_quarto_version:${quarto_version}" \
    --metadata "source_filename:${file2render}" && \
    cp ${output_basename} $output_dirname/$output_basename && \
    ${docker_script_root}/copy-assets.sh $output_dirname
