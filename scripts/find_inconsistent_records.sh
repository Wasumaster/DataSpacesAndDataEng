#!/bin/bash
cat providers/*/observations.csv | grep -v "timestamp" | sort -u | awk -F',' '{a[$2]++} END {for(i in a) if(a[i]>1) print i}'
