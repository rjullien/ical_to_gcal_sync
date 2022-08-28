This script can be used to periodically pull events from grenoble-inp iCal feed and insert them into a selected Google Calendar using the API for that service. 

This module is mainly based on ical_to_gcal_sync open source project, customized for grenoble-inp edt

I'm putting the code here in case it's useful to any grenoble-inp student similarly frustrated with edt slowness and unreadability. Note that it's not particularly polished or well-packaged.

## Using the script

> NOTE: requires Python 3.7+

Some brief instructions:
1. Edit configPhelma.py and set both needed parameters
1. Edit config.py or copy to new file (see *Multiple Configurations* below)
2. Set ICAL_FEED to the URL of the iCal feed you want to sync events from.
3. Set CALENDAR_ID to the ID of the Google Calendar instance you want to insert events into. You can set it to "primary" to use the default main calendar, or create a new secondary calendar (in which case you can find the ID on the settings page, of the form 'longID@group.calendar.google.com').
4. pip3 install -r requirements.txt
   if requirement cannot be processed, check that python is a symbolic link to python3 in /usr/bin, if not you can move it, anyway python2.7 is no more supported
5. Go through the process of registering an app in the Google Calendar API dashboard in order to obtain the necessary API credentials. This process is described at https://developers.google.com/google-apps/calendar/quickstart/python - rename the downloaded file to ical_to_gcal_sync_client_secret.json and place it in the same location as the script. 
6. Run the script. This should trigger the OAuth2 authentication process and prompt you to allow the app you created in step 4 to access your calendars. If successful it should store the credentials in ical_to_gcal_sync.json.
7. Subsequent runs of the script should not require any further interaction unless the credentials are invalidated/changed.

```   
   python3 edt_to_gcal_sync_grenoble_inp/ical_to_gcal_sync.py
```
## Multiple Configurations / Alternate Config Location

If you want to specify an alternate location for the config.py file, use the environment variable CONFIG_PATH:

```
CONFIG_PATH='/path/to/my-custom-config.py' python ical_to_gcal_sync.py
```

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
