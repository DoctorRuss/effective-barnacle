
from datetime import datetime
import requests
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict


# Dictionary to group fixtures by date
date_format = "%d/%m/%y"

def scrapeData(url, table_class):
    # Send a request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        data = soup.find('div', class_=table_class)
    return data


def scrapeFixtures(season, club, age): 
    url = f'https://fulltime.thefa.com/fixtures.html?selectedSeason={season}&selectedFixtureGroupAgeGroup={age}&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub={club}&selectedTeam=&selectedRelatedFixtureOption=3&selectedFixtureDateStatus=&selectedFixtureStatus=&previousSelectedFixtureGroupAgeGroup={age}&previousSelectedFixtureGroupKey=&previousSelectedClub=&itemsPerPage=5000'
    table_class = 'fixtures-table'

    fixtures_table = scrapeData(url, table_class)
    if not fixtures_table:
        return
    # Find all rows in the table within the div
    rows = fixtures_table.find('table').find_all('tr')

    fixtures = []
    # Iterate over each row and extract specific columns
    for row in rows:
        # Find all columns in the row
        columns = row.find_all('td')

        # Check if the row contains the expected number of columns
        if len(columns) >= 9:  # Adjust this based on how many columns you need
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
    return fixtures
        
def scrapeResults(season, club, age): 
    #fixtures_by_date = defaultdict(list)
    url = f'https://fulltime.thefa.com/results.html?selectedSeason={season}&selectedFixtureGroupAgeGroup={age}&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub={club}&selectedTeam=&selectedRelatedFixtureOption=3&selectedFixtureDateStatus=&selectedFixtureStatus=&previousSelectedFixtureGroupAgeGroup={age}&previousSelectedFixtureGroupKey=&previousSelectedClub=&itemsPerPage=5000'
    
    table_class = 'results-table-2'
    results_table = scrapeData(url, table_class)
    if not results_table:
        return
    # Find all rows in the table within the div
    rows = results_table.find('div', class_='tbody').find_all('div', id=re.compile(r'^fixture-\d{8}$'))
    
    results = []

    # Iterate over each row and extract specific columns
    for row in rows:
        fixtype = row.find('div', class_='type-col').find('a').text.strip()
        date = row.find('div', class_='datetime-col').find('span').text.strip()
        time = row.find('div', class_='datetime-col').find('span', class_='color-dark-grey').text.strip()
        home_team = row.find('div', class_='home-team-col').find('div', class_='team-name').find('a').text.strip()
        away_team = row.find('div', class_='road-team-col').find('div', class_='team-name').find('a').text.strip()  
        score = row.find('div', class_='score-col').text.strip()  
        competition = row.find('div', class_='fg-col').find('p').text.strip()

        if home_team.startswith('Rockleaze') or away_team.startswith('Rockleaze'):
            fixture = {
                'date': date,
                'fixtype': fixtype,
                'time': time,
                'home_team': home_team,
                'away_team': away_team,
                'competition': competition,
                'score': score
            }
            results.append(fixture)
    
    sorted_results = sorted(results, key=lambda x: datetime.strptime(x['date'], date_format))        
    return sorted_results

def scrapeAndSave(season, club, age, filename):
    fixtures = scrapeFixtures(season, club, age)
    results = scrapeResults(season, club, age)
    # Save to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(results+fixtures, json_file, indent=4)

    # Print the JSON data
    #json_string = json.dumps(results, indent=4)
    #print(json_string)

if __name__ == "__main__":
    # age group 8 is u15, through to age group 12 is u11
    for age in {8,10,11,12}:
        # URL of the webpage you want to scrape
        print(f"BSYL, Age group u{23-age}")
        season = 595674523
        club = 272311862
        filename = f'BSYL_u{23-age}.json' 
        scrapeAndSave(season, club, age, filename)
    for age in {7,8,9,10,11}:
        # URL of the webpage you want to scrape
        print(f"Avon Youth League, age group u{23-age}")
        season = 224185215
        club = 71590072
        filename = f'AYL_u{23-age}.json' 
        scrapeAndSave(season, club, age, filename)
    for age in {12,13}:
        # URL of the webpage you want to scrape
        print(f"Hanham Minor League, age group u{23-age}")
        season = 349469407
        club = 103988540
        filename = f'HML_u{23-age}.json'
        scrapeAndSave(season, club, age, filename)
    
    season = 153093739
    club = 780282713
    age=12
    filename = f'SVYL_u{23-age}.json'
    print(f"Severn Valley League, age group u{23-age}")
    scrapeAndSave(season, club, age, filename)
    
    season = 726305118
    club = 735841389
    age=0
    filename = f'FCL_u18.json'
    print(f"Football Combination League, age group u18")
    scrapeAndSave(season, club, age, filename)