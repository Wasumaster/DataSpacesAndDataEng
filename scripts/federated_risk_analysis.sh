#!/bin/bash
duckdb -c "SELECT 'FULL: ' || f, 'FEDERATED: ' || fed, 'MISSING: ' || (f-fed), 'LOSS: ' || ROUND((f-fed)*100.0/f, 1) || '%' FROM (SELECT COUNT(*) as f FROM read_csv_auto('providers/*/observations.csv', header=False)) AS full_q, (SELECT COUNT(*) as fed FROM read_csv_auto(['providers/satellite_A/observations.csv','providers/satellite_B/observations.csv'], header=False)) AS fed_q;"
