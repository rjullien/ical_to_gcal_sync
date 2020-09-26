
# ---
# Module to read grenoble.inp agenda (edt) and filter keep only the groups I belong to
# Configuration is done into configPhelma.py 
#
# example of configPhelma.py (not commited for security raison)
#
# ICAL_FEED = 'https://loggin:passwd@edt.grenoble-inp.fr/directCal/2020-2021/etudiant/phelma?resources=20868,5574'
#
# This config keep G4 for English, G7 for Math & Physique and remove all Educ. Phy
# SET_TO_REMOVE=(("English","PMKANG6_2020_S5_TD_G4"),("TC Math - TI PET-PMP S5","PET_DE_PMP_CDE_G7\n"),\
#  ("TC Physique PET-PMP S5","PET_DE_PMP_CDE_G7\n"),("Educ. Phy. et Sportive PET-PMP S5","Impossibletomatch"))
#
# ----

from ics import Calendar, Event
import requests
# Switch following import if used standalone
# import configPhelma as cfg
from phelma_calendar import configPhelma as cfg

def get_phelma_calendar():

    # Read grenoble-inp agenda
    c = Calendar()
    url = cfg.ICAL_FEED
    c = Calendar(requests.get(url).text)

    # create the list of events to be filtered out from the one read previously
    eventOut=c.events.copy()

    # for each event, if it matches the filter out rule, remove them from the event list
    for EventEdt in c.events:
        for (f1,f2) in cfg.SET_TO_REMOVE:
            if(EventEdt.name.find(f1)!=-1): # If it matches a candidate topic
                if(EventEdt.description.find(f2)==-1): # Check if the group in the description <> from my group
                     eventOut.remove(EventEdt) # remove this event
                     #print("Remove "+EventEdt.name + " Desc: " + EventEdt.description)

    # print(str(eventOut))
    return eventOut

# ----
# Main : used to test the module and produce and .ics file for a manual import into google agenda
#        To fully automate, this module is used with a modified version of ical_to_gcal_sync (start-> begin, summary-> name, call this module instead of the ulr)
# Do not forget to set the proper values into config.py (one for this module, one for ical_to_gcal_sync)
# ----
calendarOut  = open("./ADECalFiltered.ics", "w") 
calendarOut.write("BEGIN:VCALENDAR\nMETHOD:REQUEST\nPRODID:-//ADE/version 6.0\nVERSION:2.0\nCALSCALE:GREGORIAN\n")
eventOut=get_phelma_calendar()
for EventEdt in eventOut:
    calendarOut.write(str(EventEdt)+'\n')

calendarOut.write("END:VCALENDAR\n")
calendarOut.close() 