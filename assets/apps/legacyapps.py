import sys,os,time,glob
sys.path.insert(1, '/home/werku/pianka')
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.oled.device import sh1106


white = 255
black = 0
def menuinit():
    oled.clear()
    draw.rectangle((0 ,0, 128, 64), outline=255, fill=white)
    draw.rectangle((1, 1, 126, 62), outline=0, fill=black)
def menu():
    global files,ffile,pliki,oled,draw

    draw.rectangle((1, 1, 126, 62), outline=0, fill=black)
    if y_pointer == 0: 
        draw.text((9,5), pliki[y_pointer], fill=white, font=font)
        draw.text((9,16), pliki[y_pointer+1], fill=white, font=font)
        draw.text((9,27), pliki[y_pointer+2], fill=white, font=font)
        draw.text((9,38), pliki[y_pointer+3], fill=white, font=font)
        pointer(0)
    elif y_pointer == len(pliki)-1:
        draw.text((9,5), pliki[y_pointer-3], fill=white, font=font)
        draw.text((9,16), pliki[y_pointer-2], fill=white, font=font)
        draw.text((9,27), pliki[y_pointer-1], fill=white, font=font)
        draw.text((9,38), pliki[y_pointer], fill=white, font=font)
        pointer(3)
    elif y_pointer == len(pliki)-2:
        draw.text((9,5), pliki[y_pointer-2], fill=white, font=font)
        draw.text((9,16), pliki[y_pointer-1], fill=white, font=font)
        draw.text((9,27), pliki[y_pointer], fill=white, font=font)
        draw.text((9,38), pliki[y_pointer+1], fill=white, font=font)
        pointer(2)
    else:
        draw.text((9,5), pliki[y_pointer-1], fill=white, font=font)
        draw.text((9,16), pliki[y_pointer], fill=white, font=font)
        draw.text((9,27), pliki[y_pointer+1], fill=white, font=font)
        draw.text((9,38), pliki[y_pointer+2], fill=white, font=font)
        pointer(1)
    #ytext = 5
    #for i in range(len(pliki)): 
    #    draw.text((10,ytext), pliki[i], fill=white, size=0,font=font)
    #    ytext = ytext+11
    #oled.display(image1)

def pointer(pointer_at):
    global files,ffile,pliki,oled,draw
    if pointer_at == 0 and len(pliki) >=  1:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,9 , 8, 13), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
    elif pointer_at == 1 and len(pliki) >=  2:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,20 , 8, 24), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
    elif pointer_at == 2 and len(pliki) >=  3:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,31 , 8, 35), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
    elif pointer_at == 3 and len(pliki) >=  4:
        draw.rectangle((5 ,9 , 8, 46), outline=0, fill=black)
        draw.rectangle((5 ,42 , 8, 46), outline=0, fill=white)
        print(str(pointer_at) + " at")
        oled.display(image1)
def full():
    global files,ffile,pliki,oled,draw,y_pointer,is_exit,downbutton,upbutton,okbutton,offbutton,backbutton, leftbutton,rightbutton,image1
    while True:
        if y_pointer <= -1:

            y_pointer = 0
            menu()
        elif y_pointer >= len(pliki):
            y_pointer = len(pliki)-1
        if downbutton.is_pressed:
            if y_pointer+1 >= len(pliki)-1:
                y_pointer = len(pliki)-1
            else:
                y_pointer = y_pointer + 1
            
            menu()
            downbutton.wait_for_release()
            time.sleep(0.3)
            print("down")
            print(y_pointer)
            
            oled.display(image1)
        elif upbutton.is_pressed:
           
            if y_pointer-1 <= -1:
                y_pointer = 0
            else:
                y_pointer = y_pointer - 1
            menu()

            upbutton.wait_for_release()
            print("up")
            print(y_pointer)
            time.sleep(0.3)
            
    
        elif backbutton.is_pressed:
              
            downbutton.close()
            upbutton.close()
            leftbutton.close()
            rightbutton.close()
            okbutton.close()                   
            backbutton.close()
            offbutton.close()
            break            
        elif offbutton.is_pressed:
            draw.rectangle((0,0,128,64), fill=black)
            oled.display(image1)
            time.sleep(1)
            offbutton.wait_for_press()
            menuinit()
            menu()
           
            time.sleep(1)
        elif okbutton.is_pressed:
            
            
            downbutton.close()
            upbutton.close()
            leftbutton.close()
            rightbutton.close()
            okbutton.close()                   
            backbutton.close()
            offbutton.close()
            print("open")

            
            filename = pliki[y_pointer].replace(".py","")
            exec(f"import apps.{filename}")
            eval(f"apps.{filename}.main()")







                
            #os.system("~/pianka/bin/python ~/pianka/piankamain.py")
            print("exit from program")
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
            menuinit()
            menu()
            
                
             
    
     
# STARTING PROGRAM
def main():
    global oled,image1,draw,downbutton,upbutton,rightbutton,leftbutton,okbutton,backbutton,offbutton,is_exit,y_pointer,pliki,font
    font = ImageFont.truetype("Arial.ttf", 10)
    pliki= []
    for files in glob.glob("./apps/*.py"):
        ffile = files.replace("./apps/","")
        pliki.append(ffile)
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
    is_exit = False
    y_pointer = 0
    menuinit()
    menu()
    full()
if __name__ == "__main__":
    main()
