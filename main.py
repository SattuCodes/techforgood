import csv
import os
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# SCOPES defines the access level for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Load Google Sheet data
def load_google_sheet_data(spreadsheet_id, range_name):
    creds = None
    # The token.json stores the user's access and refresh tokens, and is created automatically.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no valid credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Fetch the data from the Google Sheet
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values

# Load leaderboard.csv data
def load_leaderboard_data():
    leaderboard_data = {}
    with open("leaderboard.csv", mode="r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            token = row['token']
            leaderboard_data[token] = {
                'name': row['name'],
                'itemsDonated': row['itemsDonated']
            }
    return leaderboard_data

# Merge Google Sheet data with leaderboard.csv
def merge_data(google_data, leaderboard_data):
    merged_data = []
    header = ['token', 'name', 'itemsDonated', 'email', 'timestamp']

    # Loop through Google Sheet data and merge with leaderboard
    for row in google_data[1:]:  # Skip header row
        token = row[3]  # Assuming token is the fourth column in the Google Sheet
        email = row[1]  # Email is in the second column
        timestamp = row[0]  # Timestamp is in the first column
        
        if token in leaderboard_data:
            merged_data.append([token, leaderboard_data[token]['name'], leaderboard_data[token]['itemsDonated'], email, timestamp])
    
    return header, merged_data

# Write merged data to a new CSV
def write_merged_csv(header, merged_data):
    with open("merged_leaderboard.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(merged_data)
    print("Merged CSV created as 'merged_leaderboard.csv'")

def main():
    # Google Sheet information
    spreadsheet_id = '1bIwBP7W8b9opi0miWTHxZjIz0hZJavABiDXWIza4zLs'  # Your actual Google Sheet ID
    range_name = 'Form Responses 1!A:D'  # Adjust the range as needed
    
    # Load data
    google_data = load_google_sheet_data(spreadsheet_id, range_name)
    leaderboard_data = load_leaderboard_data()

    # Merge data
    header, merged_data = merge_data(google_data, leaderboard_data)

    # Write to merged CSV
    write_merged_csv(header, merged_data)

if __name__ == '__main__':
    main()
