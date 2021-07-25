date
cd /home/pi
tar -czvf Phelma.tar.gz /home/pi/PhelmaEdt
ssh Rene@10.182.207.243 cp /var/services/homes/Rene/RPI4/Backup/Phelma-2.tar.gz /var/services/homes/Rene/RPI4/Backup/Phelma-3.tar.gz
ssh Rene@10.182.207.243 cp /var/services/homes/Rene/RPI4/Backup/Phelma-1.tar.gz /var/services/homes/Rene/RPI4/Backup/Phelma-2.tar.gz
ssh Rene@10.182.207.243 cp /var/services/homes/Rene/RPI4/Backup/Phelma.tar.gz /var/services/homes/Rene/RPI4/Backup/Phelma-1.tar.gz
scp Phelma.tar.gz Rene@10.182.207.243:/var/services/homes/Rene/RPI4/Backup/
rm /home/pi/Phelma.tar.gz
