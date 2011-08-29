'''
Created on Aug 17, 2011

@author: kashim
'''
from lxml import etree
import logging
import marathon_consts
from marathon_sport_parser import MarathonSportParser

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
        file = open( fileName )
        ufile = unicode(file.read(), encoding)
        file.close()
        return ufile

    def getInitialXML(self):
        if self.__XML == None:
            htmlTxt = self.__getUStrFromFile(self.getFileName(), self.getEncoding())
            self.__XML = etree.fromstring( htmlTxt, self.__getParser() )
            
        return self.__XML

    def __init__(self, fileName, encoding):
        self.__fileName = fileName
        self.__encoding = encoding

    def getSportList(self):
        xml = self.getInitialXML()
        sportList = xml.xpath( 
                              marathon_consts.SPORT_LIST_XPATH,
                              namespaces = marathon_consts.XPATH_REG_EX_NAMESPACE_MAP 
                             )
        return sportList
    
    def processXML(self):
        sportList = self.getSportList()
        for sport in sportList:
            sportParser = MarathonSportParser( sport )
            
            if sportParser.getSportID() == "119460":
#            if sportParser.getSportID() == "416141":
                toLog( str( sportParser ) ) 
                sportParser.parseSport()
        
if __name__ == "__main__":
    parser = MarathonParser(
#                            "/Users/kashim/Projects/Bookmaker/4_marathon/all_ru.html",
                            "/Users/kashim/Projects/Bookmaker/4_marathon/all_en.html",
                            "UTF-8"
#                            "windows-1251"
                           )
    parser.processXML()
    
        