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
from .Teams import Team, TeamList

@dataclass
class ConfusionMatrix:
    """A confusion matrix for a team list.\n
    The matrix is a square matrix of size len(team_list) x len(team_list).\n
    The matrix is indexed by the team_list's team ids.
    The i,j entry is the number of games won by team i against team j.\n"""
    team_list:TeamList
    matrix:np.ndarray
    def __init__(self, team_list:TeamList, matrix:np.ndarray=None) -> None:
        self.team_list = team_list
        self.team_to_index = {team.id: i for i, team in enumerate(team_list)}
        self.index_to_team = {i: team.id for i, team in enumerate(team_list)}
        self.matrix = matrix if matrix is not None else np.zeros((len(team_list), len(team_list)))
    def add_game(self, team_win:TeamID, team_loss:TeamID)->None:
        if isinstance(team_win, Team):
            team_win = team_win.id
        if isinstance(team_loss, Team):
            team_loss = team_loss.id
        if team_win is not None:
            self.matrix[self.team_to_index[team_win], self.team_to_index[team_loss]] += 1 if team_win != team_loss else 0
            
    def get_entry(self, team1:TeamID, team2:TeamID,percentage:bool=False)->Union[Tuple[int,int],Tuple[float,float]]:
        won = self.matrix[self.team_to_index[team1], self.team_to_index[team2]]
        lost = self.matrix[self.team_to_index[team2], self.team_to_index[team1]]
        if percentage:
            p = won/(won+lost)
            return p, 1.0-p
        else:
            return won, lost
    @property
    def win_percentages(self)->np.ndarray:
        total = (self.matrix+self.matrix.T)
        total[total==0] = 1 # Avoid division by zero
        # Devide elementwise
        return self.matrix/total
    def __getitem__(self, teams:Tuple[TeamID,TeamID])->int:
        return self.get_entry(*teams)
    def __repr__(self):
        return f"ConfusionMatrix({self.team_list.team_names})"
    def __str__(self):
        return f"ConfusionMatrix({self.team_list.team_names})"
    def plot(self, ax:plt.Axes=None, title:str="Confusion Matrix", cmap:str="Blues", show:bool=True)->plt.Axes:
        if ax is None:
            fig, ax = plt.subplots(figsize=(10,10))
        ax.set_title(title)
        ax.set_xlabel("Team")
        ax.set_ylabel("Team")
        ax.set_xticks(np.arange(len(self.team_list)))
        ax.set_yticks(np.arange(len(self.team_list)))
        ax.set_xticklabels(self.team_list.team_names, rotation=45, ha="right")
        ax.set_yticklabels(self.team_list.team_names)
        ax.imshow(self.win_percentages, cmap=cmap)
        # Heat bar
        cbar = ax.figure.colorbar(ax.images[0], ax=ax)
        cbar.ax.set_ylabel("Win Percentage", rotation=-90, va="bottom")
        if show:
            plt.show()
        # Make all labels visible in window
        plt.tight_layout()
        return ax

# This is the main class for the season.
# The Season class should hold the following:
# 1. A SeasonID and a TeamList.
# 2. Ability to access the rankings, stats and records of the teams given a Date.
# 3. Ability to return the stats of a team given a Date.
# 4. Confusion matrix for the season at a given Date.

@dataclass
class Season:
    season_id:SeasonID
    team_list:TeamList
    games:List[Tuple[Date, Stats, Stats, GameResult]]
    def __init__(self, team_list:TeamList,season_id:SeasonID=None) -> None:
        # self.season_id:SeasonID = season_id if season_id is not None else 
        if season_id is not None:
            assert season_id == team_list.season_id, f"SeasonID and TeamList's SeasonID must be the same, but got as argument - SeasonID: {season_id}, TeamList's SeasonID: {team_list.season_id}."
        self.season_id = team_list.season_id
        self.team_list:TeamList = team_list
        self.confusion_matrix = ConfusionMatrix(team_list)
        # The games list should contain the date, stats leading up to the game for both teams, and the result of the game.
        self.games:List[Tuple[Date, Stats, Stats, GameResult]] = [] 
    def add_game(self, game:Game)->GameResult:
        # Retrieve the stats of the teams at the date of the game.
        # Get the result of the game.
        # Add the game to the games list.
        # Add the game to the confusion matrix.
        # Add the game to the team's records.
        date = game.date # The date of the game
        home_team, away_team = game.teams
        home_team_stats = self.team_list[home_team].total_to_date(date)
        away_team_stats = self.team_list[away_team].total_to_date(date)

        result = game.result
        # print(f"Adding game: {game} - score {result.one_hot} to {self.season_id}.")
        self.games.append((date, home_team_stats, away_team_stats, result))
        self.confusion_matrix.add_game(result.winner, result.loser)
        # Add the game to the team's records.
        self.team_list[home_team].add_game(game)
        self.team_list[away_team].add_game(game)
        return result
    def print_games(self)->None:
        # Print the games in the season.
        for game in self.games:
            print(game)