#ALOT OF BUGS
#MADE IN 06/07/2022 till 07/07/2022
#Work the whole on it
#probably will never recode
#works sometimes
#thanks radioegor146

import json
import requests
import validators
from urllib.parse import urlparse
from urllib import request
from modclass import Mod
import pathlib
import wget

#mod_link = "https://mods.factorio.com/mod/SeaBlock"
mod_link = "https://mods.factorio.com/mod/bobores"
required_dep = True
optional_dep = False
chooseoptional_dep = False
menu_end = False
menu_choose = 0
max_choices = 8
factorio_webdownloader = "https://1488.me/factorio/mods/modinfo?id="
mod = object
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
jsonmod = {}
storage_link = "https://factorio-launcher-mods.storage.googleapis.com/"
init = False
cleaned = False
all_mods = []
downloadable_dict = dict()
#Log Only
def log(str,option=0, rl=True):
    #0 normal log as such []  Text | DEFAULT
    #1 input log as such  []: Text
    #2 bad input as such  [-] Text
    #3 No idea just added it

    #rl for  ReturnLine
    end_ = ""
    if(rl == True):
        end_ = "\n"
    if(option == 0):
        print(f"[]  {str}",end=end_)
    elif(option == 1):
        print(f"[]: {str}",end=end_)
    elif(option==2):
        print(f"[-] {str}",end=end_)
    else:
        print(f"[!] {str}",end=end_)

#Literally the first menu you see
def first_menu():
    global menu_choose
    global mod_link
    global optional_dep
    global required_dep
    global chooseoptional_dep
    print("\n\n--=========== FACTORIO MOD DOWNLOADER ===========--")
    print(f"(mod link): {mod_link}")
    print(f"(Download All Required Dependencies ?): {required_dep}")
    print(f"(Dowbload All Optional Dependencies ?): {optional_dep}")
    print(f"[NOT IMPLEMENTED] (Download And Choose The Dependencies You Like ?): {chooseoptional_dep}\n")
    print("="*50)
    print("1) Enter Mod Link [mods.factorio.com]")
    print("2) Enable or Disable Required Dependencies")
    print("3) Enable or Disable Optional Dependencies")
    print("4) Enable Choose Optional Dependencies")
    print("5) Init All Mods [Important]")
    print("6) Download Mods")
    print("7) Show Information")
    print("8) Exit")
    print("="*50)
    print()
    try:
        menu_choose = int(input("[]: "))
    except ValueError:
        print(f"[]  input is not a number")

#Link Where You Can Change Main Mod Link
def link_menu():
    global mod_link
    global menu_choose
    print("[]  Enter Mod Link [mods.factorio.com]: ",end='')
    tmp_link = input()
    if(tmp_link == "exit"):
        menu_choose = 0
    elif(validators.url(tmp_link)):
        #check if domain is mods.factorio.com
        domain = urlparse(tmp_link).netloc
        if(domain=="mods.factorio.com"):
            mod_link = tmp_link
            menu_choose = 0
    else:
        #bad link
        print("[-] Please Retry Again, Not A Valide Link ! or type exit")

#Link to change If The Required Dep Are Wanted
def requiredep_menu():
    global menu_choose
    global required_dep

    print("[] Do You Want To Download All Required Dependecies?\n[]: Enter (y)Yes or (n)No :",end='')
    choice = input().lower()
    if(choice == 'y'):
        required_dep = True
        menu_choose = 0
    elif(choice == 'n'):
        required_dep = False
        menu_choose = 0
    else:
        print("[-] Bad Input !")

#Link to change If the Optional Dep Are Wanted
def optionaldep_menu():
    global menu_choose
    global optional_dep

    print("[]  Do You Want To Download All Optional Dependecies?\n[]: Enter (y)Yes or (n)No :",end='')
    choice = input().lower()
    if(choice == 'y'):
        optional_dep = True
        menu_choose = 0
    elif(choice == 'n'):
        optional_dep = False
        menu_choose = 0
    else:
        print("[-] Bad Input !")

#Not Implemented
def choosedep_menu():
    global menu_choose
    global chooseoptional_dep

    print("[]  Do You Want To Download And Choose Some Optional Dependecies?\n[]: Enter (y)Yes or (n)No :",end='')
    choice = input().lower()
    if(choice == 'y'):
        chooseoptional_dep = True
        menu_choose = 0
    elif(choice == 'n'):
        chooseoptional_dep = False
        menu_choose = 0
    else:
        print("[-] Bad Input !")

#Get Main Mod Information
def init_modinfo():
    global factorio_webdownloader
    global mod_link
    global menu_choose
    global jsonmod
    global required_dep
    global optional_dep
    global mod 
    global init

    init = True
    #check if link has been intered
    if(mod_link == ""):
        log("Mod Link Wasnt Entered\n")
        menu_choose = 1
    else:
        modpage = requests.get(factorio_webdownloader+mod_link[30:], headers=headers).json()
        jsonmod = modpage
        if(modpage["name"] == ""):
            #bad
            log("Mod Link Not Valid !")
            menu_choose = 0
            return
        else:
            mod = Mod('', '')
            mod.setjson(jsonmod)
            mod.getinformationfromjson()
            mod.setinfolink()
            
            log(f'{mod.id} {mod.infolink}')
            if(required_dep):
                for x in mod.requiredmods:
                    '''
                    jsonmod_ = requests.get(x.infolink, headers=headers).json()
                    x.setjson(jsonmod_)
                    x.getinformationfromjson()
                    print(x)
                    '''
                    jsonmod_ = requests.get(x.infolink, headers=headers).json()
                    x.setjson(jsonmod_)
                    x.getinformationfromjson()
                    
                    log(f'{x.id} {x.infolink}')
            if(optional_dep):
                for x in mod.optionalmods:
                    jsonmod_ = requests.get(x.infolink, headers=headers).json()
                    try:
                            x.setjson(jsonmod_)
                            x.getinformationfromjson()
                    except:
                            log("aborting an optional mod (?)")
                    
                    
                    log(f'{x.id} {x.infolink}')
            req = mod.returnall_requiredmods()
            req2 = mod.returnall_requiredmods_foroptional()
            req3 = mod.returnall_optionalmods_foroptional()
            req4 = mod.returnall_optionalmods_forequired()

            if(required_dep):
                log(f'\nRequired Mods ({len(req)+len(req2)}):',3,True)
                for x in req:
                    log(f"{x.id} {x.infolink}")
                for x in req2:
                    log(f"{x.id} {x.infolink}")
            if(optional_dep):
                log(f'\nOptional Mods ({len(req3)+len(req4)}):',3,True)
                for x in req3:
                    log(f"{x.id} {x.infolink}")
                for x in req4:
                    log(f"{x.id} {x.infolink}")
        menu_choose = 0
        return

def clean_links(array):
    #array should contain Object of class Mod
    global cleaned
    cleaned = True
    newdict = dict()
    for x in array:
        if x.id == ")":
            log(f"Pass (trashy link)")
        elif x.id  not in newdict:
            newdict[x.id] = x
        else:
            log(f"Duplicant {x.id}",4)

    log(f"Removed ({-(len(newdict)-len(array))}) Duplicante or TrashyLink Combined")
    return newdict
                


def show_information():
    global init
    global mod
    global mod_link
    global menu_choose
    global downloadable_dict
    global required_dep
    global optional_dep
    if(init and mod_link!=""):
        log(f"{mod}")
        req = mod.returnall_requiredmods()
        req2 = mod.returnall_requiredmods_foroptional()
        req3 = mod.returnall_optionalmods_foroptional()
        req4 = mod.returnall_optionalmods_forequired()
        if(required_dep):
            mod.allmods += req
        if(optional_dep):
            mod.allmods += req2
            mod.allmods += req3
            mod.allmods += req4
        if(required_dep):
            log(f'\nRequired Mods ({len(req)+len(req2)}):',3,True)
            for x in req:
                log(f"{x.id} {x.downloadlink}")
            for x in req2:
                log(f"{x.id} {x.downloadlink}")
        if(optional_dep):
            log(f'\nOptional Mods ({len(req3)+len(req4)}):',3,True)
            for x in req3:
                log(f"{x.id} {x.downloadlink}")
            for x in req4:
                log(f"{x.id} {x.downloadlink}")
        
        if(len(downloadable_dict)>0):
            log("Everything Already Set up")
            log("Showing All Mods")
            for x in downloadable_dict:
                log(x)
        else:
            log("Cleaning Some Repeated Links and Trashy ones ...")
            downloadable_dict = clean_links(mod.allmods)
            log("Showing All Mods")
            for x in downloadable_dict:
                log(x)
        
        menu_choose = 0
    elif(mod_link == ""):
        log("Please Enter mod link")
        menu_choose = 1
    else:
        log("Init Next Time")
        log("Initiliazing for you")
        menu_choose = 5
    

def download():
    global menu_choose
    global downloadable_dict
    global mod 
    global cleaned
    location = pathlib.Path().absolute()
    if(not cleaned):
        log("cleaning data")
        show_information() 

    tmplocation = pathlib.Path().absolute()
    filename = mod.id+"_"+mod.version+".zip"
    tmplocation = tmplocation.joinpath(f"{location}/mods/{(filename)}")
    log(f"Downloading {mod.id} {mod.downloadlink} at {tmplocation}")
    response = wget.download(mod.downloadlink,tmplocation.__str__())
    for x in downloadable_dict.values():
        tmplocation = pathlib.Path().absolute()
        filename = x.id+"_"+x.version+".zip"
        tmplocation = tmplocation.joinpath(f"{location}/mods/{(filename)}")
        try:
            log(f"Downloading {x.id} {x.downloadlink} at {tmplocation}")
            response = wget.download(x.downloadlink,tmplocation.__str__())
            print()
        except requests.ConnectionError as e:
            log(e)

        
    menu_choose = 0

#main function
if __name__ == "__main__":
    #main Loop
    while(not menu_end):
        if(menu_choose == 0):
            first_menu()
        elif(menu_choose == 1):
            init = False
            cleaned = False
            link_menu()
        elif(menu_choose == 2):
            cleaned = False
            requiredep_menu()
        elif(menu_choose == 3):
            cleaned = False
            optionaldep_menu()
        elif(menu_choose == 4):
            cleaned = False
            choosedep_menu()
        elif(menu_choose == 8):
            #exit
            print("[]  Exiting")
            menu_end = True
        elif(menu_choose == 5):
            init_modinfo()    
        elif(menu_choose == 6):
            if(init):
                download()
            else:
                log("Please Initilize before")
                log("Initializing for you")
                if(mod_link == ""):
                    log("Please Enter Mod Link")
                    menu_choose = 1
                else:
                    menu_choose = 5
        elif(menu_choose == 7):
            show_information()
        else:
            print(f"[]  Please Enter a Number between 1 and {max_choices}")
            menu_choose = 0