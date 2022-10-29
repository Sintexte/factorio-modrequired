class Mod:
    def __init__(self, id="", version=0):
        self.link           = ""
        self.id             = id
        self.name           = ""
        self.owner          = ""
        self.category       = ""
        self.downloads      = 0
        self.requiredmods   = []#MOD
        self.optionalmods   = []#MOD
        self.incompatible   = []#MOD
        self.json           = {}
        self.sumarry        = ""
        self.version        = version
        self.factorioversion= ""
        self.idandzip       = ""
        self.storage_link   = "https://factorio-launcher-mods.storage.googleapis.com"
        self.infodomain     = "https://1488.me/factorio/mods/modinfo?id="
        self.downloadlink   = f"{self.storage_link}/{id}/{version}.zip"
        self.infolink       = f"{self.infodomain}{self.id}"
        self.allmods= []

    def __eq__(self, other):
        return self.id == self.id or self.downloadlink == self.downloadlink
    def __hash__(self) -> int:
        return hash(('id', self.id,
                 'downloadlink', self.downloadlink))
    def getinfolink(self):
        return  self.infolink
    def setinfolink(self):
        self.infolink = f"{self.infodomain}{self.id}"
    '''
    def __init__(self):
        self.link           = ""
        self.id             = ""
        self.name           = ""
        self.owner          = ""
        self.category       = ""
        self.downloads      = 0
        self.requiredmods   = [Mod]
        self.optionalmods   = [Mod]
        self.avoidmods      = [Mod]
        self.downloadlink   = ""
        self.json           = {}
        self.sumarry        = ""
        self.version        = ""
        self.factorioversion= ""
        self.idandzip       = ""
        self.storage_link   = "https://factorio-launcher-mods.storage.googleapis.com"
    '''
    def _init_idversion_(self, id ,version):
        self.id = id
        self.version = version

    def getname(self):
        return self.name

    def setjson(self,json):
        self.json = json
    
    def setid(self, id):
        self.id = id
    def setversion(self, version):
        self.version = version
    def _addmodependeciefromidandversion(self, stype, idandversion):
        #0 what something  wrong
        #1 requried mod null
        #2 optional mod ?
        #3 incompatible mod ! not gonna implement
        #4 TF ?
        #5 weird example: (?) WaterAsAResource >= 0.7.8 and no not an incompatible mod
        if(stype!=1 and stype<=4):
            idandversion = idandversion[2:]
        elif(stype==5):
            idandversion = idandversion[4:]
        id = ""
        version = ""
        collenctingid = True
        for x in idandversion:
            if(collenctingid):
                if(x == " "):
                    #collenting version
                    collenctingid = False
                    version = idandversion[len(id)+4:]
                else:
                    id+=x
        if(stype == 1):
            if(id!="base"):
                self.requiredmods.append(Mod(id,version))
        elif(stype == 3):
            self.incompatible.append(Mod(id,version))
        else:
            self.optionalmods.append(Mod(id,version))
        
                

    def getinformationfromjson(self):
        try:
            self.category   = self.json["category"]
        except:
            self.category   = ""
        self.id             = self.json["name"]
        try:
            self.name           = self.json["title"]
        except:
            self.name = ""
        self.owner          = self.json["owner"]
        self.downloads      = self.json["downloads_count"]
        self.sumarry        = self.json["summary"]
        self.version        = self.json["releases"][len(self.json["releases"])-1]['version']
        self.factorioversion= self.json["releases"][len(self.json["releases"])-1]["info_json"]["factorio_version"]
        self.idandzip       = f"/{self.id}/{self.version}.zip"
        self.downloadlink   = f"{self.storage_link+self.idandzip}"
        self._getalldependencies()

    def _getalldependencies(self):
        #get all dependencies
        #tmp_json = self.json["releases"][len(self.json["releases"])-1]
        dep = (self.json["releases"][len(self.json["releases"])-1]["info_json"]["dependencies"])
        for x in dep:
            dep_type = 0
            if(x[0]=="!"):
                #incompatible mod
                #not implemented
                dep_type = 3
            elif(x[0]=="?"):
                #optional mod
                dep_type = 2
            elif(x[0]=="~"):
                #optional mod ?
                dep_type = 2
            elif(x[:3] == "(?)"):
                dep_type = 5
            elif(x[0].isalnum()):
                #required mod
                dep_type = 1
            else:
                dep_type = 2
            self._addmodependeciefromidandversion(dep_type,x)
    
    # Have to work more on  the recursive part  only work on surface level of  all required dependencie but doesnt  do the 
    # required dependencie of  the required dependencies for the  require dependencie
    # not deep down for each dependecie possible ever
    # get required mods for the required mods
    def returnall_requiredmods(self):
        list_ = self.requiredmods
        if(len(self.requiredmods)>0):
            for x in self.requiredmods:
                list_ += x.returnall_requiredmods()
        return list_
    
    def returnall_requiredmods_foroptional(self):
        #list_ = self.requiredmods
        list_ = []
        if(len(self.requiredmods)>0):
            for x in self.optionalmods:
                list_ += x.returnall_requiredmods()
        return list_

    #get optional mods for  optional mods
    def returnall_optionalmods_foroptional(self):
        list_ = self.optionalmods
        if(len(self.optionalmods)>0):
            for x in self.optionalmods:
                list_ += x.returnall_optionalmods_foroptional()
        return list_
    

    #get optional mods for required mods
    def returnall_optionalmods_forequired(self):
        #list_ = self.optionalmods
        list_ = []
        if(len(self.optionalmods)>0):
            for x in self.requiredmods:
                list_ += x.returnall_optionalmods_forequired()
        return list_

    def __str__(self):
        text = ""
        text += (f"\t\tID: {self.id}\n")
        text += (f"\t\tName: {self.name}\n")
        text += (f"\t\tOwner: {self.owner}\n")
        text += (f"\t\tCategory: {self.category}\n")
        text += (f"\t\tDownloads: {self.downloads}\n")
        text += (f"\t\tSummarry: {self.sumarry}\n")
        text += (f"\t\tVersion: {self.version}\n")
        text += (f"\t\tGame Version: {self.factorioversion}\n")
        text += (f"\t\tOwner: {self.owner}\n")
        text += (f"\t\tDownload Link: {self.downloadlink}\n")
        text += (f"\t\tInfo Link (json): {self.infolink}\n")
        text += (f"\t\tRequired Mods (surface  level): {len(self.requiredmods)}\n")
        text += (f"\t\tOptional Mods (surface  level): {len(self.optionalmods)}\n")
        text += (f"\t\tGame Breaking Mods (surface  level): {len(self.incompatible)}\n")
        return text