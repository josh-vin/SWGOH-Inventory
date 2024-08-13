import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://swgoh.gg"
url = "https://swgoh.gg/stats/mod-meta-report/guilds_100_gp/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the rows in the table
rows = soup.find_all('tr')

mod_data = []

# for row in rows:
#     cols = row.find_all('td')
#     if len(cols) < 5:
#         continue  # Skip rows that don't have enough columns
    
#     # Character name
#     character_name = cols[0].find('a').text.strip()
    
#     # Mod sets
#     mod_sets = [mod['title'].strip().split('\n')[2].strip() for mod in cols[1].find_all('div', class_='stat-mod-set-def-icon')]
    
#     # Recommended stats
#     recommended_stats = [col.text.strip() for col in cols[2:]]

#     # Character Profile Picture
#     portrait_url = row.find('img', class_='character-portrait__img')['src']

#     # Best Mods link
#     best_mods_url = row.find('a', href=True)['href']
    
#     mod_data.append({
#         'character_name': character_name,
#         'character_mods_url': best_mods_url,
#         'portrait_url': portrait_url,
#         'mod_sets': mod_sets,
#         'recommended_stats': recommended_stats
#     })

# # Example output
# for mod in mod_data:
#     print(mod)

# Prepare CSV data
csv_data = [["Character Name", "Mod Sets", "Arrow", "Triangle", "Circle", "Cross"]]

for row in rows:
    cols = row.find_all('td')
    if len(cols) < 5:
        continue  # Skip rows that don't have enough columns
    
    # Character name
    character_name = cols[0].find('a').text.strip().replace('"', '" & CHAR(34) & "')

    best_mods_href = cols[0].find('a', href=True)['href']
    best_mods_url = base_url + best_mods_href

    # Format character name as a hyperlink for Google Sheets
    character_name_link = f'=HYPERLINK("{best_mods_url}", "{character_name}")'
    
    # Mod sets
    mod_sets = [mod['title'].strip().split('\n')[2].strip() for mod in cols[1].find_all('div', class_='stat-mod-set-def-icon')]
    mod_sets_str = ', '.join(mod_sets)
    
    # Recommended stats
    recommended_stats = [col.text.strip() for col in cols[2:]]
    
    # Map recommended stats to specific gear slots
    arrow_stat = recommended_stats[0] if len(recommended_stats) > 0 else ""
    triangle_stat = recommended_stats[1] if len(recommended_stats) > 1 else ""
    circle_stat = recommended_stats[2] if len(recommended_stats) > 2 else ""
    cross_stat = recommended_stats[3] if len(recommended_stats) > 3 else ""
    
    # Append to CSV data
    csv_data.append([character_name_link, mod_sets_str, arrow_stat, triangle_stat, circle_stat, cross_stat])

# Write to CSV file
with open("swgoh_mod_recommendations.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print("CSV file created: swgoh_mod_recommendations.csv")