#!/usr/bin/bash

Yellow='\033[0;33m'       # Yellow
echo $Yellow"Instaling pianka version 1.0 alfa"



echo -e $Green"Instaling needed packages"
sudo apt install zlib1g-dev libjpeg-dev libpng-dev python3.11 python3-venv python3-pip python3.11-dev
echo -e $Green"Creating python virtual environments"
python3 -m venv /home/${USER}/pianka
echo -e $Green"Instaling needed python packages"
/home/${USER}/pianka/bin/pip3 install --upgrade pip gpiozero luma.oled scapy pandas 
echo -e $Green"Setting systemd service"
sed -i 's/username/${USER}/g' /home/${USER}/pianka/pianka.service
sudo systemctl enable /home/${USER}/pianka/pianka.service
sudo systemctl start pianka.service
echo -e $Green"Done"
echo ""
echo -e $Green"You can stop my by running the command"
echo -e $Green"            systemctl stop pianka"
echo -e $Green"or check by running the command"
echo -e $Green"            systemctl status pianka"
echo -e $Green"and also you can start me by running the command"
echo -e $Green"            systemctl status pianka"

