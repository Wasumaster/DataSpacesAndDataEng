#!/bin/bash
cat providers/*/observations.csv | grep -v "timestamp" | cut -d',' -f2 | sort | uniq -c > /tmp/obj_cov
num_prov=$(ls -d providers/*/ | wc -l)
echo "In all providers:"
awk -v np="$num_prov" '$1 == np {print $2}' /tmp/obj_cov
echo "Only one provider:"
awk '$1 == 1 {print $2}' /tmp/obj_cov
