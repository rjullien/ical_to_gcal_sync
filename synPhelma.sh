cd /home/pi/PhelmaEdt
echo "Copy Alex"
cp edt_to_gcal_sync_grenoble_inp-0.2/configAlex.py  edt_to_gcal_sync_grenoble_inp-0.2/config.py
cp edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelmaAlex.py edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelma.py
echo "synch Alex"
python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py
echo "Copy Romane"
cp edt_to_gcal_sync_grenoble_inp-0.2/configRomane.py  edt_to_gcal_sync_grenoble_inp-0.2/config.py
cp edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelmaRomane.py edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelma.py
echo "synch Romane"
python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py
