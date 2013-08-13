# Pycal
This code is the result of playing around with Python and the Google Calendar API. 

__This code is for learning purposes and is NOT production ready.__

## Notes
Remember to add client_secrets.json (instructions in gcal.py).

The form could be switched from simple HTML form to [WTForms](http://flask.pocoo.org/docs/patterns/wtforms/).

## This test app needs to:
  - collect the users phone number, time
  - know not to double-schedule
  - ask for the user's name
  - track the user's email
  - send an email to <company_email> about the scheduled call
  - add the event to owner's cal
  - integrated into our website