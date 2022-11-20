# This is a file that contains the Team class and the TeamList class.
# The Team class is a dataclass that contains all the information about the team.
# The TeamList class is a list of Team objects which contains all the teams in the league.

# How to install to venv: pip install -e .

from dataclasses import dataclass
from typing import List
import numpy as np
import pandas as pd
import os
import sys
import re
import datetime as dt
import matplotlib.pyplot as plt
from .Representations import Record, Season, Game, GameStats,TeamStats
"""
Team specific features:
* Powerplay precentage up to that point in the season (PP%)
* Boxplay precentage up to that point in the season (BP%)
* Avg. goals   might not be normalizable. That would be the (ranking of goals scored)/(number of teams). (AG)
* Avg. goals against   might not be normalizable. That would be the (ranking of goals against)/(number of teams). (AGA)
* Shots per game (SPG)
* Save percentage  (SV%)
* Hits per game (HPG)
* Blocks per game (BPG)
* Faceoff win percentage (FOW%)
* Ratio of goals scored to goals against (GvsGA)
* Ratio of goals scored in even strength to goals scored in powerplay (GvsPPG)
* Ratio of goals conceded in even strength to goals conceded in boxplay. (GAvsBPA)
* Ranking of penalty minutes taken. (PIM)
* Ranking of penalty minutes drawn. (PIMD)
* Ratio home wins to Total wins (HWvsW)
* Ratio home losses to Total losses (HLvsL)
* Ratio home ties to Total ties (HTvsT)
* Ratio home goals scored to Total goals scored (HGvsG)
* Ratio home goals against to Total goals against (HGAvsGA)
* Ratio home shots to Total shots (HSPGvsSPG)
* Ratio home hits to Total hits (HHPGvsHPG)
* Ratio home blocks to Total blocks (HBPGvsBPG)
* Ratio home faceoff to Total faceoff (HFOWvsFOW)
* Ratio home powerplay goals to Total powerplay goals (HPPGvsPPG)
* Ratio home powerplay goals against to Total powerplay goals against (HPPGAvsPPGA)
* Ratio home boxplay goals to Total boxplay goals (HBPGvsBPG)
* Ratio home boxplay goals against to Total boxplay goals against (HBPGAvsBPGA)
* Ratio home powerplay opportunities to Total powerplay opportunities (HPPvsAPP)

As well as the last "n" trends for each of the above features.
"""
from collections import OrderedDict

# The Team class should contain a ordered dictionary of the team´s statistics upon that point of the season.
# Within the dictionary should be the statistics up to that point of the season in total values.
# This values will then be normalized when creating the dataset.

# Given a date and a Team class object the statistics of that team up to that point in the season should be returned.

# Import ordered dictionary
@dataclass
class Team:
    name: str
    team_id: int
    team_stats: OrderedDict
    categories: List[str]
    def __init__(self, name, team_id, season):
        self.name = name
        self.team_id = team_id
        self.played_dates = []
        self.categories = None
        self.record = Record(season, self)
        self.team_stats = TeamStats(self)
    def add_stats(self, date, stats:GameStats):
        if not len(self.played_dates):
            # If the team has not played yet, then the categories should be set.
            self.categories = list(stats.keys())
        self.team_stats[date] = stats
        self.played_dates.append(date)
    def get_stats(self, date):
        return self.team_stats[date]
    def add_game(self, date,game:Game):
        # This should add the stats of a game to the team_stats cumulative stats.
        # This should be done by adding the stats of the game to the stats of the previous game.
        # If the team has no stats yet, then the stats of the game should be added to the team_stats.
        if not len(self.played_dates):
            self.add_stats(date, game.stats)
        else:
            # Get the stats of the previous game
            #previous_stats = self.get_stats(self.played_dates[-1])
            # Add the stats of the game to the stats of the previous game
            new_stats = self.team_stats+game.stats # See GameStats class for implementation of the + operator.
            # Add the new stats to the team_stats
            self.add_stats(date, new_stats)
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Team):
            return self.team_id == __o.team_id
        else:
            return False
    def get_stats_up_to_date(self, date):
        # If the team has not played yet:
        if not len(self.team_stats):
            raise NotImplementedError("The team has not played yet.")
            # TODO: Decide what to do here.
        # If the team has played but not on the given date:
        elif date not in self.team_stats.keys():
            # Check if the date is before the first game of the team
            if date < self.played_dates[0]:
                raise NotImplementedError("The team has not played yet.")
                # TODO: Decide what to do here, probably return None and handle elsewhere.
            # Otherwise, return the stats of the last game played.
            else:
                return self.get_stats(self.played_dates[-1])
            



