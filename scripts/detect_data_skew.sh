#!/bin/bash
wc -l providers/*/observations.csv | grep -v "total" | sort -n > /tmp/counts
min=$(head -n 1 /tmp/counts | awk '{print $1}')
max=$(tail -n 1 /tmp/counts | awk '{print $1}')
echo "Difference: $((max - min))"
