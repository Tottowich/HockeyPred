from testingfunctions import *
from DataCreation.Teams import *
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
    print(f"\n\n\n{'-'*20}HOME{'-'*20}")
    print(tl[-2].home_total())
    print(tl[-2].home_total())
    print(f"\n\n\n{'-'*20}AWAY{'-'*20}")
    print(tl[-2].away_total())
    print(tl[-2].away_total())
    print(f"\n\n\n{'-'*20}TOTAL{'-'*20}")
    print(tl[-2].total())
    print(tl[-2].total())
def main():
    test_team_list()
if __name__ == '__main__':
    main()