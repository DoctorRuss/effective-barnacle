import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import sys

# Authenticate using service account credentials
def authenticate_google_sheets(credentials_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# Load CSV and update the Google Sheet
def update_google_sheet(csv_file, sheet_id, sheet_name, credentials_file):
    client = authenticate_google_sheets(credentials_file)
    
    # Open the sheet
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    
    # Clear the existing content
    sheet.clear()
    
    # Load the CSV data
    #with open(csv_file, 'r') as f:
     #   reader = csv.reader(f)
     #   csv_data = list(reader)
    header_line = ["Cup","Date","Home Team","Away Team","Venue","Competition","Notes"]
    csv_data=[ header_line ]
    with open('Sunday.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            csv_data.append(row)
    
    # Update the sheet with CSV data
    sheet.update(csv_data)

if __name__ == "__main__":
    # Replace with your actual file and sheet details
    CSV_FILE = "output.csv"  # The CSV file generated from your script
    CREDENTIALS_FILE = "google_sheets_credentials.json"  # Path to the downloaded JSON file
    
    update_google_sheet(CSV_FILE, sys.argv[1], sys.argv[2], CREDENTIALS_FILE)
