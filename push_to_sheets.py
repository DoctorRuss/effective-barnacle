import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

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
    csv_data=[
    ["L", "06/10/24", "U12 Colts", "Bristol Central Youth U12, Hillside", "U12 Div 4"],
    ["L", "06/10/24", "U14", "Hallen Youth U14", "Hillside", "U14 Div 1"],
    ["L", "06/10/24", "U14 Reds", "Backwell Athletic Junior Youth U14", "Hillside", "U14 Div 2"],
    ["L", "06/10/24", "U16", "Whitchurch Sports Junior Youth U16", "Hillside", "U16 Div 1 (White)"],
    ["L", "06/10/24", "U17 Youth", "Rockleaze Rangers Youth U18 Youth", "Hillside", "Division 2"],
    ["Cup", "06/10/24", "U10", "Mangotsfield United Youth U10 United", "Hillside", "U10 Autumn Cup_2024 - 2025"]
    ]
    # Update the sheet with CSV data
    sheet.update(csv_data)

if __name__ == "__main__":
    # Replace with your actual file and sheet details
    CSV_FILE = "output.csv"  # The CSV file generated from your script
    SHEET_ID = "Rockleaze_Sunday_Fixtures"  # The Google Sheet ID
    SHEET_NAME = "Sheet1"  # The name of the sheet/tab within the Google Sheet
    CREDENTIALS_FILE = "google_sheets_credentials.json"  # Path to the downloaded JSON file
    
    update_google_sheet(CSV_FILE, SHEET_ID, SHEET_NAME, CREDENTIALS_FILE)
