import xml.etree.ElementTree as ET
from .edi_defines import EdiVersion

class EdiHeader():
    '''
        This class contains all data from the EDI Header which we want to use
    '''
    def __init__(self, raw_data):
        self.RawData = raw_data
        self.Version = EdiVersion.HC_NO_VER
        self.ArticleCode = ""
        self.LayoutId = ""
        self.Description = ""
        self.Height = 0.0
        self.Width = 0.0
        self.Trim = {
            "left" : 0.0,
            "top" : 0.0,
            "right" : 0.0,
            "bottom" : 0.0
        }
        self.MinBreakOutDist = 0.0
        self.MinCutSize = 0.0
        self.CuttInfo = {
            "pressure" : 0,
            "speed" : 0,
            "information" : ""
        }
        self.GrindingInfo = {
            "pressure" : 0,
            "speed" : 0,
            "information" : ""
        }       

    def __str__(self):
        '''
            returns a small string for logging
        '''
        return f"{self.ArticleCode}: {self.Width}x{self.Height}"

    def setVersion(self, ver):
        '''
            set the version of the current edi file
            if RawData is set, it will parse its content automatically
        '''
        self.Version = ver
        if self.RawData != "":
            self.parseHeader(self.Version)

    def parseHeader(self, ver):
        '''
            wrapper for parsing, it decides which function will be called depending on version
        '''
        if ver > EdiVersion.HC_4_1.value:
            self.parseXML()
        else:
            self.parseOld()
    
    def parseXML(self):
        '''
            parses the xml contents of new edi version
        '''
        root = ET.fromstring(self.RawData)
        #First go to Header info and set to node elem
        node = root.find('Header')
        #than get all info
        self.ArticleCode = self.getXMLParameter(node,'ArticleNr')
        self.LayoutId = self.getXMLParameter(node, 'LayoutId')
        self.Description = self.getXMLParameter(node, 'Description')
        self.Width = self.getXMLParameter(node, 'Width', type=float)
        self.Height = self.getXMLParameter(node, 'Height', type=float)
        self.Trim["left"] = self.getXMLParameter(node, 'TrimLeft', type=float)
        self.Trim["top"] = self.getXMLParameter(node, 'TrimTop', type=float)
        self.Trim["right"] = self.getXMLParameter(node, 'TrimRight', type=float)
        self.Trim["bottom"] = self.getXMLParameter(node, 'TrimBottom', type=float)
        self.MinBreakOutDist = self.getXMLParameter(node, 'MinimumBreakoutDistance', type=float)
        self.MinCutSize = self.getXMLParameter(node, 'MinimumCutSize', type=float)
        self.CuttInfo["pressure"] = self.getXMLParameter(node, 'CuttingPressure', type=int)
        self.CuttInfo["speed"] = self.getXMLParameter(node, 'CuttingSpeed', type=int)
        self.CuttInfo["information"] = self.getXMLParameter(node, 'CuttingWheelInformation')
        self.GrindingInfo["pressure"] = self.getXMLParameter(node, 'GrindingPressure', type=int)
        self.GrindingInfo["speed"] = self.getXMLParameter(node, 'GrindingSpeed', type=int)
        self.GrindingInfo["information"] = self.getXMLParameter(node, 'GrindingWheelInformation')

    def getXMLParameter(self, node, id, type=str):
        '''
            retrieves the value of given id from the given node. Also converts the result to the given type
            Type can be [str, float, int]
        '''
        buff = node.find(id)
        if buff is not None:
            return type(buff.text)
        elif type == float:
            return type("0.0")
        elif type == int:
            return type("0")
        else:
            return type("")


    def parseOld(self): 
        '''
            parses the xml contents of new edi version
        '''
        self.ArticleCode = self.getOldParameter(self.RawData, 1, 5)
        self.LayoutId = "" #Old format does not have this
        self.Description = self.getOldParameter(self.RawData, 6, 20)
        self.Width = self.getOldParameter(self.RawData, 32, 6, type=float)
        self.Height = self.getOldParameter(self.RawData, 38, 6, type=float)
        self.Trim["left"] = self.getOldParameter(self.RawData, 50, 6, type=float)
        self.Trim["top"] = self.getOldParameter(self.RawData, 56, 6, type=float)
        self.Trim["right"] = self.getOldParameter(self.RawData, 62, 6, type=float)
        self.Trim["bottom"] = self.getOldParameter(self.RawData, 44, 6, type=float)
        self.MinBreakOutDist = self.getOldParameter(self.RawData, 73, 4, type=float)
        self.MinCutSize = self.getOldParameter(self.RawData, 38, 6, type=float)
        self.CuttInfo["pressure"] = self.RawData[95:98]
        self.CuttInfo["speed"] = self.RawData[98:101]
        self.CuttInfo["information"] = self.RawData[101:105]
        self.GrindingInfo["pressure"] = self.RawData[113:116]
        self.GrindingInfo["speed"] = self.RawData[116:119]
        self.GrindingInfo["information"] = self.RawData[119:123]

    def getOldParameter(self, data, start, length, type=str):
        '''
            retrieves the value from given data part. Also converts the result to the given type
            Type can be [str, float, int]
        '''
        if len(data) > (start + length):
            return type(data[start : start+length])
        elif type == float:
            return type("0.0")
        elif type == int:
            return type("0")
        else:
            return type("")
    
    def exportToEdiFile(self, version):
        pass
    
    def exportToJson(self):
        ret = {
            "AricleCode" : self.ArticleCode,
            "LayoutId" : self.LayoutId,
            "Description" : self.Description,
            "Height" : self.Height,
            "Widht" : self.Width,
            "Trim" : self.Trim,
            "MinBreakOutDistance" : self.MinBreakOutDist,
            "MinCutSize" : self.MinCutSize,
            "CuttingInfo" : self.CuttInfo,
            "GrindingInfo" : self.GrindingInfo
        }
        return ret

