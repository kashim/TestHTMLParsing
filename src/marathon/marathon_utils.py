'''
Created on Aug 28, 2011

@author: kashim
'''
SPORT_LIST_XPATH = "//div[reg:match(@id, 'container_[0-9]+')]"
XPATH_REG_EX_NAMESPACE_NAME = "http://exslt.org/regular-expressions"
XPATH_REG_EX_NAMESPACE_MAP = { 'reg': XPATH_REG_EX_NAMESPACE_NAME } 
DEFAULT_FEED_NAME = "marathonbet.com"
DEFAULT_OFFICE_NAME = "Marathon"

EVENT_ELEMENT_TEAMS = u"event_name"
EVENT_ELEMENT_WIN1 = u"win1"
EVENT_ELEMENT_WIN2 = u"win2"

NAME_CONVERSION_MAP = {
    u"Home1": EVENT_ELEMENT_WIN1,
    u"Away2": EVENT_ELEMENT_WIN2,
    u"Handicap1": u"handicap1",
    u"Handicap2": u"handicap2",
    u"Total under": u"total_under",
    u"Total over": u"total_over",
    u"Athlete1": EVENT_ELEMENT_WIN1,
    u"Athlete2": EVENT_ELEMENT_WIN2,
    u"DrawX": u"draw",
    u"1X": u"1x",
    u"X2": u"x2",
    u"12": u"12",
    u"Fighter1": EVENT_ELEMENT_WIN1,
    u"Fighter2": EVENT_ELEMENT_WIN2,
    u"Player1": EVENT_ELEMENT_WIN1,
    u"Player2": EVENT_ELEMENT_WIN2,
    u"Event Name": EVENT_ELEMENT_TEAMS
}

EXCLUDE_LEAGUE_NAME_LIST = [ u"Ante Post", u"Horse Racing" ]

def needParseSport( sportName, leagueName):
    res = True
    i = 0
    while ( i < len( EXCLUDE_LEAGUE_NAME_LIST ) ) and res:
        elem = EXCLUDE_LEAGUE_NAME_LIST[i]
        elem = elem.strip().upper()
        if leagueName.strip().upper() == elem:
            res = False
        elif sportName.strip().upper().find( elem ) > -1:
            res = False
        
        i += 1

    return res
    
def is_number(s):
    try:
        int(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True