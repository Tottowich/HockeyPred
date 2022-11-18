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
from typing import List, Dict, Tuple, Union, Optional
# Create custom typing given a string
from typing import TypeVar
Team = TypeVar('Team')


@dataclass
class Season:
    season_id: int
    number_of_teams: int
    number_of_games: int
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