from vlc import MediaPlayer
from time import sleep,gmtime,strftime
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from glob import glob
from os import system
def playlist():
    global continueplay
    continueplay = True
    queplay = []
    for f in open("playlist.txt", "r"):
        b = f.replace("\n","")
        queplay.append(b.replace("./apps/music/",""))
    for que in queplay:
        print(continueplay)
        if continueplay == True:
            print(que)
            play(str("apps/music/"+que))
        else:
            break
    
def mainscreen():
    global mainscreenlist
    mainscreenlist = ["play","playlist","bluetooth","setings"]
    menu(mainscreenlist)
def menu(listmenu):
    global oled,draw

    draw.rectangle((1, 1, 126, 62), outline=0, fill=black)
    if y_pointer == 0: 
        draw.text((9,5), listmenu[y_pointer], fill=white, font=font)
        draw.text((9,16), listmenu[y_pointer+1], fill=white, font=font)
        draw.text((9,27), listmenu[y_pointer+2], fill=white, font=font)
        draw.text((9,38), listmenu[y_pointer+3], fill=white, font=font)
        pointer(0,listmenu)
    elif y_pointer == len(listmenu)-1:
        draw.text((9,5), listmenu[y_pointer-3], fill=white, font=font)
        draw.text((9,16), listmenu[y_pointer-2], fill=white, font=font)
        draw.text((9,27), listmenu[y_pointer-1], fill=white, font=font)
        draw.text((9,38), listmenu[y_pointer], fill=white, font=font)
        pointer(3,listmenu)
    elif y_pointer == len(listmenu)-2:
        draw.text((9,5), listmenu[y_pointer-2], fill=white, font=font)
        draw.text((9,16), listmenu[y_pointer-1], fill=white, font=font)
        draw.text((9,27), listmenu[y_pointer], fill=white, font=font)
        draw.text((9,38), listmenu[y_pointer+1], fill=white, font=font)
        pointer(2,listmenu)
    else:
        draw.text((9,5), listmenu[y_pointer-1], fill=white, font=font)
        draw.text((9,16), listmenu[y_pointer], fill=white, font=font)
        draw.text((9,27), listmenu[y_pointer+1], fill=white, font=font)
        draw.text((9,38), listmenu[y_pointer+2], fill=white, font=font)
        pointer(1,listmenu)
def pointer(pointer_at,listpoiter):
    global files,ffile,pliki,oled,draw
    if pointer_at == 0 and len(listpoiter) >=  1:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,9 , 8, 13), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
    elif pointer_at == 1 and len(listpoiter) >=  2:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,20 , 8, 24), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
    elif pointer_at == 2 and len(listpoiter) >=  3:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,31 , 8, 35), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
    elif pointer_at == 3 and len(listpoiter) >=  4:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,42 , 8, 46), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
def full():
    global files,ffile,pliki,oled,draw,y_pointer,is_exit,downbutton,upbutton,okbutton,offbutton,backbutton, leftbutton,rightbutton,image1
    loop = True
    while loop:
        if y_pointer <= -1:

            y_pointer = 0
            menu(pliki)
        elif y_pointer >= len(pliki):
            y_pointer = len(pliki)-1
        if downbutton.is_pressed:
            if y_pointer+1 >= len(pliki)-1:
                y_pointer = len(pliki)-1
                print("true")
            else:
                y_pointer = y_pointer + 1
                print("else")
            
            menu(pliki)
            downbutton.wait_for_release()
            sleep(0.3)
            print("down")
            print(y_pointer)
            
            oled.display(image1)
        elif upbutton.is_pressed:
           
            if y_pointer-1 <= -1:
                y_pointer = 0
            else:
                y_pointer = y_pointer - 1
            menu(pliki)

            upbutton.wait_for_release()
            print("up")
            print(y_pointer)
            sleep(0.3)
            
    
        elif backbutton.is_pressed:
            print("exit")
            backbutton.wait_for_release()
            sleep(0.3)                    

            y_pointer = 0
            loop = False
            break
            
        elif offbutton.is_pressed:
            draw.rectangle((0,0,128,64), fill=black)
            oled.display(image1)
            sleep(1)
            offbutton.wait_for_press()
            
            menu(pliki)
           
            sleep(1)
        elif okbutton.is_pressed:
            
            
            play(str("apps/music/"+pliki[y_pointer]))
            
            menu(pliki)
            
            full()
            

def screenfull():
    global files,ffile,pliki,oled,draw,y_pointer,is_exit,downbutton,upbutton,okbutton,offbutton,backbutton, leftbutton,rightbutton,image1
    while True:
        if y_pointer <= -1:

            y_pointer = 0
            menu(mainscreenlist)
        elif y_pointer >= len(mainscreenlist):
            y_pointer = len(mainscreenlist)-1
        if downbutton.is_pressed:
            if y_pointer+1 >= len(mainscreenlist)-1:
                y_pointer = len(mainscreenlist)-1
                print(True)
                print(y_pointer)
            else:
                y_pointer = y_pointer + 1
                print(False)
            
            menu(mainscreenlist)
            downbutton.wait_for_release()
            sleep(0.3)
            print("down")
            print(y_pointer)
            
            oled.display(image1)
        elif upbutton.is_pressed:
           
            if y_pointer-1 <= -1:
                y_pointer = 0
            else:
                y_pointer = y_pointer - 1
            menu(mainscreenlist)

            upbutton.wait_for_release()
            print("up")
            print(y_pointer)
            sleep(0.3)
            
    
        elif backbutton.is_pressed:
            print("exit")
                       
            downbutton.close()
            upbutton.close()
            leftbutton.close()
            rightbutton.close()
            okbutton.close()                   
            backbutton.close()
            offbutton.close()
            print("button") 
            
            break
        elif offbutton.is_pressed:
            draw.rectangle((0,0,128,64), fill=black)
            oled.display(image1)
            sleep(1)
            offbutton.wait_for_press()
            
            menu(pliki)
           
            sleep(1)
        elif okbutton.is_pressed:
            okbutton.wait_for_release()
            sleep(0.3)
            if mainscreenlist[y_pointer] == "play":
                menu(pliki)
                full()
            elif mainscreenlist[y_pointer] == "bluetooth":
                system("bluetoothctl connect 74:2A:8A:C1:65:7F")
            elif mainscreenlist[y_pointer] == "playlist":
                playlist()
            menu(mainscreenlist)
            
            
            
                       
def play(song):
    global vol,continueplay
    p = MediaPlayer(song)
    p.play()
    timec,timea = -1,-1
    sleep(1)
    draw.rectangle((0,0,128,64), fill=black)
    draw.text(xy=(cx, cy), text=song.replace("apps/music/",""), font=font, fill=white, anchor='mm')
    
    while p.is_playing():
        if not (timec == strftime("%M:%S", gmtime(p.get_time()/1000))):
            timec = strftime("%M:%S", gmtime(p.get_time()/1000))
            timea = strftime("%M:%S", gmtime(p.get_length()/1000))
            #timea = datetime.timedelta(seconds=p.get_length()/1000) #strftime("%H:%M:%S", gmtime(p.get_length()/1000))
            #timec = datetime.timedelta(seconds=p.get_time()/1000)
            draw.rectangle((0,0,10,10), fill=black)
            draw.text((0,0), str(p.audio_get_volume()), fill=white, font=font)
            draw.rectangle((37,54,87,64), fill=black)
            draw.text((37,54), f"{timec}/{timea}", fill=white, font=font)
            oled.display(image1)
            

        if downbutton.is_pressed: #elif upbutton.is_pressed:
            downbutton.wait_for_release(0.3)
            sleep(0.3)
            if not(vol == 5):
                vol = vol - 5
            else:
                pass
            p.audio_set_volume(int(vol))
            print(p.audio_get_volume())
            draw.rectangle((0,0,10,10), fill=black)
            draw.text((0,0), str(p.audio_get_volume()), fill=white, font=font)
            oled.display(image1)
        elif upbutton.is_pressed:
            upbutton.wait_for_release(0.3)
            sleep(0.3)
            if not(vol == 70):
                vol = vol + 5
            else:
                pass
            p.audio_set_volume(int(vol))
            print(p.audio_get_volume())
            draw.rectangle((0,0,10,10), fill=black)
            draw.text((0,0), str(p.audio_get_volume()), fill=white, font=font)
            oled.display(image1)
        elif okbutton.is_pressed:
            
            okbutton.wait_for_release()
            
            sleep(0.3)
            p.pause()
            okbutton.wait_for_press()
            okbutton.wait_for_release()
            sleep(0.5)
            
            
        elif backbutton.is_pressed:
            backbutton.wait_for_release()
            sleep(0.2)
            continueplay = False      
            p.stop()
            break
        elif rightbutton.is_pressed:
            rightbutton.wait_for_release()
            sleep(0.2)   
            p.stop()
            break
   
def main():
    global downbutton,upbutton,leftbutton,rightbutton,okbutton,backbutton,offbutton,oled,image1,draw,white,black,font,y_pointer,pliki,vol,cx,cy
    oled = sh1106(spi(device=0, port=0, ),rotate=2)
    oled.clear()
    image1 = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image1)
    y_pointer= 0
    white = 255
    black = 0
    vol = 50
    font = ImageFont.truetype("Arial.ttf", 9)
    downbutton = Button(19)
    upbutton = Button(6)
    leftbutton = Button(5)
    rightbutton = Button(26)
    okbutton = Button(21)                   
    backbutton = Button(16) 
    offbutton = Button(13)
    pliki= []
    for files in glob("./apps/music/*.mp3"):
        pliki.append(files.replace("./apps/music/",""))
    w, h = oled.width, oled.height
    cx, cy = int(w/2), int(h/2)
    
    mainscreen()

    screenfull()
if __name__ == "__main__":
    main()
