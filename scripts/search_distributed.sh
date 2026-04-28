#!/bin/bash
OBJ_ID=$1
grep -h "$OBJ_ID" providers/*/observations.csv
count=$(grep -h "$OBJ_ID" providers/*/observations.csv | wc -l)
echo "Total matches: $count"
