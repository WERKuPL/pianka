import sys
sys.path.append('/home/werku/pianka')
from piankamain import *
from time import sleep
import digitalio
import board
from PIL import Image, ImageDraw
import adafruit_ssd1306

oled_reset = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=oled_reset)
oled.fill(0)
image = Image.new("1", (128, 64))
draw = ImageDraw.Draw(image)
#button = Button(17)
x = 0
draw.text((10,25), str(0), fill=255)
oled.image(image)
oled.show()

while True:
    if okbutton.is_pressed:
        x = x+1
        draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
        draw.text((10,25), str(x), fill=255)
        oled.image(image)
        oled.show()
        okbutton.wait_for_release()
        sleep(0.05)
    if backbutton.is_pressed:
        break
    
    
    