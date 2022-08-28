date
cd /home/pi/PhelmaEdt
# printf "Subject:Synchronisation edt Phelma\nDebut de synchronisation des calendriers d Alexandre, Romane, Arthur, Enola" | sudo msmtp alexandre.jullien06@gmail.com

echo "synch Alex"
CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configAlex.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

echo "synch Romane"
CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configRomane.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

echo "synch Baptiste"
CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configBapt.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

echo "synch Victor"
CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configVictor.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

echo "synch done"

# printf "Subject:Synchronisation edt Phelma\nCalendriers Alexandre, Romane, Enola et Arthur synchronises" | sudo msmtp alexandre.jullien06@gmail.com
# printf "Subject:Synchronisation edt INP\nCalendriers Alexandre, Romane, Baptiste synchronises" | sudo msmtp alexandre.jullien06@gmail.com
