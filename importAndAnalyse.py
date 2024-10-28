import json
from datetime import datetime
import os


# Dictionary to group fixtures by date
date_format = "%d/%m/%y"

# Directory where your JSON files are stored
directory = '.'  # Replace with the actual directory path

# List to hold all fixtures
all_fixtures = []

# Read each JSON file and aggregate the data
for filename in os.listdir(directory):
    if filename.endswith('.json') and not filename.startswith('aggregated'):
        with open(os.path.join(directory, filename), 'r') as json_file:
            age_group_fixtures = json.load(json_file)
            all_fixtures.extend(age_group_fixtures)



# Optional: Save the aggregated fixtures to a new JSON file
#with open('aggregated_fixtures.json', 'w') as json_file:
#    json.dump(all_fixtures, json_file, indent=4)


# Print the grouped fixtures by date
# Sort the fixtures by date
sorted_fixtures = sorted(all_fixtures, key=lambda x: datetime.strptime(x['date'], date_format))

#for fixture in sorted_fixtures:
#    print(f"Date: {fixture['date']}, Home Team: {fixture['home_team']}, Away Team: {fixture['away_team']}, Fixture Type: {fixture['fixtype']} , Time: {fixture['time']}")
    
for fixture in sorted_fixtures:
    if fixture['home_team'].startswith('U'):
        print(f"Date: {fixture['date']}, Home Team: {fixture['home_team']}, Away Team: {fixture['away_team']}, Fixture Type: {fixture['fixtype']} , Time: {fixture['time']}")

print('\n Spreadsheet format \n')

for fixture in sorted_fixtures:
    if fixture['home_team'].startswith('U'):
        print(f"{fixture['fixtype']}, {fixture['date']}, {fixture['home_team']}, {fixture['away_team']}, Hillside, {fixture['competition']}")        