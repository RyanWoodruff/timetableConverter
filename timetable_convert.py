from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
service = None


def get_timetable_input():
    valid_timetable = False
    while (not valid_timetable):
        timetable = input("Enter URL to your timetable: ")
        if (timetable.startswith('http://timetable.leeds.ac.uk') or timetable.startswith('https://timetable.leeds.ac.uk')):
            valid_timetable = True
        else:
            print('Please enter a valid timetable URL (link begins with timetable.leeds.ac.uk)')

    return timetable
    
def get_module_input():
    

def scrape_timetable(timetable_link):
    page = requests.get(timetable_link)
    content = page.content
    # Events stored as an array of dictionaries
    soup = BeautifulSoup(content)
    events = []

    for event in soup.findAll('td', attrs={'class':'object-cell-border'}):
        print("====================New Event====================")
        print(event)


def add_event():
    ## Construct the event

    # event = {
    # 'summary': 'Google I/O 2015',
    # 'location': '800 Howard St., San Francisco, CA 94103',
    # 'description': 'A chance to hear more about Google\'s developer products.',
    # 'start': {
    #     'dateTime': '2015-05-28T09:00:00-07:00',
    #     'timeZone': 'America/Los_Angeles',
    # },
    # 'end': {
    #     'dateTime': '2015-05-28T17:00:00-07:00',
    #     'timeZone': 'America/Los_Angeles',
    # },
    # 'recurrence': [
    #     'RRULE:FREQ=DAILY;COUNT=2'
    # ],
    # 'attendees': [
    #     {'email': 'lpage@example.com'},
    #     {'email': 'sbrin@example.com'},
    # ],
    # 'reminders': {
    #     'useDefault': False,
    #     'overrides': [
    #     {'method': 'email', 'minutes': 24 * 60},
    #     {'method': 'popup', 'minutes': 10},
    #     ],
    # },
    # }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service
    service = build('calendar', 'v3', credentials=creds)
    if not service:
        print("Service is null, exiting")
        exit()
    


    # Get the calendar input
    timetable_link = get_timetable_input()
    module_name_link = get_module_input()
    timetable = scrape_timetable(timetable_link)
    # Call the Calendar API
    # add_event()


if __name__ == '__main__':
    main()