from api import Pianka
from os import system
from time import sleep

def exit():
    
    root.draw.rectangle((0,0,128,64), fill=0)
    root.draw.rectangle((20, 20, 108, 51), outline=255, fill=255)
    root.draw.rectangle((22, 22, 106, 49), outline=255, fill=0)
    root.draw.text((30,28), "Shutdown?", fill=255, font=root.fonts.get("fontbold"))
    root.display()
    #draw.bitmap((120,0), scrollicon,fill=255)
if __name__ == "__main__":
    root = Pianka("./config.yml")
                                                                                
    
    apps = [
        {"name": "Snake","icon":root.icons["snakeicon"]},
        {"name": "MP3 Player","icon":root.icons["mp3icon"]},
        {"name": "Legacy apps","icon":root.icons["legacyappsicon"]},
        {"name": "Wifi","icon":root.icons["wifiicon"]},
        {"name": "BadUSB","icon":root.icons["usbicon"]},
        {"name": "Counter","icon":root.icons["countericon"]},
        {"name": "3D Box","icon":root.icons["boxicon"]},
        {"name": "Settings","icon":root.icons["settingsicon"]},
    ]
    appslibrary = {
        "Snake":"snake.py",
        "MP3 Player":"mp3.py",
        "Legacy apps":"legacyapps.py",
        "Wifi":"wifi.py",
        "BadUSB":"badusb.py",
        "Counter":"counter.py",
        "3D box":"box.py",
    }
    exitVar = False
    while not exitVar:
        selected = root.MainMenu(apps)
        if selected == None:
            exitVar = True
            exit()
            print("exit")
            root.backbutton.wait_for_release()
            while exitVar:
                if root.okbutton.is_pressed:
                    system("sudo shutdown now")
                elif root.backbutton.is_pressed:
                    exitVar = False
                    root.backbutton.wait_for_release()
                    sleep(0.011)
                    
                elif root.offbutton.is_pressed:
                    root.draw.rectangle((0,0,128,64), fill=0)
                    system("sudo systemctl stop pianka")
            root.backbutton.wait_for_release()  
        else:   
            for i in appslibrary:
                if i == selected.get("name"): 
                    print(i)
                    selectedAppName = appslibrary.get(i)
                    break
            del root
            exec(f"import assets.apps.{selectedAppName.replace('.py','')} ")
            eval(f"assets.apps.{selectedAppName.replace('.py','')}.main()") 
            root = Pianka("./config.yml")
    
