#!/bin/bash
duckdb -c "SELECT 'TOTAL OBJECTS: ' || COUNT(*), 'FULL COVERAGE: ' || SUM(CASE WHEN providers=3 THEN 1 ELSE 0 END), 'COVERAGE SCORE: ' || ROUND(SUM(CASE WHEN providers=3 THEN 1 ELSE 0 END)*100.0/COUNT(*), 0) || '%' FROM (SELECT column1, COUNT(DISTINCT filename) as providers FROM read_csv_auto('providers/*/observations.csv', filename=True, header=False) GROUP BY 1);"
