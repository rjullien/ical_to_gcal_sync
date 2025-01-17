# Behind a few PR, TBD:
# Added support for multiple calendars in the same config file:
# this one is complex to merge:
# https://github.com/rjullien/edt_to_gcal_sync_grenoble_inp/commit/22cdb78da987c5604d5ef622fe4421f9974a092f
# https://github.com/rjullien/edt_to_gcal_sync_grenoble_inp/commit/ea6955886532a888f22f51e104d3434d8ae4ad82
# https://github.com/rjullien/edt_to_gcal_sync_grenoble_inp/commit/d94fa009145182fe3fe75721efda2acd17bb19f8

#
# Modif for ENAC: begin -> start, name -> summary

from __future__ import print_function

import logging
import time
import string
import re
import sys
import os

from ics import Calendar, Event
import requests
import os
from pathlib import Path

import googleapiclient
import arrow
from googleapiclient import errors
from icalevents.icalevents import events
import socket
from dateutil.tz import gettz

from datetime import datetime, timezone, timedelta

from auth import auth_with_calendar_api
from pathlib import Path
from httplib2 import Http

config = {}
config_path=os.environ.get('CONFIG_PATH', 'config.py')
exec(Path(config_path).read_text(), config)

def get_phelma_calendar(url):
    # Read grenoble-inp agenda
    c = Calendar()
    c = Calendar(requests.get(url).text)

    # create the list of events to be filtered out from the one read previously
    eventOut=c.events.copy()

    # for each event, if it matches the filter out rule, remove them from the event list
    for EventEdt in c.events:
        for (f1,f2) in config['SET_TO_REMOVE']:
            # test if EventEdt.name exits
            if hasattr(EventEdt,'name'):
                if(EventEdt.name.find(f1)!=-1): # If it matches a candidate topic
                    if(EventEdt.description.find(f2)==-1): # Check if the group in the description <> from my group
    #                     print("Remove "+EventEdt.name + " Desc: " + EventEdt.description)
                        # try to remove the event from the list
                        try:
                            eventOut.remove(EventEdt)   # remove the event from the list
                        except:
                            print("Error: Cannot remove this Event: "+EventEdt.name+ " Desc: " + EventEdt.description)
            else:
                print("Error: No name for event: ")
                print(EventEdt)
                              
    # print(str(eventOut))
    return eventOut

def filter_out_useless_items (eventIn):
    # create the list of events to be filtered out from the one recived in input 
    eventOut=eventIn.copy()

    # for each event, if it matches the filter out rule, remove them from the event list
    for EventEdt in eventIn:
        for (f1,f2) in config['SET_TO_REMOVE']:
            # test if EventEdt.summary exits
            if hasattr(EventEdt,'summary'):
                if(EventEdt.summary.find(f1)!=-1): # If it matches a candidate topic
                    if(EventEdt.description.find(f2)==-1): # Check if the group in the description <> from my group
                        logger.info("> Remove "+EventEdt.summary + " Desc: " + EventEdt.description)
                        #print("Remove "+EventEdt.summary + " Desc: " + EventEdt.description)
                        # try to remove the event from the list
                        try:
                            eventOut.remove(EventEdt)   # remove the event from the list
                        except:
                            logger.error("> Error: Cannot remove this Event: "+EventEdt.summary + " Desc: " + EventEdt.description)
                            #print("Error: Cannot remove this Event: "+EventEdt.summary+ " Desc: " + EventEdt.description)
            else:
                #logger.error(">Error:  No summary for event:"+EventEdt)
                print("Error: No summary for event: ")
                print(EventEdt)
                              
    # print(str(eventOut))
    return eventOut

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if config.get('LOGFILE', None):
    handler = logging.FileHandler(filename=config['LOGFILE'], mode='a')
else:
    handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(asctime)s|[%(levelname)s] %(message)s'))
logger.addHandler(handler)

DEFAULT_TIMEDELTA = timedelta(days=365)

import fileinput
import os

def patch_ics_files(directory):
    """
    Patch all .ics files in the specified directory by replacing the X-WR-TIMEZONE property
    with a standard timezone definition.
    """
    # Specify the replacement value for X-WR-TIMEZONE
    replacement = """BEGIN:VTIMEZONE
TZID:Europe/Paris
BEGIN:STANDARD
DTSTART:19710101T030000
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
END:STANDARD
END:VTIMEZONE"""

    # Loop over each file in the directory
    for filename in os.listdir(directory):
        # Check that the file has a .ics extension
        if filename.endswith('.ics'):
            # Open the file for in-place editing
            with fileinput.FileInput(os.path.join(directory, filename), inplace=True) as file:
                # Loop over each line in the file
                for line in file:
                    # Replace the X-WR-TIMEZONE property with the replacement value
                    if line.startswith('X-WR-TIMEZONE:'):
                        print(replacement)
                    else:
                        print(line, end='')

def get_current_events_from_files(path):
    
    """Retrieves data from iCal files.  Assumes that the files are all 
    *.ics files located in a single directory.

        Returns the parsed Calendar object of None if no events are found.

    """

    from glob import glob
    from os.path import join

    event_ics = glob(join(path, '*.ics'))

    logger.debug('> Found {} local .ics files in {}'.format(len(event_ics), join(path, '*.ics')))
    if len(event_ics) > 0:
        ics = event_ics[0]
        logger.debug('> Loading file {}'.format(ics))
        cal = get_current_events(feed_url_or_path=ics, files=True)
        logger.debug('> Found {} new events'.format(len(cal)))
        for ics in event_ics[1:]:
            logger.debug('> Loading file {}'.format(ics))
            evt = get_current_events(feed_url_or_path=ics, files=True)
            if len(evt) > 0:
                cal.extend(evt)
            logger.debug('> Found {} new events'.format(len(evt)))
        return cal
    else:
        logger.error('No ics files found')
        return None

def get_current_events(feed_url_or_path, files):
    """Retrieves data from iCal iCal feed and returns an ics.Calendar object 
    containing the parsed data.

    Returns the parsed Calendar object or None if an error occurs.
    """

    events_end = datetime.now()
    # Subtract the number of days to sync
    past_date = datetime.now() - timedelta(days=config.get('PAST_DAYS_TO_SYNC', 0))

    # Set the time to 7 am to avoiid removing items of today
    past_date = past_date.replace(hour=7, minute=0, second=0, microsecond=0)
    #print("past_date: ", past_date)
    
    if config.get('ICAL_DAYS_TO_SYNC', 0) == 0:
        # default to 1 year ahead
        events_end += DEFAULT_TIMEDELTA
    else:
        # add on a number of days
        events_end += timedelta(days=config['ICAL_DAYS_TO_SYNC'])

    try:
        if files:
            logger.info(f"> Retrieving events from local folder: {feed_url_or_path}")
            cal = events(file=feed_url_or_path, start=past_date, end=events_end)
        else:
            logger.info('> Retrieving events from iCal feed')
            # directly configure http connection object to set ssl and authentication parameters
            http_conn = Http(disable_ssl_certificate_validation=not config.get('ICAL_FEED_VERIFY_SSL_CERT', True))

            if config.get('ICAL_FEED_USER') and config.get('ICAL_FEED_PASS'):
                # credentials used for every connection
                http_conn.add_credentials(name=config.get('ICAL_FEED_USER'), password=config.get('ICAL_FEED_PASS'))
            cal = events(feed_url_or_path, start=past_date, end=events_end, http=http_conn)
    except Exception as e:
        logger.error('> Error retrieving iCal data ({})'.format(e))
        return None

    return cal

def get_gcal_events(calendar_id, service, from_time, to_time):
    """Retrieves the current set of Google Calendar events from the selected
    user calendar. Only includes upcoming events (those taking place from start
    of the current day. 

    Returns a dict containing the event(s) existing in the calendar.
    """

    # The list() method returns a dict containing various metadata along with the actual calendar entries (if any). 
    # It is not guaranteed to return all available events in a single call, and so may need called multiple times
    # until it indicates no more events are available, signalled by the absence of "nextPageToken" in the result dict

    logger.debug('Retrieving Google Calendar events')

    # make an initial call, if this returns all events we don't need to do anything else,,,
    events_result = service.events().list(calendarId=calendar_id,
                                         timeMin=from_time, 
                                         timeMax=to_time,
                                         singleEvents=True, 
                                         orderBy='startTime', 
                                         showDeleted=True).execute()

    events = events_result.get('items', [])
    # if nextPageToken is NOT in the dict, this should be everything
    if 'nextPageToken' not in events_result:
        logger.info('> Found {:d} upcoming events in Google Calendar (single page)'.format(len(events)))
        return events

    # otherwise keep calling the method, passing back the nextPageToken each time
    while 'nextPageToken' in events_result:
        token = events_result['nextPageToken']
        events_result = service.events().list(calendarId=calendar_id,
                                             timeMin=from_time, 
                                             timeMax=to_time,
                                             pageToken=token, 
                                             singleEvents=True, 
                                             orderBy='startTime', 
                                             showDeleted=True).execute()
        newevents = events_result.get('items', [])
        events.extend(newevents)
        logger.debug('> Found {:d} events on new page, {:d} total'.format(len(newevents), len(events)))
    
    logger.info('> Found {:d} upcoming events in Google Calendar (multi page)'.format(len(events)))
    
    return events

def delete_all_events(service):
    for gc in get_gcal_events(service):
        try:
            service.events().delete(calendarId=config['CALENDAR_ID'],eventId=gc['id']).execute()
            time.sleep(config['API_SLEEP_TIME'])
        except googleapiclient.errors.HttpError:
            pass # event already marked as deleted

def get_gcal_datetime(py_datetime, gcal_timezone):
    py_datetime = py_datetime.astimezone(gettz(gcal_timezone))
    return {u'dateTime': py_datetime.strftime('%Y-%m-%dT%H:%M:%S%z'), 'timeZone': gcal_timezone}

def get_gcal_date(py_datetime):
    return {u'date': py_datetime.strftime('%Y-%m-%d')}

def ics_color(title):
    """
    Returns the colorId to use for the event based on the title of the event

    Color ID	Color Name	Hex Code
    1	Lavender	#7986cb
    2	Sage	#33b679
    3	Grape	#8e24aa
    4	Flamingo	#e67c73
    5	Banana	#f0e68c
    6	Teal	#138d75
    7	Sky	#82b1ff
    8	Grapefruit	#ff8f00
    9	Sandstone	#d97d52
    10	Blueberry	#5978bb
    11	Raspberry	#e91e63
    12	Mint	#a6ffcc
    13	Olive	#a2cf6e
    14	Pumpkin	#ff7c4d
    15	Apricot	#ffbf8f
    16	Sky Blue	#87cefa
    """
    # test if color_ics_dict exits
    if color_ics_dict is not None:
        # test if the name of the event is in the dictionary
        for title_color in color_ics_dict.keys():
            if title_color.lower() in title.lower():
                #print(title_color + " is in " + title.lower())
                # return the color ID corresponding to the title
                return color_ics_dict[title_color]
    # return the default color ID
    return 0

def create_id(uid, begintime, endtime, prefix=''):
    """ Converts ical UUID, begin and endtime to a valid Gcal ID

    Characters allowed in the ID are those used in base32hex encoding, i.e. lowercase letters a-v and digits 0-9, see section 3.1.2 in RFC2938
    Te length of the ID must be between 5 and 1024 characters
    https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html

    Returns:
        ID
    """
    allowed_chars = string.ascii_lowercase[:22] + string.digits
    return prefix + re.sub('[^{}]'.format(allowed_chars), '', uid.lower()) + str(arrow.get(begintime).int_timestamp) + str(arrow.get(endtime).int_timestamp)
if __name__ == '__main__':
    mandatory_configs = ['CREDENTIAL_PATH', 'ICAL_FEEDS', 'APPLICATION_NAME']
    for mandatory in mandatory_configs:
        if not config.get(mandatory) or config[mandatory][0] == '<':
            logger.error("Must specify a non-blank value for %s in the config file" % mandatory)
            sys.exit(1)

    # setting up Google Calendar API for use
    logger.debug('> Loading credentials')
    service = auth_with_calendar_api(config)

    # dateime instance representing the start of the current day (UTC)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    for feed in config.get('ICAL_FEEDS'):
        logger.info('> Processing source %s' % feed['source'])
    
    # dateime instance representing the max to synchonize
    maxday =  today + timedelta(days=config['GCAL_DAYS_TO_SYNC'])
   
    # retrieve events from Google Calendar, starting from beginning of current day
    logger.info(f'> Retrieving events from Google Calendar from %s to %s for destination %s' % (today.isoformat()[:10], maxday.isoformat()[:10],feed['destination']))
    logger.info(f'> Retrieving events from Google Calendar from %s to %s for destination %s' % (today-timedelta(days=config.get('PAST_DAYS_TO_SYNC', 0)).isoformat()[:10], maxday.isoformat()[:10],feed['destination']))

  
    try:
        gcal_events = get_gcal_events(calendar_id=feed['destination'], service=service, from_time=(today-timedelta(days=config.get('PAST_DAYS_TO_SYNC', 0))).isoformat(), to_time=maxday.isoformat())
    except socket.timeout:
        print("La requête get_gcal_events a expiré. Veuillez vérifier votre connexion réseau et réessayer.")
        logger.error("La requête get_gcal_events a expiré. Veuillez vérifier votre connexion réseau et réessayer.")
        exit(1)
    # retrieve events from the iCal feed
    # logger.info('> Retrieving events from iCal feed')
    # ical_cal = get_current_events()
    if config['GRENOBLE_INP']:
        logger.info('> Retrieving events from iCal feed using get_phelma_calendar module')
        ical_cal = get_phelma_calendar(feed['source'])
    else:
         if feed['files']: # Used for ENAC
            if feed.get('school') == "ENAC":
                from enac import get_enac_ics
                logger.info('Retrieving events from enac website')
                month_to_sync = int(config['GCAL_DAYS_TO_SYNC']) // 30
                logger.info(f"get_enac_ics('{feed['download']}' ,'{feed['source']}', '{feed['url']}', '{config['ICAL_FEED_USER']}', '{config['ICAL_FEED_PASS']}', {month_to_sync})")
                #print(f"get_enac_ics('{feed['download']}' ,'{feed['source']}', '{feed['url']}', '{config['ICAL_FEED_USER']}', '{config['ICAL_FEED_PASS']}', {month_to_sync})")
                get_enac_ics(feed['download'],feed['source'],feed['url'],config['ICAL_FEED_USER'],config['ICAL_FEED_PASS'],month_to_sync) # get ics files from enac website
                # Should use credentials to get ics files from config['ICAL_FEED_USER'] and config['ICAL_FEED_PASS'] and config['ICAL_FEED_URL'] and config['GCAL_DAYS_TO_SYNC']/30
                # ICAL_FEED_USER = None
                # ICAL_FEED_PASS = None
                logger.info('patch timezone of ics files')
                patch_ics_files(feed['source']) # patch timezone of ics files

            logger.info(f"> Retrieving events from local folder: {feed['source']}")
            eventIn = get_current_events_from_files(feed['source'])
            logger.info('> Filtering out events from iCal feed')
            ical_cal = filter_out_useless_items (eventIn)
         else:
            logger.info('> Retrieving events from iCal feed')
            eventIn = get_current_events(feed_url_or_path=feed['source'], files=False)
            logger.info('> Filtering out events from iCal feed')
            ical_cal = filter_out_useless_items (eventIn)

    if ical_cal is None:
        logger.error('> Error retrieving iCal data: ical_cal is None"')
        sys.exit(-1)

    # convert iCal event list into a dict indexed by (converted) iCal UID
    ical_events = {}

    for ev in ical_cal:
        # explicitly set any events with no timezone to use UTC (icalevents
        # doesn't seem to do this automatically like ics.py)

        if ev.start.tzinfo is None:
            print("ev.start.tzinfo is None")
            ev.start = ev.start.replace(tzinfo=timezone.utc)
        if ev.end is not None and ev.end.tzinfo is None:
            ev.end = ev.end.replace(tzinfo=timezone.utc)
            print("ev.end is not None and ev.end.tzinfo is None")
            try:
                if 'EVENT_PREPROCESSOR' in config:
                    keep = config['EVENT_PREPROCESSOR'](ev)
                    if not keep:
                        logger.debug("Skipping event %s - EVENT_PREPROCESSOR returned false" % (str(ev)))
                        continue

            except Exception as ex:
                logger.error("Error processing entry (%s) - leaving as-is" % str(ev))

        ical_events[create_id(ev.uid, ev.start, ev.end, config.get('EVENT_ID_PREFIX', ''))] = ev

    logger.debug('> Collected {:d} iCal events'.format(len(ical_events)))
   
    # retrieve the Google Calendar object itself
    gcal_cal = service.calendars().get(calendarId=feed['destination']).execute()

    logger.info('> Processing Google Calendar events...')
    gcal_event_ids = [ev['id'] for ev in gcal_events]

    # first check the set of Google Calendar events against the list of iCal
    # events. Any events in Google Calendar that are no longer in iCal feed
    # get deleted. Any events still present but with changed start/end times
    # get updated.
    for gcal_event in gcal_events:
        eid = gcal_event['id']

        if eid not in ical_events:
            # if a gcal event has been deleted from iCal, also delete it from gcal.
            # Apparently calling delete() only marks an event as "deleted" but doesn't
            # remove it from the calendar, so it will continue to stick around. 
            # If you keep seeing messages about events being deleted here, you can
            # try going to the Google Calendar site, opening the options menu for 
            # your calendar, selecting "View bin" and then clicking "Empty bin 
            # now" to completely delete these events.
            try:
                # already marked as deleted, so it's in the "trash" or "bin"
                if gcal_event['status'] == 'cancelled': continue

                logger.info(u'> Deleting event "{}" from Google Calendar...'.format(gcal_event.get('summary', '<unnamed event>')))
                service.events().delete(calendarId=feed['destination'], eventId=eid).execute()
                time.sleep(config['API_SLEEP_TIME'])
            except googleapiclient.errors.HttpError:
                pass # event already marked as deleted
        else:
            ical_event = ical_events[eid]
            gcal_begin = arrow.get(gcal_event['start'].get('dateTime', gcal_event['start'].get('date')))
            gcal_end = arrow.get(gcal_event['end'].get('dateTime', gcal_event['end'].get('date')))

            gcal_has_location = bool(gcal_event.get('location'))
            ical_has_location = bool(ical_event.location)

            gcal_has_description = 'description' in gcal_event
            ical_has_description = ical_event.description is not None

            # event name can be left unset, in which case there's no summary field
            gcal_name = gcal_event.get('summary', None)
            log_name = '<unnamed event>' if gcal_name is None else gcal_name

            times_differ = gcal_begin != ical_event.start or gcal_end != ical_event.end
            titles_differ = gcal_name != ical_event.summary

            #locs_differ = gcal_has_location != ical_has_location and gcal_event.get('location') != ical_event.location

            locs_differ = ((gcal_has_location and ical_has_location) and gcal_event.get('location') != ical_event.location) or (gcal_has_location and not ical_has_location) or (not gcal_has_location and ical_has_location)

            # test if locs_differ:
            # trace if location is different
            if locs_differ:
                print("gcal_has_location: " + str(gcal_has_location) + " -- " + str(ical_has_location) + "--"  + str(gcal_event.get('location')) + " -- " + str(ical_event.location))

            descs_differ = gcal_has_description != ical_has_description and (gcal_event.get('description') != ical_event.description)
            
            needs_undelete = config.get('RESTORE_DELETED_EVENTS', False) and gcal_event['status'] == 'cancelled'
            
            changes = []
            if times_differ: changes.append("begin/end times")
            if titles_differ: changes.append("name")
            if locs_differ: changes.append("locations")
            if descs_differ: changes.append("descriptions")
            if needs_undelete: changes.append("undeleted")

            try:
                color_ics_dict = config['COLOR_ICS_DICT']
            except KeyError:
                print("No COLOR_ICS_DICT in config.py")
                color_ics_dict = None
            # appel fonction color
            color_id = ics_color(gcal_event['summary'])

            gcal_color = gcal_event.get('colorId')

            if(gcal_color is None):
                gcal_color = 0
            else:
                gcal_color = int(gcal_color)
            if color_id != gcal_color:
                #print("color_id: " + str(color_id) + " gcal_color: " + str(gcal_color))
                color_differ = True
            else:
                color_differ = False

            # check if the iCal event has a different: start/end time, name, location,
            # or description, and if so sync the changes to the GCal event
            if needs_undelete or times_differ or titles_differ or locs_differ or descs_differ or color_differ:  
                print('updating due to change: undelete:'+ str(needs_undelete) + " times:" + str(times_differ) + " title:" + str(titles_differ) + " loc:" + str(locs_differ) + " desc:" + str(descs_differ)+" color:" + str(color_differ))
                logger.info(u'> Updating event "{}" due to changes: {}'.format(log_name, ", ".join(changes)))
                delta = ical_event.end - ical_event.start
                # all-day events handled slightly differently
                # TODO multi-day events?
                if delta.days >= 1:
                    gcal_event['start'] = get_gcal_date(ical_event.start)
                    gcal_event['end'] = get_gcal_date(ical_event.end)
                else:
                    gcal_event['start'] = get_gcal_datetime(ical_event.start, gcal_cal['timeZone'])
                    if ical_event.end is not None:
                        gcal_event['end']   = get_gcal_datetime(ical_event.end, gcal_cal['timeZone'])

                logger.info('Adding iCal event called "{}", starting {}'.format(ical_event.summary, gcal_event['start']))
                # if the event was deleted, the status will be 'cancelled' - this restores it
                gcal_event['status'] = 'confirmed'
                gcal_event['summary'] = ical_event.summary
                gcal_event['description'] = ical_event.description

                if config['GRENOBLE_INP']:
                    url_feed=config['GRENOBLE_INP_SRC']
                else:
                    if feed['files']:
                        url_feed = 'https://events.from.ics.files.com' 
                    else:
                        url_feed = feed['source']
                gcal_event['source'] = {'title': 'Imported from ical_to_gcal_sync.py', 'url': url_feed}
                gcal_event['location'] = ical_event.location

                # set the color of the event
                if color_differ:
                    gcal_event['colorId'] = color_id

                service.events().update(calendarId=feed['destination'], eventId=eid, body=gcal_event).execute()
                time.sleep(config['API_SLEEP_TIME'])
            else:
                logger.info(u'> skipping event "{}" no changes: {}'.format(log_name, ", ".join(changes)))

    # now add any iCal events not already in the Google Calendar 
    logger.info('> Processing iCal events...')
    for ical_id, ical_event in ical_events.items():
        if ical_id not in gcal_event_ids:
            gcal_event = {}
            gcal_event['summary'] = ical_event.summary
            gcal_event['id'] = ical_id
            gcal_event['description'] = ical_event.description
            if config['GRENOBLE_INP']:
                url_feed=config['GRENOBLE_INP_SRC']
            else: 
                if feed['files']:
                    url_feed = 'https://events.from.ics.files.com'
                else:
                    url_feed = feed['source']
            gcal_event['source'] = {'title': 'Imported from ical_to_gcal_sync.py', 'url': url_feed}

            gcal_event['location'] = ical_event.location


            # check if no time specified in iCal, treat as all day event if so
            delta = ical_event.end - ical_event.start
            # TODO multi-day events?
            if delta.days >= 1:
                gcal_event['start'] = get_gcal_date(ical_event.start)
                logger.info(u'iCal all-day event {} to be added at {}'.format(ical_event.summary, ical_event.start))
                if ical_event.end is not None:
                    gcal_event['end'] = get_gcal_date(ical_event.end)
            else:
                gcal_event['start'] = get_gcal_datetime(ical_event.start, gcal_cal['timeZone'])
                logger.info(u'iCal event {} to be added at {}'.format(ical_event.summary, ical_event.start))
                if ical_event.end is not None:
                    gcal_event['end'] = get_gcal_datetime(ical_event.end, gcal_cal['timeZone'])
            logger.info('Adding iCal event called "{}", starting {}'.format(ical_event.summary, gcal_event['start']))

            try:
                time.sleep(config['API_SLEEP_TIME'])
                service.events().insert(calendarId=feed['destination'], body=gcal_event).execute()
            except Exception:
                time.sleep(config['API_SLEEP_TIME'])
                try:
                    service.events().update(calendarId=feed['destination'], eventId=gcal_event['id'], body=gcal_event).execute()
                except Exception as ex:
                    # print("Item skiped - ERROR: "+ str(gcal_event['id']) + " body: " + str(gcal_event))
                    logger.info("Item skiped - ERROR: "+ str(gcal_event['id']) + " body: " + str(gcal_event))
                    logger.error("Error updating: %s (%s)" % ( gcal_event['id'], ex ) )

    logger.info('> Processing of source %s completed' % feed['source'])
