date
cd /home/pi/PhelmaEdt
# printf "Subject:Synchronisation edt Phelma\nDebut de synchronisation des calendriers d Alexandre, Romane, Arthur, Enola" | sudo msmtp alexandre.jullien06@gmail.com

# if time hour is 19
if [ "$(date +%H)" -eq 19 ]
then

    echo "synch Alex"
    CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configAlex.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

    echo "synch Romane"
    CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configRomane.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

    echo "synch Victor"
    CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configVictor.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

fi
echo "synch Baptiste"
CONFIG_PATH='/home/pi/PhelmaEdt/edt_to_gcal_sync_grenoble_inp-0.2/configBapt.py' python3 edt_to_gcal_sync_grenoble_inp-0.2/ical_to_gcal_sync.py

echo "synch done"

RES_ERR=`grep "ERROR" ./ical_to_gcal_sync_log.txt` 
if [ -n "$RES_ERR" ]; then
    #curl --insecure 'https://10.182.207.57/core/api/jeeApi.php?apikey=YQFCKcxGJ52BSrHCc73U&type=cmd&id=8308&title=montitre&message=ErrorsFoundInINPSync'
    curl 'http://10.182.207.57/core/api/jeeApi.php?apikey=YQFCKcxGJ52BSrHCc73U&type=scenario&id=94&action=start&tags=message%3D%22Il%20y%20a%20des%20erreurs%20dans%20la%20synchronisation%20des%20calendriers%20I%20N%20P.%22%20MsgSev%3D1'
fi

RES_ERR=`grep "invalid_grant" ./cron.txt` 
if [ -n "$RES_ERR" ]; then
    #curl --insecure 'https://10.182.207.57/core/api/jeeApi.php?apikey=YQFCKcxGJ52BSrHCc73U&type=cmd&id=8308&title=montitre&message=ErrorsFoundInINPSync'
    curl 'http://10.182.207.57/core/api/jeeApi.php?apikey=YQFCKcxGJ52BSrHCc73U&type=scenario&id=94&action=start&tags=message%3D%22Il%20y%20a%20des%20erreurs%20dans%20la%20synchronisation%20des%20calendriers%20I%20N%20P..%20pour%20Baptiste..%20Invalid%20grante.%22%20MsgSev%3D1'
fi
#RES_ERR=`grep -i "error" ./cron.txt` 
RES_ERR=`grep -v "Cannot remove this Event:" ./cron.txt | grep -i "error" `
if [ -n "$RES_ERR" ]; then
    #curl --insecure 'https://10.182.207.57/core/api/jeeApi.php?apikey=YQFCKcxGJ52BSrHCc73U&type=cmd&id=8308&title=montitre&message=ErrorsFoundInINPSync'
    curl 'http://10.182.207.57/core/api/jeeApi.php?apikey=YQFCKcxGJ52BSrHCc73U&type=scenario&id=94&action=start&tags=message%3D%22Il%20y%20a%20des%20erreurs%20dans%20la%20synchronisation%20des%20calendriers%20I%20N%20P..%20error%20trouvé%20dans%20le%20log%20de%20la%20crontab.%22%20MsgSev%3D1'
else
    curl 'http://10.182.207.57/core/api/jeeApi.php?apikey=YQFCKcxGJ52BSrHCc73U&type=scenario&id=94&action=start&tags=message%3D%22l%27I%20N%20P.%20Est%20de%20retour!!!%22%20MsgSev%3D1'  
fi
mv ./cron.txt ./cronold.txt
touch ./cron.txt
