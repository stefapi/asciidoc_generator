#!/bin/bash
#
# Install openai for Python
# pip install openai


#set -x
set -euo pipefail

prog="$(realpath "$0")"
prog_dirname="$(dirname "$prog")"
outdir="$(realpath .)/english"

dirs="./maindocs ./common ./policy"

for dir in $dirs; do
    for file in "$dir"/*.asc; do
        target="$outdir/$file"
        mkdir -p "$(dirname "$target")"

        if [ ! -e "$target" ] || [ "$file" -nt "$target" ]; then
            "$prog_dirname/translate.py" "$file" "$target"
        fi
    done
done

