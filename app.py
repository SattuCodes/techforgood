import csv
from datetime import datetime
import os

def inp():
    n = input("Name: ")
    c = input("Class with section: ")
    items = input("Number of items donated: ")
    return n, c, items

def get_next_suffix():
    if not os.path.exists("suffix_tracker.txt"):
        with open("suffix_tracker.txt", "w") as f:
            f.write("00")

    with open("suffix_tracker.txt", "r+") as f:
        last_suffix = f.read().strip()
        next_suffix = int(last_suffix) + 1
        next_suffix_str = f"{next_suffix:02d}"
        f.seek(0)
        f.write(next_suffix_str)
    
    return last_suffix

def generate_token():
    date_str = datetime.now().strftime("%d%m%y")
    suffix = get_next_suffix()
    token = date_str + suffix
    return token

def csvv():
    headings = ['name', 'class', 'section', 'itemsDonated', 'token']
    file_exists = os.path.exists("leaderboard.csv")
    
    with open("leaderboard.csv", "a+", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headings)
        
        name, class_section, items = inp()
        token = generate_token()
        writer.writerow([name, class_section.split()[0], class_section.split()[1], items, token])
        print("Your token is: ", token)

csvv()
