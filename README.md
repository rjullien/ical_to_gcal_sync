This script can be used to periodically pull events from grenoble-inp iCal feed and insert them into a selected Google Calendar using the API for that service. 

This module is mainly based on ical_to_gcal_sync open source project, customized for grenoble-inp edt

I'm putting the code here in case it's useful to any grenoble-inp student similarly frustrated with edt slowness and unreadability. Note that it's not particularly polished or well-packaged.

## Using the script

> NOTE: requires Python 3.7+

Some brief instructions:
1. Edit configPhelma.py and set both needed parameters
2. Edit config.py, Set CALENDAR_ID to the ID of the Google Calendar instance you want to insert events into. You can set it to "primary" to use the default main calendar, or create a new secondary calendar (in which case you can find the ID on the settings page, of the form 'longID@group.calendar.google.com').
3. pip install -r requirements.txt
4. Go through the process of registering an app in the Google Calendar API dashboard in order to obtain the necessary API credentials. This process is described at https://developers.google.com/google-apps/calendar/quickstart/python - rename the downloaded file to ical_to_gcal_sync_client_secret.json and place it in the same location as the script. 
5. Run the script. This should trigger the OAuth2 authentication process and prompt you to allow the app you created in step 4 to access your calendars. If successful it should store the credentials in ical_to_gcal_sync.json.
6. Subsequent runs of the script should not require any further interaction unless the credentials are invalidated/changed.
   
   python3 edt_to_gcal_sync_grenoble_inp/ical_to_gcal_sync.py

## Alternative:
The submodule phelma_calendar could be used as a standalone product to produce a filtered ICS and manually import the edt 
into your google calendar.
The following file is generated: ADECalFiltered.ics

   python3 edt_to_gcal_sync_grenoble_inp/phelma_calendar/phelma_calendar.py
