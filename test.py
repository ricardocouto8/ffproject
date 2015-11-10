import Game as GAME
from Config import *

GAME.new_game()
GAME.add_human_manager("Ricardo", 31)
GAME.season_start()

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

one_season()
