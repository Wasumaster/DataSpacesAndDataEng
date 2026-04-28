#!/bin/bash
for file in providers/*/observations.csv; do
    fname=$(basename $(dirname "$file"))"_observations.csv"
    if [ -f "central_repository/$fname" ] && ! cmp -s "$file" "central_repository/$fname"; then
        echo "Not synchronized: $file"
    fi
done
