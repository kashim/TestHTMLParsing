# encoding: utf-8

'''
Created on Aug 17, 2011

@author: kashim
'''
from lxml import etree
import simplejson as json
import logging
import marathon_utils
from marathon_sport_parser import MarathonSportParser
import sys
from pprint import pprint

def toLog(msg):
    logging.warning(msg)

#############################################

#############################################
class MarathonParser():
    __parser = None
    __XML = None
    __fileName = ""
    __encoding = ""
    
    def getEncoding(self):
        return self.__encoding
    
    def getFileName(self):
        return self.__fileName
    
    def __getParser(self):
        if self.__parser == None:
            self.__parser = etree.HTMLParser( recover = True )
            
        return self.__parser 

    def __getUStrFromFile(self, fileName, encoding):
        srcFile = open( fileName )
        ufile = unicode( srcFile.read(), encoding )
        srcFile.close()
        return ufile

    def getInitialXML(self):
        if self.__XML == None:
            htmlTxt = self.__getUStrFromFile(self.getFileName(), self.getEncoding())
            self.__XML = etree.fromstring( htmlTxt, self.__getParser() )
            
        return self.__XML

    def __init__(self, fileName, encoding):
        self.__fileName = fileName
        self.__encoding = encoding
        self.__parser = None
        self.__XML = None

    def getSportList(self):
        xml = self.getInitialXML()
        sportList = xml.xpath( 
                              marathon_utils.SPORT_LIST_XPATH,
                              namespaces = marathon_utils.XPATH_REG_EX_NAMESPACE_MAP 
                             )
        return sportList
    
    def processXML(self):
        sportList = self.getSportList()
        sportJsonList = []
        for sport in sportList:
            sportParser = MarathonSportParser( sport )
            
#            if sportParser.getSportID() == "119460":
#            if sportParser.getSportID() == "416141":
#                toLog( str( sportParser ) ) 
            events = sportParser.parseSport()
            if events != None:
                try:
                    result = map(lambda o: o.as_dict(), events)
        #            pprint( result, indent = 4 )
                    sportJson = json.dumps( result )
                    sportJsonList.append(sportJson)
                except:
                    tmp = u"Error: events length = {0}"
                    print tmp.format( len( events ) )    
                    for event in events:
                        print str( event )
        
        return sportJsonList
        
if __name__ == "__main__":
    fileName = "/Users/kashim/Projects/Bookmaker/4_marathon/all_en.html"
#    fileName = "/Users/kashim/Projects/Bookmaker/4_marathon/all_ru.html"
#    fileName = sys.argv[1] # filename could be command name also
    outFileName = "/Users/kashim/Projects/Eclipse/DefWorkplace/TestHTMLParsing/src/marathon.json"
#    outFileName = sys.argv[2]
    encoding = "UTF-8"
    
    parser = MarathonParser(
                            fileName,
                            encoding
                           )
    sportJsonList = parser.processXML()
    if len( sportJsonList ) > 0:
        with open(outFileName, 'wb') as _f:
            for sport in sportJsonList:
                _f.write( sport )
    
        