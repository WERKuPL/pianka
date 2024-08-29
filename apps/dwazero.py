import sys
sys.path.append('/home/werku/pianka')
import piankamain #import *
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import random
import math
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
FPS =60
WIDTH, HEIGHT = 64,64
ROWS = 4
COLS = 4
RECT_HEIGHT,RECT_WIDTH = 16,16

WHITE = 255
BLACK = 0
MOVE_VEL = 20

downbutton = Button(19)
upbutton = Button(6)
leftbutton = Button(5)
rightbutton = Button(26)
okbutton = Button(21)                   
backbutton = Button(16)
offbutton = Button(13)
oled = sh1106(spi(device=0, port=0, ),rotate=2)
image1 = Image.new('1', (oled.width, oled.height))
draw = ImageDraw.Draw(image1)
font = ImageFont.truetype("Arial.ttf", 8)

draw.rectangle((62,0,128,64), fill=WHITE)
draw.rectangle((63,1,126,62), fill=BLACK)



class Tile:
    def __init__(self,value, row,col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * 16
        self.y = row * 16
    def itdraw(self):
        draw.rectangle((63+self.x,1+self.y,63+self.x+14,1+self.y+14), fill=BLACK)
        draw.text((66+self.x,4+self.y), str(self.value) , fill=WHITE, font=font)
        
        oled.display(image1)
    def get_color(self):
        pass
        
    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)
    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]




def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col






def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles



def move_tiles(tiles,direction):
    updated = True
    blocks = set()
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile:tile.col == 0
        
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x >next_tile + MOVE_VEL
        move_check = lambda tile,next_tile: tile.x > next_tile.x + 16 + MOVE_VEL
        ceil = True 
    elif direction == "right":
        y += 1
    elif direction == "up":
        x -= 1
    elif direction == "down":
        x += 1
    while updated:
        
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(tiles, sorted_tiles)

    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue" 

def update_tiles(tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    drawback(tiles)

def draw_grid():
    
    draw.line((63,16, 126, 16), fill=WHITE)
    draw.line((63,32, 126, 32), fill=WHITE)
    draw.line((63,48, 126, 48), fill=WHITE)
    
    draw.line((79,0, 79, 64), fill=WHITE)
    draw.line((95,0, 95, 64), fill=WHITE)
    draw.line((111,0, 111, 64), fill=WHITE)
    oled.display(image1)
def drawback(tiles):
    
    draw.rectangle((0 ,0, 128, 64), outline=255, fill=BLACK)
    for tile in tiles.values():
        tile.itdraw()
    draw_grid()
        

    
    oled.display(image1)
def main():

    tiles = generate_tiles()

    run = True

    while run:
        sleep(1)
        
        if leftbutton.is_pressed:
            leftbutton.wait_for_release()
            move_tiles(tiles, "left")
            oled.display(image1)
        elif rightbutton.is_pressed:
            rightbutton.wait_for_release()
            move_tiles(tiles, "right")
            oled.display(image1)
        elif upbutton.is_pressed:
            upbutton.wait_for_release()
            move_tiles(tiles, "up")
            oled.display(image1)
        elif downbutton.is_pressed:
            downbutton.wait_for_release()
            move_tiles(tiles, "down")
            oled.display(image1)
        drawback(tiles)
        

if __name__ == "__main__":
    main()