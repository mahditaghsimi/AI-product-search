import pandas as pd
import os

# CSV file path from data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, 'data', '##yor_data_file_name##')

# Load the CSV
df = pd.read_csv(csv_path)

print("✅ Dataset loaded successfully!\n")
print("📐 Shape (rows, columns):", df.shape)

print("\n🧱 Column names:")
print(df.columns.tolist())

print("\n🧮 Data types per column:")
print(df.dtypes)

print("\n🚨 Missing values (% per column):")
nulls = df.isnull().mean().round(3) * 100
print(nulls[nulls > 0].sort_values(ascending=False))

print("\n🔍 Sample data (random 3 rows):")
print(df.sample(3))

print("\n📊 Descriptive statistics (numeric columns):")
print(df.describe())

print("\n🔢 Unique value counts for selected columns:")
for col in ['categories', 'brand', 'company_name', 'availability', 'unit']:
    if col in df.columns:
        print(f"- {col}: {df[col].nunique()} unique values")

# Load the CSV file

print("🔢 Unique value counts per column:\n")
for col in df.columns:
    unique_count = df[col].nunique(dropna=True)
    print(f"- {col}: {unique_count} unique values")