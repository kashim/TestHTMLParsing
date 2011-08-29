'''
Created on Aug 28, 2011

@author: kashim
'''
import logging
from lxml import etree
from copy import deepcopy
import marathon_consts

def toLog(msg):
#    pass
    logging.warning(msg)

class MarathonSportParser():
    __sportXML = None
    __sportID = None
    __sportName = ""
    __tournamentName = ""
    __tournamentCountry = ""
    __eventHeader = []
    
    def __init__(self, sportXML):
        self.__sportXML = sportXML
        self.__processGeneralEventInfo()
        
    def __repr__(self):
        tmp = "marathon Sport Parser created. SportID = " + str( self.getSportID() )
        tmp += ";\n Sport Name = " + self.getSportName()
        tmp += "; \n Tournament Name = " + self.getTournamentName()
        return tmp

    def getEventHeaderStr(self):
        return u";".join( hdr for hdr in self.__eventHeader )
    
    def getXML(self):
        return self.__sportXML
    
    def __processGeneralEventInfo(self):
        node = self.getXML()[1]
        fullNameList = node[2].tail.strip().split(".")
        self.__sportName = " ".join( str( elem ).strip() for elem in fullNameList[:1] )
        self.__tournamentName = " ".join( str( elem ).strip() for elem in fullNameList[1:] )
        
        tmp = self.getXML().get("id")
        indx = tmp.index("_") + 1
        self.__sportID = tmp[indx:]
        
    def __processEventHeader(self):
        node = self.getXML()[2][0][0][0]
        for elem in node:
            tmp = deepcopy( elem )
            txt = tmp.xpath( "//text()" )
            txt = u"".join( str( lstElem ).strip() for lstElem in txt )
            toLog( txt )
            # check for empty string to detect comments
            if txt != "":
                self.__eventHeader.append(txt)
        toLog( self.getEventHeaderStr() )
        self.__normalizeEventHeader()
        
    def __normalizeEventHeader(self):
        toLog( "before for start" )
        for i in range( 0, len( self.__eventHeader ) - 1 ):
            toLog( "iteration num " + str( i ) )
            elem = self.__eventHeader[i]
            if elem in marathon_consts.NAME_CONVERSION_MAP:
                toLog( "True" )
                self.__eventHeader[i] = marathon_consts.NAME_CONVERSION_MAP[ elem ]
            else:
                toLog( "False" )
                self.__eventHeader[i] = ""
        toLog( self.getEventHeaderStr() )
    
    def __processEventElement(self, eventXML):
        pass    

    def __processEvents(self):
        node = self.getXML()[2][0][0] #etree.ElementTree( self.getXML() )
        for i in range(1, len( node ) - 1):
            self.__processEventElement(node[i])
        
    def getSportID(self):
        return self.__sportID

    def getSportName(self):
        return self.__sportName
    
    def getTournamentName(self):
        return self.__tournamentName
    
    def parseSport(self):
        self.__processEventHeader()
        self.__processEvents()