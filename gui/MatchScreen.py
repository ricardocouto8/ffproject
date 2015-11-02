from kivy.uix.screenmanager import Screen
from Config import *

class MatchScreen(Screen):
    def update_screen(self, *args, **kwargs):
        self.ids["home_goalscorers"].clear_widgets()
        self.ids["away_goalscorers"].clear_widgets()
        human_games, cpu_games = GAME.turn_matches()
        match = self.match
        txt = match.txt(LANG)
        btns = self.ids
        for key, value in txt.iteritems():
            try:
                btns[key].text = value
            except:
                pass
        if match.home.manager.human:
            self.ids['home_team_name'].color = (1,0,1,1)
        else:
            self.ids['home_team_name'].color = (1,1,1,1)
        if match.away.manager.human:
            self.ids['away_team_name'].color = (1,0,1,1)
        else:
            self.ids['away_team_name'].color = (1,1,1,1)
        self.ids["minutes"].value = match.minutes
        for player in match.txt(LANG)["home_team_goalscorers"]:
            p = PlayerGoalscorer()
            txt = player[0].txt(LANG)
            minutes = str(player[1])
            p.ids['player_name'].text = txt['player_name']
            p.ids['minutes'].text = minutes
            self.ids["home_goalscorers"].add_widget(p)
        for player in match.txt(LANG)["away_team_goalscorers"]:
            p = PlayerGoalscorer()
            txt = player[0].txt(LANG)
            minutes = str(player[1])
            p.ids['player_name'].text = txt['player_name']
            p.ids['minutes'].text = minutes
            self.ids["away_goalscorers"].add_widget(p)

        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        sorted_players = TURN.sort_players("Squad")
        for player in sorted_players:
            txt = player.txt(LANG)
            btn = PlayerBtn(size_hint_y=None, height=45, group='tits')
            for key, value in txt.iteritems():
                try:
                    btn.ids[key].text = value
                except:
                    pass
            btn.player_idx = player.idx
            layout.add_widget(btn)

        self.ids["player_list"].add_widget(layout)

        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        sorted_players = TURN.sort_players("Subs")
        for player in sorted_players:
            txt = player.txt(LANG)
            btn = PlayerBtn(size_hint_y=None, height=45, group='subs')
            for key, value in txt.iteritems():
                try:
                    btn.ids[key].text = value
                except:
                    pass
            btn.player_idx = player.idx
            layout.add_widget(btn)

        self.ids["subs_list"].add_widget(layout)

    def minute(self, *args, **kwargs):
        if GAME.minute_matches():
            self.update_screen()

    def substitution(self, *args, **kwargs):
        player_in = None
        player_out = None
        for btn in self.ids["player_list"].children[0].children:
            if btn.state == "down":
                player_out = btn.player_idx
        for btn in self.ids["subs_list"].children[0].children:
            if btn.state == "down":
                player_in = btn.player_idx

        if (player_in is None) or (player_out is None):
            return None

        team_idx = TURN.team.idx
        self.match.substitution(team_idx, player_out, player_in)
        self.ids["player_list"].clear_widgets()
        self.ids["subs_list"].clear_widgets()
        self.update_screen()

    def go_back(self, *args, **kwargs):
        Clock.unschedule(self.minute)
        sm.current = 'allmatches'

    def on_pre_enter(self):
        self.update_screen()

    def on_leave(self):
        self.ids["player_list"].clear_widgets()
        self.ids["subs_list"].clear_widgets()
