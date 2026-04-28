#!/bin/bash
OBJ_ID=$1
dist_count=$(./scripts/search_distributed.sh "$OBJ_ID" | grep "Total matches:" | awk '{print $3}')
fed_count=$(./scripts/search_federated.sh "$OBJ_ID" | grep "Total matches:" | awk '{print $3}')
echo "Distributed count: $dist_count"
echo "Federated count: $fed_count"

if [ "$dist_count" -eq "$fed_count" ]; then
    echo "Consistency check: yes"
else
    echo "Consistency check: no"
fi
