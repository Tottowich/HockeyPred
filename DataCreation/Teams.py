# This is a file that contains the Team class and the TeamList class.
# The Team class is a dataclass that contains all the information about the team.
# The TeamList class is a list of Team objects which contains all the teams in the league.

# How to install to venv: pip install -e .

from dataclasses import dataclass
from typing import List,Dict, Union, Tuple, Optional, TypeVar
import numpy as np
import pandas as pd
import os
import sys
import re
import datetime as dt
import matplotlib.pyplot as plt
from .Representations import Record, SeasonID, TeamID,Game, GameStats,TeamStats,Date,Stats,DateList,GameResult
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
        self.categories = None
        self.season_id = season_id 
        self.record = Record(season_id, self.team_id)
        self.team_stats = TeamStats(self.team_id)
        self.played_dates = DateList()
        self.played_dates_home = DateList()
        self.played_dates_away = DateList()
    def add_stats(self, stats:GameStats):
        if not len(self.played_dates):
            # If the team has not played yet, then the categories should be set.
            self.categories = stats.categories
        self.team_stats.add_stats(stats)
    def total(self)->Stats:
        """
        Returns the total stats of the team.
        """
        return self.team_stats.total()
    def total_to_date(self, date:Date)->Stats:
        """
        Returns the total stats of the team up to that date.
        """
        return self.team_stats.total_to_date(date)
    def average(self)->Stats:
        """Returns the average stats of the team."""
        return self.team_stats.average()
    def average_to_date(self, date:Date)->Stats:
        """Returns the average stats of the team up to that date."""
        return self.team_stats.average_to_date(date)
    def home_total(self)->Stats:
        """
        Returns the total stats of the team at home.
        Only the games played at home are considered."""
        return self.team_stats.home_total()
    def home_total_to_date(self, date:Date)->Stats:
        """ Returns the total stats of the team at home up to that date.
        Only the games played at home are considered."""
        return self.team_stats.home_total_to_date(date)
    def home_average(self)->Stats:
        """
        Returns the average stats of the team at home.
        Only the games played at home are considered."""
        return self.team_stats.home_average()
    def home_average_to_date(self, date:Date)->Stats:
        """ Returns the average stats of the team at home up to that date."""
        return self.team_stats.home_average_to_date(date)
    def away_total(self)->Stats:
        """ Returns the total stats of the team away."""
        return self.team_stats.away_total()
    def away_total_to_date(self, date:Date)->Stats:
        """ Returns the total stats of the team away up to that date."""
        return self.team_stats.away_total_to_date(date)
    def away_average(self)->Stats:
        """ Returns the average stats of the team away."""
        return self.team_stats.away_average()
    def away_average_to_date(self, date:Date)->Stats:
        """ Returns the average stats of the team away up to that date."""
        return self.team_stats.away_average_to_date(date)
    def get_stat(self, stat:str, date:Date=None)->Stats:
        """ Returns the stat of the team up to that date."""
        return self.team_stats.get_stat(stat, date)
    def _add_dates(self, date:Date,home:bool):
        assert isinstance(date, Date), f"date must be of type Date, not {type(date)}"
        self.played_dates.add_date(date)
        if home:
            self.played_dates_home.add_date(date)
        else:
            self.played_dates_away.add_date(date)
    def add_game(self, game:Game)->GameResult:
        """ Adds a game to the team. Returns the result of the game, 1 for win, 0 for tie and -1 for loss."""
        assert self.id in game.teams, f"{self.id} is not in {game.teams}"
        home = game.home_team_id == self.id
        self._add_dates(game.date, home)
        result = self.record.add_game(game.date, game) # Counts the wins, losses and ties.
        self.team_stats.add_game(game, home) # Adds the stats of the game to the team.
        return result
    def get_game_stats(self, occasion:Union[Date,Game])->GameStats:
        if isinstance(occasion, Date):
            date = occasion
        elif isinstance(occasion, Game):
            date = occasion.date
        else:
            raise TypeError(f"occasion must be either Date or Game, not {type(occasion)}")
        return self.team_stats.get_game_stats(date)
    @property
    def streak(self)->int:
        return self.record.streak
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
    def plot(self, metric="Total",title:str=None, xlabel:str=None, ylabel:str=None, **kwargs)->Tuple[plt.Figure,plt.Axes]:
        fig,axs= self.team_stats.plot(metric=metric,title=title, xlabel=xlabel, ylabel=ylabel, **kwargs)        
        plt.show()
        return fig,axs
class TeamList:
    TL = TypeVar("TL", bound="TeamList")
    def __init__(self,teams:Optional[List[Team]]=None,season_id:SeasonID=None) -> None:
        self.teams = teams if teams is not None else []
        self.team_dict = OrderedDict()
        self.season_id = season_id if season_id is not None else SeasonID(number_of_teams=len(self.teams))
    def add_team(self, team:Team):
        if team not in self.teams:
            self.teams.append(team)
            self.team_dict[team.id] = team
            self.season_id.number_of_teams = len(self.teams)
    def sort_by_id(self,in_place:bool=False)->Union[List[Team],None]:
        # return self.teams.sort(key=lambda x: x.id) # Inplace sort
        if in_place:
            return self.teams.sort(key=lambda x: x.id) # Inplace sort
        else:
            return sorted(self.teams, key=lambda x: x.id)
    def sort_by_name(self,in_place:bool=False)->Union[List[Team],None]:
        # return self.teams.sort(key=lambda x: x.name) # Inplace sort
        if in_place:
            return self.teams.sort(key=lambda x: x.name)
        else:
            return sorted(self.teams, key=lambda x: x.name)
    def sort_by_city(self,in_place:bool=False)->Union[List[Team],None]:
        # return self.teams.sort(key=lambda x: x.city) # Inplace sort
        if in_place:
            return self.teams.sort(key=lambda x: x.city)
        else:
            return sorted(self.teams, key=lambda x: x.city)
    def sort_by_stat(self, stat:str,date:Date=None,reverse:bool=True,in_place:bool=False)->Union[List[Team],None]:
        # return self.teams.sort(key=lambda x: x.get_stat(stat, date), reverse=reverse) # Inplace sort
        if in_place:
            return self.teams.sort(key=lambda x: x.get_stat(stat, date), reverse=reverse)
        else:
            return sorted(self.teams, key=lambda x: x.get_stat(stat, date), reverse=reverse)
        #      return self.teams.sort(key=lambda x: x.get_stat(stat,date), reverse=reverse) # Inplace sort
        # #return sorted(self.teams, key=lambda x: x.get_stat(stat))
    def get_team_stats_to_date(self, date:Date)->List[GameStats]:
        return [team.total_to_date(date) for team in self.teams]
    def get_team_stats(self)->List[GameStats]:
        return [team.total() for team in self.teams]
    def print_stat_ranking(self, stat:str="Goals", date:Date=None, reverse:bool=True)->None:
        self.sort_by_stat(stat, date, reverse)
        print(f"Rankings by {stat}"+(" to date" if date is not None else ""))
        for i, team in enumerate(self.teams):
            print(f"{i+1}. {team.name} ({team.id}) - {team.get_stat(stat, date)}")
    def __getitem__(self, item:TeamID)->Team:
        if isinstance(item, TeamID):
            return self.team_dict[item]
        elif isinstance(item, int):
            return self.teams[item]
        else:
            raise TypeError(f"item must be either TeamID or int, not {type(item)}")
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
