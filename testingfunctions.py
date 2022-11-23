
from DataCreation.Teams import Team
from DataCreation.Representations import SeasonID,Record,Game,GameStats,Date,TeamStats,TeamID,SeasonID

def rand_teams():
    pit_id = TeamID("Pitsburgh Penguins",team_id=1,team_city="Pitsburgh")
    nyr_id = TeamID("New York Rangers",team_id=2,team_city="New York")
    van_id = TeamID("Vancouver Canucks",team_id=3,team_city="Vancouver")
    season_id = SeasonID(2019,3)
    Pitsburgh = Team(pit_id, season_id)
    New_York = Team(nyr_id, season_id)
    Vancouver = Team(van_id, season_id)
    return Pitsburgh, New_York, Vancouver, season_id
# Generate dictionaries like the above for each game:
def rand_team_stats():
    rnd_game = rnd_game_stats_home = {
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
import random
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
def rand_teamstats(Pitsburgh, Vancouver):
    day = 1
    month = 1
    year = 2019
    date = Date(year, month, day)
    for i in range(1000):
        Pit_stat = rand_team_stats()
        Van_stat = rand_team_stats()
        Pit_home = random.randint(0,1)==1
        Van_home = not Pit_home
        Pit_stat = GameStats(Pitsburgh, date, Pit_stat, Pit_home)
        Van_stat = GameStats(Vancouver, date, Van_stat, Van_home)
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
    for i in range(N):
        pit_stat, van_stat = rand_game()
        Pit_home = random.randint(0,1)==1
        Van_home = not Pit_home
        Pit_stat = GameStats(Pitsburgh, date, pit_stat, Pit_home)
        Van_stat = GameStats(Vancouver, date, van_stat, Van_home)
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
            





# date = Date(2019, 1, 3)
# game_stats_home = GameStats(home_team, date, test_game_stats_home,True)
# game_stats_away = GameStats(away_team, date, test_game_stats_away,False)
# game = Game(season, home_stats=game_stats_home, away_stats=game_stats_away,date=date)

# date2 = Date(2019, 1, 4)
# game_stats_home2 = GameStats(home_team, date2, test2_game_stats_home,True)
# game_stats_away2 = GameStats(away_team, date2, test2_game_stats_away,False)
# game2 = Game(season, home_stats=game_stats_home2, away_stats=game_stats_away2,date=date2)
# print(game)
# print(game2)