import httplib2
import datetime

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

CLIENT_SECRETS = 'client_secrets.json'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S-04:00'

# Set up a Flow object to be used for authentication.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message="MISSING_CLIENT_SECRETS")


def authenticate_google_calendar():
  # If the Credentials don't exist or are invalid, run through the native
  # client flow. The Storage object will ensure that if successful the good
  # Credentials will get written back to a file.
  storage = Storage('sample.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  return build('calendar', 'v3', http=http)


def list_events():
  service = authenticate_google_calendar()
  upcoming_events = []

  # Use current_time to pull events happening in the future
  # We're using EST (-4:00 hours)
  now = datetime.datetime.now()
  current_time = now.strftime(TIME_FORMAT)

  # Use max_time to look at events happening in the next 2 weeks
  two_weeks_from_now = now + datetime.timedelta(days=14)
  max_time = two_weeks_from_now.strftime(TIME_FORMAT)
  print max_time

  # Parameters definition
  ## calendarId='primary' - Look at the primary calendar for the authenticated user
  ## orderBy='startTime'  - Order events listed by start_time
  ## singleEvents='False' - Expand recurring events into instances to see when each recurrence happens
  ## timeMin=current_time - Use current_time as lower bound (only pull events happening in the future)
  ## timeMax=max_time     - Use max_time as upper bound (only look 2 weeks ahead in the calendar)
  ## pageToken=page_token - Token specifying which result page to return

  page_token = None
  while True:
    events = service.events().list(calendarId='primary', orderBy='startTime', singleEvents='False', timeMin=current_time, timeMax=max_time, pageToken=page_token).execute()
    for event in events['items']:
      upcoming_events.append([event['summary'], event['start'], event['end']])
    page_token = events.get('nextPageToken')
    if not page_token:
      break
  return upcoming_events


# check to make sure timeslot is available prior to scheduling new event
def check_time_availability(start_time, end_time):
  service = authenticate_google_calendar()


def create_event(summary, name, tel, email, start_time):
  # Ensure necessary fields are passed
  if summary == '' or name == '' or tel == '' or email == '' or start_time == '':
    print "You're missing a field"
    return

  service = authenticate_google_calendar()
  full_description = 'Call %s at %s. Email: %s' % (name, tel, email)

  # Format start time. Expected input = YYYY-MM-DD HH:MM
  formatted_start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M').strftime(TIME_FORMAT)
  
  # Calculate end time by adding 30 minutes to start time.
  end_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M') + datetime.timedelta(minutes=30)
  formatted_end_time = end_time.strftime(TIME_FORMAT)

  event = {
    'summary': summary,
    'description': full_description,
    'location': 'Phone',
    'start': {
      'dateTime': formatted_start_time
    },
    'end': {
      'dateTime': formatted_end_time
    }
  }

  # Create the event
  service.events().insert(calendarId='primary', body=event).execute()


@app.route('/')
def view_calendar():
  events = list_events()
  return render_template('schedule.html', event_list=events)


@app.route('/new', methods=['POST'])
def new_event():
  create_event(request.form['summary'], request.form['name'], 
    request.form['tel'], request.form['email'], request.form['start-time'])
  return redirect('/')


if __name__ == '__main__':
  # Enable server to reload on code changes
  # You can also add '$ assert False' to debug
  app.debug = True 
  app.run()
