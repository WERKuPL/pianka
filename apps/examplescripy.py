import sys
sys.path.append('/home/werku/pianka')
import piankamain as pianka
from gpiozero import Button 
from time import sleep
import digitalio
import board
from PIL import Image, ImageDraw
import adafruit_ssd1306
pianka.menu()