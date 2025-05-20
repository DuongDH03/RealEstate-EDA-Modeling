import os
import json
import csv
from pathlib import Path

# Adjust paths if needed
jsonl_dir = Path(__file__).parent.parent / "alonhadat.com" / "json_new"
output_dir = Path(__file__).parent.parent / "alonhadat.com" / "raw"
output_filename = "merged_alonhadat_new.csv"

output_dir.mkdir(parents=True, exist_ok=True)

jsonl_files = list(jsonl_dir.glob("*.jsonl"))
if not jsonl_files:
    print(f"No .jsonl files found in {jsonl_dir}")
    exit(1)

all_records = []
for jsonl_file in jsonl_files:
    print(f"Processing {jsonl_file}")
    try:
        with jsonl_file.open('r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                try:
                    record = json.loads(line)
                    all_records.append(record)
                except json.JSONDecodeError as de:
                    print(f"Skipping invalid JSON in {jsonl_file}: {de}")
    except Exception as e:
        print(f"Error reading {jsonl_file}: {e}")

if not all_records:
    print("No records to write")
    exit(1)

# collect all field names
fieldnames = set()
for rec in all_records:
    fieldnames.update(rec.keys())
fieldnames = sorted(fieldnames)

out_path = output_dir / output_filename
with out_path.open('w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(all_records)

print(f"Merged {len(all_records)} records into {out_path}")
print("Columns:", fieldnames)