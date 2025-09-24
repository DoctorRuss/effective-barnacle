
from datetime import datetime
import requests
import re
import json
import os
from bs4 import BeautifulSoup
from collections import defaultdict

# Date formats
incoming_date_format = "%a %d %b %Y %H:%M"
outgoing_date_format = "%Y-%m-%d"
outgoing_time_format = "%H:%M"

# Build the random seed
def calculateRandomSeed():
    now = datetime.now()
    return now.strftime("%Y%m%d%H")+str(now.minute)[0] if now.minute >= 10 else str(now.minute)

def sort_match(item):
    # parse into datetime objects so sorting works correctly
    dt = datetime.strptime(item["date"] + " " + item["time"], outgoing_date_format + " " + outgoing_time_format)
    return (dt.date(), dt.time(), item["home_team"])

# Take the incoming snippet_id, build the URL of the HTML snippet
# and extract the table
def scrapeData(snippet_id):
    
    seed=calculateRandomSeed()
    url = (
        f"https://fulltime.thefa.com/js/cs1.html"
        f"?cs={snippet_id}&random={seed}"
    )
    # Send a request to the website
    response = requests.get(url)
    response.raise_for_status()

    # Regex: grab the string after innerHTML =
    match = re.search(r'innerHTML\s*=\s*\'(.+?)\';', response.text, re.DOTALL)
    if not match:
        raise ValueError("No innerHTML assignment found")

    html_str = match.group(1)

    # Convert escaped sequences (e.g. \" & \n) into real characters
    return html_str.encode("utf-8").decode("unicode_escape")

def scrapeFixtures(snippet_id):
    html_str = scrapeData(snippet_id)
    fixtures = []
    if not html_str:
        return fixtures

    # take the table and extract the fixtures
    soup = BeautifulSoup(html_str, 'html.parser')
    fixtures_table = soup.find('table')
    rows = fixtures_table.find_all('tr')
    
    date=""
    time=""
    for row in rows:
        if (row.find("td", attrs={'colspan': True})):
            # check for the final row
            if (row.text.strip() == "League"):
                break
            # date
            dt = datetime.strptime(row.text.strip(), incoming_date_format)

            date = dt.strftime("%Y-%m-%d")  # or any format you like
            time = dt.strftime("%H:%M")
        else:
            columns = row.find_all('td')
            fixtype = columns[0].text.strip()
            home_team = columns[1].text.strip()  
            away_team = columns[3].text.strip()  
            venue = columns[4].text.strip()
            fixture = {
                'date': date,
                'fixtype': fixtype,
                'time': time,
                'home_team': home_team,
                'away_team': away_team,
                'venue': venue,
#                'competition': competition,
#                'notes': notes
            }
            fixtures.append(fixture)
    return fixtures

def scrapeResults(snippet_id):
    html_str = scrapeData(snippet_id)
    results = []
    if not html_str:
        return results

    # take the table and extract the results
    soup = BeautifulSoup(html_str, 'html.parser')
    fixtures_table = soup.find('table')
    rows = fixtures_table.find_all('tr')

    date=""
    time=""
    for row in rows:
        if (row.find("td", attrs={'colspan': True})):
            # check for the final row
            if (row.text.strip() == "League"):
                break
            # date
            dt = datetime.strptime(row.text.strip(), incoming_date_format)

            date = dt.strftime("%Y-%m-%d")
            time = dt.strftime("%H:%M")
        else:
            columns = row.find_all('td')
            fixtype = columns[0].text.strip()
            home_team = columns[1].text.strip()  
            away_team = columns[5].text.strip()  
            home_score = columns[2].text.strip()  
            away_score = columns[4].text.strip()  
            venue = columns[6].text.strip()
            result = {
                'date': date,
                'fixtype': fixtype,
                'time': time,
                'home_team': home_team,
                'away_team': away_team,
                'venue': venue,
                "score": home_score + " - " + away_score
            }
            results.append(result)

    return results

# Save to a JSON file
def write(matches, filename):
    with open(filename, 'w') as json_file:
        json.dump(sorted(matches, key=sort_match), json_file, indent=4)

def scrapeBSYL():
    write(scrapeFixtures(os.environ["BSYL_FIXTURES_ID"]), "bsyl_fixtures.json")
    write(scrapeResults(os.environ["BSYL_RESULTS_SNIPPET_ID"]), "bsyl_results.json")


if __name__ == "__main__":
    # BSYL
    scrapeBSYL()
