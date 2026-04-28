#!/bin/bash
OBJ_ID=$1
dist=$(./scripts/search_distributed.sh "$OBJ_ID" | grep "Total matches" | awk '{print $3}')
fed=$(./scripts/search_federated.sh "$OBJ_ID" | grep "Total matches" | awk '{print $3}')
if [ "$dist" -eq "$fed" ]; then echo "yes"; else echo "no"; fi
