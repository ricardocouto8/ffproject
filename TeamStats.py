class TeamStats(object):

	def set_goal_difference(self):
		self.goal_difference = self.goals_scored - self.goals_conceded

	def __init__(self, competition, wins = None, draws = None, losses = None, goals_scored = None, goals_conceded = None, points = None):
		self.competition = competition

		if wins is None:
			wins = 0
		self.wins = wins

		if draws is None:
			draws = 0
		self.draws = draws

		if losses is None:
			losses = 0
		self.losses = losses

		if goals_scored is None:
			goals_scored = 0
		self.goals_scored = goals_scored

		if goals_conceded is None:
			goals_conceded = 0
		self.goals_conceded = goals_conceded

		self.goal_difference = self.goals_scored - self.goals_conceded

		if points is None:
			points = 0
		self.points = points
