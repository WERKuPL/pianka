
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi,i2c
from luma.oled.device import sh1106,ssd1306  
from yaml import safe_load as ymlload
from gpiozero import Button
from time import sleep
class Pianka:
    def __init__(self,config: str):
        with open(config,"r") as f:
            self.config  = ymlload(f)
        if self.config["display"].get("spi") is not None:
            #print(self.config["display"]["spi"]["device"],self.config["display"]["spi"]["port"])
            #self.serial = spi(device=0, port=0)
            self.serial=spi(device=self.config["display"]["spi"]["device"], port=self.config["display"]["spi"]["port"])
    
        elif self.config["display"].get("i2c") is not None:
            self.serial = i2c(port=1, address=0x3C)
        else:
            print(self.config)
            raise Exception("can't find serial") 
        if self.config["display"].get("rotate") == None:
            self.deviceRotate = 2
        else:
            self.deviceRotate = self.config["display"].get("rotate") 
        if self.config["display"]["screen"] == "sh1106":
            screen =sh1106(self.serial, rotate=self.deviceRotate)
        elif self.config["display"]["screen"] == "ssd1306":
            screen = ssd1306(self.serial, rotate=self.deviceRotate)
        self.screen = screen
        self.downbutton = Button(self.config["buttons"]["downbutton"])
        self.upbutton = Button(self.config["buttons"]["upbutton"])
        self.leftbutton = Button(self.config["buttons"]["leftbutton"])
        self.rightbutton = Button(self.config["buttons"]["rightbutton"])
        self.okbutton = Button(self.config["buttons"]["okbutton"])                   
        self.backbutton = Button(self.config["buttons"]["backbutton"])
        self.offbutton = Button(self.config["buttons"]["offbutton"])
        self.image = Image.new('1', (128, 64))
        self.draw = ImageDraw.Draw(self.image)
        self.icons = {}
        self.fonts = {}
        for i in self.config["fonts"]:
            self.fonts[i["name"]] = ImageFont.truetype(i["path"], i["size"])
        for i in self.config["bitmaps"]:
            self.icons[i["name"]] = Image.open(i["path"]).convert('1')


    def __del__(self):
        self.downbutton.close()
        self.upbutton.close()
        self.leftbutton.close()
        self.rightbutton.close()
        self.okbutton.close()  
        self.backbutton.close()
        self.offbutton.close()        
    def display(self):
        self.screen.display(self.image)
    def drawBitmap(self,xy: tuple, Image,color: int):
        """0=black 255=white"""
        self.draw.bitmap(xy,Image,color)
    def drawRec(self,xy: tuple, fill):
        self.draw.rectangle(xy,fill )
    def drawLine(self,xy: tuple, fill, width):
        self.draw.line(xy,fill,width)
    
    def MainMenu(self,applist: list):
        """[{"name": "1","icon":self.icons[mp3icon]},{"name": "2","icon":self.icons[snakeicon]},{"name": "3","icon":self.icons[legacyappsicon]},{"name": "4","icon":self.icons[boxicon]}]"""
        current_app = 0
        def drawCurrnetMenu():
            def drawapp(posision,app):
                if  posision == "up":
                    self.draw.bitmap((4,2), applist[app].get("icon"),fill=255)
                    self.draw.text((24,5), applist[app].get("name"), font=self.fonts["font"],fill=255)
                elif posision == "middle":
                    self.draw.bitmap((4,24), applist[app].get("icon"),fill=255)
                    self.draw.text((24,25), applist[app].get("name"), font=self.fonts["font"],fill=255)
                elif posision == "down":
                    self.draw.bitmap((4,46), applist[app].get("icon"),fill=255)
                    self.draw.text((24,45), applist[app].get("name"), font=self.fonts["font"],fill=255)
                elif  posision == "upf":
                    self.draw.bitmap((4,2), applist[app].get("icon"),fill=255)
                    self.draw.text((24,5), applist[app].get("name"), font=self.fonts["fontbold"],fill=255)
                elif posision == "middlef":
                    self.draw.bitmap((4,24), applist[app].get("icon"),fill=255)
                    self.draw.text((24,25), applist[app].get("name"), font=self.fonts["fontbold"],fill=255)
                elif posision == "downf":
                    self.draw.bitmap((4,46), applist[app].get("icon"),fill=255)
                    self.draw.text((24,45), applist[app].get("name"), font=self.fonts["fontbold"],fill=255)
            self.draw.rectangle((0 ,0, 128, 64), outline=0, fill=0)
            if current_app+1 >= len(applist):
                drawapp("up",current_app-2)
                drawapp("middle",current_app-1)
                drawapp("downf",current_app)
                self.draw.bitmap((-1,43), self.icons.get("outlineicon"),fill=255)
            elif current_app <= 0:
                drawapp("upf",current_app)
                drawapp("middle",current_app+1)
                drawapp("down",current_app+2)
                self.draw.bitmap((-1,1), self.icons.get("outlineicon"),fill=255)
            else:    

                drawapp("up",current_app-1)
                drawapp("middlef",current_app)
                drawapp("down",current_app+1)
                self.draw.bitmap((-1,22), self.icons.get("outlineicon"),fill=255)
            self.draw.bitmap((119,0), self.icons.get("scrollicon"),fill=255)
            self.draw.rectangle((124,int(64/len(applist))*current_app,126,int(64/len(applist))*current_app+7), fill=255)
        drawCurrnetMenu()
        self.display()
        while True:
            if self.downbutton.is_pressed:
                if current_app+1 >= len(applist)-1:
                    current_app  = len(applist)-1
                else:
                    current_app = current_app  + 1
                drawCurrnetMenu()
                self.display()
                self.downbutton.wait_for_release()
            elif self.upbutton.is_pressed:
            
                if current_app -1 <= -1:
                    current_app  = 0
                else:
                    current_app  = current_app  - 1
                drawCurrnetMenu()
                self.display()
                self.upbutton.wait_for_release()
            elif self.okbutton.is_pressed:
                return applist[current_app]
            elif self.backbutton.is_pressed:
                return None
            elif self.offbutton.is_pressed:
                self.draw.rectangle((0,0,128,64), fill=0)
                self.display()
                
                self.offbutton.wait_for_release()
                sleep(0.5)
                self.offbutton.wait_for_press()
                drawCurrnetMenu()
                self.display()
                self.offbutton.wait_for_release()
                sleep(0.5)

    def KeybordInput(self,Title: str,startText: str, maxChars: int):
        """"max value of chars is 20"""
        def drawUpperMenu(title:str,text:str):
            
            self.draw.bitmap((2,12), self.icons.get("TextOutlineicon"),fill=255)
            self.draw.text((3,-2), Title, font=self.fonts["font14"],fill=255)
            self.draw.text((7,12), startText, font=self.fonts["fontmidle"],fill=255)
        def drawFullKeyboard(pressedkey:str,caps:bool):

            def drawKeyboard(currentKey: str,caps: bool, color: int):
                if caps == False:
                    match currentKey:
                        case "q":
                            self.draw.text((4,23),"q",fill=color,font=self.fonts["font"])
                        case "a":
                            self.draw.text((4,35),"a",fill=color,font=self.fonts["font"])
                        case "z":
                            self.draw.text((4,47),"z",fill=color,font=self.fonts["font"])


                        case "w":
                            self.draw.text((13,23),"w",fill=color,font=self.fonts["font"])
                        case "s":
                            self.draw.text((13,35),"s",fill=color,font=self.fonts["font"])
                        case "x":
                            self.draw.text((13,47),"x",fill=color,font=self.fonts["font"])


                        case "e":
                            self.draw.text((22,23),"e",fill=color,font=self.fonts["font"])
                        case "d":
                            self.draw.text((22,35),"d",fill=color,font=self.fonts["font"])
                        case "c":
                            self.draw.text((22,47),"c",fill=color,font=self.fonts["font"])

                        case "r":
                            self.draw.text((31,23),"r",fill=color,font=self.fonts["font"])
                        case "f":
                            self.draw.text((31,35),"f",fill=color,font=self.fonts["font"])
                        case "v":
                            self.draw.text((31,47),"v",fill=color,font=self.fonts["font"])

                        case "t":
                            self.draw.text((40,23),"t",fill=color,font=self.fonts["font"])
                        case "g":
                            self.draw.text((40,35),"g",fill=color,font=self.fonts["font"])
                        case "b":
                            self.draw.text((40,47),"b",fill=color,font=self.fonts["font"])

                        case "y":
                            self.draw.text((49,23),"y",fill=color,font=self.fonts["font"])
                        case "h":
                            self.draw.text((49,35),"h",fill=color,font=self.fonts["font"])
                        case "n":
                            self.draw.text((49,47),"n",fill=color,font=self.fonts["font"])
                        case "u":
                            self.draw.text((58,23),"u",fill=color,font=self.fonts["font"])
                        case "j":
                            self.draw.text((58,35),"j",fill=color,font=self.fonts["font"])
                        case "m":
                            self.draw.text((58,47),"m",fill=color,font=self.fonts["font"])
                        case "i":
                            self.draw.text((67,23),"i",fill=color,font=self.fonts["font"])
                        case "k":
                            self.draw.text((67,35),"k",fill=color,font=self.fonts["font"])
                        case "o":
                            self.draw.text((76,23),"o",fill=color,font=self.fonts["font"])
                        case "l":
                            self.draw.text((76,35),"l",fill=color,font=self.fonts["font"])
                        case "p":
                            self.draw.text((85,23),"p",fill=color,font=self.fonts["font"])

                elif caps == True:
                    match currentKey:
                        case "_":
                            self.draw.text((69,47),"_",fill=color,font=self.fonts["font"])

                        case "q":
                            self.draw.text((4,23),"Q",fill=color,font=self.fonts["font"])
                        case "a":
                            self.draw.text((4,35),"A",fill=color,font=self.fonts["font"])
                        case "z":
                            self.draw.text((4,47),"Z",fill=color,font=self.fonts["font"])

                        case "w":
                            self.draw.text((13,23),"W",fill=color,font=self.fonts["font"])
                        case "s":
                            self.draw.text((13,35),"S",fill=color,font=self.fonts["font"])
                        case "x":
                            self.draw.text((13,47),"X",fill=color,font=self.fonts["font"])


                        case "e":
                            self.draw.text((22,23),"E",fill=color,font=self.fonts["font"])
                        case "d":
                            self.draw.text((22,35),"D",fill=color,font=self.fonts["font"])
                        case "c":
                            self.draw.text((22,47),"C",fill=color,font=self.fonts["font"])

                        case "r":
                            self.draw.text((31,23),"R",fill=color,font=self.fonts["font"])
                        case "f":
                            self.draw.text((31,35),"F",fill=color,font=self.fonts["font"])
                        case "v":
                            self.draw.text((31,47),"V",fill=color,font=self.fonts["font"])

                        case "t":
                            self.draw.text((40,23),"T",fill=color,font=self.fonts["font"])
                        case "g":
                            self.draw.text((40,35),"G",fill=color,font=self.fonts["font"])
                        case "b":
                            self.draw.text((40,47),"B",fill=color,font=self.fonts["font"])

                        case "y":
                            self.draw.text((49,23),"Y",fill=color,font=self.fonts["font"])
                        case "h":
                            self.draw.text((49,35),"H",fill=color,font=self.fonts["font"])
                        case "n":
                            self.draw.text((49,47),"N",fill=color,font=self.fonts["font"])
                        case "u":
                            self.draw.text((58,23),"U",fill=color,font=self.fonts["font"])
                        case "j":
                            self.draw.text((58,35),"J",fill=color,font=self.fonts["font"])
                        case "m":
                            self.draw.text((58,47),"M",fill=color,font=self.fonts["font"])
                        case "i":
                            self.draw.text((67,23),"I",fill=color,font=self.fonts["font"])
                        case "k":
                            self.draw.text((67,35),"K",fill=color,font=self.fonts["font"])
                        case "o":
                            self.draw.text((76,23),"O",fill=color,font=self.fonts["font"])
                        case "l":
                            self.draw.text((76,35),"L",fill=color,font=self.fonts["font"])
                        case "p":
                            self.draw.text((85,23),"P",fill=color,font=self.fonts["font"])
                match currentKey:

                    case "0":
                        self.draw.text((94,23),"0",fill=color,font=self.fonts["font"])
                    case "1":
                        self.draw.text((103,23),"1",fill=color,font=self.fonts["font"])
                    case "2":
                        self.draw.text((112,23),"2",fill=color,font=self.fonts["font"])
                    case "3":
                        self.draw.text((121,23),"3",fill=color,font=self.fonts["font"])
                    case "4":
                        self.draw.text((103,35),"4",fill=color,font=self.fonts["font"])
                    case "5":
                        self.draw.text((112,35),"5",fill=color,font=self.fonts["font"])
                    case "6":
                        self.draw.text((121,35),"6",fill=color,font=self.fonts["font"])
                    case "7":
                        self.draw.text((103,47),"7",fill=color,font=self.fonts["font"])
                    case "8":
                        self.draw.text((112,47),"8",fill=color,font=self.fonts["font"])
                    case "9":
                        self.draw.text((121,47),"9",fill=color,font=self.fonts["font"])
        
            drawKeyboard("q",caps)
            drawKeyboard("a",caps)
            drawKeyboard("z",caps)
            drawKeyboard("w",caps)
            drawKeyboard("x",caps)
            drawKeyboard("e",caps)
            drawKeyboard("d",caps)
            drawKeyboard("c",caps)
            drawKeyboard("r",caps)
            drawKeyboard("f",caps)
            drawKeyboard("v",caps)
            drawKeyboard("t",caps)
            drawKeyboard("g",caps)
            drawKeyboard("b",caps)
            drawKeyboard("y",caps)
            drawKeyboard("h",caps)
            drawKeyboard("n",caps)
            drawKeyboard("u",caps)
            drawKeyboard("j",caps)
            drawKeyboard("m",caps)
            drawKeyboard("i",caps)
            drawKeyboard("k",caps)
            drawKeyboard("o",caps)
            drawKeyboard("l",caps)
            drawKeyboard("p",caps)
            drawKeyboard("_",caps)
            drawKeyboard("0",caps)
            drawKeyboard("1",caps)
            drawKeyboard("2",caps)
            drawKeyboard("3",caps)
            drawKeyboard("4",caps)
            drawKeyboard("5",caps)
            drawKeyboard("6",caps)
            drawKeyboard("7",caps)
            drawKeyboard("8",caps)
            drawKeyboard("9",caps)

        drawUpperMenu(Title,startText)
        drawFullKeyboard("a",False)
    def Submenu(self):
        pass
    def SetMenu(self):
        pass
    def ButtonMenu(self):
        pass
    def ConfirmMenu(self):
        pass


