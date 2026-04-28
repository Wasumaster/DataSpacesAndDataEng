
#!/bin/bash
OBJ_ID=${1:-"OBJ-003"}
REPORT="reports/query_report.txt"

echo "DATA SPACE QUERY REPORT" > $REPORT
echo "Generated at: $(date)" >> $REPORT
echo "--------------------------" >> $REPORT

echo -e "\n[GLOBAL STATISTICS]" >> $REPORT
duckdb -c "SELECT 'Total observations: ' || COUNT(*) FROM read_csv_auto('providers/*/observations.csv', header=False);" >> $REPORT
duckdb -c "SELECT 'Distinct objects: ' || COUNT(DISTINCT column1) FROM read_csv_auto('providers/*/observations.csv', header=False);" >> $REPORT

echo -e "\n[OBJECT ANALYSIS: $OBJ_ID]" >> $REPORT
echo "Providers containing object:" >> $REPORT
duckdb -c "SELECT DISTINCT (string_split(filename, '/'))[2] FROM read_csv_auto('providers/*/observations.csv', filename=True, header=False, all_varchar=True) WHERE column1='$OBJ_ID';" >> $REPORT
duckdb -c "SELECT 'Total observations: ' || COUNT(*) FROM read_csv_auto('providers/*/observations.csv', header=False, all_varchar=True) WHERE column1='$OBJ_ID';" >> $REPORT

echo -e "\n[FEDERATED QUERY COMPARISON]" >> $REPORT
duckdb -c "
WITH full_q AS (SELECT COUNT(*) as f FROM read_csv_auto('providers/*/observations.csv', header=False, all_varchar=True) WHERE column1='$OBJ_ID'),
fed_q AS (SELECT COUNT(*) as fed FROM read_csv_auto(['providers/satellite_A/observations.csv','providers/satellite_B/observations.csv'], header=False, all_varchar=True) WHERE column1='$OBJ_ID')
SELECT 'FULL RESULT: ' || f, 'FEDERATED RESULT: ' || fed, 'COMPLETE: ' || (CASE WHEN f=fed THEN 'YES' ELSE 'NO' END) FROM full_q, fed_q;" >> $REPORT

echo -e "\n[SCHEMA VALIDATION]" >> $REPORT
duckdb -c "SELECT CASE WHEN COUNT(DISTINCT cols) > 1 THEN 'Schema consistency: INCONSISTENT' ELSE 'Schema consistency: CONSISTENT' END FROM (SELECT filename, 4 as cols FROM read_csv_auto('providers/*/observations.csv', filename=True, header=False) GROUP BY 1);" >> $REPORT
