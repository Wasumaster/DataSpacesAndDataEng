#!/bin/bash
duckdb -c "SELECT CASE WHEN COUNT(DISTINCT column_count) > 1 THEN 'SCHEMA DRIFT DETECTED' ELSE 'SCHEMA STATUS: CONSISTENT' END FROM (SELECT filename, COUNT(*) as column_count FROM read_csv_auto('providers/*/observations.csv', filename=True, header=False) GROUP BY 1);"
