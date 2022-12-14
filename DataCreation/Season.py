from dataclasses import dataclass
from typing import List, Union, Tuple, Optional, TypeVar
import numpy as np
import pandas as pd
import os
import sys
import re
import datetime as dt
import matplotlib.pyplot as plt
from .Representations import Record, SeasonID, TeamID,Game,Date,Stats,GameResult
from .Teams import Team, TeamList
from tqdm import tqdm
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
    games:List[Tuple[Date, List[Stats],Record, List[Stats],Record, GameResult]]
    def __init__(self, 
                team_list:TeamList,
                season_id:SeasonID=None,
                average:bool=True,
                home:bool=False,
                away:bool=False,
                total:bool=False,
                last_n:int=None,
                ) -> None:
        # self.season_id:SeasonID = season_id if season_id is not None else 
        if season_id is not None:
            assert season_id == team_list.season_id, f"SeasonID and TeamList's SeasonID must be the same, but got as argument - SeasonID: {season_id}, TeamList's SeasonID: {team_list.season_id}."
        self.season_id = team_list.season_id
        self.team_list:TeamList = team_list
        self.confusion_matrix = ConfusionMatrix(team_list)
        # The games list should contain the date, stats leading up to the game for both teams, and the result of the game.
        self.games = [] 
        self.average:bool = average
        self.home:bool = home
        self.away:bool = away
        self.total:bool = total
        self.last_n:int = last_n
        self._init = True
        self._played_dates = None
    def add_game(self, game:Game,date:Date=None)->GameResult:
        # Retrieve the stats of the teams at the date of the game.
        # Get the result of the game.
        # Add the game to the games list.
        # Add the game to the confusion matrix.
        # Add the game to the team's records.
        date = game.date if date is None else date
        home_team_id, away_team_id = game.teams
        # stats_home = []
        # stats_away = []
        home_team = self.team_list[home_team_id]
        away_team = self.team_list[away_team_id]
        home_prev_date = home_team.played_dates.get_closest_date(date)
        away_prev_date = away_team.played_dates.get_closest_date(date)
        record_home = home_team.record.record_by_date(home_prev_date)
        record_away = away_team.record.record_by_date(away_prev_date)
        # This is quite ugly, but it works.
        stats_home,stats_away = self._get_stats(home_team, away_team, date)
        result = game.result
        # print(f"Adding game: {game} - score {result.one_hot} to {self.season_id}.")
        self.games.append((date, stats_home,record_home, stats_away, record_away, result))
        self.confusion_matrix.add_game(result.winner, result.loser)
        # Add the game to the team's records.
        self.team_list[home_team_id].add_game(game)
        self.team_list[away_team_id].add_game(game)
        return result
    def _get_stats(self, home_team:Team, away_team:Team, date:Date)->Tuple[List[Stats],List[Stats]]:
        # Get the stats of the teams at the date of the game.
        stats_home = []
        stats_away = []
        if self.last_n:
            # Get all the dates of the last n games
            dates_home = home_team.played_dates.get_n_closest_dates(date, self.last_n)
            dates_home_home = home_team.played_dates_home.get_n_closest_dates(date, self.last_n)
            dates_home_away = home_team.played_dates_home.get_n_closest_dates(date, self.last_n)
            # The same for the away team
            dates_away_home = away_team.played_dates_away.get_n_closest_dates(date, self.last_n)
            dates_away_away = away_team.played_dates_away.get_n_closest_dates(date, self.last_n)
            dates_away = away_team.played_dates.get_n_closest_dates(date, self.last_n) 
        if self.average:
            stats_home.append(home_team.average_to_date(date))
            stats_away.append(away_team.average_to_date(date))
            if self.last_n:
                stats_home.append(home_team.team_stats.dates_to_statlist(dates_home).average())
                stats_away.append(away_team.team_stats.dates_to_statlist(dates_away).average())
        if self.home:
            stats_home.append(home_team.home_average_to_date(date)) 
            stats_away.append(away_team.home_average_to_date(date))
            if self.last_n: # Find the last n games played at home
                stats_home.append(home_team.team_stats.dates_to_statlist(dates_home_home).average())
                stats_away.append(away_team.team_stats.dates_to_statlist(dates_away_home).average())
        if self.away:
            stats_home.append(home_team.home_average_to_date(date))
            stats_away.append(away_team.away_average_to_date(date))
            if self.last_n: # Find the last n games played away
                stats_home.append(home_team.team_stats.dates_to_statlist(dates_home_away).average())
                stats_away.append(away_team.team_stats.dates_to_statlist(dates_away_away).average())
        if self.total:
            stats_home.append(home_team.total_to_date(date))
            stats_away.append(away_team.total_to_date(date))
            if self.last_n:
                stats_home.append(home_team.team_stats.dates_to_statlist(dates_home).total())
                stats_away.append(away_team.team_stats.dates_to_statlist(dates_away).total())
        return stats_home, stats_away
    def print_games(self,n:int=None)->None:
        # Print the games in the season.
        index_to_stat_type = self.index_desc
        print(index_to_stat_type)
        for k,game in enumerate(self.games):
            # Print the contents of the game.
            date, stats_home, record_home, stats_away, record_away, result = game
            print(f"\n\nGame date: {date}")
            print(f"Home Team record before: {record_home}")
            print(f"Away Team record before: {record_away}")
            print(f"Result: {result}")
            print(f"Number of stats: {len(stats_home)}")
            print(f"Number of stats: {len(stats_away)}")
            for i,stat in enumerate(stats_home):
                print(f"Home Team: \'{index_to_stat_type[i]}\': {stat}")
            for i,stat in enumerate(stats_away):
                print(f"Away Team: \'{index_to_stat_type[i]}\': {stat}")
            if n and k > n:
                break
    def print_single_game(self,index)->None:
        # Print a single game.
        index_to_stat_type = self.index_desc
        date, stats_home, record_home, stats_away, record_away, result = self.games[index]
        print(f"\n\nGame date: {date}")
        print(f"Home Team record before: {record_home}")
        print(f"Away Team record before: {record_away}")
        print(f"Result: {result}")
        for i,stat in enumerate(stats_home):
            print(f"Home Team: \'{index_to_stat_type[i]}\': {stat}")
        for i,stat in enumerate(stats_away):
            print(f"Away Team: \'{index_to_stat_type[i]}\': {stat}")
        return date, stats_home, record_home, stats_away, record_away, result
    @property
    def index_desc(self)->list[str]:
        index_to_stat_type = []
        if self.average:
            index_to_stat_type.append("TD")
        if self.last_n:
            index_to_stat_type.append(f"Last{self.last_n}")
        if self.home:
            index_to_stat_type.append("H")
            if self.last_n:
                index_to_stat_type.append(f"H-Last{self.last_n}")
        if self.away:
            index_to_stat_type.append("A")
            if self.last_n:
                index_to_stat_type.append(f"A-Last{self.last_n}")
        if self.total:
            index_to_stat_type.append("Tot")
            if self.last_n:
                index_to_stat_type.append(f"Tot-Last{self.last_n}")
        return index_to_stat_type

    def sort_games(self)->None:
        # Sort the games in the season.
        self.games.sort(key=lambda x: x[0]) # Sort by date
        return self.games
    def stats_to_pandas(self,stat:str)->pd.DataFrame:
        """Store the stat for each team at each date in a pandas dataframe.
        Structre of the dataframe:

        Header: | Date | Team | Team | Team | ... |
        Row:    | Date | Stat | Stat | Stat | ... |
        """
        self.sort_games()
        # Create the header.
        header = ["Date"]
        for team in self.team_list:
            header.append(team.name)
        # Create the rows.
        rows = []
        for date in self.played_dates:
            row = [str(date)]
            for team in self.team_list:
                if stat.lower() not in ["win%","win percentage"]:
                    row.append(team.get_stat_to_date(date,stat))
                else:
                    row.append(team.record.win_percentage)
                # row.append(team.get_stat_per_game(date,stat))
            rows.append(row)
        # Create the dataframe.
        df = pd.DataFrame(rows,columns=header)
        return df
    def last_date(self)->Date:
        # Find the maximum date in the season.
        return max(self.games,key=lambda x: x[0])[0]
    def first_date(self)->Date:
        # Find the minimum date in the season.
        return min(self.games,key=lambda x: x[0])[0]
    @property
    def played_dates(self)->list[Date]:
        if not self._played_dates:
            self._all_played_dates()
        return self._played_dates
    @property
    def number_of_teams(self)->int:
        return len(self.team_list)
    def _all_played_dates(self)->list[Date]:
        # Find all the dates in the season.
        self._played_dates = []
        for game in self.games:
            date, stats_home, record_home, stats_away, record_away, result = game
            if date not in self._played_dates:
                self._played_dates.append(date)
        self._played_dates.sort()
        return self._played_dates



from matplotlib.animation import FuncAnimation
class SeasonVisualizer:
    """
    Class to help visualize a season.
    The visualizable for any given Date will be:    
        - The confusion matrix.
        - The team records, sorted by win percentage.
        - The team stats, sorted by the given stat.
        - Animation of the confusion matrix through time.
        - Animation of the team rankings through time.
        - Animation of the team stats through time.
    Animations are handled by matplotlib.animation.FuncAnimation.
    """
    def __init__(self,season:Season):
        self._season = season
        self._season.sort_games()
        self._last_date = season.last_date()
        self._first_date = season.first_date()
    def _nice_axes(self,ax:plt.Axes):
        ax.set_facecolor('.8')
        ax.tick_params(labelsize=8, length=0)
        ax.grid(True, axis='x', color='white')
        ax.set_axisbelow(True)
        [spine.set_visible(False) for spine in ax.spines.values()]
        return ax
    def animate(self,stat:str='Win%',save:bool=False,figsize:tuple=(10,10),interval:int=100):
        """
        Animate the season based on the given stat.
        """
        import bar_chart_race as bcr
        self._season.sort_games()
        played_dates = self._season.played_dates
        df = self._season.stats_to_pandas(stat)
        # print(f"df: {df}")
        # html = bcr.bar_chart_race(df=df,filename="test.gif",figsize=figsize,period_length=len(played_dates))
        # print(f"Played dates: {played_dates}")
        # exit()
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()
        colors = plt.cm.Dark2(range(self._season.number_of_teams))
        def init():
            print(f"Initalizing animation for stat: {stat}")
            ax.clear()
            self._nice_axes(ax)
            # Set the y axis to be the team names.
            ax.set_yticks(range(self._season.number_of_teams))
            ax.set_yticklabels(self._season.team_list.team_names)
        def update(i):
            for bar in ax.containers:
                bar.remove()
            name_value_list = self._season.team_list.team_stat_list(stat,date=self._season.played_dates[i])
            name_value_list.sort(key=lambda x: x[1],reverse=False)
            print(f"Name value list: {name_value_list}")
            names = [name for name,value in name_value_list]
            values = [value for name,value in name_value_list]
            # The x axis will be the stat value.
            # The y axis will be the team names, should be sorted by the stat value.
            ax.barh(range(self._season.number_of_teams),values,color=colors)
            ax.set_title(f"Season {stat} on {self._season.played_dates[i]}")
        # anim = FuncAnimation(fig=fig, func=update, init_func=init, frames=len(self._season.played_dates), interval=200, repeat=False,blit=False)
        # # View the animation.
        # if save:
        #     anim.save(f"Season_{stat}.gif", writer='imagemagick')
        # plt.show()
    
        # return anim


class SeasonExporter:
    """
    Export a season to a file.
    The export file will be a csv of the following structure:
    # Start File
    Row 0 - Col 0: Game ID, Col 1 - Home Team ID, Col 2: Away Team ID, Col 3 Date
    Row 1 - Col 0: Stat key, Col 1 - Home Team Stat, Col 2 - Away Team Stat
    Row 2 - Col 0: Stat key, Col 1 - Home Team Result, Col 2 - Away Team Stat
    ...
    Row n - Col 0: Stat key, Col 1 - Home Team Stat, Col 2 - Away Team Stat # n is the number of stats.
    Row n+1 - Col 0: Result key, Col 1 - 1 if home team won, Col 2 - 1 if away team won, Col 3 - 1 if tie.
    # The next row is the next game.
    Row n+2 - Col 0: Game ID, Col 1: Date, Col 2 - Home Team ID, Col 3: Away Team ID
    ...
    # End File
    """
    def __init__(self, season:Season,
                export_dir:str=None,
                export_file:str=None,
                export_format:str="csv",
                ):
        self.season = season
        self.export_dir = export_dir
        self.export_file = export_file
        self.export_format = export_format.split(".")[-1]
        self.export_path = None
        self._build_export_path()
        self._game_id = 0
    def _build_export_path(self)->None:
        # Build the export path.
        if not self.export_dir:
            self.export_dir = os.path.join(os.getcwd(), "exports")
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
        if not self.export_file:
            self.export_file = f"{self.season.season_id}.{self.export_format}"
        self.export_path = os.path.join(self.export_dir, self.export_file)
    def export(self)->None:
        if self.export_format == "csv":
            self._export_csv()
        else:
            raise NotImplementedError(f"Export format {self.export_format} not implemented yet.")
    def _export_csv(self)->None:
        # Export the games to a csv file.
        games = self.season.games
        index_to_stat_type = self.season.index_desc
        with open(self.export_path, "w") as f:
            # Initialize Progression bar:
            pbar = tqdm(total=len(games),desc="Exporting games!")
            # Comment out the following line if you don't want the header.
            f.write("Game ID,Home Team ID,Away Team ID,Date\n")
            for game in games:
                pbar.update(1)
                date, stats_home, record_home, stats_away, record_away, result = game # Extract the game data.
                home_team_id = result.home_team
                away_team_id = result.away_team
                f.write(f"Game_{self._game_id},{home_team_id.name},{away_team_id.name},{date}\n")
                self._game_id += 1
                f.write(f"TeamIDHome,{home_team_id.id},{home_team_id.name},\n")
                for i,stat in enumerate(stats_home):
                    stat = stat.to_pandas(index_to_stat_type[i])
                    # Write using the pandas to_csv method.
                    stat.to_csv(f, mode="a", header=False)
                    # New line after each stat.
                    f.write("\n")
                f.write(f"TeamIDAway,{away_team_id.id},{away_team_id.name},\n")
                for i,stat in enumerate(stats_away):
                    stat = stat.to_pandas(index_to_stat_type[i])
                    # Write using the pandas to_csv method.
                    stat.to_csv(f, mode="a", header=False)
                    # New line after each stat.
                    f.write("\n")
                # Last row is the result.
                f.write(f"Result,{result.home_win},{result.away_win},{result.tie}\n\n")
                # if self._game_id > 10:
                #     break # Temporarily only write one game.
                    
                








            



       