from time import sleep
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.oled.device import sh1106

def main():
    rpi4 = True
    midlebutton = Button(20)
    okbutton = Button(21)                   
    backbutton = Button(16)
    offbutton = Button(13)
    downbutton = Button(19)
    upbutton = Button(6)
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
            okbutton.wait_for_release()
            x = x+1
            draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
            draw.text((10,25), str(x), fill=255)
            oled.display(image1)
            
            sleep(0.08)
        
        elif midlebutton.is_pressed and rpi4 == False:
            okbutton.wait_for_release()
            x = x-1
            draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
            draw.text((10,25), str(x), fill=255)
            oled.display(image1)
            
            sleep(0.08)
        elif backbutton.is_pressed:
            okbutton.close()                   
            backbutton.close()
            offbutton.close()
            midlebutton.close()
            
            upbutton.close()
            downbutton.close()
            break
if __name__ == "__main__":
    main()