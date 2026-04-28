#!/bin/bash
for meta in metadata_catalog/*.json; do
    path=$(grep '"data_path"' "$meta" | cut -d'"' -f4)
    if [ ! -f "$path" ]; then
        echo "Inconsistent: $path does not exist"
    elif [ ! -s "$path" ]; then
        echo "Inconsistent: $path is empty"
    fi
done
