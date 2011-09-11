'''
Created on Aug 28, 2011

@author: kashim
'''
import logging
from lxml import etree
from copy import deepcopy
import marathon_utils
#from marathon_utils import MarathonEvent, MarathonBet
import re
from datetime import datetime
from models import Event, Bet
import sys

def toLog(msg):
    pass
#    logging.warning(msg)

class MarathonSportParser():
    __sportXML = None
    __sportID = None
    __sportName = ""
    __league = ""
    __country = ""
    __eventHeader = []
    __eventList = []
    
    def __init__(self, sportXML):
        self.__sportXML = deepcopy( sportXML )
        self.__sportID = None
        self.__sportName = ""
        self.__league = ""
        self.__country = ""
        self.__eventHeader = []
        self.__eventList = []

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
        #div->div[2]->div->table->tr - general event
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
        for i in range( 0, len( self.__eventHeader ) ):
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
        i = 0
        while i < len( cellValue ):
            tmp = re.search( "[0-9]\.", cellValue[i] )
            # if found number then next elem is team name
            if tmp != None:
                curVal = tmp.group(0)[:-1]
                teamName = unicode( cellValue[ i + 1 ] )
                if int( curVal ) == 1:
                    event.team1 = teamName
                else:
                    event.team2 = teamName
                i += 1
            else:
                # searching for event time with date
                tmp = re.search( "[0-9]{2} [a-zA-Z]{3} [0-9]{2}:[0-9]{2}", cellValue[i] )
                eventDate = None
                if tmp != None:
                    eventDate = datetime.strptime( str( tmp.group(0) ), "%d %b %H:%M" )
                    eventDate = eventDate.replace( year = datetime.today().year )
                else:
                    #search for event time without date
                    tmp = re.search( "[0-9]{2}:[0-9]{2}", cellValue[i] )
                    if tmp != None:
                        eventDate = datetime.strptime( str( tmp.group(0) ), "%H:%M" )
                        today = datetime.today()
                        eventDate = eventDate.replace( year = today.year, month = today.month, day = today.day )
                
                if eventDate != None:
                    event.utc_unixtime = eventDate.strftime( "%d.%m.%Y %H:%M" )

            i += 1
    
    def __parseEventElementParamValue(self, event, elementHeader, xml):
        if elementHeader != "":
            betCoef = xml.xpath( "//text()" )
            betCoef = u"".join( str( lstElem ).strip() for lstElem in betCoef )
            betValue = 0
            val = betCoef.find("(")
            if val > -1:
                val2 = betCoef.find(")")
                if val2 > -1:
                    betValue = float( betCoef[val + 1:val2] )
                    betCoef = betCoef[val2 + 1:]
            
            bet = Bet()
            bet.coef = elementHeader
            bet.odds_decimal = betCoef
            bet.odds_value = betValue
            
            event.addBet( bet )
           
    
    def __processEventElementParam(self, event, eventXML):
        for i in range( 0, len( self.__eventHeader ) ):
            try:
                currElem = deepcopy( eventXML[0][i] )
                if self.__eventHeader[i] == marathon_utils.EVENT_ELEMENT_TEAMS:
                    self.__parseEventTeams( currElem, event )
                else:
                    self.__parseEventElementParamValue(event, self.__eventHeader[i], currElem )
            except:
                tmp = u"index = {0}; header length = {1}; header value = {2}; sport id = {3}; sport name = {4}"
                tmp += u" tournament name = {5}"
                tmp = tmp.format(
                            i, len( self.__eventHeader ), self.__eventHeader[i], self.getSportID(),
                            self.getSportName(), self.getLeagueName()
                      )
                print tmp
                
        try:
            toLog( u"event = " + str( event ) )
        except:
            print "  "
            tmp = u"sport id = {0}; sport name = {1} tournament name = {2}"
            tmp = tmp.format(
                        self.getSportID(),
                        self.getSportName(), 
                        self.getLeagueName()
                  )
            print tmp
    
    def __processEventElement(self, eventXML):
        event = Event()
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
        toLog( len( node ) )
        #first element is table header 
        for i in range(1, len( node ) ):
            toLog( node[i].tag )
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
        if marathon_utils.needParseSport(self.getSportName(), self.getLeagueName()):
            self.__processEventHeader()
            self.__processEvents()
            res = self.__eventList
        else:
            res = None

        return res