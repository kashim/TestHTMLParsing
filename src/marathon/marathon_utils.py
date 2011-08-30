'''
Created on Aug 28, 2011

@author: kashim
'''
SPORT_LIST_XPATH = "//div[reg:match(@id, 'container_[0-9]+')]"
XPATH_REG_EX_NAMESPACE_NAME = "http://exslt.org/regular-expressions"
XPATH_REG_EX_NAMESPACE_MAP = { 'reg': XPATH_REG_EX_NAMESPACE_NAME } 
DEFAULT_FEED_NAME = "marathonbet.com"
DEFAULT_OFFICE_NAME = "Marathon"


NAME_CONVERSION_MAP = {
    u"Home1": u"team1",
    u"Away2": u"team2",
    u"Handicap1": u"handicap1",
    u"Handicap2": u"handicap2",
    u"Total under": u"total_under",
    u"Total over": u"total_over",
    u"Athlete1": u"team1",
    u"Athlete2": u"team2",
    u"DrawX": u"draw",
    u"1X": u"1x",
    u"X2": u"x2",
    u"12": u"12",
    u"Fighter1": u"team1",
    u"Fighter2": u"team2",
    u"Player1": u"team1",
    u"Player2": u"team2"
}

class MarathonBet():
    betType = ""
    coef = 1
    value = 0
    
    def __init__(self):
        pass

class MarathonEvent():
    utc_unixtime = None
    team1 = ""
    team2 = ""
    country = ""
    feed = ""
    league = ""
    office = ""
    sport = ""
    betList = []
    
    def __init__(self):
        pass