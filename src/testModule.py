'''
Created on Aug 14, 2011

@author: kashim
'''

from marathonParser import MarathonParser
import lxml
from lxml import etree
import logging

LOG = logging.getLogger(__name__)


def printWhiteLines( lineCount, printSeparator=True, separator="############################" ):
    for i in range( 0, lineCount - 1 ): 
        print "\n"
    if printSeparator:
        print separator

def getUStrFromFile(fileName):
    file = open( fileName )
    ufile = unicode(file.read(), encoding)
    file.close()
    return ufile

def getParser():
    parser = lxml.etree.HTMLParser( recover = True )
    return parser


def myTest(fileName):
    text = getUStrFromFile( fileName )
    tree = lxml.etree.fromstring(text, parser=getParser())
#    tree = etree.parse( fileName )
    print "imported tree\n" + str(tree)
    printWhiteLines(1)
    print etree.tostring( tree, pretty_print = True )
    printWhiteLines(1)
    print len(tree)
    printWhiteLines(1)
    print tree.get("test_attr")
    printWhiteLines(1)
    tree.set( "test_attr", "test_val" )
    print tree.get("test_attr")
    printWhiteLines(1)
    print "iterate through children"
    children = (tree[0])[0]
    for c in children.iter("th"):
        print u"%s - %s" %( c.tag, c[0].tag )
    
    printWhiteLines(1)
    print "XPath test"
    tmp = tree.xpath( "//tr" )
    if len(tmp) > 0:
        print str( len( tmp ) )
        cnt = 0
        for elem in tmp:
            print "%2d - %s" % ( cnt, elem.tag )
            cnt += 1
    else:
        print "Nothing found"
#    print etree.tostring( tmp, pretty_print = True )
    
def myTestFromDoc():
    from cStringIO import StringIO
    xml_file = StringIO('''\
                             <root>
                               <a><b>ABC</b><c>abc</c></a>
                               <a><b>MORE DATA</b><c>more data</c>tail</a>
                               <a><b>XYZ</b><c>xyz</c></a>
                             </root>'''
                            )
    myXML = etree.parse( xml_file )
    txt = myXML.xpath("//text()")
    print txt
    print "".join( str(elem).strip() for elem in txt  )

#    for event, element in etree.iterparse(xml_file, tag='a', events=("start", "end")):
#        print('%s: %s -- %s' % (event, element.findtext('b'), element[1].text))
#        if event == "end":
#            element.clear()
            
def myTestFromMarathon(fileName):
    print "myTestFromMarathon(fileName): - start"
    text = getUStrFromFile( fileName )
    tree = lxml.etree.fromstring(text, parser=getParser())

    sportList = tree.xpath( 
                          "//div[reg:match(@id, 'container_[0-9]+')]",
                          namespaces = { 'reg': 'http://exslt.org/regular-expressions' } 
                         )
    print "elem count = " + str( len(sportList) )
    for sport in sportList:
#        print sport.get( "id" )
        logging.warning(sport.get("id"))
#    print etree.tostring( sportList[0], pretty_print = True )
#    print etree.tostring( tree, pretty_print = True )

if __name__ == '__main__':
    print "test"
#    encoding = 'windows-1251'
    encoding = "UTF-8"
#    myTest("/Users/kashim/Temp/test.html")
#    myTestFromMarathon("/Users/kashim/Projects/Bookmaker/4_marathon/all_en.html") 
    myTestFromDoc()
#    tmp = MarathonParser()