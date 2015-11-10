from Config import *
import random
random.seed()
from pprint import pprint
from operator import add, sub

class Team(object):

    id_counter = 0
    def txt(self, language):
    #   Returns a dict of strings for the GUI
        goal_difference = self.league_stats.goal_difference
        if goal_difference >= 0:
            goal_difference = '+' + str(goal_difference)
        else:
            goal_difference = str(goal_difference)
        txt = {
        "team_name" : str(self.name),
        "team_league_points"  : str(self.league_stats.points),
        "team_goal_difference" : goal_difference,
        "team_money" : str(num2str(self.money)),
        "team_league_position" : str(self.league_position),
        }
        return txt

    def sort_players(self, sort):
        if sort == "Skill":
            return sorted(self.players, key=lambda player: player.skill, reverse = True)
        elif sort == "Pos + Skill":
            return sorted(self.players, key=lambda player: (-player.pos, player.skill), reverse = True)
        elif sort == "Squad":
            return sorted(self.squad, key=lambda player: (-player.pos, player.skill), reverse = True)
        elif sort == "Subs":
            return sorted(self.subs, key=lambda player: (-player.pos, player.skill), reverse = True)

    def team_equilibrium(self):
    #   Returns list with how many players the team needs to buy/sell to be balanced (ex: [0, 1, -1, 2] means the team needs to sell 1 defender and 2 strikers, and buy 1 midfielder)
        players_per_pos = self.players_per_position()
        ideal_players_per_pos = [3, 0, 0, 0]
        for i in range(3):
            ideal_players_per_pos[i+1] = int(round(self.tactic[i] + self.tactic[i] * 0.5, 0))

        return map(sub, players_per_pos, ideal_players_per_pos)

    def auto_transfer_list(self):
    #   Calculates ranking of players per skill
    #   Transfer-lists the worst players in each position according to team equilibrium
        for player in self.players:
            player.transfer_listed = True

    def get_player_by_idx(self, player_idx):
    #   Gets player_idx
    #   Returns player with that idx
        for player in self.players:
            if player.idx == player_idx:
                return player

    def update_skill_tactic(self):
    #   Calculates def,mid,atk according to the players in squad
    #   Sets self.skill -> def,mid,atk skill of a human team
    #   Sets self.tactic -> tuple with the tactic selected
        if self.manager.human:
            skill = [0, 0, 0, 0]
            count = [0, 0, 0, 0]
            sk = [0, 0, 0]

            for player in self.squad:
                skill[player.pos] += player.skill
                count[player.pos] += 1

            skill[1] += skill[0]
            count[1] += count[0]
            skill = skill[1:]
            count = count[1:]

            for i, ski in enumerate(skill):
                if count[i] > 0:
                    sk[i] = ski / float(count[i])
                else:
                    sk[i] = 0

            self.skill = sk
            self.tactic = tuple(count)

    def training(self):
    #   Trains all players in team
    # & Run once per turn

        ground_norm = normalize(5, TEAM_GLOBALS["MIN_TRAINING_GROUND"], TEAM_GLOBALS["MAX_TRAINING_GROUND"])
        for player in self.players:
            skill_norm = normalize(player.skill, PLAYER_GLOBALS["MIN_SKILL"], PLAYER_GLOBALS["MAX_SKILL"])
            if ground_norm >= skill_norm:
                ground_inf = 1
            else:
                ground_inf = min(max(1 - 3 * (skill_norm - ground_norm), 0), 1)

            player.turn_training(ground_inf)

    def remove_player(self, player):
    #   Gets player
    #   Removes player from team
        try:
            self.players.remove(player)
        except:
            pass
        try:
            self.squad.remove(player)
        except:
            pass
        try:
            self.subs.remove(player)
        except:
            pass

    def players_per_position(self):
    #   Returns tuple w/ how many players per position the team has
        player_per_pos = [0,0,0,0]
        for pla in self.players:
            player_per_pos[pla.pos] += 1
        return tuple(player_per_pos)

    def team_can_sell_player(self, player):
    #   Checks if there's enough players in the team for you to sell one
    #   Returns True if player can be sold, False if cannot
        player_per_pos = self.players_per_position()
        if player_per_pos[0] >= 1:
            if player_per_pos[1] + player_per_pos[2] + player_per_pos[3] > 10:
                return True
        return False

    def sell_player(self, player):
    #   Checks if you can sell a player
    #   Calls remove_player
    #   Updates the team money
    #   Returns True if player was sold, False if not
        if team_can_sell_player(player):
            pl = self.get_player_by_idx(player)
            self.remove_player(pl)
            self.money += pl.value
            return True
        return False

    def add_player(self, player):
    #   Adds player to player list
        self.players.append(player)

    def team_can_buy_player(self, player, value):
        if self.money >= value:
            if len(players) <= TEAM_GLOBALS["MAX_PLAYERS"]:
                return True
        return False

    def buy_player(self, player, value):
    #   Checks if you can buy a player
    #   Calls add_player
    #   Updates the team money
    #   Returns True if player was sold, False if not
        if team_can_buy_player(player, value):
            pl = self.get_player_by_idx(player)
            self.add_player(pl)
            self.money -= value
            return True
        return False

    def __str__(self):
        return str(self.idx) + '\n' + "Rep: " + str(self.rep) + '\n' +  "DF|MD|AT: " + str(self.skill[0]) + " | " + str(self.skill[1]) + " | " + str(self.skill[2]) + '\n\n'

    def __init__(self, rep, name = None, skill = None, tactic = None, manager = None, players = None, turn_scouted_players = None, league_position = None, league_stats = None):

        self.idx = Team.id_counter
        Team.id_counter += 1

        def random_name(idx):
            return "Team " + str(idx%8) + "- Div " + str(idx/8)

        def random_skill(rep):
            skill = []
            skill_variation = int(round(PLAYER_GLOBALS["MAX_SKILL"] * 0.05, 0))
            avg_skill = rep * PLAYER_GLOBALS["MAX_SKILL"]/float(TEAM_GLOBALS["MAX_REP"])

            for i in range(3):
                sk = avg_skill + random.randint(-skill_variation, skill_variation)
                sk = int(min(max(sk, PLAYER_GLOBALS["MIN_SKILL"]), PLAYER_GLOBALS["MAX_SKILL"]))
                skill.append(sk)

            return skill

        if name is None:
            name = random_name(self.idx)
        self.name = name

        self.rep = rep

        if skill is None:
            skill = random_skill(rep)
        self.skill = skill

        if tactic is None:
            tactic = random.choice(TEAM_GLOBALS['TACTICS'])
        self.tactic = tactic

        self.manager = manager

        if players is None:
            players = []
        self.players = players

        self.squad = []

        self.subs = []

        if turn_scouted_players is None:
            turn_scouted_players = []
        self.turn_scouted_players = turn_scouted_players

        self.money = rep * TEAM_GLOBALS["MIN_MONEY"]

        self.league_position = league_position

        self.league_stats = league_stats
