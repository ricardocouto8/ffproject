from kivy.uix.screenmanager import Screen
from Config import *

class AllMatchesScreen(Screen):
    def update_screen(self, *args, **kwargs):
        human_games, cpu_games = GAME.turn_matches()
        btns = self.ids["match_list"].children[0].children[::-1]
        index = 0
        for match in human_games:
            txt = match.txt(LANG)
            for key, value in txt.iteritems():
                try:
                    btns[index].ids[key].text = value
                except:
                    pass
            btns[index].match_idx = match.idx
            if match.home.manager.human:
                btns[index].ids['home_team_name'].color = (1,0,1,1)
            else:
                btns[index].ids['home_team_name'].color = (1,1,1,1)
            if match.away.manager.human:
                btns[index].ids['away_team_name'].color = (1,0,1,1)
            else:
                btns[index].ids['away_team_name'].color = (1,1,1,1)
            index += 1


        for match in cpu_games:
            txt = match.txt(LANG)
            for key, value in txt.iteritems():
                try:
                    btns[index].ids[key].text = value
                except:
                    pass
            btns[index].match_idx = match.idx
            index += 1
        self.ids["minutes"].value = match.minutes
        self.ids["turn"].text = "Week " + str(GAME.turn + 1)
        self.ids["play_btn"].disabled = False
        self.ids["continue_btn"].disabled = True

    def minute(self, *args, **kwargs):
        if GAME.minute_matches():
            self.update_screen()
        else:
            self.ids["continue_btn"].disabled = False

    def play_pause(self, *args, **kwargs):
        if self.ids["play_btn"].state == "down":
            Clock.schedule_interval(self.minute, 0.01)
        else:
            Clock.unschedule(self.minute)

    def continue_btn(self, *args, **kwargs):
        self.ids["continue_btn"].disabled = True
        Clock.unschedule(self.minute)
        GAME.post_league_matches()
        GAME.turn_past()
        sm.current = 'table'

    def on_pre_enter(self):
        if len(self.ids["match_list"].children) <= 0:
            self.ids["play_btn"].disabled = False
            human_games, cpu_games = GAME.turn_matches()
            layout = GridLayout(cols=1, size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))
            for match in human_games:
                txt = match.txt(LANG)
                btn = MatchBtn(size_hint_y=None, height=30)
                for key, value in txt.iteritems():
                    try:
                        btn.ids[key].text = value
                    except:
                        pass
                btn.match_idx = match.idx
                layout.add_widget(btn)
                if match.home.manager.human:
                    btn.ids['home_team_name'].color = (1,0,1,1)
                else:
                    btn.ids['home_team_name'].color = (1,1,1,1)
                if match.away.manager.human:
                    btn.ids['away_team_name'].color = (1,0,1,1)
                else:
                    btn.ids['away_team_name'].color = (1,1,1,1)

            for match in cpu_games:
                txt = match.txt(LANG)
                btn = MatchBtn(size_hint_y=None, height=30)
                for key, value in txt.iteritems():
                    try:
                        btn.ids[key].text = value
                    except:
                        pass
                btn.match_idx = match.idx
                layout.add_widget(btn)

            self.ids["match_list"].add_widget(layout)
            self.ids["minutes"].value = match.minutes
            self.ids["turn"].text = "Week " + str(GAME.turn + 1)
            self.ids["continue_btn"].disabled = True
        else:
            self.update_screen()


    def on_leave(self):
        pass
