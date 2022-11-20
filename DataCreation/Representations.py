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
    
@dataclass # This should be sortable
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.date = dt.datetime(year, month, day)   
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
class Season:
    season_id: int # The id should be unique, ex. "2019-2020"
    number_of_teams: int # Number of teams in the season
    number_of_games: int # Number of games in the season for each team
    def __init__(self, season_id, number_of_teams, number_of_games):
        self.season_id = season_id
        self.number_of_teams = number_of_teams
        self.number_of_games = number_of_games
    def __str__(self):
        return f"Season {self.season_id} with {self.number_of_teams} teams and {self.number_of_games} games."

# Each team has a record of wins, losses and ties.
# This class is used to represent that record.

@dataclass
class Record:
    season: Season
    team: Team
    wins: int
    losses: int
    ties: int
    def __init__(self, season:Season, team:Team):
        self.season = season
        self.team = team
        self._wins = 0
        self._losses = 0
        self._ties = 0
        self.streak = 0
        self.history = []
    def add_win(self):
        self._wins += 1
    def add_loss(self):
        self._losses += 1
    def add_tie(self):
        self._ties += 1
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


class Stats:
    stats: Dict[str, Union[int, float]]
    home: bool
    def __init__(self, stats:Dict[str, Union[int, float]], home:bool):
        self.stats = stats
        self.home = home
    def __str__(self):
        return f"Stats: {dict_to_print_string(self.stats)},\n Home: {self.home}"
    def __add__(self, other):
        new_stats = {}
        assert issubclass(type(other), Stats), "Can only add Stats objects"
        self_keys = self.stats.keys()
        other_keys = other.stats.keys()
        for key in other_keys:
            if key in self_keys:
                new_stats[key] += other.stats[key]
            else:
                new_stats[key] = other.stats[key]
            
        return Stats(new_stats, self.home)
    def __sub__(self, other): # Subtracting stats in order: self - other
        new_stats = self.stats
        assert issubclass(type(other), Stats), "Can only subtract Stats objects"
        self_keys = self.stats.keys()
        other_keys = other.stats.keys()
        for key in other_keys:
            if key in self_keys:
                new_stats[key] -= other.stats[key]
            else:
                new_stats[key] = -other.stats[key]
        return Stats(new_stats, self.home)
    def __mul__(self, other):
        new_stats = self.stats
        if issubclass(type(other), Stats):
            self_keys = self.stats.keys()
            other_keys = other.stats.keys()
            for key in other_keys:
                if key in self_keys:
                    new_stats[key] *= other.stats[key]
                else:
                    new_stats[key] = other.stats[key]
        elif issubclass(type(other), int) or issubclass(type(other), float):
            for key in self.stats.keys():
                new_stats[key] = self.stats[key] * other
            return Stats(new_stats, self.home)
        else:
            raise NotImplementedError(f"Cannot multiply Stats object with type {type(other)}")
    def __truediv__(self, other): # Divide stats by key in order: self / other
        new_stats = self.stats
        if issubclass(type(other), Stats):
            self_keys = self.stats.keys()
            other_keys = other.stats.keys()
            for key in other_keys:
                if key in self_keys:
                    new_stats[key] = self.stats[key] / other.stats[key]
                else:
                    new_stats[key] = other.stats[key]
        elif issubclass(type(other), int) or issubclass(type(other), float):
            for key in self.stats.keys():
                new_stats[key] = self.stats[key] / other
            return Stats(new_stats, self.home)
    def __len__(self):
        return len(self.stats)
    def __getitem__(self, key):
        return self.stats[key]
    def __eq__(self, other):
        raise NotImplementedError("Cannot compare Stats objects")
    def plot(self, ax: plt.Axes=None, title: str=None, xlabel: str=None, ylabel: str=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()
        ax.bar(self.stats.keys(), self.stats.values(), **kwargs)
        if title is not None:
            ax.set_title(title)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        return ax
        

        





@dataclass # This class is used to represent statsheets
class GameStats(Stats):
    team: Team
    #stats: Dict[str, Union[int, float]]
    def __init__(self, team:Team,date:Date,stats:Dict[str, Union[int, float]],home:bool):
        super().__init__(stats, home)
        self.team = team
        #self.stats = stats
        assert "Goals" in self.stats.keys(), "Score must be in the stats"
        self._date=date
        #self.home = home
    def __str__(self) -> str:
        return f"\'{self.team.name}\' had the following stats on {self.date}:{dict_to_print_string(self.stats,8)}"
    @property
    def date(self)->Date:
        return self._date
@dataclass
class StatList:
    stats: List[Stats]
    def __init__(self, stats:List[Stats]):
        self.stats = []
        if isinstance(stats, list):
            for stat in stats:
                self.stats.append(stat)
        else:
            self.stats.append(stats)
    def plot(self):
        # Create a subplot for each stat
        num_plots = len(self.stats[0])
        # The plot should be a square grid
        num_rows = int(np.ceil(np.sqrt(num_plots)))
        num_cols = int(np.ceil(num_plots / num_rows))
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(10,10))
        for i, stat in enumerate(self.stats):
            axs[i] = stat.plot(axs[i])
        return fig, axs
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
        self.stats.append(stat)
    def __getitem__(self, key):
        return self.stats[key]
    def __len__(self):
        return len(self.stats)
    def __iter__(self):
        return iter(self.stats)

    
    


class TeamStats:
    def __init__(self, team:Team):
        self.team = team
        self.home_stats_calendar = {}
        self.away_stats_calendar = {}
        self.stats_calendar = {}
    def add_stats(self, stats:GameStats):
        assert isinstance(stats, GameStats), "Stats must be of type GameStats"
        assert stats.team == self.team, "Stats must be for the same team"
        assert stats.date not in self.stats_calendar.keys(), "Stats for this date already exist"
        if stats.home:
            self.home_stats_calendar[stats.date] = stats
        else:
            self.away_stats_calendar[stats.date] = stats
        self.stats_calendar[stats.date] = stats
    def stats_by_date(self, date:Date):
        assert date in self.stats_calendar.keys(), "No stats for this date"
        return self.stats_calendar[date]
    def total_stats_up_to_date(self, final_date:Date):
        cumulative_stats = Stats({}, False)
        for date,stats in self.stats_calendar.items():
            if date <= final_date:
                cumulative_stats += stats
            else:
                break
        return cumulative_stats
    def __str__(self) -> str:
        return f"{self.team.name} has the following stats:{dict_to_print_string(self.stats_calendar,4)}"
        
        

@dataclass # This class is used to represent a Game
class Game:
    season: Season
    home_team: Team
    away_team: Team
    home_score: int
    away_score: int
    def __init__(self, season:Season,home_stats:GameStats,away_stats:GameStats,date:Date):
        self.season = season
        self.home_team = home_stats.team
        self.away_team = away_stats.team
        self.home_stats = home_stats
        self.away_stats = away_stats
        self.date = date
        self.home_score = home_stats.stats["Goals"]
        self.away_score = away_stats.stats["Goals"]
    def stat_by_team(self, team:Team):
        if self.home_team == team:
            return self.home_stats
        elif self.away_team == team:
            return self.away_stats
        else:
            raise ValueError(f"Team {team.name} is not in this game.")

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