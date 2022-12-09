# This file contains helpful classes to represent the data in a more convenient way.
# Path: utils\Representations.py
# Such as; Record, ...
from dataclasses import dataclass
import numpy as np
import pandas as pd
import uuid
import os
import sys
import re
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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
class DateList:
    def __init__(self, dates: List[Date]=None):
        self.dates = dates if dates is not None else []
    def add_date(self, date: Date):
        # The date should be inserted in order of date
        # if date not in self.dates:
        #     self.dates.append(date)
        #     self.dates.sort()
        self.dates.append(date)
    def get_closest_date(self, date: Date, direction: str="below"):
        if direction == "below":
            seq = [d for d in self.dates if d <= date]
            if len(seq) == 0:
                return None
            return max(seq)
        elif direction == "above":
            seq = [d for d in self.dates if d >= date]
            if len(seq) == 0:
                return None
            return min(seq)
        else:
            raise ValueError("Invalid direction")
    def get_n_closest_dates(self, date: Date, n: int=1, direction: str="below"):
        assert n > 0, "n must be greater than 0"
        if direction == "below":
            return sorted([d for d in self.dates if d <= date], reverse=True)[:n]
        elif direction == "above":
            return sorted([d for d in self.dates if d >= date])[:n]
        else:
            raise ValueError("Invalid direction")
    def __repr__(self):
        return f"DateList({self.dates})"
    def __str__(self):
        s = f"DateList:\n"
        for date in self.dates:
            s += f"{date}, "
        return s
    def __getitem__(self, index: Union[int, slice]):
        return self.dates[index]
    def __len__(self):
        return len(self.dates)
    def __iter__(self):
        return iter(self.dates)
    def __contains__(self, date):
        return date in self.dates
            

        
@dataclass
class SeasonID:
    number_of_teams: int # Number of teams in the season
    def __init__(self, season_id:Union[str,int]=None,start_date:Date=None, number_of_teams:int=None):
        self.season_id = season_id
        self.start_date = start_date
        self._number_of_teams = number_of_teams
        self._gen_id()
    def _gen_id(self):
        # Generate a random id for the season if one is not provided
        if self.season_id is None:
            self.season_id = str(uuid.uuid4())
    # Make number of teams a property 
    @property
    def number_of_teams(self):
        return self._number_of_teams
    @number_of_teams.setter
    def number_of_teams(self, number_of_teams):
        self._number_of_teams = number_of_teams
    @number_of_teams.deleter
    def number_of_teams(self):
        del self._number_of_teams


    @property
    def number_of_games(self):
        return int(self.number_of_teams * (self.number_of_teams - 1))
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
        return self._team_name if self._team_name is not None else self.id # Fall back to id
    @property
    def abbreviation(self):
        return self._team_abbreviation if self._team_abbreviation is not None else self.name
    @property
    def city(self):
        return self._team_city if self._team_city is not None else self.name # Fall back to name
    def __repr__(self):
        s = f"Team name: {self.name}, ID: {self.id}"
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
    def __add__(self, other:"Stats"):
        if other==0:
            return Stats(self.stats, self.date, self.home)
        new_stats = self.stats.copy() # Copy the stats dictionary
        assert issubclass(type(other), Stats), f"Can only add Stats objects to Stats objects. Got {type(other)}" 
        self_keys = self.stats.keys()
        other_keys = other.stats.keys()
        # Sum the stats that are in both else set to value where it is not in both
        new_stats = dict([(key, self.stats[key] + other.stats[key]) if key in self_keys and key in other_keys else (key, self.stats[key] if key in self_keys else other.stats[key]) for key in self_keys | other_keys])
        # for key in other_keys:
        #     if key in self_keys:
        #         new_stats[key] += other.stats[key]
        #     else:
        #         new_stats[key] = other.stats[key]
            
        return Stats(new_stats, other.date,self.home and other.home)
    def __sub__(self, other:"Stats"): # Subtracting stats in order: self - other
        new_stats = self.stats
        assert issubclass(type(other), Stats), "Can only subtract Stats objects"
        self_keys = self.stats.keys()
        other_keys = other.stats.keys()
        # Subtract the stats that are in both else set to value where it is not in both
        new_stats = dict([(key, self.stats[key] - other.stats[key]) if key in self_keys and key in other_keys else (key, self.stats[key] if key in self_keys else -other.stats[key]) for key in self_keys | other_keys])
        # for key in other_keys:
        #     if key in self_keys:
        #         new_stats[key] -= other.stats[key]
        #     else:
        #         new_stats[key] = -other.stats[key]
        return Stats(new_stats, other.date,self.home)
    def __mul__(self, other:"Stats"):
        new_stats = self.stats
        date = self.date
        if issubclass(type(other), Stats):
            self_keys = self.stats.keys()
            other_keys = other.stats.keys()
            date = other.date
            # Multiply the stats that are in both else set to value where it is not in both
            new_stats = dict([(key, self.stats[key] * other.stats[key]) if key in self_keys and key in other_keys else (key, self.stats[key] if key in self_keys else other.stats[key]) for key in self_keys | other_keys])
            # for key in other_keys:
            #     if key in self_keys:
            #         new_stats[key] *= other.stats[key]
            #     else:
            #         new_stats[key] = other.stats[key]
        elif issubclass(type(other), int) or issubclass(type(other), float):
            # multiply over dictionary
            new_stats = dict([(key, value*other) for key, value in self.stats.items()])
            # for key in self.stats.keys():
            #     new_stats[key] = self.stats[key] * other
            return Stats(new_stats, date,self.home)
        else:
            raise NotImplementedError(f"Cannot multiply Stats object with type {type(other)}")
    def __truediv__(self, other:"Stats"): # Divide stats by key in order: self / other
        new_stats = self.stats
        date = self.date
        if issubclass(type(other), Stats):
            self_keys = self.stats.keys()
            other_keys = other.stats.keys()
            date = other.date
            # Divide the stats that are in both else set to value where it is not in both
            new_stats = dict([(key, self.stats[key] / other.stats[key]) if key in self_keys and key in other_keys else (key, self.stats[key] if key in self_keys else other.stats[key]) for key in self_keys | other_keys])
            # for key in other_keys:
            #     if key in self_keys:
            #         new_stats[key] = self.stats[key] / other.stats[key]
            #     else:
            #         new_stats[key] = other.stats[key]
        elif issubclass(type(other), int) or issubclass(type(other), float):
            # divide over dictionary
            new_stats = dict([(key, value/other) for key, value in self.stats.items()])
            # for key in self.stats.keys():
            #     new_stats[key] = self.stats[key] / other
        return Stats(new_stats, date,self.home)
    def __len__(self):
        return len(self.stats)
    def __getitem__(self, key):
        v = self.stats.get(key, None)
        if v is None:
            print(f"WARNING: Key \'{key}\' not found in stats, replacing with 0")
            return 0
        return v
    def __eq__(self, other:"Stats"):
        raise NotImplementedError("Cannot compare Stats objects")
    def __radd__(self, other:"Stats"): # This is called when the other object is not a Stats object
        return self + other
    def plot(self, ax: plt.Axes=None, title: str=None, xlabel: str=None, ylabel: str=None, **kwargs):
        keys = self.stats.keys()
        values = self.stats.values()
        fig = None
        if ax is None:
            fig, ax = plt.subplots()
        ax.bar(keys, values, **kwargs)
        # The keys should be on the x-axis in an angle
        # ax.xaxis.set_ticklabels(keys, rotation=45, ha="right")
        ticks_loc = ax.get_xticks()
        ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
        # ax.set_yticklabels([label_format.format(x) for x in ticks_loc])
        ax.set_xticklabels(keys, rotation=45, ha="right")
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
    def __init__(self, team:TeamID,date:Date,stats:Dict[str, Union[int, float]],home:bool):
        super().__init__(stats, date,home)
        assert issubclass(type(team), TeamID), f"Team must be a TeamID object, got {type(team)}"
        self._team = team
        #self.stats = stats
        assert "Goals" in self.stats.keys(), "Score must be in the stats"
        #self.home = home
    @property
    def team(self) -> TeamID:
        return self._team
    def __str__(self) -> str:
        return f"\'{self._team.name}\' had the following stats on {self.date}:{dict_to_print_string(self.stats,8)}"
@dataclass
class StatList:
    _stats: OrderedDict[Date,Stats]
    def __init__(self, stats:List[Stats]=None):
        self._stats = OrderedDict()
        self._added_dates = DateList()
        if stats is not None:
            if isinstance(stats, list):
                self._stats = OrderedDict([(stat.date, stat) for stat in stats if issubclass(type(stat), Stats)])
                # for stat in stats:
                #     assert issubclass(type(stat), Stats), "All elements in the list must be Stats objects"
                #     self._stats[stat.date] = stat
            else:
                assert issubclass(type(stats), Stats), "All elements in the list must be Stats objects"
                self._stats[stats.date] = stats
    def plot(self, ax:plt.Axes=None,date=None,title: str=None, xlabel: str=None, ylabel: str=None, **kwargs):
        # Create a subplot for each stat
        game_stats = self.total_to_date(date)
        ax = game_stats.plot(ax=ax,title=title, xlabel=xlabel, ylabel=ylabel, **kwargs)
        return ax
    def __str__(self) -> str:
        return f"Number of recorded stats: {len(self._stats)}:\n{[str(stat) for stat in self._stats]}"
    def __add__(self, other): # Add results in combining stats for a longer list
        # Can bombine StatLists or Stats subclasses
        if issubclass(type(other), StatList):
            return StatList(self._stats + other.stats)
        elif issubclass(type(other), Stats):
            return StatList(self._stats + [other])
        else:
            raise ValueError(f"Cannot add StatList with type {type(other)}")
    def append(self, stat:Stats):
        assert issubclass(type(stat), Stats), f"Can only append Stats objects to StatList, not {type(stat)}"
        self._stats[stat.date] = stat
        self._added_dates.add_date(stat.date)
    def __getitem__(self, date:Date):
        return self._stats[date]
    def __len__(self):
        return len(self._stats)
    def __iter__(self):
        return iter(self._stats.items())
    def __contains__(self, date:Date):
        return date in self._stats.keys()
    def __eq__(self, other):
        raise NotImplementedError("Cannot compare StatLists")
    def total_to_date(self, final_date:Date=None)->Stats:
        # cumulative_stats = Stats({}, final_date, True)
        # counter = 0
        # for date, stats in self:
        #     if final_date is None or date <= final_date:
        #         counter += 1
        #         cumulative_stats += stats
        cumulative = [stats for date, stats in self if final_date is None or date <= final_date]
        return sum(cumulative), len(cumulative)
        #return cumulative_stats, counter
    def total(self)->Stats:
        return self.total_to_date()[0]
    def average(self)->Stats:
        return self.total() / len(self)
    def average_to_date(self, final_date:Date=None)->Stats:
        total, counter = self.total_to_date(final_date)
        return total / counter
    def last_n(self, n:int):
        return StatList(list(self._stats.values())[-n:])
    def clear(self):
        self._stats = OrderedDict() # Clear the stats
    @property
    def stats(self):
        return self._stats
    @property
    def added_dates(self)->List[Date]:
        return self._added_dates
    @property
    def available_stats(self)->List[str]:
        return self.total().stats.keys()
    def sort(self):
        self._stats = OrderedDict(sorted(self._stats.items(), key=lambda x: x[0]))
class TeamStats:
    def __init__(self, team:TeamID):
        self.team = team
        self.home_stats_calendar = StatList()
        self.away_stats_calendar = StatList()
        self.stats_calendar = StatList()
    def add_stats(self, stats:GameStats):
        assert isinstance(stats, GameStats), "Stats must be of type GameStats"
        assert stats._team == self.team, "Stats must be for the same team"
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
    def total(self)->Stats:
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
        if isinstance(date, (list, tuple,DateList)):
            # Sum the stats for each date
            return sum([self.stats_by_date(d) for d in date])
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
    def plot(self, metric="total",date:Date=None, title:str=None, xlabel:str=None, ylabel:str=None, **kwargs)->Tuple[plt.Figure, plt.Axes]:
        assert metric is None or metric.lower() in ["total","average"], "Metric must be either 'Total' or 'Average'"
        calenders = [self.stats_calendar, self.home_stats_calendar, self.away_stats_calendar]
        # Set first letter of metric to uppercase rest to lowercase

        metric = metric[0].upper() + metric[1:].lower()
        labels = [metric, metric+" Home", metric+" Away"]
        total = metric == "Total"
        # Create the plot with 3 subplots and figure size 15x5
        fig, axs = plt.subplots(1,3,figsize=(15,5))
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
        return [fig,axs]
    def clear(self):
        self.home_stats_calendar.clear()
        self.away_stats_calendar.clear()
        self.stats_calendar.clear()
    @property
    def available_stats(self):
        return self.stats_calendar.available_stats
    
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
    def __getitem__(self, date:Date):
        return self.stats_calendar[date]
    def clear(self):
        self.home_stats_calendar.clear()
        self.away_stats_calendar.clear()
        self.stats_calendar.clear()




# Result class, win = 1, loss = -1, draw = 0
class GameResult:
    def __init__(self, home_stats:GameStats, away_stats:GameStats):
        self.home_stats = home_stats
        self.away_stats = away_stats
        self.home_score = home_stats.stats["Goals"]
        self.away_score = away_stats.stats["Goals"]
        self.home_team:TeamID = home_stats.team
        self.away_team:TeamID = away_stats.team
        self.result = self.away_win()*-1 + self.home_win() # 1 if home win, -1 if away win, 0 if draw
        self.one_hot = np.array([self.result==1, self.result==0, self.result==-1])  # [1,0,0] if home win, [0,1,0] if draw, [0,0,1] if away win
    def home_win(self):
        return self.home_score > self.away_score
    def away_win(self):
        return self.away_score > self.home_score
    def tie(self):
        return self.home_score == self.away_score
    @property
    def winner(self):
        if self.home_win():
            return self.home_team
        elif self.away_win():
            return self.away_team
        else:
            return None
    @property
    def loser(self):
        if self.home_win():
            return self.away_team
        elif self.away_win():
            return self.home_team
        else:
            return None
    def __str__(self) -> str:
        return f"{self.home_team.name} ({self.home_score}) - ({self.away_score}) {self.away_team.name}"

@dataclass # This class is used to represent a Game
class Game:
    season: SeasonID 
    home_stats: GameStats
    away_stats: GameStats
    date: Date
    def __init__(self, season:SeasonID,home_stats:GameStats,away_stats:GameStats):
        self.season = season
        self._result = GameResult(home_stats, away_stats)
        self.home_stats = home_stats
        assert home_stats.home, "Home stats must be for home team"
        self.away_stats = away_stats
        assert not away_stats.home, "Away stats must be for away team"
        self.date = home_stats.date
        self.home_score = home_stats.stats["Goals"]
        self.away_score = away_stats.stats["Goals"]
    def stat_by_team(self, team:TeamID):
        if self.home_team == team:
            return self.home_stats
        elif self.away_team == team:
            return self.away_stats
        else:
            raise ValueError(f"Team {team.name} is not in this game.")
    def home_win(self):
        return self._result.home_win()
    def away_win(self):
        return self._result.away_win()
    def tie(self):
        return self._result.tie()
    
    @property
    def result(self)->GameResult:
        return self._result
    @property
    def home_team_id(self):
        return self.home_stats._team
    @property
    def away_team_id(self):
        return self.away_stats._team
    @property
    def teams(self):
        return [self.home_team_id, self.away_team_id]
    def __str__(self) -> str:
        return f"{self.home_team_id.name} ({self.home_score}) vs {self.away_team_id.name} ({self.away_score})"



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
    team_id: TeamID
    wins: int
    losses: int
    ties: int
    def __init__(self, season:SeasonID, team_id:TeamID):
        self.season = season
        self.team_id = team_id
        self._wins = 0
        self._losses = 0
        self._ties = 0
        self.streak = 0
        self._history = OrderedDict()
    def add_game(self,date:Date,game:Game)->int: 
        """Adds a game to the record, and returns the result of the game.\n\n 1 for win, 0 for tie, -1 for loss"""
        assert game.season == self.season, "Game must be in the same season"
        assert game.home_team_id == self.team_id or game.away_team_id == self.team_id, "Game must be for this team"
        result = 0
        if game.home_win() and game.home_team_id == self.team_id:
            self.add_win()
            result = 1
        elif game.away_win() and game.away_team_id == self.team_id:
            self.add_win()
            result = 1
        elif game.tie():
            self.add_tie()
            result = 0
        else:
            self.add_loss()
            result = -1
        self._add_history_entry(date, result)
        return result
    def _add_history_entry(self, date:Date, result:int):
        self._history[date] = (result,self.w_l_t, self.streak)

    def add_win(self):
        """Adds a win to the record"""
        self._wins += 1
        if self.streak < 0:
            self.streak = 1
        else:
            self.streak += 1
    def add_loss(self):
        """Adds a loss to the record"""
        self._losses += 1
        if self.streak > 0:
            self.streak = -1
        else:
            self.streak -= 1
    def add_tie(self):
        """Adds a tie to the record"""
        self._ties += 1
        self.streak = 0
    def clear(self):
        """Clears the record, resets all values to 0, keeps the same team and season"""
        self._wins = 0
        self._losses = 0
        self._ties = 0
        self.streak = 0
        self._history = []
    def last_n(self, n:int):
        """Returns the last n games in the record"""
        # First check if n is valid:
        assert n <= len(self._history), f"Cannot get last {n} games, only {len(self._history)} games in record."
        assert n > 0, "n must be greater than 0"
        # Now we can get the last n games:
        raise NotImplementedError # TODO: Finish Last N Record.
    def record_by_date(self, date:Date):
        """Returns the record up to and including the given date"""
        # First check if the date is valid:
        assert date >= self._history[0][0], f"Date {date} is before the first game in the record."
        # We need to sort the history by date:
        history = sorted(self._history, key=lambda x: x[0]) # This is not done in place    
        raise NotImplementedError #TODO Finish Record by date.
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
    def w_l_t(self):
        return (self.wins,self.losses,self.ties)
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
        return f"{self.team_id.name} has a record of {self._wins}-{self._losses}-{self._ties} in the {self.season.season_id} season."