import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
COMLINK_API = os.getenv('COMLINK_API')
INVENTORY_FILE = os.getenv('INVENTORY_FILE') # pulled from C3PO bot

# Load inventory and localization files
localization_file = 'Loc_ENG_US.txt.json'
output_file = 'inventory_output.csv'

with open(INVENTORY_FILE, 'r', encoding='utf-8') as inv_file:
    inventory_data = json.load(inv_file)

with open(localization_file, 'r', encoding='utf-8') as loc_file:
    localization_data = json.load(loc_file)

# Extract relevant sections
equipment = inventory_data['inventory']['equipment']
materials = inventory_data['inventory']['material']
ally_code = inventory_data['allyCode']
localization = localization_data['data']
# Prepare the output
output_lines = []
json_data = []

def fetch_player_data(ally_code):
    url = COMLINK_API + "/player" # ComLink URL
    payload = {
        "payload": {
            "allyCode": ally_code
        }
    }
    response = requests.post(url, json=payload)
    return response.json()

def parse_definition_id(definition_id):
    unit, star = definition_id.split(':')
    star_value = {
        'ONE_STAR': 1,
        'TWO_STAR': 2,
        'THREE_STAR': 3,
        'FOUR_STAR': 4,
        'FIVE_STAR': 5,
        'SIX_STAR': 6,
        'SEVEN_STAR': 7
    }.get(star, 0)
    return unit, star_value

player_data = fetch_player_data(str(ally_code))
roster_units = player_data['rosterUnit']

unit_stars = {}
for unit in roster_units:
    unit_id, star_value = parse_definition_id(unit['definitionId'])
    unit_stars[unit_id] = star_value

for item in equipment:
    item_id = item['id']
    quantity = item['quantity']
    loc_key = f"EQUIPMENT_{item_id}_NAME".upper()  # Ensure the lookup key is uppercase

        # Handle cases where _V2 is part of the loc_key
    if "_V2" in loc_key:
        loc_key = loc_key.replace("_V2", "") + "_V2"
    item_name = localization.get(loc_key, loc_key)
    
    # Format the output line
    output_line = f"\"{item_name}\", \"{quantity}\""
    output_lines.append(output_line)

    json_data.append({
            "item_name": item_name,
            "quantity": quantity
        })

# Process materials
for item in materials:
    item_id = item['id']
    quantity = item['quantity']

    if 'unitshard' in item_id.lower():
        unit_key = item_id.split('_', 1)[1]
        loc_key = f"UNIT_{unit_key}_NAME".upper()
        star_count = unit_stars.get(unit_key, 0)
        output_line = f"\"{localization.get(loc_key, loc_key)}\", \"{star_count};{quantity}\""
        json_data.append({
            "item_name": item_name,
            "star_count": star_count,
            "quantity": quantity
        })
    else:
        loc_key = f"{item_id}_NAME"
        item_name = localization.get(loc_key, loc_key)
        output_line = f"\"{item_name}\", \"{quantity}\""
        json_data.append({
            "item_name": item_name,
            "quantity": quantity
        })

    # Format the output line
    output_lines.append(output_line)

# Write the output lines to a file
with open(output_file, 'w', encoding='utf-8') as out_file:
    for line in output_lines:
        out_file.write(line + '\n')

# Write the JSON data to a file
json_output_file = 'output_data.json'
with open(json_output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

print(f"Output written to {output_file}")
print(f"Json Output written to {json_output_file}")
