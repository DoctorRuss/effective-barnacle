
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict


# Dictionary to group fixtures by date
date_format = "%d/%m/%y"

def scrapeFixtures(url, filename): 
    #fixtures_by_date = defaultdict(list)
    fixtures = []

    # Send a request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        fixtures_table_div = soup.find('div', class_='fixtures-table')

        if fixtures_table_div:
            # Find the table within the div
            table = fixtures_table_div.find('table')

            # Find all rows in the table
            rows = table.find_all('tr')

            # Iterate over each row and extract specific columns
            for row in rows:
                # Find all columns in the row
                columns = row.find_all('td')

                # Check if the row contains the expected number of columns
                if len(columns) >= 3:  # Adjust this based on how many columns you need
                    fixtype = columns[0].find('a').text.strip()  
                    date = columns[1].find('span').text.strip()  
                    time = columns[1].find('span', class_='color-dark-grey').text.strip()  
                    home_team = columns[2].text.strip()  
                    away_team = columns[6].text.strip()  
                    competition = columns[8].text.strip()  
                    notes = columns[9].text.strip()  
                    
                    if home_team.startswith('Rockleaze') or away_team.startswith('Rockleaze'):
                        fixture = {
                            'date': date,
                            'fixtype': fixtype,
                            'time': time,
                            'home_team': home_team,
                            'away_team': away_team,
                            'competition': competition,
                            'notes': notes
                        }
                        fixtures.append(fixture)

                    # Print or store the extracted data
                    #    print(f"Date: {date}, Home Team: {home_team}, Away Team: {away_team}")  

            # Save to a JSON file
            with open(f'{filename}.json', 'w') as json_file:
                json.dump(fixtures, json_file, indent=4)

            # Print the JSON data
            json_string = json.dumps(fixtures, indent=4)
            #print(json_string)
        else:
            print("No div element with class 'fixtures-table' found")
    else:
        print("Failed to retrieve the webpage")


if __name__ == "__main__":
    # age group 8 is u15, through to age group 12 is u11
    for age in {8,10,11,12}:
        # URL of the webpage you want to scrape
        print(f"BSYL, Age group u{23-age}")
        url = f'https://fulltime.thefa.com/fixtures.html?selectedSeason=595674523&selectedFixtureGroupAgeGroup={age}&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub=272311862&selectedTeam=&selectedRelatedFixtureOption=3&selectedFixtureDateStatus=&selectedFixtureStatus=&previousSelectedFixtureGroupAgeGroup={age}&previousSelectedFixtureGroupKey=&previousSelectedClub=&itemsPerPage=5000'
        scrapeFixtures(url, f"BSYL_u{23-age}")
    for age in {7,8,9,10,11}:
        # URL of the webpage you want to scrape
        print(f"Avon Youth League, age group u{23-age}")
        url = f'https://fulltime.thefa.com/fixtures.html?selectedSeason=224185215&selectedFixtureGroupAgeGroup={age}&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub=71590072&selectedTeam=&selectedRelatedFixtureOption=3&selectedFixtureDateStatus=&selectedFixtureStatus=&previousSelectedFixtureGroupAgeGroup={age}&previousSelectedFixtureGroupKey=&previousSelectedClub=&itemsPerPage=5000'
        scrapeFixtures(url, f"AYL_u{23-age}")
    for age in {12,13}:
        # URL of the webpage you want to scrape
        print(f"Hanham Minor League, age group u{23-age}")
        url = f'https://fulltime.thefa.com/fixtures.html?selectedSeason=349469407&selectedFixtureGroupAgeGroup={age}&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub=103988540&selectedTeam=&selectedRelatedFixtureOption=3&selectedFixtureDateStatus=&selectedFixtureStatus=&previousSelectedFixtureGroupAgeGroup={age}&previousSelectedFixtureGroupKey=&previousSelectedClub=&itemsPerPage=5000'
        scrapeFixtures(url, f"HML_u{23-age}")
    severnvalley = 'https://fulltime.thefa.com/fixtures.html?selectedSeason=153093739&selectedFixtureGroupAgeGroup=12&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub=780282713&selectedTeam=&selectedRelatedFixtureOption=3&selectedFixtureDateStatus=&selectedFixtureStatus=&previousSelectedFixtureGroupAgeGroup=12&previousSelectedFixtureGroupKey=&previousSelectedClub=&itemsPerPage=500'
    scrapeFixtures(severnvalley, f"SVYL_u11")
    combination = 'https://fulltime.thefa.com/fixtures.html?selectedSeason=726305118&selectedFixtureGroupAgeGroup=0&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub=735841389&selectedTeam=&selectedRelatedFixtureOption=3&selectedFixtureDateStatus=&selectedFixtureStatus=&previousSelectedFixtureGroupAgeGroup=&previousSelectedFixtureGroupKey=&previousSelectedClub=&itemsPerPage=250'
    scrapeFixtures(combination, f"FCL_u18")

    # Print the grouped fixtures by date
    #sorted_dates = sorted(fixtures_by_date.keys(), key=lambda d: datetime.strptime(d, date_format))
    #for date in sorted_dates:
    #    print(f"Date: {date}")
    #    for fixture in fixtures_by_date[date]:
    #        print(f" Home Team: {fixture['home_team']}, Away Team: {fixture['away_team']}, Fixture Type: {fixture['fixtype']}")
    #        #, Time: {fixture['time']}
            
    #for date in sorted_dates:        
    #    for fixture in fixtures_by_date[date]:
    #        print(f"{fixture['fixtype']}, {date}, {fixture['home_team']}, {fixture['away_team']}, Hillside, {fixture['competition']}")
            
