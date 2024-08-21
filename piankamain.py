import time
import board
import digitalio
import sys
import glob
from gpiozero import Button
from PIL import Image, ImageDraw
import adafruit_ssd1306
import os



def menu():
    global files,ffile,pliki,i2c,oled,draw,image
    
    
    oled.fill(0)
    draw.rectangle((0 ,0, 128, 64), outline=0, fill=255)
    draw.rectangle((2, 2, 126, 62), outline=0, fill=0)

    ytext = 5
    for i in range(len(pliki)): 
        draw.text((10,ytext), pliki[i], fill=255)
        ytext = ytext+11
    oled.image(image)
    oled.show()
def pointer(pointer_at):
    if pointer_at == 0 and len(pliki) >=  1:
        draw.rectangle((5 ,9 , 9, 37), outline=0, fill=0)
        draw.rectangle((5 ,9 , 9, 13), outline=0, fill=255)
        oled.image(image)
        oled.show()
    if pointer_at == 1 and len(pliki) >=  2:
        draw.rectangle((5 ,9 , 9, 37), outline=0, fill=0)
        draw.rectangle((5 ,20 , 9, 24), outline=0, fill=255)
        oled.image(image)
        oled.show()
    if pointer_at == 2 and len(pliki) >=  3:
        draw.rectangle((5 ,9 , 9, 37), outline=0, fill=0)
        draw.rectangle((5 ,31 , 9, 35), outline=0, fill=255)
        oled.image(image)
        oled.show()
    if pointer_at == 3 and len(pliki) >= 4:
        draw.rectangle((5 ,9 , 9, 37), outline=0, fill=0)
        draw.rectangle((5 ,42 , 9, 46), outline=0, fill=255)
        oled.image(image)
        oled.show()
def exit():
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.rectangle((20, 20, 108, 51), outline=0, fill=255)
    draw.rectangle((22, 22, 106, 49), outline=255, fill=0)
    draw.text((52,30), "Exit?", fill=255)
    oled.image(image)
    oled.show()
def button(buttons):
    buttons
def is_press(button):
   pass
# STARTING PROGRAM

if __name__ == "__main__":
    pliki= []
    for files in glob.glob("./apps/*.py"):
        ffile = files.replace("./apps/","")
        pliki.append(ffile)
    downbutton = Button(17)
    upbutton = Button(27)
    okbutton = Button(22)
    backbutton = Button(18)
    oled_reset = digitalio.DigitalInOut(board.D4)
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=oled_reset)
    oled.fill(0)
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)
    y_pointer = 0
    menu()
    pointer(y_pointer)
    while True:
        if y_pointer <= -1:
            y_pointer = 0
        elif y_pointer >= len(pliki):
            y_pointer = len(pliki)-1
        if downbutton.is_pressed:
            y_pointer = y_pointer + 1
            pointer(y_pointer)
            downbutton.wait_for_release()
            time.sleep(0.1)

        elif upbutton.is_pressed:
            y_pointer = y_pointer - 1
            pointer(y_pointer)
            upbutton.wait_for_release()
            time.sleep(0.3)
        elif backbutton.is_pressed:
            exit()
            is_exit = True
            backbutton.wait_for_release()
            time.sleep(0.3)
            while is_exit:
                if okbutton.is_pressed:
                    draw.rectangle((0 ,0, 128, 64), outline=0, fill=0)
                    oled.image(image)
                    oled.show()
                    sys.exit(0)
                elif backbutton.is_pressed:
                    menu()
                    pointer(y_pointer)
                    is_exit = False
        elif okbutton.is_pressed:
            #os.system("~/pianka/bin/python ~/pianka/apps/"+pliki[y_pointer])
            exec(open("apps/"+pliki[y_pointer]).read())
