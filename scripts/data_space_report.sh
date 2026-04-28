#!/bin/bash
total_datasets=$(ls providers/*/observations.csv | wc -l)
total_records=$(cat providers/*/observations.csv | grep -v "timestamp" | wc -l)
obj3_dist=$(./scripts/search_distributed.sh "OBJ-003" | grep "Total matches:" | awk '{print $3}')
obj3_fed=$(./scripts/search_federated.sh "OBJ-003" | grep "Total matches:" | awk '{print $3}')
consistency="no"
if [ "$obj3_dist" -eq "$obj3_fed" ]; then consistency="yes"; fi

cat << REPORT > reports/data_space_report.txt
DATA SPACE REPORT
Total datasets: $total_datasets
Total records: $total_records
Objects found for query OBJ-003: $obj3_dist
Consistency check: $consistency
REPORT
