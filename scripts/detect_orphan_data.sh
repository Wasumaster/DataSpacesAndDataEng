#!/bin/bash
for file in providers/*/observations.csv; do
    if ! grep -q "$file" metadata_catalog/*.json 2>/dev/null; then
        echo "Orphan: $file"
    fi
done
