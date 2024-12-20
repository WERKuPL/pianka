#!/usr/bin/bash
Green='\033[0;32m'
Yellow='\033[0;33m'       # Yellow
echo $Yellow"Instaling pianka version 1.01 alfa"



echo -e $Green"Instaling needed packages"
sudo apt install zlib1g-dev libjpeg-dev libpng-dev python3.11 python3-venv python3-pip python3.11-dev swig python3-pil  libfreetype6-dev liblcms2-dev libopenjp2-7 spidev -y
echo -e $Green"Creating python virtual environments"
python3 -m venv /home/${USER}/pianka
echo -e $Green"Instaling needed python packages"
/home/${USER}/pianka/bin/pip3 install --upgrade pip gpiozero luma.oled scapy pandas rpi-lgpio pyyaml
echo -e $Green"Setting systemd service"
sed -i 's/username/${USER}/g' /home/${USER}/pianka/pianka.service
sed -i 's/username/${USER}/g' /home/${USER}/pianka/startup.sh
sudo systemctl enable /home/${USER}/pianka/pianka.service
sudo systemctl start pianka.service
#echo "dtparam=spi=on" | sudo tee -a /boot/firmware/config.txt
echo -e $Green"Done"
echo ""
echo -e $Green"You can stop my by running the command"
echo -e $Green"            systemctl stop pianka"
echo -e $Green"or check by running the command"
echo -e $Green"            systemctl status pianka"
echo -e $Green"and also you can start me by running the command"
echo -e $Green"            systemctl status pianka"

