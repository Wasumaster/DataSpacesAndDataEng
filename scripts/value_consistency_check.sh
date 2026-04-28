#!/bin/bash
duckdb -c "SELECT column1 as object, 'Inconsistency (temp): ' || list_aggregate(list(column2), 'string_agg', ' vs ') FROM read_csv_auto('providers/*/observations.csv', header=False) GROUP BY 1 HAVING COUNT(*) > 1 AND (MAX(column2::DOUBLE) - MIN(column2::DOUBLE)) > 0.1;"
