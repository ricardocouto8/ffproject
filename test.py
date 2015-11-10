import Game as GAME
from Config import *

#GAME.new_game()
#GAME.season_start()

def one_season():
    while GAME.season == 0:
    	print "Turn " + str(GAME.turn + 1)
    	#Sets lineup for all teams
    	GAME.go_to_game()
    	#Runs match
    	while GAME.minute_matches():
    		pass
    	#After match
        print_table()
    	GAME.post_league_matches()
    	GAME.turn_past()

def print_table():
    tables = GAME.leagues_table()
    table = tables[0]
    position = 1
    print "Division 0"
    for team in table:
        team_name = team.txt("LANG")["team_name"]
        team_points = team.txt("LANG")["team_league_points"]
        print str(position) + '\t' + team_name + '\t' + team_points
        position += 1

def weekly_salaries():
    test_team = GAME.competitions[0].teams[0]
    print test_team.money
    test_team.weekly_player_salaries_payment()
    print test_team.money

def player_salary_test():
    for i in range(PLAYER_GLOBALS["MAX_SKILL"]):
        print "Skill:", i + 1, calc_season_salary(i)
