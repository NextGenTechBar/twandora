#launcher for the front desk music polling system
cd /
cd /home/pi/Desktop/pydora-test
echo Starting up polling system
screen -S polling -d -m /home/pi/Desktop/pydora-test/twitter+gui.py
cd /
#sudo python /home/pi/Desktop/pydora-test/twitter+gui.py

