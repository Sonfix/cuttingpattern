from .edi_body import EdiBody
from .edi_defines import EdiVersion
from .edi_body import EdiBody
from .edi_header import EdiHeader

import json

class EdiFile():
    def __init__(self):
        '''
            Inits the edi file classes.
        '''

    def ImportFromEdiFile(self, file):
        '''
            file will be a list of lines of a file!
            A file contains header information and also the cutting information, alias body
        '''
        #determine edi version
        self.file = file
        idx, value = self.getEndOf(0)
        
        ver, info = self.determineVerison(value)
        if ver.value == EdiVersion.HC_NO_VER.value:
            return
        
        if info:
            idx = 0

        #join lines for parsing
        self.Header = EdiHeader("".join(file[idx:]))        
        self.Header.setVersion(ver.value)
        
        self.Body = EdiBody()
        self.Body.parseCuttingCodeFromEdiFile(ver.value, "".join(file[idx:]), self.Header)

        return self
    
    def ExportToJson(self):
        '''
         exports header and body in json format
        '''
        result = {
            "Header" : self.Header.exportToJson(),
            "Body" : self.Body.exportToJson()
        }
        return json.dumps(result)

    def determineVerison(self, file):
        '''
            Given the plain file the function will get the Version
            The file version is given with in the first line of the file, and it needs to be there
            if there is none the function will check for certain beginnings
        '''
        if not file.startswith('HEGLACUT'):
            if file.startswith('['):
                return EdiVersion.HC_4_1, 1
            elif file.startswith('<Layout>'):
                return EdiVersion.HC_5, 1
            else:
                return EdiVersion.HC_NO_VER
        elif file.startswith('HEGLACUT050'):
            return EdiVersion.HC_5, 0
        else:
            return EdiVersion.HC_4_1, 0
        
        #if none of these could determine the version its maybe the json format

    def __str__(self) -> str:
        return f"{self.Body.exportToJson()}"

    def getEndOf(self, index, find={" ", "\n"}):
        EndPos = next(i for i,c in enumerate(self.file[index:]) if c in find)
        value = self.file[index : (index + EndPos)]
        return index + EndPos, value

