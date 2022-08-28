# imports the configPhelma file from the phelma_calendar directory
from phelma_calendar import configPhelma as cfg

# The iCal feed URL for the events that should be synced to the Google Calendar.
# Note that the syncing is one-way only.
# ICAL_FEED = 'Not used, replaced by phelma calendar if GRENOBLE_INP=True'
ICAL_FEED=cfg.ICAL_FEED
# Option to remove items from the calendar, exemple calendar contains options you are not registered for
SET_TO_REMOVE=cfg.SET_TO_REMOVE

# If FILES is True then ICAL_FEED is the path to a folder full of ics files.
FILES = False

# If GRENOBLE_INP is True then the ical feed is the one for Grenoble INP.
GRENOBLE_INP=True
GRENOBLE_INP_SRC='https://edt.grenoble-inp.fr'

# the ID of the calendar to use for iCal events, should be of the form
# 'ID@group.calendar.google.com', check the calendar settings page to find it.
# (can also be 'primary' to use the default calendar)
# CALENDAR_ID = 'primary'

# must use the OAuth scope that allows write access
SCOPES = 'https://www.googleapis.com/auth/calendar'

# API secret stored in this file
CLIENT_SECRET_FILE = 'ical_to_gcal_sync_client_secret.json'

# Location to store API credentials
CREDENTIAL_PATH = 'ical_to_gcal_sync.pckl'

# Application name for the Google Calendar API
APPLICATION_NAME = 'Phelma calendar'

# File to use for logging output
LOGFILE = 'ical_to_gcal_sync_log.txt'

# Time to pause between successive API calls that may trigger rate-limiting protection
API_SLEEP_TIME = 0.90
   
# Integer value >= 0
# Controls the timespan within which events from ICAL_FEED will be processed 
# by the script. 
# 
# For example, setting a value of 14 would sync all events from the current 
# date+time up to a point 14 days in the future. 
#
# If you want to sync all events available from the feed this is also possible
# by setting the value to 0, *BUT* be aware that due to an API limitation in the 
# icalevents module which prevents an open-ended timespan being used, this will
# actually be equivalent to "all events up to a year from now" (to sync events
# further into the future than that, set a sufficiently high number of days).
ICAL_DAYS_TO_SYNC = 0

# How long we synchronize with Google, do not support 0, a valid nb of day should be set
GCAL_DAYS_TO_SYNC = 29

# Integer value >= 0
# Controls how many days in the past to query/update from Google and the ical source.
# If you want to only worry about today's events and future events, set to 0,
# otherwise set to a positive number (e.g. 30) to include that many days in the past.
# Any events outside of that time-range will be untouched in the Google Calendar.
# If the ical source doesn't include historical events, then this will mean deleting
# a rolling number of days historical calendar entries from Google Calendar as the script
# runs
PAST_DAYS_TO_SYNC = 0