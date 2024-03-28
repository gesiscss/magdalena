#!/bin/bash
#
# Convert Microsoft Office Word 2007 (DOCX) to Markdown
#
# Syntax:
#
# docx2md.sh

set -o errexit

if test -f "/opt/quarto/bin/tools/pandoc"
then
    export PANDOC=/opt/quarto/bin/tools/pandoc
else
    export PANDOC=pandoc
fi

dirname2render=$(dirname ${file2render})
basename2render=$(basename ${file2render})

output_dirname=$output_location
output_basename=index.html

mkdir --parents $output_dirname

pandoc_version=$(${PANDOC} --version | head -n 1 | awk '{print $2}')
quarto_version=$(quarto --version)

cd $dirname2render

cover_filename=$(find . -name 'cover*' | head -n 1)

if [ -z "$cover_filename" ]
then
echo "Couldn't locate cover* file"
cover_metadata=""
else
echo "Located $cover_filename"
cover_metadata="image:$cover_filename"
fi

# --columns=288
#
# Pandoc requires a fixed length of lines in characters to preserve calculation of column widths for plain text.
# If the length of lines is too small, Pandoc will break long words into two.
#
# --reference-links
#
# Links can be very long and exceed the fixed length of lines. This creates many problems.
# Placing all the links at the end of the document, we avoid some of the problems.

ls
echo "File to render" ${file2render}
echo  ${basename2render}

${PANDOC} \
    --from docx+styles \
    --to html \
    --wrap=auto \
    --columns=288 \
    --reference-links \
    --standalone \
    --extract-media=./ \
    ${cover_metadata:+"--metadata" "$cover_metadata"} \
    --metadata "guide:true" \
    --metadata "citation:true" \
    --metadata "date:${git_date}" \
    --metadata "info_pandoc_version:${pandoc_version}" \
    --metadata "source_filename:${file2render}" \
    --lua-filter=_pandoc-filters/remove-toc.lua \
    --lua-filter=_pandoc-filters/remove-hyperlink-custom-style.lua \
    --lua-filter=_pandoc-filters/custom-style-to-class.lua \
    --lua-filter=_pandoc-filters/merge-div.lua \
    --lua-filter=_pandoc-filters/class-to-heading.lua \
    --lua-filter=_pandoc-filters/class-to-blockquote.lua \
    --lua-filter=_pandoc-filters/remove-extras.lua \
    --lua-filter=_pandoc-filters/populate-yaml-header.lua \
    --lua-filter=_pandoc-filters/class-to-keywords.lua \
    --output index.md \
    ${basename2render} && \
    cp index.md $output_dirname/$output_basename && \
    ${docker_script_root}/copy-assets.sh $output_dirname
