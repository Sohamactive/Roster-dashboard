import pandas as pd

# Check roster_processing_details columns
print("=" * 60)
print("ROSTER_PROCESSING_DETAILS.CSV COLUMNS:")
print("=" * 60)
df1 = pd.read_csv('roster_processing_details.csv')
for i, col in enumerate(df1.columns, 1):
    print(f"{i:2d}. {col}")

print(f"\nTotal: {len(df1.columns)} columns, {len(df1)} rows")

# Check aggregated_operational_metrics columns  
print("\n" + "=" * 60)
print("AGGREGATED_OPERATIONAL_METRICS.CSV COLUMNS:")
print("=" * 60)
df2 = pd.read_csv('aggregated_operational_metrics.csv')
for i, col in enumerate(df2.columns, 1):
    print(f"{i:2d}. {col}")

print(f"\nTotal: {len(df2.columns)} columns, {len(df2)} rows")

# Show sample data
print("\n" + "=" * 60)
print("SAMPLE DATA FROM EACH FILE:")
print("=" * 60)
print("\nRoster Processing Details (first 2 rows & key columns):")
key_cols = ['RO_ID', 'ORG_NM', 'CNT_STATE', 'LOB', 'RUN_NO', 'IS_FAILED', 'FAILURE_STATUS', 'LATEST_STAGE_NM']
available = [c for c in key_cols if c in df1.columns]
print(df1[available].head(2))

print("\nAggregated Metrics (first 2 rows):") 
print(df2.head(2))
