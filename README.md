This script can be used to periodically pull events from grenoble-inp iCal feed and insert them into a selected Google Calendar using the API for that service. 

This module is mainly based on ical_to_gcal_sync open source project, customized for grenoble-inp edt

I'm putting the code here in case it's useful to any grenoble-inp student similarly frustrated with edt slowness and unreadability. Note that it's not particularly polished or well-packaged.

## Using the script

> NOTE: requires Python 3.7+

Some brief instructions:
0. Edit configPhelma.py and set both needed parameters
   NB: the config file in root directory must start by config and the config file in the phelma_calendar directory must start by configPhelma. Any identical suffix is allowed, could also be empty.
1. Copy `config.py.example` to a new file `config.py` or a custom file (see *Multiple Configurations* below)
2. Modify the value of `ICAL_FEEDS` to configure your calendars. It should contain a list with one or more entries where each entry is a dict with the following structure:
```python
ICAL_FEEDS = [
    {
        # source of calendar events. normally this is an iCal feed URL, but you can also use a local path
        # containing .ics files as a data source instead (in that case set 'files' to True)
        'source': '<ICAL URL OR DIRECTORY PATH>',
        # the ID of the Google calendar to insert events into. this can be "primary" if you want to use the
        # default main calendar, or a 'longID@group.calendar.google.com' string for secondary calendars. You
        # can find the long calendar ID on its settings page.
        'destination': '<GOOGLE CAL ID>',
        # set to False if source is a URL, True if it's a local path
        'files': False,
    },
]
```
3. If your iCal feed is password protected you should also set the variables `ICAL_FEED_USER` and `ICAL_FEED_PASS` appropriately. 
4. Create and activate a virtualenv and then run `pip install -r requirements.txt`
5. Go through the process of registering an app in the Google Calendar API dashboard in order to obtain an OAuth client ID. This process is described at https://developers.google.com/google-apps/calendar/quickstart/python. It's important to select "Desktop app" for the OAuth "Application Type" field. Once the credentials are created, download the JSON file, rename it to `ical_to_gcal_sync_client_secret.json` and  place it in the same location as the script. 
6. Until recently you could leave your Google Cloud project in "testing" mode and the OAuth flow would work indefinitely. However as [described here](https://support.google.com/cloud/answer/10311615#publishing-status&zippy=%2Ctesting) any tokens for apps in this mode will now expire after 7 days, including refresh tokens. To avoid having to manually re-auth every time this happens, go to [your OAuth consent page configuration](https://console.cloud.google.com/apis/credentials/consent) and set the "Publishing status" to "Production". This will display a warning that you need to do a lot of verification steps, but things still seem to work if you ignore the warnings. 
7. Run the script. This should trigger the OAuth2 authentication process and prompt you to allow the app you created in step 5 to access your calendars. If successful it should store the credentials in `ical_to_gcal_sync.json`.
8. Subsequent runs of the script should not require any further interaction unless the credentials are invalidated/changed.

```   
   python3 edt_to_gcal_sync_grenoble_inp/ical_to_gcal_sync.py
```
## Multiple Configurations / Alternate Config Location

If you want to specify an alternate location for the config.py file, use the environment variable CONFIG_PATH:

```
CONFIG_PATH='/path/to/my-custom-config.py' python ical_to_gcal_sync.py
```

## Rewriting Events / Skipping Events

If you specify a function in the config file called EVENT_PREPROESSOR, you can use that
function to rewrite or even skip events from being synced to the Google Calendar.

Some example rewrite rules:

```python
import icalevents
def EVENT_PREPROCESSOR(ev: icalevents.icalparser.Event) -> bool:
    from datetime import timedelta


    # Skip Bob's out of office messages
    if ev.summary == "Bob OOO":
        return False

   # Skip gaming events when we're playing Monopoly
    if ev.summary == "Gaming" and "Monopoly" in ev.description:
        return False

   # convert fire drill events to all-day events
    if ev.summary == "Fire Drill":
        ev.all_day = True
        ev.start = ev.start.replace(hour=0, minute=0, second=0)
        ev.end = ev.start + timedelta(days=1)

    # include all other entries
    return True

    # This preprocessor method is a more powerfull alternative to the SET_REMOVE


## Alternative:
The submodule phelma_calendar could be used as a standalone product to produce a filtered ICS and manually import the edt 
into your google calendar.
The following file is generated: ADECalFiltered.ics
```
   python3 edt_to_gcal_sync_grenoble_inp/phelma_calendar/phelma_calendar.py
```
## Install on RPI - BUSTER only, need Python3.7 

```
mkdir PhelmaEdt
cd PhelmaEdt
wget https://github.com/rjullien/edt_to_gcal_sync_grenoble_inp/archive/V0.2.tar.gz
tar xvf V0.2.tar.gz
rm V0.2.tar.gz
pip3 install -r edt_to_gcal_sync_grenoble_inp-0.2/requirements.txt
--> Update both config files + google credential
python3 edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/phelma_calendar.py
Update the API_SLEEP_TIME if you get 'Rate Limit Exceeded' 
```

## Add a crontab and sync two calendars (example to show how to set up for several calendars at 10pm daily but Saturday)

```
cd PhelmaEdt
mv edt_to_gcal_sync_grenoble_inp-0.2/synPhelma.sh .
mv edt_to_gcal_sync_grenoble_inp-0.2/startSynPhelma.sh .
```
Update crontab (crontab -e) with:
```
00 22 * * 0-5 /home/pi/PhelmaEdt/startSynPhelma.sh >>/home/pi/PhelmaEdt/cron.txt 2>&1
Provide source config files referenced into synPhelma.sh
```
## Send email during the process

install msmtp
```
sudo apt-get install msmtp
```
create config file /etc/msmtprc
```
# Valeurs par défaut pour tous les comptes.
defaults
auth           on
tls            on
tls_starttls   on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        /var/log/msmtp.log

# Exemple pour un compte Gmail
account        gmail
auth           plain
host           smtp.gmail.com
port           587
from           root@raspi-buster
user           BBB@gmail.com
password       Passwd

# Default
account default : gmail
```

Add this line into the .sh
```
printf "Subject:Synchronise edt INP\nCalendar of XXX, YYY, ZZZ synchronised" | sudo msmtp AAA@gmail.com
```

## Possible evolutions

move from opt-in to opt-out the config file to ensure nothing is lost (e.g.: keep #3PMKTCP6_2020_S5_DS_PET_PMP_G1 while removing al #3PMKTCP6_2020_S5_CTD_PET_DE_PMP_CDE_G* but keeping the rigth Gn)

Ability to create from scratch recurring activities such as sport, that are mandatory but not into edt
