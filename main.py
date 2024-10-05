import csv
import os
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
def load_google_sheet_data(spreadsheet_id, range_name):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values
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
def merge_data(google_data, leaderboard_data):
    merged_data = []
    header = ['token', 'name', 'itemsDonated', 'email', 'timestamp']
    for row in google_data[1:]:
        token = row[3] 
        email = row[1] 
        timestamp = row[0]
        
        if token in leaderboard_data:
            merged_data.append([token, leaderboard_data[token]['name'], leaderboard_data[token]['itemsDonated'], email, timestamp])
    return header, merged_data
def write_merged_csv(header, merged_data):
    with open("merged_leaderboard.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(merged_data)
    print("Merged CSV created as 'merged_leaderboard.csv'")

def main():
    spreadsheet_id = '1bIwBP7W8b9opi0miWTHxZjIz0hZJavABiDXWIza4zLs'
    range_name = 'Form Responses 1!A:D'
    google_data = load_google_sheet_data(spreadsheet_id, range_name)
    leaderboard_data = load_leaderboard_data()
    header, merged_data = merge_data(google_data, leaderboard_data)
    write_merged_csv(header, merged_data)
if __name__ == '__main__':
    main()
