# This is a file that contains the Team class and the TeamList class.
# The Team class is a dataclass that contains all the information about the team.
# The TeamList class is a list of Team objects which contains all the teams in the league.

# How to install to venv: pip install -e .

from dataclasses import dataclass
from typing import List,Dict, Union, Tuple, Optional
import numpy as np
import pandas as pd
import os
import sys
import re
import datetime as dt
import matplotlib.pyplot as plt
from .Representations import Record, SeasonID, TeamID,Game, GameStats,TeamStats,Date
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

@dataclass
class Team:
    team_id: TeamID
    season_id: SeasonID
    def __init__(self, team_id:TeamID, season_id:SeasonID):
        self.team_id = team_id
        self.played_dates = []
        self.categories = None
        self.season_id = season_id
        self.record = Record(season_id, self)
        self.team_stats = TeamStats(self)
    def add_stats(self, stats:GameStats):
        if not len(self.played_dates):
            # If the team has not played yet, then the categories should be set.
            self.categories = stats.categories
        self.team_stats.add_stats(stats)
    def total(self)->GameStats:
        return self.team_stats.total()
    def total_to_date(self, date:Date)->GameStats:
        return self.team_stats.total_to_date(date)
    def average(self)->GameStats:
        return self.team_stats.average()
    def average_to_date(self, date:Date)->GameStats:
        return self.team_stats.average_to_date(date)
    def home_total(self)->GameStats:
        return self.team_stats.home_total()
    def home_total_to_date(self, date:Date)->GameStats:
        return self.team_stats.home_total_to_date(date)
    def home_average(self)->GameStats:
        return self.team_stats.home_average()
    def home_average_to_date(self, date:Date)->GameStats:
        return self.team_stats.home_average_to_date(date)
    def away_total(self)->GameStats:
        return self.team_stats.away_total()
    def away_total_to_date(self, date:Date)->GameStats:
        return self.team_stats.away_total_to_date(date)
    def away_average(self)->GameStats:
        return self.team_stats.away_average()
    def away_average_to_date(self, date:Date)->GameStats:
        return self.team_stats.away_average_to_date(date)
    def get_stat(self, stat:str, date:Date=None)->GameStats:
        return self.team_stats.get_stat(stat, date)
    def add_game(self, game:Game)->None:
        self.played_dates.append(game.date)
        assert self.id in game.teams, f"{self.id} is not in {game.teams}"
        home = game.home_team == self
        self.record.add_game(game.date, game)
        self.team_stats.add_game(game, home)
    def get_game_stats(self, occasion:Union[Date,Game])->GameStats:
        if isinstance(occasion, Date):
            date = occasion
        elif isinstance(occasion, Game):
            date = occasion.date
        else:
            raise TypeError(f"occasion must be either Date or Game, not {type(occasion)}")
        return self.team_stats.get_game_stats(date)
    def dates_played(self)->List[Date]:
        return self.played_dates
    @property
    def name(self)->str:
        return self.team_id.name
    @property
    def id(self)->TeamID:
        return self.team_id
    @property
    def city(self)->str:
        return self.team_id.city
    @property
    def abbreviation(self)->str:
        return self.team_id.abbreviation
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Team):
            return self.id == __o.id
        elif isinstance(__o, TeamID):
            return self.id == __o
        else:
            return False
    def __hash__(self) -> int:
        return hash(self.team_id)
    def __str__(self) -> str:
        # A small summary of the team´s statistics.
        return f"{self.name} ({self.id}) - {self.season_id} - {self.record}"
    def __repr__(self) -> str:
        return f"Team({self.id}, {self.season_id})"
    def plot(self, metric="Total",title:str=None, xlabel:str=None, ylabel:str=None, **kwargs):
        return self.team_stats.plot(metric=metric,title=title, xlabel=xlabel, ylabel=ylabel, **kwargs)


class TeamList:
    def __init__(self,teams:Optional[List[Team]]=None) -> None:
        self.teams = teams if teams is not None else []
        self.team_dict = {}
    def add_team(self, team:Team):
        self.teams.append(team)
        self.team_dict[team.id] = team
    def sort_by_id(self)->List[Team]:
        return sorted(self.teams, key=lambda x: x.id)
    def sort_by_name(self)->List[Team]:
        return sorted(self.teams, key=lambda x: x.name)
    def sort_by_city(self)->List[Team]:
        return sorted(self.teams, key=lambda x: x.city)
    def sort_by_stat(self, stat:str)->List[Team]:
        return sorted(self.teams, key=lambda x: x.get_stat(stat))
    def __getitem__(self, item:TeamID)->Team:
        return self.team_dict[item]
    def __len__(self)->int:
        return len(self.teams)
    def __iter__(self):
        return iter(self.teams)
    def __contains__(self, item):
        return item in self.teams
    def __eq__(self, __o: object) -> bool:
        raise NotImplementedError("Not implemented yet.")
    def __repr__(self):
        return f"TeamList({self.team_names})"
    def __str__(self):
        return f"TeamList({self.team_names})"
    @property
    def team_names(self)->List[str]:
        return [team.name for team in self.teams]
    @property
    def team_ids(self)->List[TeamID]:
        return [team.id for team in self.teams]
    @property
    def team_abbreviations(self)->List[str]:
        return [team.abbreviation for team in self.teams]
    @property
    def team_cities(self)->List[str]:
        return [team.city for team in self.teams]



