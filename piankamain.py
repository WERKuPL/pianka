from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from gpiozero import Button

from time import sleep
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
    draw.text((38,30), "Shutdown?", fill=255, font=font)
    oled.display(image1)
    #draw.bitmap((120,0), scrollicon,fill=255)
def menu():
    draw.rectangle((0 ,0, 128, 64), outline=0, fill=0)
    # max down
    if current_app+1 >= len(apps):
        drawapp("up",current_app-2)
        drawapp("middle",current_app-1)
        drawapp("downf",current_app)
        draw.bitmap((0,43), outlineicon,fill=255)
    elif current_app <= 0:
        drawapp("upf",current_app)
        drawapp("middle",current_app+1)
        drawapp("down",current_app+2)
        draw.bitmap((0,1), outlineicon,fill=255)
    else:    
        
        drawapp("up",current_app-1)
        drawapp("middlef",current_app)
        drawapp("down",current_app+1)
        draw.bitmap((0,22), outlineicon,fill=255)
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
            oled.display(image1)

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
            oled.display(image1)

            sleep(0.3)
        elif okbutton.is_pressed:
            
            
            downbutton.close()
            upbutton.close()
            leftbutton.close()
            rightbutton.close()
            okbutton.close()                   
            backbutton.close()
            offbutton.close()
            print("open")
            
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
            oled.display(image1)
        elif offbutton.is_pressed:
            draw.rectangle((0,0,128,64), fill=0)
            oled.display(image1)
            sleep(1)
            print("wait")
            offbutton.wait_for_press()
            menu()
            oled.display(image1)
            print("start")
            sleep(1)
            

if __name__ == "__main__":
    oled = sh1106(spi(device=0, port=0, ),rotate=2)
    image1 = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype("assets/fonts/PixelOperator.ttf", 16)
    fontbold = ImageFont.truetype("assets/fonts/PixelOperator-Bold.ttf", 16)
    downbutton = Button(19)
    upbutton = Button(6)
    leftbutton = Button(5)
    rightbutton = Button(26)
    okbutton = Button(21)                   
    backbutton = Button(16)
    offbutton = Button(13)
    scrollicon = Image.open("assets/icons/scroll.png").convert('1')
    snakeicon = Image.open("assets/icons/snake.png").convert('1')
    outlineicon = Image.open("assets/icons/outline.png").convert('1')
    mp3icon = Image.open("assets/icons/mp3.png").convert('1')
    legacyappsicon = Image.open("assets/icons/legacyapps.png").convert('1')
    wifiicon = Image.open("assets/icons/wifi.png").convert('1')
    countericon = Image.open("assets/icons/counter.png").convert('1')
    boxicon = Image.open("assets/icons/box.png").convert('1')
    usbicon = Image.open("assets/icons/usb.png").convert('1')
    apps = [
        "Snake",
        "MP3 Player",
        "Legacy apps",
        "Wifi",
        "BadUSB",
        "Counter",
        "3D box",
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
    
    appsicon = [
        snakeicon,
        mp3icon,
        legacyappsicon,
        wifiicon,
        usbicon,
        countericon,
        boxicon,
    ]
    current_app = 0
    menu()
    oled.display(image1)
    full()



