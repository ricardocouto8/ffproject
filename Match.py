from Config import *
import random
import Line
import Player
random.seed()
from pprint import pprint

class Match(object):

    id_counter = 0

    def txt(self, language):
        home_goalscorers = []
        away_goalscorers = []
        for player in self.goalscorers[0]:
            home_goalscorers.append(player)
        for player in self.goalscorers[1]:
            away_goalscorers.append(player)

        txt = {
        "home_team_name" : str(self.home.name),
        "away_team_name" : str(self.away.name),
        "home_team_goals": str(self.result[0]),
        "away_team_goals": str(self.result[1]),
        "home_team_poss" : str(self.possession[0]),
        "away_team_poss" : str(self.possession[1]),
        "home_team_goalscorers": home_goalscorers,
        "away_team_goalscorers": away_goalscorers,
        "minutes"        : str(self.minutes),
        }

        pprint(vars(self))
        return txt

    def set_goalscorer(self, home_goal):
        if home_goal:
            team = self.home
            team_index = 0
        else:
            team = self.away
            team_index = 1

        if len(team.squad) == 0:
            self.goalscorers[team_index].append((Player.Player(skill = 1, age = 20, pos = 3, name = "Ricardo"), self.minutes))
        else:
            player_list = []
            prob_scoring_per_pos = (0, 0.1, 0.3, 0.6)
            sorted_players = sorted(team.squad, key=lambda player: player.skill, reverse = True)
            for player in sorted_players:
                player_list.append((player, player.skill * + prob_scoring_per_pos[player.pos]))

            self.goalscorers[team_index].append((weighted_choice(player_list), self.minutes))
        return True

    def minute(self):
        if self.minutes < MATCH_GLOBALS["TOTAL_TURNS"]:
            self.home.update_skill_tactic()
            self.away.update_skill_tactic()
            self.minutes += 1
            self.events = {"Home Possession": False, "Goal": False}
            home_tactic_inf = [(self.home.tactic[0] - self.away.tactic[2]) * MATCH_GLOBALS["TACTIC_INFLUENCE"],
                                (self.home.tactic[1] - self.away.tactic[1]) * MATCH_GLOBALS["TACTIC_INFLUENCE"],
                                (self.home.tactic[2] - self.away.tactic[0]) * MATCH_GLOBALS["TACTIC_INFLUENCE"]]

            home_concedes_rat   = (self.home.skill[0] - self.away.skill[2]) / float(PLAYER_GLOBALS["MAX_SKILL"]) + home_tactic_inf[0]
            home_possession_rat = (self.home.skill[1] - self.away.skill[1]) / float(PLAYER_GLOBALS["MAX_SKILL"]) + home_tactic_inf[1]
            home_scores_rat     = (self.home.skill[2] - self.away.skill[0]) / float(PLAYER_GLOBALS["MAX_SKILL"]) + home_tactic_inf[2]

            home_scores_prob     = Line.Line(((-1, MATCH_GLOBALS["MIN_GOAL_PER_POSS"]), (1, MATCH_GLOBALS["MAX_GOAL_PER_POSS"]))).solve_for_y(home_scores_rat)
            home_possession_prob = Line.Line(((-1, 1 - MATCH_GLOBALS["MAX_POSSESSION"]),(1, MATCH_GLOBALS["MAX_POSSESSION"]))).solve_for_y(home_possession_rat)
            home_concedes_prob   = Line.Line(((-1, MATCH_GLOBALS["MAX_GOAL_PER_POSS"]), (1, MATCH_GLOBALS["MIN_GOAL_PER_POSS"]))).solve_for_y(home_concedes_rat)

            poss_rand = random.uniform(0, 1)
            goal_rand = random.uniform(0, 1)

            #ANTI GOLEADAS:
            if self.result[0] >= 3 + self.result[1]:
                home_scores_prob = home_scores_prob * MATCH_GLOBALS["ANTI_GOLEADAS"]
            elif self.result[1] >= 3 + self.result[0]:
                home_concedes_prob = home_concedes_prob * MATCH_GLOBALS["ANTI_GOLEADAS"]

            #PROBABILIDADE HUMANA DE MARCAR NO FINAL
            min_norm = normalize(self.minutes, 0, MATCH_GLOBALS["TOTAL_TURNS"])
            if min_norm <= 0.2:
                if self.away.manager.human:
                    home_scores_prob = home_scores_prob * MATCH_GLOBALS["GOAL_BEGINNING_END_MULTI"]
                if self.home.manager.human:
                    home_concedes_prob = home_concedes_prob * MATCH_GLOBALS["GOAL_BEGINNING_END_MULTI"]

            if min_norm >= 0.8:
                if self.home.manager.human:
                    home_scores_prob = home_scores_prob * MATCH_GLOBALS["GOAL_BEGINNING_END_MULTI"]
                if self.away.manager.human:
                    home_concedes_prob = home_concedes_prob * MATCH_GLOBALS["GOAL_BEGINNING_END_MULTI"]

            if poss_rand <= home_possession_prob:
                self.events["Home Possession"] = True
                self.possession[0] += 1
                if goal_rand <= home_scores_prob:
                    self.result[0] += 1
                    self.events["Goal"] = True
                    self.set_goalscorer(True)
            else:
                self.events["Home Possession"] = False
                self.possession[1] += 1
                if goal_rand <= home_concedes_prob:
                    self.result[1] += 1
                    self.events["Goal"] = True
                    self.set_goalscorer(False)
            return True
        else:
            return False

    def substitution(self, team_idx, player_out, player_in):
        if self.minutes > 0 and self.minutes < 90:
            if team_idx == self.home.idx and self.substitutions[0] < self.max_substitutions:
                self.substitutions[0] += 1
                self.home.manager.substitution(player_out, player_in)
                return True
            elif team_idx == self.away.idx and self.substitutions[1] < self.max_substitutions:
                self.substitutions[1] += 1
                self.away.manager.substitution(player_out, player_in)
                return True
        return False

    def __str__(self):
        s = str(self.minutes) + "' : " + str(self.result[0]) + "x" + str(self.result[1]) + "\t"
        if self.events["Home Possession"]:
            s += "Home "
            team_index = 0
        else:
            s += "Away "
            team_index = 1
        if self.events["Goal"]:
            s += "GOAL!!!\n"
            s +=  "Scored by: " + str(self.goalscorers[team_index][-1][0])
        return s

    def __init__(self, teams, goalscorers = None, result = None, possession = None, substitutions = None, max_substitutions = None, minutes = None, updated = None):

        self.idx = Match.id_counter
        Match.id_counter += 1

        self.home = teams[0]
        self.away = teams[1]

        if goalscorers is None:
            goalscorers = [[],[]]
        self.goalscorers = goalscorers


        if result is None:
            result = [0, 0]
        self.result = result

        if possession is None:
            possession = [0, 0]
        self.possession = possession

        if substitutions is None:
            substitutions = [0, 0]
        self.substitutions = substitutions

        if max_substitutions is None:
            max_substitutions = MATCH_GLOBALS["MAX_SUBSTITUTIONS"]
        self.max_substitutions = max_substitutions

        if minutes is None:
            minutes = 0
        self.minutes = 0

        self.events = {"Home Possession": False, "Goal": False}

        if updated is None:
            updated = False
        self.updated = updated
