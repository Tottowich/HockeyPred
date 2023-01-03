# This is a file which contains the classes for the representations of the data while scraping the web of NHL data.
# Author: Theodor Jonsson
# Date: 2023-01-02
# Path: DataScraping/representations.py
#
#   These classes are used to represent the data while the data is being scraped from the web.
#   Examples of these classes are:
#   - WebSeason - A class which represents a season of an entire season. Should hold all links to all games of the season.
#   - WebGame - A class which represents a game of a season. Should hold all the raw data of the game.
#   - WebPlayer - A class which represents a player of a game. Should hold all the raw data of the player.
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import sys
from typing import List, Dict, Tuple, Union, Optional, Any
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataScraping.utils import get_soup
import pandas as pd
from tqdm import tqdm
# Constants
# This is the key for the shot data when scraping the data
PM_KEY = "Unnamed: 5_level_0"
PLAYER_KEY = "Unnamed: 1_level_0"
SHOT_KEY = "Unnamed: 14_level_0"
SHOT_PERCENTAGE_KEY = "Unnamed: 15_level_0"
SHIFT_KEY = "Unnamed: 16_level_0"
TOI_KEY = "Unnamed: 17_level_0"
# Advanced stat keys for the advanced stats
ADVANCED_KEYS = ["ALLAll","ALL5v5","ALLEV","ALLPP","ALLSH","CLAll","CL5v5"]
class WebGame:
    def __init__(self,url:str,home_team:str,away_team:str,verbose:bool=False):
        """
        A class which represents a game of a season. Should hold all the raw data of the game.
        
        Parameters
        ----------
        url : str
            The url of the game to get the data from. Should be in form of https://www.hockey-reference.com/boxscores/xxxxxxxx.html
        verbose : bool, optional
            If the class should be verbose, by default False
        """
        self.url = url   
        self.game = get_soup(self.url)
        self.verbose = verbose
        self.home_team:str = home_team
        self.away_team:str = away_team
        self.home_stats:Dict[str,Any] = {}
        self.away_stats:Dict[str,Any] = {}
        self.regular_tables = None
        self.advanced_tables = []
        self._get_tables()
    def _get_tables(self):
        """
        Get all the tables of the game, modifies self.tables
        """
        self.regular_tables = self.game.find_all('table',id=re.compile(r'(\w+)_skaters'))
        for advanced_key in ADVANCED_KEYS:
            self.advanced_tables.append((advanced_key,self.game.find_all('table',id=re.compile(r'(\w+)_'+advanced_key))))
        
    def _get_game_info(self):
        """
        Get the game info of the game, modifies self.home_stats and self.away_stats
        """
        # Get normal stats
        self._get_normal_stats()
        # Get advanced stats
        self._get_advanced_stats()
    def _get_normal_stats(self):
        """
        Get the 'normal' stats of the game, modifies self.home_stats and self.away_stats
        """
        key = "reg"
        # Find all the tables of the form 'xxx_skaters' and 'xxx_goalies'
        home_stats = self._process_table(key,self.regular_tables[0])
        away_stats = self._process_table(key,self.regular_tables[1])
        # Add goals against
        home_stats["Goals Against"] = away_stats["Goals"]
        away_stats["Goals Against"] = home_stats["Goals"]
        # Add shots against
        home_stats[key+"_SA"] = away_stats[key+"_S"]
        away_stats[key+"_SA"] = home_stats[key+"_S"]

    def _get_advanced_stats(self):
        for advanced_key,advanced_table in self.advanced_tables:
            home_adv = self._process_table(advanced_key,advanced_table[0])
            away_adv = self._process_table(advanced_key,advanced_table[1])
            self.home_stats.update(home_adv)
            self.away_stats.update(away_adv)
    def _process_table(self,key:str,table_soup:BeautifulSoup)->Dict[str,Any]:
        """
        Process the advanced table of the game.
        """
        temp_dict = {}
        # Read the table into a pandas dataframe
        df = pd.read_html(str(table_soup))[0]
        ### Remove the redundant columns ###
        df.pop("Scoring")
        df.pop("Assists")
        df.pop(PLAYER_KEY)
        df.pop(PM_KEY)
        df.pop(SHOT_PERCENTAGE_KEY)
        df.pop(SHIFT_KEY)
        df.pop(TOI_KEY)
        ###

        # The last row is the totals
        totals = df.iloc[-1,:].to_dict()
        # Remove the 'Player' column
        temp_dict = {key+"_"+k if not isinstance(k,tuple) else key+"_"+k[-1]:0 if v!=v else v for k,v in totals.items()}
        temp_dict = {k:v/100 if k.endswith("%") else v for k,v in temp_dict.items()}
        # temp_dict.pop(key+'_Player')
        temp_dict[key+"_Goals"] = temp_dict[key+"_EV"]+temp_dict[key+"_PP"]+temp_dict[key+"_SH"]
        return temp_dict
    def __str__(self) -> str:
        return f"WebGame({self.url}) {self.home_team} vs {self.away_team} {self.home_stats['reg_Goals']} - {self.away_stats['reg_Goals']}"

        

class WebSeason:
    def __init__(self,url:str,verbose:bool=False):
        """
        A class which represents a season of an entire season. Should hold all links to all games of the season.
        
        Parameters
        ----------
        season : str.
            The season to get the games from. Should be in form of https://www.hockey-reference.com/leagues/NHL_xxxx.html
            verbose : bool, optional
            If the class should be verbose, by default False
        """
        # Check if the url is valid
        assert re.match(r'https://www.hockey-reference.com/leagues/NHL_\d{4}.html',url),f"Season url must be in form of https://www.hockey-reference.com/leagues/NHL_xxxx.html, not {url}"
        self.season_soup = get_soup(url)
        # Remove the .html from the url
        self.url = url.split('.html')[0] # https://www.hockey-reference.com/leagues/NHL_xxxx Use this to get various tables/data
        self.verbose = verbose
        self.games = []
        self._get_team_names()
        self._get_games()
        self._get_game_stats()
    def _get_team_names(self):
        # Get the expanded standings table https://www.hockey-reference.com/leagues/NHL_xxxx_standings.html#expanded_standings
        standings_link = self.url + '_standings.html#expanded_standings'
        standings_table = pd.read_html(standings_link)[0]
        self.team_names = standings_table.iloc[:,1].values
        self.team_names.sort()
    def _get_games(self):
        # Get the table with all the games. https://www.hockey-reference.com/leagues/NHL_xxxx_games.html#games
        games_table_link = self.url + '_games.html#games'
        self._game_table = pd.read_html(games_table_link)[0]
        if self.verbose:
            # Print number of games
            print(f"Found {len(self._game_table)} games")
        # Get the links to the games
        # The table contains hyperlinks to the games. We need to get the links to the games.
        # The links are in the form of /boxscores/xxxxxxxx.html
        # Get soup of the games link
        games_soup = get_soup(games_table_link)
        self._game_links = [self.url+link.get('href') for link in games_soup.find(id='all_games').find_all('a') if "/boxscores/" in link.get('href')]
        # Get all the links
    def _get_game_stats(self):
        # Get the stats of all the games
        i = 10
        for game_link,away_team,home_team in tqdm(zip(self._game_links,self._game_table["Visitor"].values,self._game_table["Home"].values)):
            self.games.append(WebGame(game_link,home_team,away_team,verbose=self.verbose))
            if self.verbose:
                print(f"Found game {game_link}")
            i -= 1
            if i == 0:
                break
    def print_games(self):
        for game in self.games:
            print(game)
    def __str__(self) -> str:
        return f"WebSeason({self.url})"
            

    
    
