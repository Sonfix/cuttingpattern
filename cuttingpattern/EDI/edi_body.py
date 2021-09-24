import xml.etree.ElementTree as ET
from .edi_defines import EdiTraverseInfo, EdiVersion, EdiCutTypes, EdiCut, ModelInformation

import json

def cutCharToEnum(c):
    '''
        returns EdiCutTypes Type matching the given cut
    '''
    if c == "X":
        return EdiCutTypes.X
    if c == "Y":
        return EdiCutTypes.Y
    if c == "Z":
        return EdiCutTypes.Z
    if c == "V":
        return EdiCutTypes.V
    if c == "W":
        return EdiCutTypes.W
    else:
        return EdiCutTypes.NO_CUT

class Traverse():
    def __init__(self):
        '''
         constructor inits member variables
        '''
        self.Parent = None
        self.Childs = []
    
    def appendChild(self, leaf):
        '''
         appends given leaf to childs also sets self as parent from leaf
        '''
        self.Childs.append(leaf)
        leaf.Parent = self

    
    def appendChildByPath(self, leaf):
        '''
         only calls appendChild and returns true
        '''
        self.appendChild(leaf)
        return True    
    
    def getChildByPath(self, path):
        '''
        
        '''
        for cut in path:
            if path[cut] > 0:
                if not self.Childs[path[cut] - 1].getChildByPath(path):
                    return self.Childs[path[cut] - 1]
            else:
                return None

    def toJSON(self):
        childObjs = []
        for child in self.Childs:
            childObjs.append(child.toJSON())
           

        ret = {
            "Width" : self.Width,
            "Height" : self.Height,
            "Childs" : childObjs,
            "Parent" : "self.Parent"
        }
        return ret

class TraverseNode(Traverse):
    def __init__(self, width, length):
        '''
         inits the node and set sizes to member
        '''
        super().__init__()
        self.Width = width
        self.Height = length

    def appendChild(self, leaf):
        '''
         checks leaf for X Level and appends
        '''
        if leaf.Path["X"] >= 0:
            super().appendChild(leaf)
    
    def appendChildByPath(self, leaf):
        '''
         appends the given leaf to its correct node according to the given path
        '''
        #first get the xindex of leaf 
        XIndex = leaf.Path["X"]
        #check for child to append this leaf accoring to xindex
        for c in self.Childs:
            if c.Path["X"] == XIndex:
                return c.appendChildByPath(leaf)

    def toJSON(self):
        return super().toJSON()

class Stockplate(TraverseNode):
    def __init__(self, width, length):
        '''
         inits the node and set sizes to member
        '''
        super().__init__(width, length)
    
    def __str__(self):
        return f"Stockplate: childcount: {len(self.Childs)} size {self.Width}x{self.Height}"

    def toJSON(self):
        return super().toJSON()

class TraverseLeaf(Traverse):
    def __init__(self, path, cutSize):
        '''
         inits the leaf and sets the member variables by the given information
        '''
        super().__init__()
        self.Width = 0.0
        self.Height = 0.0
        self.CutSize = cutSize
        self.Path = path
        self.CutType = self.determineActCut()
        self.Cut = EdiCut(cutCharToEnum(self.CutType))
        self.CutIndex = self.Path[self.CutType]
        self.TravId = 0
        self.TraverseInformation = None
        self.RackCode = 0
        self.ModelInformation = None

    def determineActCut(self):
        '''
         returns the actual cutting level
        '''
        last_cut = "X"
        for c in self.Path:
            if self.Path[c] == 0:
                break
            last_cut = c
        return last_cut

    
    def __str__(self):
        return f"CutType<{self.CutType}> size {self.Width}x{self.Height} {json.dumps(self.Path)}"

    def appendChildByPath(self, leaf):
        '''
         appends the leaf to mathching child according the path
        '''

        if leaf.Path[self.CutType] == self.CutIndex and EdiCut(cutCharToEnum(self.Cut.getNextCutType())) == leaf.Cut and not leaf.Path[leaf.Cut.getNextCutType()]: #if we are on the same level just append
            return super().appendChildByPath(leaf)
        else:
            res = False
            for t in self.Childs:
                res = t.appendChildByPath(leaf)
            return res
    
    def closeCut(self):
        '''
         closes the given cut by setting the size related to the parent size
        '''
        if self.Parent:
            if self.CutType == "X" or self.CutType == "Z" or self.CutType == "W":
                self.Width = self.CutSize
                self.Height = self.Parent.Height
            elif self.CutType == "Y" or self.CutType == "V":
                self.Width = self.Parent.Width
                self.Height = self.CutSize

        return self

    def setTraverseInformation(self, information):
        self.TraverseInformation = information
    
    def setModelInformation(self, information):
        self.ModelInformation = information

    def toJSON(self):
        ret = super().toJSON()
        ret["CutType"] = self.CutType
        if self.TraverseInformation is not None:
            ret["TraverseInformation"] = self.TraverseInformation.toJson()
        else:
            ret["TraverseInformation"] = {}
        if self.ModelInformation is not None:
            ret["ModelInformation"] = self.ModelInformation.RawData
        else:
            ret["ModelInformation"] = ""
        ret["RackCode"] = self.RackCode
        return ret

    def setRackCode(self, rack):
        self.RackCode = "B" + rack

class EdiBody():
    def __init__(self):
        '''
            inits Body by setting the members
        '''
        
        self.Parser = {
            "X" : self.addCut,
            "Y" : self.addCut,
            "Z" : self.addCut,
            "W" : self.addCut,
            "V" : self.addCut,
            "F" : self.addModel,
            "T" : self.addTraverseInfoId,
            "B" : self.addRackInfomation
        }

        self.TraverseCount = {
            "X" : 0,
            "Y" : 0,
            "Z" : 0,
            "V" : 0,
            "W" : 0,
        }

        self.ModelIds = {}
        self.TravIds = {}
        self.last_leaf = None

    def resetTraverseCount(self, cut):
        '''
            resets the traverse count after new cut to determine child path
        '''
        found = False
        for level in self.TraverseCount:
            if level == cut:
                found = True
            elif found:
                self.TraverseCount[level] = 0
                
            
    
    def parseCuttingCodeFromEdiFile(self, ver, file, h):
        '''
            this function parses the cutting code from the edi like a nondeterministic finite automaton (NFA)
        '''
        
        code = ""
        if ver >= EdiVersion.HC_5.value:
            root = ET.fromstring(file)
            code = root.find('CuttingCode').find('Value').text
        else:
            code = file
        
        self.CuttingCode = code
        self.Root = Stockplate(h.Width, h.Height)

        i = 0
        while i < len(self.CuttingCode):
            c = self.CuttingCode[i]
            #call matching function according to found token
            if c in self.Parser:
                i = self.Parser[c](c, i)
            
            # don't forget to go to the next char
            i += 1
    
    def parseCuttingCodeFromJson(self):
        '''
         for future use
        '''
        pass

    def exportToEdiFile(self, version):
        '''
         for future use
        '''
        pass

    def exportToJson(self):
        return self.Root.toJSON()
    
    def peek(self, index):
        '''
         peeks to the next char on buffer with out manipulating the reading position
        '''
        return self.CuttingCode[index:index+1]

    def addCut(self, cutType, index):
        #get next space
        cutSizeEnd, size = self.getEndOf(index + 1)

        self.TraverseCount[cutType] += 1
        self.resetTraverseCount(cutType)

        leaf = TraverseLeaf(self.TraverseCount.copy(), float(size))
        if cutType == "X":
            self.Root.appendChild(leaf)
        else:
            self.Root.appendChildByPath(leaf)
        
        self.last_leaf = leaf.closeCut()
        return cutSizeEnd
    
    def addModel(self, model, index):
        modelIdEnd, modelId = self.getEndOf(index + 1)
        #take a peak to next char
        next_char = self.peek(modelIdEnd + 1)
        if next_char == "(":
            #if we found "(" means we need to check everything till upcoming ")"
            buff = self.CuttingCode.find(")", modelIdEnd) + 1
            if modelId in self.ModelIds:
                self.ModelIds[modelId].setModelInformation(
                    self.collectModelInfomation((modelIdEnd + 1), buff)
                )
            modelIdEnd = buff
        else:
            self.ModelIds[modelId] = self.last_leaf
        
        return modelIdEnd

    def addTraverseInfoId(self, trav, index):
        travEnd, travId = self.getEndOf(index + 1)
        travId = travId.strip()
        #take a peak to next char
        next_char = self.peek(travEnd + 1)
        TravInfoEnd, val = self.getEndOf(travEnd)
        if next_char == "(":
            #if we found "(" means we need to check everything till upcoming ")"
            TravInfoEnd, val = self.getEndOf(TravInfoEnd + 1) 
            buff = self.CuttingCode.find(")", TravInfoEnd)
            for key in self.TravIds:
                if key == travId:
                    #a sheet has this information                    
                    for leaf in self.TravIds[key]:
                        leaf.setTraverseInformation(
                            self.collectTraverseInformation(travId, TravInfoEnd + 1, buff)
                        )
            travEnd = buff
        else:
            if travId in self.TravIds:
                self.TravIds[travId].append(self.last_leaf)
            else:
                self.TravIds[travId] = []
                self.TravIds[travId].append(self.last_leaf)

        return travEnd
    
    def addRackInfomation(self, rack, index):
        rackEnd, rack = self.getEndOf(index + 1)

        self.last_leaf.setRackCode(rack)

        return rackEnd
        
    def getEndOf(self, index, find={" ", "\n"}):
        EndPos = next(i for i,c in enumerate(self.CuttingCode[index:]) if c in find)
        value = self.CuttingCode[index : (index + EndPos)]
        return index + EndPos, value.strip()

    def collectTraverseInformation(self, id, start, end) -> EdiTraverseInfo:
        '''
         collects all Information Tags which are starting with I
        '''
        Info = EdiTraverseInfo(id)
        '''
         Traverseinformation are coming in the following way
         I[ParameterName]=[SomeValue]
         we wann to get the ParameterName and the Value and save it to TraverseInfo
        '''
        i = start            
        while i < len(self.CuttingCode) and i < end:
            InfoNameEnd, InfoValue = self.getEndOf((i), {"\n"})
            if InfoValue != "":
                #check if an "=" is given
                if InfoValue.find("=") >= 0:
                    Info.append(InfoValue[:InfoValue.find("=")], InfoValue[InfoValue.find("=") + 1:])
                else:
                    Info.append(InfoValue, "")
            i = InfoNameEnd + 1
        return Info

    def collectModelInfomation(self, start, end) -> ModelInformation:
        '''
         collects the model information from given F Section
        '''
        Info = ModelInformation(self.CuttingCode[(start + 1) : (end - 1) ])

        return Info

