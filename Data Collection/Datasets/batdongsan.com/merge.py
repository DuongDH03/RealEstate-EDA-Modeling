import os
import json
import csv
from pathlib import Path

def merge_jsonl_to_csv(json_dir, output_dir, output_filename="merged_data.csv"):
    """
    Merge all JSONL files from json_dir to a single CSV file in output_dir
    without using pandas
    
    Args:
        json_dir (str): Directory containing JSONL files
        output_dir (str): Directory to save the merged CSV file
        output_filename (str): Name of the output CSV file
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # List all JSONL files in the json_dir
    jsonl_files = [f for f in os.listdir(json_dir) if f.endswith('.jsonl')]
    
    if not jsonl_files:
        print(f"No JSONL files found in {json_dir}")
        return
    
    print(f"Found {len(jsonl_files)} JSONL files to process")
    
    # Initialize an empty list to store all records
    all_records = []
    
    # Read and merge all JSONL files
    for jsonl_file in jsonl_files:
        file_path = os.path.join(json_dir, jsonl_file)
        print(f"Processing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        # Parse each line as JSON
                        record = json.loads(line)
                        all_records.append(record)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {jsonl_file}, line: {line[:50]}...: {e}")
        except Exception as e:
            print(f"Error reading file {jsonl_file}: {e}")
    
    if not all_records:
        print("No data found in JSONL files")
        return
    
    print(f"Total records collected: {len(all_records)}")
    
    # Get all unique field names across all records
    fieldnames = set()
    for record in all_records:
        fieldnames.update(record.keys())
    fieldnames = sorted(list(fieldnames))
    
    # Write to CSV
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(all_records)
    
    print(f"Successfully merged data and saved to {output_path}")
    print(f"Total records: {len(all_records)}")
    print("Column names:", fieldnames)

if __name__ == "__main__":
    # Set base directory to script location
    base_dir = Path(__file__).parent
    json_dir = base_dir / 'json_batdongsan'
    output_dir = base_dir / 'raw_batdongsan'
    output_filename = 'batdongsan.csv'
    # Execute the merge operation
    merge_jsonl_to_csv(str(json_dir), str(output_dir), output_filename)