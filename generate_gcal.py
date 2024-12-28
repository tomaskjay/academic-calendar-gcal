import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import re

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'client_secret.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# Create a new Google Calendar
def create_calendar(input_session_year):
    calendar = {
        'summary': f"{input_session_year} Academic Calendar",
        'timeZone': 'America/New_York'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    calendar_id = created_calendar['id']

    # Make the calendar public
    service.acl().insert(calendarId=calendar_id, body={
        'role': 'reader',
        'scope': {'type': 'default'}
    }).execute()

    print(f"Calendar created: {calendar['summary']}")
    print(f"iCal URL: https://calendar.google.com/calendar/ical/{calendar_id}/public/basic.ics")
    return calendar_id

# Scrape and parse the academic calendar
def scrape_academic_calendar(url, session, year):
    target_session = session.upper()
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table')
    table_index = None
    date_column_index = None

    for idx, table in enumerate(tables):
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        if target_session in headers:
            table_index = idx
            for col_idx, header in enumerate(headers):
                if str(year) in header:
                    date_column_index = col_idx
                    break
            if date_column_index is not None:
                break

    if table_index is None or date_column_index is None:
        print(f"No table found for session '{session}' and year '{year}'.")
        return []

    target_table = tables[table_index]
    rows = target_table.find_all('tr')
    events = []

    for row in rows[1:]:
        cells = row.find_all('td')
        if date_column_index < len(cells):
            event_name = cells[0].get_text(strip=True)
            date_text = cells[date_column_index].get_text(strip=True)

            try:
                start_date, end_date = parse_dates(date_text, year)
                events.append({
                    'summary': f"{event_name} - {session} {year}",
                    'start': {'date': start_date.strftime('%Y-%m-%d')},
                    'end': {'date': (end_date + timedelta(days=1)).strftime('%Y-%m-%d')}
                })
                print(f"Found: {event_name} ({start_date} to {end_date})")
            except ValueError as e:
                print(f"Skipping event '{event_name}' due to date parsing error: {e}")

    return events

def parse_dates(date_text, year):
    def extract_year_from_text():
        match = re.search(r'\((\d{4})\)$', date_text)
        return int(match.group(1)) if match else None

    extracted_year = extract_year_from_text()
    if extracted_year:
        year = extracted_year

    date_range_match = re.match(r"(\w+)\s(\d+)[-/](\d+)", date_text)
    single_date_match = re.match(r"(\w+)\s(\d+)", date_text)

    if date_range_match:
        month = date_range_match.group(1)
        start_day = int(date_range_match.group(2))
        end_day = int(date_range_match.group(3))
        start_date = datetime.strptime(f"{month} {start_day} {year}", "%b %d %Y")
        end_date = datetime.strptime(f"{month} {end_day} {year}", "%b %d %Y")
    elif single_date_match:
        month = single_date_match.group(1)
        day = int(single_date_match.group(2))
        start_date = end_date = datetime.strptime(f"{month} {day} {year}", "%b %d %Y")
    else:
        raise ValueError(f"Unrecognized date format: {date_text}")

    return start_date, end_date

def add_events_to_calendar(calendar_id, events):
    for event in events:
        service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Added: {event['summary']} ({event['start']['date']} - {event['end']['date']})")

def main():
    # Prompt user input
    url = "https://case.edu/registrar/dates-deadlines/academic-calendar"
    input_session_year = input("Enter the session and year (e.g., 'Fall 2024'): ").strip()
    session, year = input_session_year.split()
    year = int(year)

    print(f"Scraping academic calendar for: {input_session_year}")
    events = scrape_academic_calendar(url, session, year)

    if not events:
        print("No events found for the specified session and year.")
        return

    calendar_id = create_calendar(input_session_year)
    print(f"Adding {len(events)} events to the calendar...")
    add_events_to_calendar(calendar_id, events)

if __name__ == "__main__":
    main()
