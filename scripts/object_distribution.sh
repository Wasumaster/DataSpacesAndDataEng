#!/bin/bash
for file in providers/*/observations.csv; do
    provider=$(basename $(dirname "$file"))
    echo "Provider: $provider"
    tail -n +2 "$file" | cut -d',' -f2 | sort | uniq -c
done
