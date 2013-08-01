import datetime
import gcal

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def view_calendar():
  # Use current_time to pull events happening in the future
  now = datetime.datetime.now()
  min_time = now.strftime(gcal.TIME_FORMAT)

  # Use max_time to look at events happening in the next 2 weeks
  two_weeks_from_now = now + datetime.timedelta(days=14)
  max_time = two_weeks_from_now.strftime(gcal.TIME_FORMAT)
  
  events = gcal.list_events(min_time, max_time)
  return render_template('schedule.html', event_list=events)


@app.route('/new', methods=['POST'])
def new_event():
  gcal.create_event(request.form['summary'], request.form['name'], 
    request.form['tel'], request.form['email'], request.form['start-time'])
  return redirect('/')


if __name__ == '__main__':
  # Enable server to reload on code changes
  # You can also add '$ assert False' to debug
  app.debug = True 
  app.run()
