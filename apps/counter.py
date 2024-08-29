import sys
sys.path.append('/home/werku/pianka')
import piankamain # import # draw,oled,okbutton,backbutton
from time import sleep
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.oled.device import sh1106

def main():

    okbutton = Button(21)                   
    backbutton = Button(16)
    offbutton = Button(13)

    oled = sh1106(spi(device=0, port=0, ),rotate=2)
    oled.clear()
    image1 = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image1)

    x = 0
    draw.text((10,25), str(0), fill=255)
    oled.display(image1)
    #oled.ShowImage(oled.getbuffer(image1))
    while True:
        if okbutton.is_pressed:
            okbutton.wait_for_press()
            okbutton.wait_for_release()
            x = x+1
            draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
            draw.text((10,25), str(x), fill=255)
            oled.display(image1)
            
            sleep(0.08)
        elif backbutton.is_pressed:
            okbutton.close()                   
            backbutton.close()
            offbutton.close()
            break
        elif offbutton.is_pressed:

            offbutton.wait_for_release()
            draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
            oled.display(image1)
            sleep(1)
            offbutton.wait_for_press()
            offbutton.wait_for_release()
            draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
            draw.text((10,25), str(x), fill=255)
            oled.display(image1)
            sleep(0.08)
if __name__ == "__main__":
    main()