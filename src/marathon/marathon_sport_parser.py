'''
Created on Aug 28, 2011

@author: kashim
'''
import logging
from lxml import etree
from copy import deepcopy
import marathon_utils
from marathon_utils import MarathonEvent
import re
import time
import datetime

def toLog(msg):
#    pass
    logging.warning(msg)

class MarathonSportParser():
    __sportXML = None
    __sportID = None
    __sportName = ""
    __league = ""
    __country = ""
    __eventHeader = []
    __eventList = []
    
    def __init__(self, sportXML):
        self.__sportXML = sportXML
        self.__processGeneralEventInfo()
        
    def __repr__(self):
        tmp = "marathon Sport Parser created. SportID = " + str( self.getSportID() )
        tmp += ";\n Sport Name = " + self.getSportName()
        tmp += "; \n Tournament Name = " + self.getLeagueName()
        return tmp

    def getEventHeaderStr(self):
        return u";".join( hdr for hdr in self.__eventHeader )
    
    def getXML(self):
        return self.__sportXML
    
    def __processGeneralEventInfo(self):
        node = self.getXML()[1]
        fullNameList = node[2].tail.strip().split(".")
        self.__sportName = " ".join( str( elem ).strip() for elem in fullNameList[:1] )
        self.__league = " ".join( str( elem ).strip() for elem in fullNameList[1:] )
        
        tmp = self.getXML().get("id")
        indx = tmp.index("_") + 1
        self.__sportID = tmp[indx:]
            
    def __processEventHeader(self):
        node = self.getXML()[2][0][0][0]
        for elem in node:
            tmp = deepcopy( elem )
            txt = tmp.xpath( "//text()" )
            txt = u"".join( str( lstElem ).strip() for lstElem in txt )
#            toLog( txt )
            # check for empty string to detect comments
            if txt != "":
                self.__eventHeader.append(txt)
#        toLog( self.getEventHeaderStr() )
        self.__normalizeEventHeader()
        
    def __normalizeEventHeader(self):
        toLog( "before for start" )
        for i in range( 0, len( self.__eventHeader ) - 1 ):
#            toLog( "iteration num " + str( i ) )
            elem = self.__eventHeader[i]
            if elem in marathon_utils.NAME_CONVERSION_MAP:
#                toLog( "True" )
                self.__eventHeader[i] = marathon_utils.NAME_CONVERSION_MAP[ elem ]
            else:
#                toLog( "False" )
                self.__eventHeader[i] = ""
        toLog( self.getEventHeaderStr() )
    
    def __parseEventTeams(self, cellXML, event):
        cellValue = cellXML.xpath("//text()")
        toLog( cellValue )
        i = 0
        while i < len( cellValue ):
            tmp = re.search( "[0-9]\.", cellValue[i] )
            toLog( "re search = " + str( tmp ) )
            if tmp != None:
                curVal = tmp.group(0)[:-1]
                toLog( "tmp.group(0) " + str( curVal ) )
                event.teamList[ int( curVal ) - 1 ] = cellValue[ i + 1 ]
                i += 1
            else:
                tmp = re.search( "[0-9]{2}:[0-9]{2}", cellValue[i] )
                toLog( "re search time = " + str( tmp ) )
                if tmp != None:
                    eventTime = time.strptime( str( tmp.group(0) ) , "%H:%M")
                    eventDate = datetime.date.fromtimestamp( eventTime )
                    toLog( eventDate )
                    event.utc_unixtime = eventDate
                
            i += 1
        toLog( event.teamList )
    
    
    def __processEventElementParam(self, event, eventXML):
        for i in range( 0, len( self.__eventHeader ) ):
            currElem = deepcopy( eventXML[0][i] )
            if self.__eventHeader[i] == marathon_utils.EVENT_ELEMENT_TEAMS:
                self.__parseEventTeams( currElem, event )
                toLog( event.utc_unixtime )
                toLog( "; teams = " + str( event.teamList ) )
    
    def __processEventElement(self, eventXML):
        event = MarathonEvent()
        event.country = self.getCountry()
        event.feed = marathon_utils.DEFAULT_FEED_NAME
        event.league = self.getLeagueName()
        event.office = marathon_utils.DEFAULT_OFFICE_NAME
        event.sport = self.getSportName()
        
        eventInfo = deepcopy( eventXML )
        self.__processEventElementParam(event, eventInfo)
        
        return event

    def __processEvents(self):
        node = self.getXML()[2][0][0] #div[2] -> div -> table
        #first element is table header 
        for i in range(1, len( node ) - 1):
            newEvent = self.__processEventElement(node[i])
            self.__eventList.append( newEvent )
        
    def getSportID(self):
        return self.__sportID

    def getSportName(self):
        return self.__sportName
    
    def getLeagueName(self):
        return self.__league
    
    def getCountry(self):
        return self.__country
    
    def parseSport(self):
        self.__processEventHeader()
        self.__processEvents()