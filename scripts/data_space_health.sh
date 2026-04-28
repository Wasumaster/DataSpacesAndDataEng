#!/bin/bash
ds_count=$(ls providers/*/observations.csv | wc -l)
miss_meta=$(./scripts/check_metadata_coverage.sh | wc -l)
empty_ds=$(find providers -name "observations.csv" -empty | wc -l)
incon=$(./scripts/find_inconsistent_records.sh | wc -l)
fed_comp=$(./scripts/check_query_completeness.sh "OBJ-003")

cat << REPORT > reports/data_space_health.txt
HEALTH REPORT
Total datasets: $ds_count
Missing metadata: $miss_meta
Empty datasets: $empty_ds
Inconsistent datasets: $incon
Federated queries complete: $fed_comp
REPORT
