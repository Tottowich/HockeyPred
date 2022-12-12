
from tqdm import tqdm
from DataCreation.Teams import *
from DataCreation.Season import *
from DataCreation.Representations import SeasonID,TeamID
from DataCreation.Representations import Record,Game,Date
from DataCreation.Representations import Record, GameStats,TeamStats
from typing import List, Union
import random
from itertools import permutations
# 30 NHL team names
TEAM_NAMES = [
    "Anaheim Ducks",
    "Arizona Coyotes",
    "Boston Bruins",
    "Buffalo Sabres",
    "Calgary Flames",
    "Carolina Hurricanes",
    "Chicago Blackhawks",
    "Colorado Avalanche",
    "Columbus Blue Jackets",
    "Dallas Stars",
    "Detroit Red Wings",
    "Edmonton Oilers",
    "Florida Panthers",
    "Los Angeles Kings",
    "Minnesota Wild",
    "Montreal Canadiens",
    "Nashville Predators",
    "New Jersey Devils",
    "New York Islanders",
    "New York Rangers",
    "Ottawa Senators",
    "Philadelphia Flyers",
    "Pittsburgh Penguins",
    "San Jose Sharks",
    "St. Louis Blues",
    "Tampa Bay Lightning",
    "Toronto Maple Leafs",
    "Vancouver Canucks",
    "Vegas Golden Knights",
    "Washington Capitals",
]

def rand_teams(N:int=3):
    pit_id = TeamID("Pitsburgh Penguins",team_id=1,team_city="Pitsburgh")
    nyr_id = TeamID("New York Rangers",team_id=2,team_city="New York")
    van_id = TeamID("Vancouver Canucks",team_id=3,team_city="Vancouver")
    season_id = SeasonID(2019,3)
    Pitsburgh = Team(pit_id, season_id)
    New_York = Team(nyr_id, season_id)
    Vancouver = Team(van_id, season_id)
    return Pitsburgh, New_York, Vancouver, season_id
def team_list(N:int=30):
    # season_id = SeasonID(2019,3)
    season_id = None
    teams = []
    tl = TeamList()
    for i in range(N):
        team_id = TeamID(TEAM_NAMES[i])
        # teams.append(Team(team_id,season_id))
        tl.add_team(Team(team_id,season_id))
    return tl
    # return TeamList(teams)
def all_match_ups(team_list:Union[TeamList,List[Team]]):
    team_list = team_list.teams if isinstance(team_list,TeamList) else team_list
    l = list(permutations(team_list,2))
    # Shuffle the list
    random.shuffle(l)
    return l
# Generate dictionaries like the above for each game:
def rand_team_stats():
    rnd_game = {
        "Goals": random.randint(0, 5),
        "Goals Against": random.randint(0, 5),
        "Shots": random.randint(0, 50),
        "Shots againts": random.randint(0, 50),
        "Hits": random.randint(0, 20),
        "Blocks": random.randint(0, 20),
        "Faceoffs Won": random.randint(0, 20),
        "Faceoffs Lost": random.randint(0, 20),
        "Powerplay Goals": random.randint(0, 5),
        "Powerplay Goals Against": random.randint(0, 2),
        "Boxplay Goals": random.randint(0, 2),
        "Boxplay Goals Against": random.randint(0, 5),
        "Powerplay Opportunities": random.randint(0, 10),
        "Boxplay Opportunities": random.randint(0, 10),
        "Penalty Minutes": random.randint(0, 20),
        "Penalty Minutes Drawn": random.randint(0, 20),
    }
    return rnd_game
def very_rand_team_stats():
    team_stats = rand_team_stats()
    for key in team_stats.keys():
        # Remove some stats except for goals and goals against
        u = random.uniform(0, 1)
        if key not in ["Goals","Goals Against"] and u < 0.2:
            team_stats[key] = None
    return team_stats
def rand_game():
    # Generate random stats for one team and match them with the other team
    rnd_game = rand_team_stats()
    rnd_game_away = rand_team_stats()
    rnd_game_away["Goals"] = rnd_game["Goals Against"]
    rnd_game_away["Goals Against"] = rnd_game["Goals"]
    rnd_game_away["Shots"] = rnd_game["Shots againts"]
    rnd_game_away["Shots againts"] = rnd_game["Shots"]
    rnd_game_away["Faceoffs Won"] = rnd_game["Faceoffs Lost"]
    rnd_game_away["Faceoffs Lost"] = rnd_game["Faceoffs Won"]
    rnd_game_away["Powerplay Goals"] = rnd_game["Boxplay Goals Against"]
    rnd_game_away["Powerplay Goals Against"] = rnd_game["Boxplay Goals"]
    rnd_game_away["Boxplay Goals"] = rnd_game["Powerplay Goals Against"]
    rnd_game_away["Boxplay Goals Against"] = rnd_game["Powerplay Goals"]
    rnd_game_away["Powerplay Opportunities"] = rnd_game["Boxplay Opportunities"]
    rnd_game_away["Boxplay Opportunities"] = rnd_game["Powerplay Opportunities"]
    rnd_game_away["Penalty Minutes"] = rnd_game["Penalty Minutes Drawn"]
    rnd_game_away["Penalty Minutes Drawn"] = rnd_game["Penalty Minutes"]
    return rnd_game, rnd_game_away
def very_rand_game():
    # Generate random stats for one team and match them with the other team
    rnd_game = very_rand_team_stats()
    rnd_game_away = very_rand_team_stats()
    rnd_game_away["Goals"] = rnd_game["Goals Against"]
    rnd_game_away["Goals Against"] = rnd_game["Goals"]
    rnd_game_away["Shots"] = rnd_game["Shots againts"]
    rnd_game_away["Shots againts"] = rnd_game["Shots"]
    rnd_game_away["Faceoffs Won"] = rnd_game["Faceoffs Lost"]
    rnd_game_away["Faceoffs Lost"] = rnd_game["Faceoffs Won"]
    rnd_game_away["Powerplay Goals"] = rnd_game["Boxplay Goals Against"]
    rnd_game_away["Powerplay Goals Against"] = rnd_game["Boxplay Goals"]
    rnd_game_away["Boxplay Goals"] = rnd_game["Powerplay Goals Against"]
    rnd_game_away["Boxplay Goals Against"] = rnd_game["Powerplay Goals"]
    rnd_game_away["Powerplay Opportunities"] = rnd_game["Boxplay Opportunities"]
    rnd_game_away["Boxplay Opportunities"] = rnd_game["Powerplay Opportunities"]
    rnd_game_away["Penalty Minutes"] = rnd_game["Penalty Minutes Drawn"]
    rnd_game_away["Penalty Minutes Drawn"] = rnd_game["Penalty Minutes"]
    return rnd_game, rnd_game_away
def rand_teamstats(Pitsburgh:Team, Vancouver:Team):
    day = 1
    month = 1
    year = 2019
    date = Date(year, month, day)
    for i in range(1000):
        Pit_stat = rand_team_stats()
        Van_stat = rand_team_stats()
        Pit_home = random.randint(0,1)==1
        Van_home = not Pit_home
        Pit_stat = GameStats(Pitsburgh.id, date, Pit_stat, Pit_home)
        Van_stat = GameStats(Vancouver.id, date, Van_stat, Van_home)
        Pitsburgh.add_stats(Pit_stat)
        Vancouver.add_stats(Van_stat)
        date = date.next_date()
    return Pitsburgh, Vancouver
def rand_games(start_date:Date=None,N:int=1000):
    Pitsburgh, New_York, Vancouver, season_id = rand_teams()
    if start_date is None:
        day = 1
        month = 1
        year = 2019
        season_id = SeasonID(2019,3)
    else:
        assert isinstance(start_date, Date)
        season_id = SeasonID(start_date.year, number_of_teams=2)
    date = Date(year, month, day)
    # Generate games with progress bar
    for i in range(N):
        pit_stat, van_stat = rand_game()
        Pit_home = random.randint(0,1)==1
        Van_home = not Pit_home
        Pit_stat = GameStats(Pitsburgh.id, date, pit_stat, Pit_home)
        Van_stat = GameStats(Vancouver.id, date, van_stat, Van_home)
        if Pit_home:
            game = Game(season_id, Pit_stat, Van_stat)
            Pitsburgh.add_game(game)
            Vancouver.add_game(game)
        else:
            game = Game(season_id, Van_stat, Pit_stat)
            Vancouver.add_game(game)
            Pitsburgh.add_game(game)
        date = date.next_date()
    return Pitsburgh, Vancouver
def simulate_game(home_team:Team, away_team:Team, date:Date=None):
    home_stats, away_stats = rand_game()
    home_stats = GameStats(home_team.id, date, home_stats, True)
    away_stats = GameStats(away_team.id, date, away_stats, False)
    game = Game(home_team.season_id, home_stats, away_stats)
    return game
def simulate_weird_game(home_team:Team, away_team:Team, date:Date=None):
    home_stats, away_stats = very_rand_game()
    home_stats = GameStats(home_team.id, date, home_stats, True)
    away_stats = GameStats(away_team.id, date, away_stats, False)
    game = Game(home_team.season_id, home_stats, away_stats)
    return game
def rand_date(year:int=None,month:int=None,day:int=None):
    if year is None:
        year = random.randint(2000, 2020)
    if month is None:
        month = random.randint(1, 12)
    if day is None:
        day = random.randint(1, 28)
    return Date(year, month, day)
def rand_games_rand_date(start_date:Date=None,N:int=1000):
    Pitsburgh, New_York, Vancouver, season_id = rand_teams()
    if start_date is None:
        day = 1
        month = 1
        year = 2019
        season_id = SeasonID(2019,3)
    else:
        assert isinstance(start_date, Date)
        season_id = SeasonID(start_date.year, number_of_teams=2)
    date = Date(year, month, day)
    added_dates = [date]
    for i in range(N):
        pit_stat, van_stat = rand_game()
        Pit_home = random.randint(0,1)==1
        Van_home = not Pit_home
        Pit_stat = GameStats(Pitsburgh.id, date, pit_stat, Pit_home)
        Van_stat = GameStats(Vancouver.id, date, van_stat, Van_home)
        if Pit_home:
            game = Game(season_id, Pit_stat, Van_stat)
            Pitsburgh.add_game(game)
            Vancouver.add_game(game)
        else:
            game = Game(season_id, Van_stat, Pit_stat)
            Vancouver.add_game(game)
            Pitsburgh.add_game(game)
        date = rand_date()
        while date in added_dates:
            date = rand_date()
        added_dates.append(date)
    return Pitsburgh, Vancouver
def simulate_season(N_teams:int=30,reps:int=10,average:bool=True,away:bool=False,home:bool=False,total:bool=False,last_n:int=None):
    tl = team_list(N_teams)
    season = Season(tl,average=average,away=away,home=home,total=total,last_n=last_n)
    game_date = Date(2019,1,1)
    match_ups = all_match_ups(tl)
    # Generate games with progress bar
    pbar = tqdm(total=reps*len(match_ups))
    for i in range(reps):
        for home,away in match_ups:
            pbar.update(1)
            game = simulate_game(home,away,game_date)
            game_date = game_date.next_date()
            r = season.add_game(game)
    return season
def simulate_season_weird(N_teams:int=30,reps:int=10,average:bool=True,away:bool=False,home:bool=False,total:bool=False,last_n:int=None):
    tl = team_list(N_teams)
    season = Season(tl,average=average,away=away,home=home,total=total,last_n=last_n)
    game_date = Date(2019,1,1)
    match_ups = all_match_ups(tl)
    # Generate games with progress bar
    pbar = tqdm(total=reps*len(match_ups))
    for i in range(reps):
        for home,away in match_ups:
            pbar.update(1)
            game = simulate_weird_game(home,away,game_date)
            game_date = game_date.next_date()
            r = season.add_game(game)
    return season
