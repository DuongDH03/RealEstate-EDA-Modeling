# Merge all .json files (list of dicts) to a single CSV
import os
import json
import csv
from pathlib import Path

json_dir = "../Datasets/nhatot.com/json"  # Adjust path if running from notebook
output_dir = "../Datasets/nhatot.com/raw"
output_filename = "merged_data.csv"

Path(output_dir).mkdir(parents=True, exist_ok=True)

json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
if not json_files:
    print(f"No JSON files found in {json_dir}")
else:
    print(f"Found {len(json_files)} JSON files to process")

all_records = []
for json_file in json_files:
    file_path = os.path.join(json_dir, json_file)
    print(f"Processing {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            records = json.load(file)
            if isinstance(records, list):
                all_records.extend(records)
            else:
                print(f"File {json_file} does not contain a list, skipping.")
    except Exception as e:
        print(f"Error reading file {json_file}: {e}")

if not all_records:
    print("No data found in JSON files")
else:
    print(f"Total records collected: {len(all_records)}")
    # Get all unique field names
    fieldnames = set()
    for record in all_records:
        fieldnames.update(record.keys())
    fieldnames = sorted(list(fieldnames))

    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(all_records)
    print(f"Successfully merged data and saved to {output_path}")
    print(f"Total records: {len(all_records)}")
    print("Column names:", fieldnames)