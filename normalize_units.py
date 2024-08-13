import json
import csv

# Load localization data
localization_file = 'Loc_ENG_US.txt.json'
with open(localization_file, 'r', encoding='utf-8') as loc_file:
    localization_data = json.load(loc_file)

localization = localization_data['data']

# Read the CSV file, normalize names, and write back to a new CSV
input_csv = 'MustafarmersFull.csv'
output_csv = 'MustafarmersFull_normalized.csv'

with open(input_csv, 'r', encoding='utf-8') as csvfile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ['ReadableName']  # Add new column for ReadableName
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in reader:
        unit_key = row['BaseId']
        
        # Normalize the unit_id to get the readable name
        if "_V2" in unit_key:
            loc_key = unit_key.replace("_V2", "") + "_V2"
        else:
            loc_key = unit_key
        
        loc_key = f"UNIT_{unit_key}_NAME".upper()
        readable_name = localization.get(loc_key, unit_key)
        
        row['ReadableName'] = readable_name
        writer.writerow(row)

print("CSV file has been updated with readable names.")
