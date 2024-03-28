#!/bin/bash
#
# Convert Markdown to Markdown
#
# Syntax:
#
# md2md.sh

set -o errexit

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location/$dirname2render/${basename2render%.*}
output_basename=index.md

mkdir --parents $output_dirname

git --version

git_hash=$(git rev-parse HEAD)

# If git > 2.25
# git_date=$(git log -1 --format="%as")
# else
git_date=$(git log -1 --format=format:%ad --date=format:%Y-%m-%d)

quarto_version=$(quarto --version)

cd $dirname2render

# README.md does NOT have YAML headers.
# If processing a file without YAML headers,
#
# 1. shift the heading level
# 2. provide name of the author
# 3. search for cover image
if [[ $(head -n 1 ${basename2render} | grep -e '---' | wc -l) = 0 ]]
then
    echo ${basename2render} does NOT have a YAML header!
    shift_heading_level='-1'
    fallback_author="author:$(git log -1 --format=format:%aN)"

    cover_filename=$(find . -name 'cover*' | head -n 1)

    if [ -z "$cover_filename" ]
    then
    echo "Couldn't locate cover* file"
    cover_metadata=""
    else
    echo "Located $cover_filename"
    cover_metadata="image:$cover_filename"
    fi

else
    echo ${basename2render} has a YAML header!
    shift_heading_level='0'
    fallback_author=''
    cover_metadata=""
fi

quarto \
    render ${basename2render} \
    --to markdown \
    --output index.md-tmp \
    --wrap=none \
    ${shift_heading_level:+"--shift-heading-level-by" "$shift_heading_level"} \
    ${fallback_author:+"--metadata" "$fallback_author"} \
    ${cover_metadata:+"--metadata" "$cover_metadata"} \
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
    cp index.md-tmp "$output_dirname/$output_basename" && \
    ${docker_script_root}/copy-assets.sh "$output_dirname"
