import json
from datetime import datetime
import os
import csv

# Dictionary to group fixtures by date
date_format = "%d/%m/%y"

# Directory where your JSON files are stored
directory = '.'  # Replace with the actual directory path

def isHomeGame(fixture):
    return 'Hillside' in fixture['venue'] or fixture['home_team'].startswith('Rockleaze')

def isSaturdayLeague(filename):
    return filename.startswith('BSYL') or filename.startswith('SVYL')

def sortAndPrintFixtures(fixtures):    
    # Sort the fixtures by date
    sorted_fixtures = sorted(fixtures, key=lambda x: datetime.strptime(x['date'], date_format))
    # Print the grouped fixtures by date
    for fixture in sorted_fixtures:
        if 'Postponed' not in fixture['notes'] and isHomeGame(fixture):
            print(f"{fixture['fixtype']}, {fixture['date']}, {fixture['home_team'].removeprefix('Rockleaze Rangers ').removeprefix('Youth ')}, {fixture['away_team']}, {fixture['venue']}, {fixture['competition']}")        

def sortAndSaveFixtures(fixtures, filename):    
    # Sort the fixtures by date
    sorted_fixtures = sorted(fixtures, key=lambda x: datetime.strptime(x['date'], date_format))
    # Print the grouped fixtures by date
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for fixture in sorted_fixtures:
            if 'Postponed' not in fixture['notes'] and isHomeGame(fixture):
                spamwriter.writerow([fixture['fixtype'], fixture['date'], fixture['home_team'].removeprefix('Rockleaze Rangers ').removeprefix('Youth '), fixture['away_team'], fixture['venue'], fixture['competition'], fixture['notes']])
    
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
saturday_fixtures = [fixture for fixture in saturday_fixtures if 'score' not in fixture]
sortAndPrintFixtures(saturday_fixtures)
sortAndSaveFixtures(saturday_fixtures, "Saturday.csv")
print('\nSunday Spreadsheet format \n')
sunday_fixtures = [fixture for fixture in sunday_fixtures if 'score' not in fixture]
sortAndPrintFixtures(sunday_fixtures)
sortAndSaveFixtures(sunday_fixtures, "Sunday.csv")
