#!/bin/bash
for file in providers/*/observations.csv; do
    provider=$(basename $(dirname "$file"))
    count=$(tail -n +2 "$file" | wc -l)
    echo "${provider}: ${count}"
done
