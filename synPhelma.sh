date
cd /home/pi/PhelmaEdt
# printf "Subject:Synchronisation edt Phelma\nDebut de synchronisation des calendriers d Alexandre, Romane, Arthur, Enola" | sudo msmtp alexandre.jullien06@gmail.com
# printf "Subject:Synchronisation edt Phelma\nDebut de synchronisation des calendriers d Alexandre, Romane, Arthur" | sudo msmtp alexandre.jullien06@gmail.com
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
echo "Copy Baptiste"
cp edt_to_gcal_sync_grenoble_inp-0.2/configBapt.py  edt_to_gcal_sync_grenoble_inp-0.2/config.py
cp edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelmaBapt.py edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelma.py
echo "synch Baptiste"
python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py
#printf "Subject:Synchronisation edt Phelma\nCalendriers de Romane synchronise" | sudo msmtp bos.romane@gmail.com
#echo "Copy Arthur"
#cp edt_to_gcal_sync_grenoble_inp-0.2/configArthur.py  edt_to_gcal_sync_grenoble_inp-0.2/config.py
#cp edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelmaArthur.py edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelma.py
#echo "synch Arthur"
#python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py
#printf "Subject:Synchronisation edt Ensimag\nCalendriers d Arthur synchronise" | sudo msmtp arthurlignier06@gmail.com
#echo "Copy Enola"
#cp edt_to_gcal_sync_grenoble_inp-0.2/configEnola.py  edt_to_gcal_sync_grenoble_inp-0.2/config.py
#cp edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelmaEnola.py edt_to_gcal_sync_grenoble_inp-0.2/phelma_calendar/configPhelma.py
#echo "synch Enola"
#python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py
# printf "Subject:Synchronisation edt Phelma\nCalendriers d Enola synchronise" | sudo msmtp bos.romane@gmail.com
echo "synch done"
# printf "Subject:Synchronisation edt Phelma\nCalendriers Alexandre, Romane, Enola et Arthur synchronises" | sudo msmtp alexandre.jullien06@gmail.com
printf "Subject:Synchronisation edt INP\nCalendriers Alexandre, Romane, Baptiste synchronises" | sudo msmtp alexandre.jullien06@gmail.com
