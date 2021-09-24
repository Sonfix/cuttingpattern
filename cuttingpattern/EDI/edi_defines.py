from enum import Enum

class EdiVersion(Enum):
    HC_1 = 1
    HC_2 = 2
    HC_3 = 3
    HC_4 = 4
    HC_4_1 = 5
    HC_5 = 6 # since HeglaCut version 5 we got xml files

    HC_JSON_1 = 7
    HC_NO_VER = 0xFFFF

class EdiCutTypes(Enum):
    X = 1
    Y = 2
    Z = 3
    V = 4
    W = 5
    NO_CUT = 6

class EdiCut():
    def __init__(self, cutType):
        self.CutType = cutType
    
    def getNextCutType(self):
        '''
            returns the nex cut type
        '''
        if self.CutType == EdiCutTypes.X:
            return "Y"
        if self.CutType == EdiCutTypes.Y:
            return "Z"
        if self.CutType == EdiCutTypes.Z:
            return "V"
        if self.CutType == EdiCutTypes.V:
            return "V"
        if self.CutType == EdiCutTypes.W:
            return ""
        else:
            return ""   

    def __str__(self):
        '''
            returns EdiCutTypes Type matching the given cut
        '''
        if self.CutType == EdiCutTypes.X:
            return "X"
        if self.CutType == EdiCutTypes.Y:
            return "Y"
        if self.CutType == EdiCutTypes.Z:
            return "Z"
        if self.CutType == EdiCutTypes.V:
            return "V"
        if self.CutType == EdiCutTypes.W:
            return "W"
        else:
            return ""

    def __hash__(self) -> int:
        return hash(self.CutType)

    def __eq__(self, other):
        return (self.CutType) == (other.CutType)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


class EdiTraverseInfo():
    def __init__(self, id):
        self.TravId = "T" + id
        self.InfoTexts = {}
    
    def getInfoTexts(self):
        return self.InfoTexts

    def append(self, key, val):
        self.InfoTexts[key] = val
        return self

    def __str__(self):
        s = ""
        for elem in self.InfoTexts:
            s += "Key: " + elem + " Value: " + self.InfoTexts[elem]
        return s

    def toJson(self):
        ret = {
            "TravId" : self.TravId
        }
        for elem in self.InfoTexts:
            ret[elem] = self.InfoTexts[elem]
        return ret

class ModelInformation():
    def __init__(self, modelstring):
        self.RawData = modelstring
    