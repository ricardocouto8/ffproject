from Config import *
import random
import League
import Team
import Manager
import Player
import TeamStats
random.seed()

class Game:

    def new_game(self):
        competitions = []
        managers = []


        min_active_rep = TEAM_GLOBALS["MAX_REP"] - (TEAM_GLOBALS["MAX_REP"] - TEAM_GLOBALS["MIN_REP"]) * 0.85
        rep_step = (TEAM_GLOBALS["MAX_REP"] - min_active_rep) / float(GAME_GLOBALS["ACTIVE_LEAGUES"] * GAME_GLOBALS["TEAMS_PER_LEAGUE"])
        current_rep = TEAM_GLOBALS["MAX_REP"]

        for comp_id in range(GAME_GLOBALS["ACTIVE_LEAGUES"]):
            c = League.League("League " + str(comp_id + 1))

            for team_id in range(GAME_GLOBALS["TEAMS_PER_LEAGUE"]):
                t = Team.Team(rep = int(current_rep))
                m = Manager.Manager()
                self.hire_manager(team = t, manager = m)
                managers.append(m)
                #CREATE PLAYERS
                player_list = []
                average_skill = sum(t.skill)/3.0 - PLAYER_GLOBALS["MAX_SKILL"] * 0.05
                for pos, qty in enumerate(TEAM_GLOBALS["PLAYERS_PER_POSITION"]):
                    if pos == 0:
                        how_many_players = qty + random.randint(0, 1)
                    else:
                        how_many_players = qty + random.randint(0, 2)

                    for i in range(how_many_players):
                        this_player_skill = average_skill - (PLAYER_GLOBALS["MAX_SKILL"] * 0.05 * i) / float(how_many_players)
                        player = Player.Player(skill = this_player_skill, pos = pos, avg_skill = True)
                        player.season_training_increase_per_turn()
                        player_list.append(player)

                t.players = player_list
                t.league_stats = TeamStats.TeamStats(c)
                c.teams.append(t)
                current_rep -= rep_step

            competitions.append(c)

        c = League.League("Non League")

        for team_id in range(GAME_GLOBALS["TEAMS_PER_LEAGUE"]):
            t = Team.Team(rep = int(current_rep - rep_step))
            m = Manager.Manager()
            self.hire_manager(team = t, manager = m)
            managers.append(m)
            #CREATE PLAYERS
            player_list = []
            average_skill = sum(t.skill)/3.0
            for pos, qty in enumerate(TEAM_GLOBALS["PLAYERS_PER_POSITION"]):
                for i in range(qty):
                    player = Player.Player(skill = average_skill, pos = pos, avg_skill = True)
                    player.season_training_increase_per_turn()
                    player_list.append(player)
            t.players = player_list
            t.league_stats = TeamStats.TeamStats(c)
            c.teams.append(t)

        competitions.append(c)

        self.competitions = competitions
        self.managers = managers

    #GET BY IDX
    def get_match_by_idx(self, match_idx):
        for comp in self.competitions:
            for game in comp.fixtures[self.turn]:
                if game.idx == match_idx:
                    return game

    def get_team_by_idx(self, team_idx):
        for comp in self.competitions:
            for team in comp.teams:
                if team.idx == team_idx:
                    return team

    def go_to_game(self):
        humans = self.get_managers()
        for human in humans:
            if not human.ready:
                return False
            human.ready = False
        for manager in self.managers:
            if manager.team is not None:
                if manager.human is False:
                    #SETS SQUAD FOR ALL TEAMS
                    manager.team.squad = manager.assman_team(tactic = manager.team.tactic)
        return True

    def leagues_table(self):
        tables = []
        for comp in self.competitions:
            table = []
            comp.sort_table()
            for team in comp.teams:
                table.append(team)
            tables.append(table)

        return tables

    #MANAGERS
    def get_managers(self, human = True):
        managers = []
        for manager in self.managers:
            if manager.human == human:
                managers.append(manager)
        return managers

    def get_manager_by_idx(self, manager_idx):
        for manager in self.managers:
            if manager.idx == manager_idx:
                return manager

    def manager_turn(self):
        humans = self.get_managers()
        return humans[0]

    def hire_manager(self, team, manager):
        self.fire_manager(team)
        team.manager = manager
        manager.team = team

    def fire_manager(self, team):
        if team.manager is not None:
            team.manager.team = None
            team.manager = None

    def add_human_manager(self, str_name, team_idx):
        manager = Manager.Manager(name = str_name, human = True)
        team = self.get_team_by_idx(team_idx)
        self.hire_manager(team = team, manager = manager)
        self.managers.append(manager)
        return True

    #MATCHES
    def turn_matches(self):
        human_games = []
        cpu_games = []
        for comp in self.competitions:
            for game in comp.fixtures[self.turn]:
                if game.home.manager.human or game.away.manager.human:
                    human_games.append(game)
                else:
                    cpu_games.append(game)
        return human_games, cpu_games

    def turn_past(self):
        humans = self.get_managers()
        for human in humans:
            human.team.training()
        self.turn += 1
        if self.turn >= GAME_GLOBALS["TOTAL_TURNS"]:
            self.season_start()
            self.season_end()

    def minute_matches(self):
        match_status = []
        for comp in self.competitions:
            for game in comp.fixtures[self.turn]:
                    match_status.append(game.minute())
        if sum(match_status) == 0:
            return False
        return True

    def post_league_matches(self):
        for comp in self.competitions:
            comp.turn_update_stats(self.turn)
            comp.sort_table()
            comp.all_teams_position()

    def season_start(self):
        self.turn = 0
        for comp in self.competitions:
            comp.season_fixtures()

    def season_end(self):
        #PROMOTION, DEMOTION
        index = 0
        while index < len(self.competitions) - 1:
            # Ultimas 2 a[-2:]
            # Primeiras 2 a[:2]
            # Todas menos as ultimas 2 a[:-2]
            # Todas menos as primeiras 2 a[2:]
            # Todas menos as primeiras 2 e ultimas 2 a[:-2][2:]
            qty = self.competitions[index].demoted
            demoted = self.competitions[index].teams[-qty:]
            promoted = self.competitions[index + 1].teams[:qty]
            self.competitions[index].teams = self.competitions[index].teams[:-qty] + promoted
            self.competitions[index + 1].teams = demoted + self.competitions[index + 1].teams[qty:]
            index += 1

        for comp in self.competitions:
            for team in comp.teams:
                team.league_stats = TeamStats.TeamStats(comp)

        #ADD SEASON
        self.season += 1

    def __init__(self, competitions = None, managers = None, turn = None, season = None):

        self.competitions = competitions
        self.managers = managers
        self.turn = turn
        self.season = season
