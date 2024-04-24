from datetime import datetime, timedelta, date
import requests
from bs4 import BeautifulSoup

def get_week_start():
    today = date.today()
    days_until_next_week = 7 - today.weekday()
    next_week_start = today + timedelta(days=days_until_next_week)
    return next_week_start

def fetch_timetable(week, intake, intake_group):
    respone = requests.get(f'https://api.apiit.edu.my/timetable-print/index.php?Week={week}&Intake={intake}&Intake_Group={intake_group}&print_request=print_tt')
    soup = BeautifulSoup(respone.text, features="html")
    return soup.find('table', class_='table')

def main():
    intake = "APU3F2402CS(AI)"
    intake_group = "G1"
    remove_module = ['ALG'] #filter
    week_start = get_week_start()

    timetable_table = (fetch_timetable(week_start, intake, intake_group))

    if timetable_table:
        timetable_data = []
        rows = timetable_table.find_all('tr')[2:]

        if rows:
            for row in rows:
                cells = row.find_all('td')

                date = cells[0].text.strip()
                time = cells[1].text.strip()
                classroom = cells[2].text.strip()
                location = cells[3].text.strip()
                subject = cells[4].text.strip()
                lecturer = cells[5].text.strip()

                module_name = subject.split('-')[2]

                if module_name not in remove_module:
                    timetable_data.append({
                        'Date' : date,
                        'Time' : time,
                        'Classroom' : classroom,
                        'Location' : location,
                        'Subject/Module' : subject,
                        'Lecturer' : lecturer
                    })

print(fetch_timetable(get_week_start(), "APU3F2402CS(AI)", "G1"))
