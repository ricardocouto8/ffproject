from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import Game
import Languages
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Config import *
from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')


# from kivy.core.window import Window
# Window.size = (320, 480)

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<PlayerLabel@BoxLayout>:
    Label:
        id: label_player_pos
        size_hint_x: 0.15
    Label:
        id: label_player_name
        size_hint_x: 0.4
    Label:
        id: label_player_age
        size_hint_x: 0.1
    Label:
        id: label_player_skill
        size_hint_x: 0.1
    Label:
        id: label_player_salary
        size_hint_x: 0.1
    Label:
        id: label_player_value
        size_hint_x: 0.1

<PlayerBtn>:
    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        Label:
            id: player_pos
            size_hint_x: 0.15
        Label:
            id: player_name
            size_hint_x: 0.4
        Label:
            id: player_age
            size_hint_x: 0.1
        Label:
            id: player_skill
            size_hint_x: 0.1
        Label:
            id: player_salary
            size_hint_x: 0.1
        Label:
            id: player_value
            size_hint_x: 0.1

<TableTeamBtn>:
    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        Label:
            id: position
            size_hint_x: 0.1
        Label:
            id: team_name
            size_hint_x: 0.6
        Label:
            id: team_goal_difference
            size_hint_x: 0.15
        Label:
            id: team_league_points
            size_hint_x: 0.15

<MatchBtn>:
    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        Label:
            id: home_team_name
            size_hint_x: 0.2
        Label:
            id: home_team_goals
            size_hint_x: 0.05
        Label:
            text: "x"
            size_hint_x: 0.05
        Label:
            id: away_team_goals
            size_hint_x: 0.05
        Label:
            id: away_team_name
            size_hint_x: 0.2
        Label:
            size_hint_x: 0.1
        Label:
            id: last_goalscorer
            size_hint_x: 0.25
        Label:
            id: last_goal_minute
            size_hint_x: 0.1


<PlayerGoalscorer>:
    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        Label:
            id: player_name
            size_hint_x: 0.7
        Label:
            id: minutes
            size_hint_x: 0.3

<TableScreen>:
    canvas:
        Color:
            rgba: 0, 92/255.0, 9/255.0, 1
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            size_hint_y: 0.45
            orientation: "horizontal"
            spacing: 20
            BoxLayout:
                orientation: "vertical"
                id: division_0
            BoxLayout:
                orientation: "vertical"
                id: division_2
        BoxLayout:
            size_hint_y: 0.45
            orientation: "horizontal"
            spacing: 20
            BoxLayout:
                orientation: "vertical"
                id: division_1
            BoxLayout:
                orientation: "vertical"
                id: division_3
        BoxLayout:
            orientation: "horizontal"
            id: options
            size_hint_y: 0.1
            Button:
                text: "Continue!"
                on_release: root.go_to_main()

<TeamViewScreen>:
    canvas:
        Color:
            rgba: 0, 92/255.0, 9/255.0, 1
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            Label:
                id: team_league_position
            Label:
                id: team_name
            Label:
                id: team_money
        PlayerLabel:
            id: player_list_label
            size_hint_y: 0.05
        ScrollView:
            id: player_list
            size_hint_y: 0.75
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            Spinner:
                id: assman_team
                on_text: root.assman_team(self.text)
                text: "AssMan Team"
            Button:
                on_release: root.sell_player()
                text: "Sell"
            Button:
                text: "Go to Game"
                on_release: root.go_to_game()



<AllMatchesScreen>:
    canvas:
        Color:
            rgba: 0, 92/255.0, 9/255.0, 1
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        orientation: "vertical"
        Label:
            id: turn
            size_hint_y: 0.1
        ProgressBar:
            max: 90
            id: minutes
            height: '48dp'
            size_hint_y: 0.05
        ScrollView:
            id: match_list
            size_hint_y: 0.75
        BoxLayout:
            id: options
            orientation: "horizontal"
            size_hint_y: 0.1
            ToggleButton:
                id: play_btn
                text: "Play!"
                on_release: root.play_pause()
            Button:
                id: continue_btn
                text: "Continue!"
                on_release: root.continue_btn()

<MatchScreen>:
    canvas:
        Color:
            rgba: 0, 92/255.0, 9/255.0, 1
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            Label:
                id: home_team_name
                font_size: '40sp'
            Label:
                id: away_team_name
                font_size: '40sp'
        ProgressBar:
            max: 91
            id: minutes
            height: '48dp'
            size_hint_y: 0.05
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            Label:
                id: home_team_goals
                font_size: '60sp'
                text: "0"
            Label:
                id: away_team_goals
                font_size: '60sp'
                text: "0"
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.2
            BoxLayout:
                orientation: "vertical"
                id: home_goalscorers
            BoxLayout:
                orientation: "vertical"
                id: away_goalscorers
        ProgressBar:
            id: home_team_poss
            max: 100
            height: '48dp'
            size_hint_y: 0.05
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.5
            ScrollView:
                id: player_list
            BoxLayout:
                orientation: "vertical"
                ScrollView:
                    id: subs_list
                    size_hint_y: 0.7
                Button:
                    text: "Sub"
                    size_hint_y: 0.15
                    on_release: root.substitution()
                Button:
                    text: "Back"
                    size_hint_y: 0.15
                    on_release: root.go_back()
""")

GAME = Game.Game()
GAME.new_game()
GAME.add_human_manager("Ricardo", 31)
GAME.season_start()
TURN = GAME.manager_turn()
LANG = Languages.ENGLISH

def tactic2txt(tactic):
    return str(tactic[0]) + '-' + str(tactic[1]) + '-' +str(tactic[2])

def txt2tactic(tactic):
    return tuple([int(i) for i in tactic.rsplit('-')])

class TableTeamBtn(Button):
    pass

class PlayerBtn(ToggleButton):
    pass

class PlayerGoalscorer(Button):
    pass

class MatchBtn(Button):
    def on_release(self, *args, **kwargs):
        self.disabled = True
        match = GAME.get_match_by_idx(self.match_idx)
        Clock.unschedule(sm.get_screen('allmatches').minute)
        sm.get_screen('match').match = match
        sm.current = 'match'
        self.disabled = False

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
# Declare both screens
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

class TableScreen(Screen):
    def update_screen(self):
        tables = GAME.leagues_table()
        division = 0
        for table in tables:
            if division < GAME_GLOBALS["ACTIVE_LEAGUES"]:
                position = 1
                for team in table:
                    txt = team.txt(LANG)
                    btn = TableTeamBtn(size_hint_y=None, height=30)
                    if team.manager.human:
                        for lbl in btn.children[0].children:
                            lbl.bold = True
                    for key, value in txt.iteritems():
                        try:
                            btn.ids[key].text = value
                        except:
                            pass
                    btn.ids['position'].text = str(position)
                    if position <= 2:
                        btn.background_color = (0,1,0,1)
                    elif position >= 7:
                        btn.background_color = (1,0,0,1)
                    position += 1
                    self.ids["division_" + str(division)].add_widget(btn)
                division += 1

    def go_to_main(self):
        self.disabled = True
        sm.current = 'main'
        self.disabled = False

    def on_pre_enter(self):
        self.update_screen()

    def on_leave(self):
        self.ids["division_0"].clear_widgets()
        self.ids["division_1"].clear_widgets()
        self.ids["division_2"].clear_widgets()
        self.ids["division_3"].clear_widgets()

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

# Create the screen manager
sm = ScreenManager()
sm.add_widget(TeamViewScreen(name='main'))
sm.add_widget(MatchScreen(name='match'))
sm.add_widget(AllMatchesScreen(name='allmatches'))
sm.add_widget(TableScreen(name='table'))

class FootyApp(App):

    def build(self):
        sm.current = 'main'
        return sm

if __name__ == '__main__':
    FootyApp().run()
