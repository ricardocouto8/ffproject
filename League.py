from Config import *
import random
import Match
from operator import attrgetter
random.seed()

class League(object):

	def turn_update_stats(self, turn):
		for match in self.fixtures[turn]:
			if not match.updated:
				match.home.league_stats.goals_scored += match.result[0]
				match.home.league_stats.goals_conceded += match.result[1]
				match.away.league_stats.goals_scored += match.result[1]
				match.away.league_stats.goals_conceded += match.result[0]
				match.home.league_stats.set_goal_difference()
				match.away.league_stats.set_goal_difference()
				if match.result[0] > match.result[1]:
					match.home.league_stats.wins += 1
					match.away.league_stats.losses += 1
					match.home.league_stats.points += self.points_per_win
				elif match.result[1] > match.result[0]:
					match.away.league_stats.wins += 1
					match.home.league_stats.losses += 1
					match.away.league_stats.points += self.points_per_win
				else:
					match.home.league_stats.draws += 1
					match.away.league_stats.draws += 1
					match.home.league_stats.points += self.points_per_draw
					match.away.league_stats.points += self.points_per_draw
				match.updated = True

	def season_fixtures(self):
	    """ Generates a schedule of "fair" pairings from a list of units """
	    units = self.teams
	    if len(units) % 2:
	        units.append(None)
	    count    = len(units)
	    sets     = count - 1
	    half     = count / 2
	    schedule = []
	    for turn in range(sets):
	        left = units[:half]
	        right = units[count - half - 1 + 1:][::-1]
	        pairings = zip(left, right)
	        if turn % 2 == 1:
	            pairings = [(y, x) for (x, y) in pairings]
	        units.insert(1, units.pop())
	        schedule.append(pairings)

	    schedule2 = []
	    for pairing in schedule:
	        pairings = []
	        for pair in pairing:
	            pairings.append((pair[1], pair[0]))
	        schedule2.append(pairings)

	    for pairing in schedule2:
	        schedule.append(pairing)

	    fixtures = []
	    for pairing in schedule:
	    	turn = []
	    	for teams in pairing:
	    		turn.append(Match.Match(teams))
	    	fixtures.append(turn)

	    self.fixtures = fixtures

	def sort_table(self, order = None):
		if order is None:
			return self.teams.sort(key=attrgetter('league_stats.points', 'league_stats.goal_difference', 'league_stats.goals_scored', 'league_stats.wins', 'league_stats.draws'), reverse = True)

	def all_teams_position(self):
		for pos, team in enumerate(self.teams):
			team.league_position = pos + 1

	def __str__(self):
		s = str(self.name) + "\n"
		for team in self.teams:
			s += team.name + "\t" + str(team.league_stats.points) + "\n"
		s +=  '\n'
		return s

	def __init__(self, name, teams = None, fixtures = None, league_size = None, demoted = None):
		self.name = name

		if teams is None:
			teams = []
		self.teams = teams

		if fixtures is None:
			fixtures = []
		self.fixtures = fixtures

		if league_size is None:
			league_size = GAME_GLOBALS["TEAMS_PER_LEAGUE"]
		self.league_size = league_size

		if demoted is None:
			demoted = GAME_GLOBALS["DEMOTED_PER_LEAGUE"]
		self.demoted = 2

		self.points_per_win = 3
		self.points_per_draw = 1
