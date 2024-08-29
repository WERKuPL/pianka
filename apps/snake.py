import sys
sys.path.append('/home/werku/pianka')
import piankamain #import *
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import random
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
SPEED = 0.2

long_game_over = False

class Snake:
    
    def __init__(self):
        self.body_size = 3
        self.coordinates = []
        self.squares = []
        for i in range(0, 3):
            self.coordinates.append([15, 15])
        for x, y in self.coordinates:
            square = pixel(0, 0)
            #print(self.coordinates)
            self.squares.append(square)
        
            

class Food:
    
    def __init__(self):
        x = random.randint(0,30)
        y = random.randint(0,28)
        #x = 30
        #y = 28
        self.coordinates = [x,y]

        pixel(x, y)

def pixel(xb, yb): 
    xb = xb * 2
    yb = yb * 2
    draw.rectangle((xb + 64, yb + 4, xb + 65, yb + 5), outline=255, fill=white)

def next_turn(snake, food):
    while True:    
        x, y = snake.coordinates[0]
        global score                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        
        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        snake.coordinates.insert(0,(x, y))
        draw.rectangle((0, 0, 128, 64), outline=0, fill=black)
        draw.rectangle((60, 0, 128, 64), outline=255, fill=white)
        draw.rectangle((62, 2, 126, 62), outline=255, fill=black)
        draw.text((10,10), text="Score", fill=255)
        draw.text((10,25), text=str(score), fill=255)
        #print(snake.coordinates)
        #print(snake.coordinates[1])
        for i in range(0 ,len(snake.coordinates)):
                #print("end")
                cordinates_x = [x for x,y in snake.coordinates]
                cordinates_y = [y for x,y in snake.coordinates]
                #print(snake.coordinates)
                #print(direction)
                pixel(cordinates_x[i], cordinates_y[i])
        pixel(food.coordinates[0],food.coordinates[1])
        square = pixel(x, y)

        snake.squares.insert(0,square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            score += 1
            food = Food()
        else:

            del snake.coordinates[-1]

            del snake.squares[-1]
        if check_collision(snake):
            game_over()
            break
        else:
            oled.display(image1)
            sleep(SPEED)
        #next_turn(snake, food) 
    
def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction !='right':
            direction = new_direction
            #print("left set")
    elif new_direction == 'up':
        if direction !='down':
            direction = new_direction
            #print("up set")
    elif new_direction == 'down':
        if direction !='up':
            direction = new_direction
            #print("down set")
    if new_direction == 'right':
        if direction !='left':
            direction = new_direction
            #print("right set")
    


    
def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or  x >= 31:
        print("over by x") 
        return True
    elif y < 0 or y >= 29:
        print("over by y")
        return True
    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            print("over by colider")
            
            return True
    return False
def game_over():
    draw.rectangle((0, 0, 128, 64), outline=0, fill=black)
    draw.text((10,10), text="Score", fill=white)
    draw.text((10,25), text=str(score), fill=white)

   
    if long_game_over == True: 
        draw.text((50,13), text="KONIEC GRY", fill=white)
        draw.text((40,23), text="Wszystko bedzie", fill=white)
        draw.text((40,33), text="dobrze", fill=white)
        #draw.text((50,43), text="poddac")
        oled.display(image1)
    
        okbutton.wait_for_press()
        okbutton.wait_for_release()
        draw.rectangle((30, 23, 128, 50), outline=0, fill=black)
        draw.text((40,23), text="Graczu", fill=white)
        draw.text((40,33), text="Determinacji", fill=white)
        oled.display(image1)
        
        sleep(1)
    else:
        draw.text((50,13), text="KONIEC GRY", fill=white)
        oled.display(image1)
    okbutton.wait_for_press()
    
def main():
    global direction,oled,draw,image1,okbutton,upbutton,downbutton,leftbutton,rightbutton,backbutton,offbutton,white,black,score
    downbutton = Button(19)
    upbutton = Button(6)
    leftbutton = Button(5)
    rightbutton = Button(26)
    okbutton = Button(21)                   
    backbutton = Button(16)
    offbutton = Button(13)
    white = 255
    black = 0
    score = 0
    oled = sh1106(spi(device=0, port=0, ),rotate=2)
    image1 = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image1)


    score = 0
    direction = "down"
    draw.rectangle((0, 0, 128, 64), outline=0, fill=black)
    draw.rectangle((60, 0, 128, 64), outline=255, fill=white)
    draw.rectangle((62, 2, 126, 62), outline=255, fill=black)
    draw.text((10,10), text="Score")
    draw.text((10,25), text=str(score))
    oled.display(image1)
    leftbutton.when_pressed = lambda: change_direction('left')
    rightbutton.when_pressed = lambda: change_direction('right')
    upbutton.when_pressed = lambda: change_direction('up')
    downbutton.when_pressed = lambda: change_direction('down')
    snake = Snake()
    food = Food()
    next_turn(snake, food)
    okbutton.close()
    downbutton.close()
    upbutton.close()
    leftbutton.close()
    rightbutton.close()
    backbutton.close()
    offbutton.close() 
if __name__ == "__main__":
 
    main()
      
#draw.rectangle((64, 0, 128, 64), outline=0, fill=white)
#oled.ShowImage(oled.getbuffer(image1))
