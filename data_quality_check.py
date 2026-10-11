from pathlib import Path
import pandas as pd

folder = Path(__file__).parent
file_path = folder / "call_records_clean.csv"
df = pd.read_csv(file_path)

print("=" * 60)
print("CONTACT CENTER DATA QUALITY AUDIT")
print("=" * 60)

# 1. Basic dataset overview
print("\n1. DATASET OVERVIEW")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Duplicate call IDs: {df['call_id'].duplicated().sum()}")

# 2. Missing values
print("\n2. MISSING VALUES BY COLUMN")
missing = df.isna().sum()
print(missing[missing > 0].to_string() if missing.any() else "No missing values")

# 3. Check key fields
print("\n3. KEY FIELD VALIDATION")
print("Missing call IDs:", df["call_id"].isna().sum())
print("Missing timestamps:", df["call_datetime"].isna().sum())
print("Invalid call hours:", (~df["call_hour"].between(0, 23)).sum())
print("Invalid CSAT scores:", (~df["csat_score"].dropna().between(1, 5)).sum())
print("Invalid wait times:", (df["wait_time_seconds"] < 0).sum())
print("Invalid handling times:", (df["handling_time_seconds"] < 0).sum())

# 4. Category checks
print("\n4. CALL STATUS COUNTS")
print(df["call_status"].value_counts(dropna=False).to_string())

print("\n5. SURVEY RESPONSE COUNTS")
print(df["survey_responded"].value_counts(dropna=False).to_string())

# 5. CSAT consistency
print("\n6. CSAT CHECK")
print("Missing CSAT when survey was answered:",
      df.loc[df["survey_responded"] == 1, "csat_score"].isna().sum())
print("CSAT present when no survey response:",
      df.loc[df["survey_responded"] == 0, "csat_score"].notna().sum())

# 6. Numeric summary
print("\n7. NUMERIC SUMMARY")
print(df[[
    "wait_time_seconds",
    "handling_time_seconds",
    "csat_score",
    "revenue_inr"
]].describe().round(2).to_string())

# 7. Save a reusable report
report_path = folder / "data_quality_report.txt"
with report_path.open("w", encoding="utf-8") as report:
    report.write("CONTACT CENTER DATA QUALITY AUDIT\n")
    report.write(f"Rows: {len(df)}\n")
    report.write(f"Columns: {len(df.columns)}\n")
    report.write(f"Duplicate rows: {df.duplicated().sum()}\n")
    report.write(f"Duplicate call IDs: {df['call_id'].duplicated().sum()}\n")
    report.write("\nMissing values:\n")
    report.write(df.isna().sum().to_string())
    report.write("\n\nCall status counts:\n")
    report.write(df["call_status"].value_counts(dropna=False).to_string())

print(f"\nAudit report saved to: {report_path}")
print("\nAUDIT COMPLETE")
