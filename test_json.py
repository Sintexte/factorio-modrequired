import json 
from modclass import Mod

with open("space.json") as jsonfile:
    data = json.load(jsonfile)
    mod = Mod()
    mod.setjson(data)
    mod.getinformationfromjson()
    print(mod.__str__()) 
    t = mod.returnall_requiredmods()
    for x in t:
        print(x)
    print(len(t))