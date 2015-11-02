from Config import *
import random
import string
random.seed()

class Manager(object):

    id_counter = 0
    """docstring for Manager"""

    def sort_players(self, sort):
        if sort == "Skill":
            return sorted(self.team.players, key=lambda player: player.skill, reverse = True)
        elif sort == "Pos + Skill":
            return sorted(self.team.players, key=lambda player: (-player.pos, player.skill), reverse = True)
        elif sort == "Squad":
            return sorted(self.team.squad, key=lambda player: (-player.pos, player.skill), reverse = True)
        elif sort == "Subs":
            return sorted(self.team.subs, key=lambda player: (-player.pos, player.skill), reverse = True)

    def sell_player(self, player_idx):
        if self.team.sell_player(player_idx):
            return True
        return False

    def substitution(self, player_out, player_in):
        pl_out = self.team.get_player_by_idx(player_out)
        pl_in  = self.team.get_player_by_idx(player_in)
        if pl_out.pos == 0 and pl_in.pos != 0:
            return False
        if pl_out.pos != 0 and pl_in.pos == 0:
            return False
        self.team.squad.remove(pl_out)
        self.team.squad.append(pl_in)
        self.team.subs.remove(pl_in)
        return True

    def go_to_game(self, squad):
        players_per_pos = [[],[],[],[]]
        player_list = list(self.team.players)
        for player_id in squad:
            for player in player_list:
                if player.idx == player_id:
                    player_list.remove(player)
                    players_per_pos[player.pos].append(player)

        #CHECK IF ALL OK
        if len(players_per_pos[0]) == 1:
            squad_list = players_per_pos[0] + players_per_pos[1] + players_per_pos[2] + players_per_pos[3]
            if len(squad_list) == 11:
                self.team.squad = squad_list
                self.team.subs = player_list
                self.team.update_skill_tactic()
                self.ready = True



    def assman_team(self, tactic = None):
        player_per_pos = [[],[],[],[]]
        player_list = []
        sorted_players = self.team.sort_players("Skill")
        for player in sorted_players:
            player_per_pos[player.pos].append(player)

        #GK
        player_list.append(player_per_pos[0][0])

        #FIELD PLAYERS
        if not tactic:
            field_players = player_per_pos[1] + player_per_pos[2] + player_per_pos[3]
            field_players.sort(key=lambda player: player.skill, reverse = True)
            player_list += field_players[:10]

        else:
            for pos, qty in enumerate(tactic):
                player_list += player_per_pos[pos + 1][:qty]

        return player_list

    def possible_tactics(self):
        player_per_pos = [[],[],[],[]]
        for player in self.team.players:
            player_per_pos[player.pos].append(player)

        possible_tactics = []
        for tactic in TEAM_GLOBALS["TACTICS"]:
            allowed = True

            for pos, qty in enumerate(tactic):
                if len(player_per_pos[pos + 1]) < qty:
                    allowed = False
                    break

            if allowed:
                possible_tactics.append(tactic)

        return possible_tactics

    def __init__(self, name = None, team = None, human = False):

        self.idx = Manager.id_counter
        Manager.id_counter += 1
        super(Manager, self).__init__()

        def random_name():
            first = random.choice(string.ascii_uppercase)
            delimiter =  '. '
            last = random.choice(PEOPLE_NAMES)
            return str(first + delimiter + last)

        if name is None:
            name = random_name()
        self.name = name

        self.team = team

        self.human = human

        self.ready = False
