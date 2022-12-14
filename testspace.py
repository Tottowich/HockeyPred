from testingfunctions import *
from DataCreation.Teams import *
from DataCreation.Season import *
def test_team_list(N:int=30):
    tl = team_list(N)
    # for team in tl:
    #     print(f"\n{team.name}: {team.total()}")
    match_ups = all_match_ups(tl)
    print(f"\n{len(match_ups)} match ups")
    date = Date(2019,1,1)
    for home,away in match_ups:
        # print(f"{away.name} @ {home.name}")
        game = simulate_game(home,away,date)
        # Add the game to the teams
        home.add_game(game)
        away.add_game(game)
        date = date.next_date()
    # print(f"\n{len(tl)} teams")
    # for team in tl:
    #     print(f"\n{team.name}: {team.home_total()}")
    # for team in tl:
    #     print(f"\n{team.name}: {team.record}")
    # tl.print_stat_ranking("Powerplay Goals")
    team_stats = tl[0].team_stats
    print(team_stats.home_stats_calendar.added_dates.get_closest_date(Date(2019,3,3),direction='below'))
    print(len(team_stats.away_stats_calendar.added_dates))
    print(team_stats.get_game_stats(team_stats.away_stats_calendar.added_dates))
    # print(f"\n\n\n{'-'*20}HOME{'-'*20}")
    # print(tl[-2].home_total())
    # print(f"\n\n\n{'-'*20}AWAY{'-'*20}")
    # print(tl[-2].away_total())
    # print(f"\n\n\n{'-'*20}TOTAL{'-'*20}")
    print(tl[0].total())
    # tl[0].plot()
    print(tl.season_id)
def test_confusion_matrix(N:int=30):
    tl = team_list(N)
    cm = ConfusionMatrix(tl)
    # for team in tl:
    #     print(f"\n{team.name}: {team.total()}")
    match_ups = all_match_ups(tl)
    print(f"\n{len(match_ups)} match ups")
    date = Date(2019,1,1)
    for i in range(10): # 20 matche ups.
        for home,away in match_ups:
            # print(f"{away.name} @ {home.name}")
            game = simulate_game(home,away,date)
            # Add the game to the teams
            home_win = home.add_game(game)
            away.add_game(game)
            date = date.next_date()
            team_win = home if home_win else away
            team_loss = away if home_win else home
            cm.add_game(team_win,team_loss)
    cm.plot()
def test_season(N:int=30,reps:int=10):
    season = simulate_season(reps=reps,average=True,home=True,away=True,last_n=10)
    games = season.games
    cm = season.confusion_matrix
    # season.print_games(10)
    date,home,home_rec,away,away_rec,result = season.print_single_game(-1)
    cm.plot()
def test_season_weird(N:int=30,reps:int=10):
    season = simulate_season_weird(reps=reps,average=True,home=True,away=True,last_n=10)
    games = season.games
    cm = season.confusion_matrix
    # season.print_games(10)
    date,home,home_rec,away,away_rec,result = season.print_single_game(-1)
    cm.plot()
def test_exporting_season(N:int=30,reps:int=10):
    season = simulate_season_weird(reps=reps,average=True,home=True,away=True,last_n=10)
    se = SeasonExporter(season)
    se.export()
def test_visualizer():
    # season = simulate_season(reps=1,average=True,home=True,away=True,last_n=10)
    season_weird = simulate_season_weird(N_teams=2,reps=100,average=True,home=True,away=True,last_n=10)
    sv = SeasonVisualizer(season_weird)
    sv.animate()
def main():
    # test_season_weird(reps=1)
    # test_team_list()
    test_visualizer()
if __name__ == '__main__':
    main()