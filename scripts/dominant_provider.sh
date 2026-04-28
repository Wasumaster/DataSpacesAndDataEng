#!/bin/bash
duckdb -c "SELECT (string_split(filename, '/'))[2] as provider, COUNT(*) || ' (' || ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv', header=False)), 0) || '%)' as contribution FROM read_csv_auto('providers/*/observations.csv', filename=True, header=False) GROUP BY 1 ORDER BY 1 DESC;"
