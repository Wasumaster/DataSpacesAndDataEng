#!/bin/bash
OBJ_ID=$1
count=0
for meta in metadata_catalog/*.json; do
    path=$(grep '"data_path"' "$meta" | cut -d'"' -f4)
    if [ -f "$path" ]; then
        grep -h "$OBJ_ID" "$path"
        c=$(grep -h "$OBJ_ID" "$path" | wc -l)
        count=$((count + c))
    fi
done
echo "Total matches: $count"
