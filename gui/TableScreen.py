from kivy.uix.screenmanager import Screen
from Config import *

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
