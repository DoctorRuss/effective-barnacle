import json
from datetime import datetime
import os

# Dictionary to group fixtures by date
date_format = "%d/%m/%y"

# Directory where your JSON files are stored
directory = '.'  # Replace with the actual directory path

def isSaturdayLeague(filename):
    return filename.startswith('BSYL') or filename.startswith('SVYL')

def sortAndPrintFixtures(fixtures):    
    # Sort the fixtures by date
    sorted_fixtures = sorted(fixtures, key=lambda x: datetime.strptime(x['date'], date_format))
    # Print the grouped fixtures by date
    for fixture in sorted_fixtures:
        if 'Postponed' not in fixture['notes'] and fixture['home_team'].startswith('Rockleaze'):
            print(f"{fixture['fixtype']}, {fixture['date']}, {fixture['home_team'].removeprefix('Rockleaze Rangers ').removeprefix('Youth ')}, {fixture['away_team']}, Hillside, {fixture['competition']}")        
    
# Read each JSON file and aggregate the data

# List to hold all fixtures
saturday_fixtures = []
sunday_fixtures = []


for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as json_file:
            if isSaturdayLeague(filename):
                saturday_fixtures.extend(json.load(json_file))
            else:
                sunday_fixtures.extend(json.load(json_file))

print('\nSaturday Spreadsheet format \n')
sortAndPrintFixtures(saturday_fixtures)
print('\nSunday Spreadsheet format \n')
sortAndPrintFixtures(sunday_fixtures)

# Optional: Save the aggregated fixtures to a new JSON file
#with open('aggregated_fixtures.json', 'w') as json_file:
#    json.dump(all_fixtures, json_file, indent=4)

#for fixture in sorted_fixtures:
#    print(f"Date: {fixture['date']}, Home Team: {fixture['home_team']}, Away Team: {fixture['away_team']}, Fixture Type: {fixture['fixtype']} , Time: {fixture['time']}")
    
#for fixture in saturday_sorted_fixtures:
#    if 'Postponed' in fixture['notes']:
#        continue
#    elif fixture['home_team'].startswith('Rockleaze'):
#        print(f"Date: {fixture['date']}, Home Team: {fixture['home_team'].removeprefix('Rockleaze Rangers ').removeprefix('Youth ')}, Away Team: {fixture['away_team']}, Fixture Type: {fixture['fixtype']} , Time: {fixture['time']}")



