#!/usr/bin/env python
# encoding: utf-8

class Event(object):
    def __init__(self, **kwargs):
        self.utc_unixtime = kwargs.get('utc_unixtime')
        self.team1 = kwargs.get('team1')
        self.team2 = kwargs.get('team2')

        self.sport = kwargs.get('sport')
        self.country = kwargs.get('country')
        self.league = kwargs.get('league')

        self.office = kwargs.get('office_id')
        self.feed = kwargs.get('feed_id')

        self.bets = []
        
    def addBet(self, bet):
        self.bets.append( bet )

    def as_dict(self):
        return dict(team1 = self.team1,
                   team2 = self.team2,
                   sport = self.sport,
                   utc_unixtime = self.utc_unixtime,
                   country = self.country,
                   league = self.league,
                   feed = self.feed,
                   office = self.office,
                   bets = map(lambda b: b.as_dict(), self.bets)
                   )

    def __str__(self):
        return u"{0} - {1}. {2} bets".format(self.team1, self.team2, len(self.bets) )


class Bet(object):
    def __init__(self, **kwargs):
        #type of coef
        self.coef = kwargs.get('coef')
        #coef itself. Example 1.99
        self.odds_decimal = kwargs.get('odds_decimal')
        #coef value. For total and handicap. Example (for total) +2.5 
        self.odds_value = kwargs.get('odds_value')

    def as_dict(self):
        return dict(coef = self.coef,
                    odds_decimal = self.odds_decimal,
                    odds_value = self.odds_value
               )

    def __str__(self):
        return "%s - %s" % (self.coef, self.odds_decimal)


