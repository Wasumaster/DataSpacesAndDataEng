#!/bin/bash
duckdb -c "SELECT column1 AS OBJECT, MAX(CASE WHEN filename LIKE '%satellite_A%' THEN 'X' ELSE '-' END) AS A, MAX(CASE WHEN filename LIKE '%satellite_B%' THEN 'X' ELSE '-' END) AS B, MAX(CASE WHEN filename LIKE '%ground_station%' THEN 'X' ELSE '-' END) AS G FROM read_csv_auto('providers/*/observations.csv', filename=True, header=False, all_varchar=True) GROUP BY 1 ORDER BY 1;"
