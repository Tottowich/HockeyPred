# This file contains helpful classes to represent the data in a more convenient way.
# Path: utils\Representations.py
# Such as; Record, ...
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
import sys
import re
import datetime as dt
import matplotlib.pyplot as plt
# Custom name for typing
from typing import List, Dict, Tuple, Union, Optional,Any
# Create custom typing given a string
from typing import TypeVar
Team = TypeVar('Team')
import datetime as dt
# Create custom named dictionary
from typing import NamedTuple
# Ordered dictionary
from collections import OrderedDict

@dataclass # This should be sortable
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.date = dt.datetime(year, month, day)
    def next_date(self):
        # See if the next day is valid and return it
        if self.month in [1, 3, 5, 7, 8, 10]:
            if self.day == 31:
                return Date(self.year, self.month + 1, 1)
            else:
                return Date(self.year, self.month, self.day + 1)
        elif self.month in [4, 6, 9, 11]:
            if self.day == 30:
                return Date(self.year, self.month + 1, 1)
            else:
                return Date(self.year, self.month, self.day + 1)
        elif self.month == 2:
            if self.day == 28:
                return Date(self.year, self.month + 1, 1)
            else:
                return Date(self.year, self.month, self.day + 1)
        elif self.month == 12:
            if self.day == 31:
                return Date(self.year + 1, 1, 1)
            else:
                return Date(self.year, self.month, self.day + 1)
        else:
            raise ValueError("Invalid date")

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}"
    def __repr__(self):
        return f"{self.year}-{self.month}-{self.day}"
    def __gt__(self, other):
        return self.date > other.date
    def __lt__(self, other):
        return self.date < other.date
    def __ge__(self, other):
        return self.date >= other.date
    def __le__(self, other):
        return self.date <= other.date
    def __eq__(self, other):
        return self.date == other.date
    def __ne__(self, other):
        return self.date != other.date
    def __hash__(self):
        return hash(self.date)

        
@dataclass
class SeasonID:
    number_of_teams: int # Number of teams in the season
    number_of_games: int # Number of games in the season for each team
    def __init__(self, season_id:Union[str,int], number_of_teams:int, number_of_games:int=None):
        self.season_id = season_id
        self.number_of_teams = number_of_teams
        self.number_of_games = number_of_games
        if self.number_of_games is None:
            # Calculate total number of games
            self.number_of_games = int(self.number_of_teams * (self.number_of_teams - 1) / 2)
    def __str__(self):
        return f"Season {self.season_id} with {self.number_of_teams} teams and {self.number_of_games} games."
    def id(self):
        return self.season_id
    def __eq__(self, __o: object) -> bool:
        return self.season_id == __o.season_id
    def __hash__(self):
        return hash(self.season_id)
    def __repr__(self):
        return f"Season {self.season_id} with {self.number_of_teams} teams and {self.number_of_games} games."
@dataclass
class TeamID:
    def __init__(self, team_name,team_id:int=None, team_abbreviation:str=None, team_city:str=None):
        self._team_name = team_name
        self._team_id = team_id
        self._team_abbreviation = team_abbreviation
        self._team_city = team_city
        if self._team_id is None: # If the id is not given, then create it
            self._team_id = id(self)
    @property
    def id(self):
        return self._team_id
    @property
    def name(self):
        return self._team_name
    @property
    def abbreviation(self):
        return self._team_abbreviation
    @property
    def city(self):
        return self._team_city
    def __str__(self):
        s = f"( Team name: {self.name}"
        s += f" ID: {self.id}" if self.id is not None else ""
        s += f" Abrv: {self.abbreviation}" if self.abbreviation is not None else ""
        s += f" City: {self.city}" if self.city is not None else ""
        s += " )"
        return s
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, TeamID):
            return self.id == __o.id
        else:
            return False
    def __hash__(self):
        return hash(self.id)
    def __contains__(self, __o: object) -> bool:
        # if "self in __o" is called, then this function is called
        # This is used to check if a team is in a list of teams
        if isinstance(__o, TeamID):
            return self.id == __o.id
        elif isinstance(__o, str):
            return self.name == __o
    def __repr__(self):
        return f"{self.name} ({self.id})"
    def __lt__(self, other):
        return self.id < other.id
    def __gt__(self, other):
        return self.id > other.id
    def __le__(self, other):
        return self.id <= other.id
    def __ge__(self, other):
        return self.id >= other.id
    def __ne__(self, other):
        return self.id != other.id
    def __eq__(self, other):
        return self.id == other.id
    
    

# Each team has a record of wins, losses and ties.
# This class is used to represent that record.




class Stats:
    stats: Dict[str, Union[int, float]]
    date: Date
    home: bool
    def __init__(self, stats:Dict[str, Union[int, float]], date:Date,home:bool):
        self.stats = stats
        self.date = date
        self.home = home
    @property
    def categories(self):
        return list(self.stats.keys())
    def __str__(self):
        return f"---Date: {self.date}---\nStats: {dict_to_print_string(self.stats)},\n Home: {self.home}"
    def __add__(self, other):
        if other==0:
            print("Adding 0")
            return Stats(self.stats, self.date, self.home)
        new_stats = self.stats.copy() # Copy the stats dictionary
        assert issubclass(type(other), Stats), f"Can only add Stats objects to Stats objects. Got {type(other)}" 
        self_keys = self.stats.keys()
        other_keys = other.stats.keys()
        for key in other_keys:
            if key in self_keys:
                new_stats[key] += other.stats[key]
            else:
                new_stats[key] = other.stats[key]
            
        return Stats(new_stats, other.date,self.home and other.home)
    def __sub__(self, other): # Subtracting stats in order: self - other
        new_stats = self.stats
        assert issubclass(type(other), Stats), "Can only subtract Stats objects"
        self_keys = self.stats.keys()
        other_keys = other.stats.keys()
        #date = self.date
        for key in other_keys:
            if key in self_keys:
                new_stats[key] -= other.stats[key]
            else:
                new_stats[key] = -other.stats[key]
        return Stats(new_stats, other.date,self.home)
    def __mul__(self, other):
        new_stats = self.stats
        date = self.date
        if issubclass(type(other), Stats):
            self_keys = self.stats.keys()
            other_keys = other.stats.keys()
            date = other.date
            for key in other_keys:
                if key in self_keys:
                    new_stats[key] *= other.stats[key]
                else:
                    new_stats[key] = other.stats[key]
        elif issubclass(type(other), int) or issubclass(type(other), float):
            for key in self.stats.keys():
                new_stats[key] = self.stats[key] * other
            return Stats(new_stats, date,self.home)
        else:
            raise NotImplementedError(f"Cannot multiply Stats object with type {type(other)}")
    def __truediv__(self, other): # Divide stats by key in order: self / other
        new_stats = self.stats
        date = self.date
        if issubclass(type(other), Stats):
            self_keys = self.stats.keys()
            other_keys = other.stats.keys()
            date = other.date
            for key in other_keys:
                if key in self_keys:
                    new_stats[key] = self.stats[key] / other.stats[key]
                else:
                    new_stats[key] = other.stats[key]
        elif issubclass(type(other), int) or issubclass(type(other), float):
            for key in self.stats.keys():
                new_stats[key] = self.stats[key] / other
        return Stats(new_stats, date,self.home)
    def __len__(self):
        return len(self.stats)
    def __getitem__(self, key):
        return self.stats[key]
    def __eq__(self, other):
        raise NotImplementedError("Cannot compare Stats objects")
    def __radd__(self, other): # This is called when the other object is not a Stats object
        return self + other
    def plot(self, ax: plt.Axes=None, title: str=None, xlabel: str=None, ylabel: str=None, **kwargs):
        fig = None
        if ax is None:
            fig, ax = plt.subplots()
        ax.bar(self.stats.keys(), self.stats.values(), **kwargs)
        # The keys should be on the x-axis in an angle
        ax.xaxis.set_ticklabels(self.stats.keys(), rotation=45, ha="right")
        # Make the window fit the labels
        if title is not None:
            ax.set_title(title)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        if fig is not None:
            fig.tight_layout()
            plt.show()
        return ax
        

        





@dataclass # This class is used to represent statsheets
class GameStats(Stats):
    #stats: Dict[str, Union[int, float]]
    def __init__(self, team:Team,date:Date,stats:Dict[str, Union[int, float]],home:bool):
        super().__init__(stats, date,home)
        self.team = team
        #self.stats = stats
        assert "Goals" in self.stats.keys(), "Score must be in the stats"
        #self.home = home
    def __str__(self) -> str:
        return f"\'{self.team.name}\' had the following stats on {self.date}:{dict_to_print_string(self.stats,8)}"
@dataclass
class StatList:
    stats: OrderedDict[Date,Stats]
    def __init__(self, stats:List[Stats]=None):
        self.stats = OrderedDict()
        if stats is not None:
            if isinstance(stats, list):
                for stat in stats:
                    assert issubclass(type(stat), Stats), "All elements in the list must be Stats objects"
                    self.stats[stat.date] = stat
            else:
                assert issubclass(type(stats), Stats), "All elements in the list must be Stats objects"
                self.stats[stats.date] = stats
    def plot(self, ax:plt.Axes=None,date=None,title: str=None, xlabel: str=None, ylabel: str=None, **kwargs):
        # Create a subplot for each stat
        game_stats = self.total_to_date(date)
        ax = game_stats.plot(ax=ax,title=title, xlabel=xlabel, ylabel=ylabel, **kwargs)
        return ax
    def __str__(self) -> str:
        return f"Number of recorded stats: {len(self.stats)}:\n{[str(stat) for stat in self.stats]}"
    def __add__(self, other): # Add results in combining stats for a longer list
        # Can bombine StatLists or Stats subclasses
        if issubclass(type(other), StatList):
            return StatList(self.stats + other.stats)
        elif issubclass(type(other), Stats):
            return StatList(self.stats + [other])
        else:
            raise ValueError(f"Cannot add StatList with type {type(other)}")
    def append(self, stat:Stats):
        assert issubclass(type(stat), Stats), "Can only append Stats objects"
        self.stats[stat.date] = stat
    def __getitem__(self, date:Date):
        return self.stats[date]
    def __len__(self):
        return len(self.stats)
    def __iter__(self):
        return iter(self.stats.items())
    def __contains__(self, date:Date):
        return date in self.stats.keys()
    def __eq__(self, other):
        raise NotImplementedError("Cannot compare StatLists")
    def total_to_date(self, final_date:Date=None):
        cumulative_stats = Stats({}, final_date, True)
        counter = 0
        for date, stats in self:
            if final_date is None or date <= final_date:
                counter += 1
                cumulative_stats += stats
            else:
                return cumulative_stats, counter # If date specified, return the stats up to that date and the number of games
        return cumulative_stats
    def total(self):
        return self.total_to_date()
    def average(self):
        return self.total() / len(self)
    def average_to_date(self, final_date:Date=None):
        total, counter = self.total_to_date(final_date)
        return total / counter
    def last_n(self, n:int):
        return StatList(list(self.stats.values())[-n:])
    def clear(self):
        self.stats = OrderedDict() # Clear the stats
    @property
    def added_dates(self):
        return list(self.stats.keys())
    def sort(self):
        self.stats = OrderedDict(sorted(self.stats.items(), key=lambda x: x[0]))
class TeamStats:
    def __init__(self, team:Team):
        self.team = team
        self.home_stats_calendar = StatList()
        self.away_stats_calendar = StatList()
        self.stats_calendar = StatList()
    def add_stats(self, stats:GameStats):
        assert isinstance(stats, GameStats), "Stats must be of type GameStats"
        assert stats.team == self.team, "Stats must be for the same team"
        assert stats.date not in self.stats_calendar.added_dates, "Stats for this date already exist"
        if stats.home:
            self.home_stats_calendar.append(stats)
        else:
            self.away_stats_calendar.append(stats)
        self.stats_calendar.append(stats)
    def add_game(self, game:"Game", home:bool):
        if home:
            self.add_stats(game.home_stats)
        else:
            self.add_stats(game.away_stats)
    def stats_by_date(self, date:Date):
        assert date in self.stats_calendar.added_dates, "No stats for this date"
        return self.stats_calendar[date]
    def total(self):
        return self.stats_calendar.total()
    def total_to_date(self, final_date:Date=None):
        return self.stats_calendar.total_to_date(final_date)
    def average(self):
        return self.stats_calendar.average()
    def average_to_date(self, final_date:Date=None):
        return self.stats_calendar.average_to_date(final_date)
    def home_total(self):
        return self.home_stats_calendar.total()
    def home_total_to_date(self, final_date:Date=None):
        return self.home_stats_calendar.total_to_date(final_date)
    def home_average(self):
        return self.home_stats_calendar.average()
    def home_average_to_date(self, final_date:Date=None):
        return self.home_stats_calendar.average_to_date(final_date)
    def away_total(self):
        return self.away_stats_calendar.total()
    def away_total_to_date(self, final_date:Date=None):
        return self.away_stats_calendar.total_to_date(final_date)
    def away_average(self):
        return self.away_stats_calendar.average()
    def away_average_to_date(self, final_date:Date=None):
        return self.away_stats_calendar.average_to_date(final_date)
    def get_game_stats(self, date:Union[Date,List[Date]]):
        if isinstance(date, list):
            # Sum the stats for each date
            return 
        else:
            return self.stats_calendar[date]
    def get_stat(self,stat_name:str, date:Date=None):
        if date is None:
            return self.total()[stat_name]
        else:
            return self.total_to_date(date)[stat_name]
    def get_stat_per_game(self,stat_name:str, date:Date=None):
        if date is None:
            return self.average()[stat_name]
        else:
            return self.average_to_date(date)[stat_name]
    def get_home_stat(self,stat_name:str, date:Date=None):
        if date is None:
            return self.home_total()[stat_name]
        else:
            return self.home_total_to_date(date)[stat_name]
    def get_home_stat_per_game(self,stat_name:str, date:Date=None):
        if date is None:
            return self.home_average()[stat_name]
        else:
            return self.home_average_to_date(date)[stat_name]
    def get_away_stat(self,stat_name:str, date:Date=None):
        if date is None:
            return self.away_total()[stat_name]
        else:
            return self.away_total_to_date(date)[stat_name]
    def get_away_stat_per_game(self,stat_name:str, date:Date=None):
        if date is None:
            return self.away_average()[stat_name]
        else:
            return self.away_average_to_date(date)[stat_name]
    def last_n(self, n:int):
        return self.stats_calendar.last_n(n)
    def last_n_home(self, n:int):
        return self.home_stats_calendar.last_n(n)
    def last_n_away(self, n:int):
        return self.away_stats_calendar.last_n(n)
    def last_n_average(self, n:int):
        return self.last_n(n).average()
    def last_n_home_average(self, n:int):
        return self.last_n_home(n).average()
    def last_n_away_average(self, n:int):
        return self.last_n_away(n).average()
    def plot(self, metric="total",date:Date=None, title:str=None, xlabel:str=None, ylabel:str=None, **kwargs):
        assert metric is None or metric.lower() in ["total","average"], "Metric must be either 'Total' or 'Average'"
        calenders = [self.stats_calendar, self.home_stats_calendar, self.away_stats_calendar]
        # Set first letter of metric to uppercase rest to lowercase

        metric = metric[0].upper() + metric[1:].lower()
        labels = [metric, metric+" Home", metric+" Away"]
        total = metric == "Total"
        # Create the plot
        fig, axs = plt.subplots(1,3)
        for calender,ax,label in zip(calenders,axs,labels):
            if date is None:
                title = f"{self.team.name} {label} Stats."
                if total:
                    calender.total().plot(ax,title=title, xlabel=xlabel, ylabel=ylabel,**kwargs)
                else:
                    calender.average().plot(ax,title=title, xlabel=xlabel, ylabel=ylabel,**kwargs)
            else:
                title = f"{self.team.name} {label} Stats to {date}."
                if total:
                    calender.total_to_date(date).plot(ax,title=title, xlabel=xlabel, ylabel=ylabel,**kwargs)
                else:
                    calender.average_to_date(date).plot(ax,title=title, xlabel=xlabel, ylabel=ylabel,**kwargs)
        fig.tight_layout()
        # Set windown size:
        fig.set_size_inches(14.5, 8.5)
        plt.show()
    def clear(self):
        self.home_stats_calendar.clear()
        self.away_stats_calendar.clear()
        self.stats_calendar.clear()
    
    @property
    def home_games_played(self):
        return len(self.home_stats_calendar)
    @property
    def away_games_played(self):
        return len(self.away_stats_calendar)
    @property
    def games_played(self):
        return len(self.stats_calendar)
    def __str__(self) -> str:
        return f"{self.team.name} has the following stats:\n{self.stats_calendar}"
    def __len__(self):
        return len(self.stats_calendar)
    def clear(self):
        self.home_stats_calendar.clear()
        self.away_stats_calendar.clear()
        self.stats_calendar.clear()

        
        

@dataclass # This class is used to represent a Game
class Game:
    season: SeasonID 
    home_stats: GameStats
    away_stats: GameStats
    date: Date
    def __init__(self, season:SeasonID,home_stats:GameStats,away_stats:GameStats):
        self.season = season
        self.home_stats = home_stats
        assert home_stats.home, "Home stats must be for home team"
        self.away_stats = away_stats
        assert not away_stats.home, "Away stats must be for away team"
        self.date = home_stats.date
        self.home_score = home_stats.stats["Goals"]
        self.away_score = away_stats.stats["Goals"]
    def stat_by_team(self, team:Team):
        if self.home_team == team:
            return self.home_stats
        elif self.away_team == team:
            return self.away_stats
        else:
            raise ValueError(f"Team {team.name} is not in this game.")
    def home_win(self):
        return self.home_score > self.away_score
    def away_win(self):
        return self.away_score > self.home_score
    def tie(self):
        return self.home_score == self.away_score
    @property
    def home_team(self):
        return self.home_stats.team
    @property
    def away_team(self):
        return self.away_stats.team
    @property
    def teams(self):
        return [self.home_team.id, self.away_team.id]
    def __str__(self) -> str:
        return f"{self.home_team.name} ({self.home_score}) vs {self.away_team.name} ({self.away_score})"



def dict_to_print_string(d, indent=0) -> str:
    s = f""
    for key, value in d.items():
        if isinstance(value, dict):
            s += f"\n{' '*indent}{key}:\n{dict_to_print_string(value, indent+4)}"
        else:
            s += f"\n{' '*indent}{key}: {value}"
    return s
@dataclass
class Record:
    season: SeasonID
    team: Team
    wins: int
    losses: int
    ties: int
    def __init__(self, season:SeasonID, team:Team):
        self.season = season
        self.team = team
        self._wins = 0
        self._losses = 0
        self._ties = 0
        self.streak = 0
        self.history = []
    def add_game(self,date:Date,game:Game):
        assert game.season == self.season, "Game must be in the same season"
        assert game.home_team == self.team or game.away_team == self.team, "Game must be for this team"
        result = 0 # 1 for win, 0 for tie, -1 for loss
        if game.home_win() and game.home_team == self.team:
            result = 1
            self.add_win()
            self.streak += 1
        elif game.away_win() and game.away_team == self.team:
            result = 1
            self.add_win()
            self.streak += 1
        elif game.tie():
            self.add_tie()
            self.streak = 0
        else:
            self.add_loss()
            self.streak = -1 if self.streak > 0 else self.streak - 1
        self.history.append((date,game))
    def add_win(self):
        self._wins += 1
    def add_loss(self):
        self._losses += 1
    def add_tie(self):
        self._ties += 1
    def clear(self):
        self._wins = 0
        self._losses = 0
        self._ties = 0
        self.streak = 0
        self.history = []
    def last_n(self, n:int):
        return self.history[-n:]
    @property
    def wins(self):
        return self._wins
    @property
    def losses(self):
        return self._losses
    @property
    def ties(self):
        return self._ties
    @property
    def games_played(self):
        return self._wins + self._losses + self._ties
    @property
    def win_percentage(self):
        return self._wins / self.games_played
    @property
    def loss_percentage(self):
        return self._losses / self.games_played
    @property
    def tie_percentage(self):
        return self._ties / self.games_played
    def __str__(self) -> str:
        return f"{self.team.name} has a record of {self._wins}-{self._losses}-{self._ties} in the {self.season.season_id} season."