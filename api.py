
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

    def KeybordInput(self):
        pass
    def Submenu(self):
        pass
    def SetMenu(self):
        pass
    def ButtonMenu(self):
        pass
    def ConfirmMenu(self):
        pass


if __name__ == "__main__":


    root = Pianka("./config.yml")
    samplemenu = [{"name": "1","icon":root.icons["mp3icon"]},{"name": "2","icon":root.icons["snakeicon"]},{"name": "3","icon":root.icons["legacyappsicon"]},{"name": "4","icon":root.icons["boxicon"]}]
    root.MainMenu(samplemenu)