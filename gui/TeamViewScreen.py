from kivy.uix.screenmanager import Screen
from Config import *

class TeamViewScreen(Screen):
    def update_screen(self, *args, **kwargs):
        self.ids["player_list"].clear_widgets()
        txt = TURN.team.txt(LANG)
        for key, value in txt.iteritems():
            try:
                self.ids[key].text = value
            except:
                pass
        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        sorted_players = TURN.sort_players("Pos + Skill")
        for player in sorted_players:
            txt = player.txt(LANG)
            btn = PlayerBtn(size_hint_y=None, height=45)
            for key, value in txt.iteritems():
                try:
                    btn.ids[key].text = value
                except:
                    pass
            btn.player_idx = player.idx
            layout.add_widget(btn)

        self.ids["player_list"].add_widget(layout)
        possible_tactics = []
        for tactic in TURN.possible_tactics():
            possible_tactics.append(tactic2txt(tactic))
        possible_tactics.append("Best 11")
        possible_tactics.append("Clear")
        self.ids["assman_team"].values = possible_tactics

        labels = [self.ids["player_list_label"]]
        for x in labels:
            for i in x.ids:
                x.ids[i].text = LANG[i]

    def assman_team(self, *args, **kwargs):
        player_list = []
        if args[0] == "Best 11":
            player_list = TURN.assman_team()
        elif args[0] == "Clear":
            for btn in self.ids["player_list"].children[0].children:
                btn.state = "normal"
                btn.canvas.ask_update()
        else:
            tactic = txt2tactic(args[0])
            player_list = TURN.assman_team(tactic)

        for btn in self.ids["player_list"].children[0].children:
            for player in player_list:
                if btn.player_idx == player.idx:
                    btn.state = "down"
                    break
                btn.state = "normal"
            btn.canvas.ask_update()

    def go_to_game(self, *args, **kwargs):
        selected_players_idx = []
        for btn in self.ids["player_list"].children[0].children:
            if btn.state == "down":
                selected_players_idx.append(btn.player_idx)
        TURN.go_to_game(selected_players_idx)
        if GAME.go_to_game():
            sm.current = 'allmatches'

    def sell_player(self, *args, **kwargs):
        selected_players_idx = []
        for btn in self.ids["player_list"].children[0].children:
            if btn.state == "down":
                selected_players_idx.append(btn.player_idx)
        for player_idx in selected_players_idx:
            TURN.sell_player(player_idx)
        self.update_screen()

    def on_pre_enter(self):
        self.update_screen()

    def on_leave(self):
        self.ids["player_list"].clear_widgets()
