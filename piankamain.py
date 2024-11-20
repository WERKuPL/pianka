from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.oled.device import sh1106

from gpiozero import Button
from os import system
from time import sleep
RemoteGpio = True
RemoteGpioIp = "192.168.0.34"
if RemoteGpio == True:
    from gpiozero.pins.pigpio import PiGPIOFactory
    import tkinter
    from PIL import ImageTk
    factory = PiGPIOFactory(host=RemoteGpioIp)

def drawapp(posision,app):
    if  posision == "up":
        draw.bitmap((4,2), appsicon[app],fill=255)
        draw.text((24,5), apps[app], font=font,fill=255)
    elif posision == "middle":
        draw.bitmap((4,24), appsicon[app],fill=255)
        draw.text((24,25), apps[app], font=font,fill=255)
    elif posision == "down":
        draw.bitmap((4,46), appsicon[app],fill=255)
        draw.text((24,45), apps[app], font=font,fill=255)
    elif  posision == "upf":
        draw.bitmap((4,2), appsicon[app],fill=255)
        draw.text((24,5), apps[app], font=fontbold,fill=255)
    elif posision == "middlef":
        draw.bitmap((4,24), appsicon[app],fill=255)
        draw.text((24,25), apps[app], font=fontbold,fill=255)
    elif posision == "downf":
        draw.bitmap((4,46), appsicon[app],fill=255)
        draw.text((24,45), apps[app], font=fontbold,fill=255)

def eexit():
    
    draw.rectangle((0,0,128,64), fill=0)
    draw.rectangle((20, 20, 108, 51), outline=255, fill=255)
    draw.rectangle((22, 22, 106, 49), outline=255, fill=0)
    draw.text((30,28), "Shutdown?", fill=255, font=fontbold)
    display(image1)
    #draw.bitmap((120,0), scrollicon,fill=255)
def submenu(itemlist, title):
    def submenudrawapp(pos,name):
        if  pos == "up":
            draw.text((24,5), name, font=fontsmall,fill=255)
        elif pos == "middle":
            draw.text((24,25), name, font=fontsmall,fill=255)
        elif pos == "down":
            draw.text((24,45), name, font=fontsmall,fill=255)
        elif  pos == "upf":
            draw.text((24,5), name, font=fontsmallbold,fill=255)
        elif pos == "middlef":
            draw.text((24,25), name, font=fontsmallbold,fill=255)
        elif pos == "downf":
            draw.text((24,45), name, font=fontsmallbold,fill=255)
    def makemenu(pos, title):
        item = 0
        draw.rectangle((0 ,0, 128, 64), outline=0, fill=0)
        if pos+1 >= len(list):
            submenudrawapp("up",itemlist[pos]-2)
            submenudrawapp("middle",itemlist[pos]-1)
            submenudrawapp("downf",itemlist[pos])
            draw.bitmap((-1,43), outlineicon,fill=255)
        elif pos <= 0:
            submenudrawapp("upf",itemlist[pos])
            submenudrawapp("middle",itemlist[pos]+1)
            submenudrawapp("down",itemlist[pos]+2)
            draw.bitmap((-1,1), outlineicon,fill=255)
        else:    

            submenudrawapp("up",list[pos]-1)
            submenudrawapp("middlef",list[pos])
            submenudrawapp("down",list[pos]+1)
            draw.bitmap((-1,22), outlineicon,fill=255)
        draw.bitmap((119,0), scrollicon,fill=255)
    while True:
        if downbutton.is_pressed:
            if itemlist+1 >= len(itemlist)-1:
                current_app  = len(apps)-1
            else:
                current_app = current_app  + 1
        
            downbutton.wait_for_release()
            
            print("down")
            print(current_app)
            makemenu()
            display(image1)

            sleep(0.3)
        elif upbutton.is_pressed:
           
            if current_app -1 <= -1:
                current_app  = 0
            else:
                current_app  = current_app  - 1
            

            upbutton.wait_for_release()
            print("up")
            print(current_app)
            menu()
            display(image1)

            sleep(0.3)
        elif okbutton.is_pressed:

            if apps[current_app] == "Settings":
                setings()
                
            else: 
                downbutton.close()
                upbutton.close()
                leftbutton.close()
                rightbutton.close()
                okbutton.close()                   
                backbutton.close()
                offbutton.close()
                exec(f"import assets.apps.{appslibrary.get(apps[current_app]).replace('.py','')} ")
                eval(f"assets.apps.{appslibrary.get(apps[current_app]).replace('.py','')}.main()") 
                oled = sh1106(spi(device=0, port=0, ),rotate=2)
                oled.clear()
                image1 = Image.new('1', (oled.width, oled.height))
                draw = ImageDraw.Draw(image1)
                is_exit = False
                upbutton = Button(6)
                leftbutton = Button(5)
                rightbutton = Button(26)
                downbutton = Button(19)
                okbutton = Button(21)                   
                backbutton = Button(16)
                offbutton = Button(13)
            menu()
            display(image1)
        elif backbutton.is_pressed:
            break
    #draw.rectangle((124,int(64/len(list))*pos,126,int(64/len(list))*pos+7), fill=255)
def setings():
    pass
def menu(): 
    draw.rectangle((0 ,0, 128, 64), outline=0, fill=0)
    if current_app+1 >= len(apps):
        drawapp("up",current_app-2)
        drawapp("middle",current_app-1)
        drawapp("downf",current_app)
        draw.bitmap((-1,43), outlineicon,fill=255)
    elif current_app <= 0:
        drawapp("upf",current_app)
        drawapp("middle",current_app+1)
        drawapp("down",current_app+2)
        draw.bitmap((-1,1), outlineicon,fill=255)
    else:    
        
        drawapp("up",current_app-1)
        drawapp("middlef",current_app)
        drawapp("down",current_app+1)
        draw.bitmap((-1,22), outlineicon,fill=255)
    draw.bitmap((119,0), scrollicon,fill=255)
    draw.rectangle((124,int(64/len(apps))*current_app,126,int(64/len(apps))*current_app+7), fill=255)
    
def full():
    global current_app,downbutton,upbutton,okbutton,oled,image1,offbutton,backbutton, leftbutton,rightbutton,draw
    while True:
        if downbutton.is_pressed:
            if current_app+1 >= len(apps)-1:
                current_app  = len(apps)-1
            else:
                current_app = current_app  + 1
        
            downbutton.wait_for_release()
            
            print("down")
            print(current_app)
            menu()
            display(image1)

            sleep(0.3)
        elif upbutton.is_pressed:
           
            if current_app -1 <= -1:
                current_app  = 0
            else:
                current_app  = current_app  - 1
            

            upbutton.wait_for_release()
            print("up")
            print(current_app)
            menu()
            display(image1)

            sleep(0.3)
        elif okbutton.is_pressed:

            if apps[current_app] == "Settings":
                setings()
                
            else: 
                downbutton.close()
                upbutton.close()
                leftbutton.close()
                rightbutton.close()
                okbutton.close()                   
                backbutton.close()
                offbutton.close()
                exec(f"import assets.apps.{appslibrary.get(apps[current_app]).replace('.py','')} ")
                eval(f"assets.apps.{appslibrary.get(apps[current_app]).replace('.py','')}.main()") 
                oled = sh1106(spi(device=0, port=0, ),rotate=2)
                oled.clear()
                image1 = Image.new('1', (oled.width, oled.height))
                draw = ImageDraw.Draw(image1)
                is_exit = False
                upbutton = Button(6)
                leftbutton = Button(5)
                rightbutton = Button(26)
                downbutton = Button(19)
                okbutton = Button(21)                   
                backbutton = Button(16)
                offbutton = Button(13)
            menu()
            display(image1)
        elif offbutton.is_pressed:
            draw.rectangle((0,0,128,64), fill=0)
            display(image1)
            sleep(1)
            print("wait")
            offbutton.wait_for_press()
            menu()
            display(image1)
            print("start")
            sleep(1)
        elif backbutton.is_pressed:
            print("exit")                    
            draw.rectangle((0 ,0, 128, 64), outline=0, fill=0)
            eexit()
            display(image1)
            sleep(0.3)
            is_exit = True
            while is_exit:
                if okbutton.is_pressed:
                    system("sudo shutdown now")
                elif backbutton.is_pressed:
                    is_exit = False
                    menu()
                    display(image1)
                    sleep(0.3)
                    break
                elif offbutton.is_pressed:
                    quit()
def display(picture):
    if RemoteGpio == False:
        oled.display(picture)
    elif RemoteGpio == True:
        img=picture.resize((450, 350))
        root.update()
        print(emulator)
if __name__ == "__main__":
    image1 = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype("assets/fonts/PixelOperator.ttf", 16)
    fontsmall = ImageFont.truetype("assets/fonts/PixelOperator.ttf", 8)
    fontsmallbold = ImageFont.truetype("assets/fonts/PixelOperator-Bold.ttf", 8)
    fontbold = ImageFont.truetype("assets/fonts/PixelOperator-Bold.ttf", 16)
    scrollicon = Image.open("assets/icons/scroll.png").convert('1')
    snakeicon = Image.open("assets/icons/snake.png").convert('1')
    outlineicon = Image.open("assets/icons/outline.png").convert('1')
    mp3icon = Image.open("assets/icons/mp3.png").convert('1')
    legacyappsicon = Image.open("assets/icons/legacyapps.png").convert('1')
    wifiicon = Image.open("assets/icons/wifi.png").convert('1')
    countericon = Image.open("assets/icons/counter.png").convert('1')
    boxicon = Image.open("assets/icons/box.png").convert('1')
    usbicon = Image.open("assets/icons/usb.png").convert('1')
    settingsicon = Image.open("assets/icons/settings.png").convert('1')
    if RemoteGpio == False:
        downbutton = Button(19)
        upbutton = Button(6)
        leftbutton = Button(5)
        rightbutton = Button(26)
        okbutton = Button(21)                   
        backbutton = Button(16)
        offbutton = Button(13)
        oled = sh1106(spi(device=0, port=0, ),rotate=2,)
        
    elif RemoteGpio == True:
        img=image1.resize((450, 350))
        draw = ImageDraw.Draw(img)
        draw.bitmap((0,0),settingsicon)
        root = tkinter.Tk()
        emulator = ImageTk.PhotoImage(image1)
        label1 = tkinter.Label(master=root,image=emulator)
        label1.image = emulator
        label1.place(x=0, y=0)
        downbutton = Button(19, pin_factory=factory)
        upbutton = Button(6, pin_factory=factory)
        leftbutton = Button(5, pin_factory=factory)
        rightbutton = Button(26, pin_factory=factory)
        okbutton = Button(21, pin_factory=factory)                   
        backbutton = Button(16, pin_factory=factory)
        offbutton = Button(13, pin_factory=factory)
        print("afterloop")
    
    apps = [
        "Snake",
        "MP3 Player",
        "Legacy apps",
        "Wifi",
        "BadUSB",
        "Counter",
        "3D box",
        "Settings",
    ]
    appslibrary = {
        "Snake":"snake.py",
        "MP3 Player":"mp3.py",
        "Legacy apps":"legacyapps.py",
        "Wifi":"wifi.py",
        "BadUSB":"badusb.py",
        "Counter":"counter.py",
        "3D box":"box.py",
    }
    settings = [
        "Wifi",
        "Update",
        "Verison",
    ]
    appsicon = [
        snakeicon,
        mp3icon,
        legacyappsicon,
        wifiicon,
        usbicon,
        countericon,
        boxicon,
        settingsicon,
    ]
    current_app,current_setting = 0,0
    menu()
    display(image1)
    full()
    