from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def is_class(ev_summary):
    return (("Methodo" in ev_summary) or
                ("111" in ev_summary) or
                ("121" in ev_summary) or
                ("122" in ev_summary) or
                ("222" in ev_summary) or
                ("MTU" in ev_summary) or
                ("4.2" in ev_summary) or
                ("TP" in ev_summary))


#Thanks http://mvsourcecode.com/python-how-to-get-date-range-from-week-number-mvsourcecode/
def get_first_day(p_week):
    p_year = 2021
    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek

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

    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime(2021, 1, 1).isoformat()+'Z'
    idip_id = "qeu13lrte853qa6vh7mq4e057g@group.calendar.google.com"
    events_result = service.events().list(calendarId=idip_id, timeMin=now,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    classes = [i for i in events if is_class(i['summary'])]
    res = []
    if not events:
        print('No upcoming events found.')
    for event in classes:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['start'].get('date'))
        res.append({"start":start,"end":end,"id":event["summary"]})
    with open('cours.pkl', 'wb') as f:
        pickle.dump(res, f)
    return res

def get_date(c):
      # 2020-09-25T14:30:00+02:00
    c = c[:-6]
    s = "%Y-%m-%dT%H:%M:%S"
    return datetime.datetime.strptime(c,s)

def agregate_data(class_list,is_test=False):
    res = {}
    if is_test :
        class_list = class_list[:3]
    for c in class_list:
        start = get_date(c["start"])
        end = get_date(c["end"])
        week = start.isocalendar()[1]+1
        duration = end - start
        if week in res.keys():
                res[week] = res[week] + duration
        else:
            res[week] = duration
    l = sorted(res.keys())
    for k in l:
        d = str(get_first_day(k).strftime("%d %b"))
        print(d+" : " + str(round(res[k].total_seconds()/3600)) + " heures")
    total = sum([round(i.total_seconds()/3600.0) for i in res.values()])
    print("Total : "+ str(total)+" heures")
    print("Moyenne hebdo : "+str(round(total/len(l),1)))

if __name__ == '__main__':
    list = None
    list = main()
    #with open('cours.pkl', 'rb') as f:
    #    list = pickle.load(f)
    agregate_data(list)
