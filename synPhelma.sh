

date
cd /home/pi/PhelmaEdt

echo "synch A"
CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.3/configA.py' python3 edt_to_gcal_sync_grenoble_inp-0.3/ical_to_gcal_sync.py

echo "synch A done"
echo "synch B"
CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.3/configB.py' python3 edt_to_gcal_sync_grenoble_inp-0.3/ical_to_gcal_sync.py

echo "synch B done"

RES_ERR=`grep "ERROR" ./ical_to_gcal_sync_log.txt` 
if [ -n "$RES_ERR" ]; then
    # Manage Error
fi

RES_ERR=`grep "invalid_grant" ./cron.txt` 
if [ -n "$RES_ERR" ]; then
    # Manage Error
fi
RES_ERR=`grep -i "error" ./cron.txt` 

if [ -n "$RES_ERR" ]; then
    # Manage Error
fi
mv ./cron.txt ./cronold.txt
touch ./cron.txt
