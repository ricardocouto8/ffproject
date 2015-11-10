from Config import *
import sys, math, random
import string
random.seed()
import Line
import HelperMethods

class Player(object):

    id_counter = 0

    def txt(self, language):
    #   Returns a dict of strings for the GUI
        turn_skill_change = ''
        if self.turn_skill_change is not None:
            if self.turn_skill_change >= 1:
                turn_skill_change = ' [+1]'
            elif self.turn_skill_change <= (-1):
                turn_skill_change = ' [-1]'

        txt = {
        "player_name" : str(self.name),
        "player_age"  : str(self.age),
        "player_skill": str(self.skill) + str(turn_skill_change),
        "player_pos"  : language["pos" + str(self.pos)],
        "player_salary" : str(HelperMethods.num2str(self.season_salary)),
        "player_value" : str(HelperMethods.num2str(self.value)),
        }

        return txt

    def season_training_increase_per_turn(self):
    #   Sets increase_per_turn -> how much a player trains per turn
    #   Returns True if worked, False if not
    # & Run once per season
        if self.age >= PLAYER_GLOBALS["MIN_AGE"]:
            age_int = PLAYER_GLOBALS["AGE_TRAINING_INF"]
            inc_int = PLAYER_GLOBALS["TRAINING_PER_AGE"]
            age_norm = HelperMethods.normalize(self.age, PLAYER_GLOBALS["MIN_AGE"], PLAYER_GLOBALS["MAX_AGE"])
            skill_norm = HelperMethods.normalize(self.skill, PLAYER_GLOBALS["MIN_SKILL"], PLAYER_GLOBALS["MAX_SKILL"])
            skill_inf = 1
            if skill_norm >= 0.85:
                skill_inf = 0.5
            for index, age_range in enumerate(age_int):
                if age_norm < age_range:
                    x1 = age_int[index]
                    x2 = age_int[index - 1]
                    y1 = inc_int[index]
                    y2 = inc_int[index - 1]
                    increase = HelperMethods.ysolver(point1=(x1, y1), point2=(x2, y2), x = age_norm)
                    break

            self.increase_per_turn = (increase * skill_inf) / float(GAME_GLOBALS["TOTAL_TURNS"])
            return True
        return False

    def season_retire(self):
    #   Decides if a player retired and if so, sets retired = True
    #   Returns True if retired, False if not
    # & Run once per season
        age_norm = HelperMethods.normalize(self.age, PLAYER_GLOBALS["MIN_AGE"], PLAYER_GLOBALS["MAX_AGE"])
        skill_norm = HelperMethods.normalize(self.skill, PLAYER_GLOBALS["MIN_SKILL"], PLAYER_GLOBALS["MAX_SKILL"])
        if age_norm >= 1:
            self.retired = True
            return True
        elif age_norm >= 0.9:
            if random.random() >= 0.5:
                self.retired = True
                return True
        elif age_norm >= 0.8:
            if skill_norm <= 0.15:
                self.retired = True
                return True
            else:
                if random.random() >= 0.25:
                    self.retired = True
                    return True
        elif age_norm >= 0.7 and skill_norm <= 0.1:
            self.retired = True
            return True
        return False

    def turn_training(self, ground_inf):
    #   Gets ground_inf -> int that sets how much influence the training field has on the increase of experience
    #   Sets turn_exp_increase -> how much a player experience increased this turn
    #   Sets turn_skill_change -> how much a player skill changed this turn
    #   Returns True if skill changed, False if not
    # & Run once per turn
        training = (self.increase_per_turn * ground_inf) * (1 + random.uniform(-0.25, 0.25))
        change = 0
        self.skill_exp += training
        if self.skill_exp >= 1:
            change = 1
            self.skill_exp -= 1
        elif self.skill_exp < 0:
            change = -1
            self.skill_exp += 1

        self.turn_skill_change = change
        self.turn_exp_increase = training

        return self.change_skill(change)

    def change_skill(self, change):
    #   Gets change -> int that sets how much the skill should change
    #   Sets self_skill += change
    #   Returns True if skill changed, False if not
        skill = min(max(int(round(self.skill + change, 0)), PLAYER_GLOBALS["MIN_SKILL"]), PLAYER_GLOBALS["MAX_SKILL"])

        if skill == self.skill:
            return False
        self.skill = skill
        return True

    def calc_season_salary(self):
        apparent_skill = self.skill
        print apparent_skill
        factors = PLAYER_GLOBALS["PRICE_SKILL"]
        power = [0, 0, 0, 0, 0, 0]
        print factors
        get_lastpower = (apparent_skill - PLAYER_GLOBALS["MIN_SKILL"]) / 10
        get_howmuchpower = (apparent_skill - PLAYER_GLOBALS["MIN_SKILL"]) % 10
        print get_lastpower
        print get_howmuchpower
        for i in range(get_lastpower + 1):
            power[i] = 3
            if i == get_lastpower:
                power[i] = get_howmuchpower / 3.0

        salary = pow(factors[0],power[0]) * pow(factors[1],power[1]) * pow(factors[2],power[2]) * pow(factors[3],power[3]) * pow(factors[4],power[4]) * 1000
        print salary
        annual_salary = salary  / PLAYER_GLOBALS["AVERAGE_SALARIES_PER_VALUE"]
        return int(round(annual_salary, 0))

    def turn_salary(self):
        return self.season_salary / float(GAME_GLOBALS["TOTAL_TURNS"])

    def calc_price(self):
        apparent_skill = self.skill
        starting_values = PLAYER_GLOBALS["PRICE_AGE"]
        factors = PLAYER_GLOBALS["PRICE_SKILL"]
        power = [0, 0, 0, 0, 0, 0]

        age_norm = HelperMethods.normalize(self.age, PLAYER_GLOBALS["MIN_AGE"], PLAYER_GLOBALS["MAX_AGE"])
        age_inf_price = int(age_norm * (len(starting_values) - 2))
        point1 = (age_inf_price, starting_values[age_inf_price])
        point2 = (age_inf_price + 1, starting_values[age_inf_price + 1])

        start_value = Line.Line((point1, point2)).solve_for_y(age_norm * (len(starting_values) - 2))

        get_lastpower = (apparent_skill - PLAYER_GLOBALS["MIN_SKILL"]) / 10
        get_howmuchpower = (apparent_skill - PLAYER_GLOBALS["MIN_SKILL"]) % 10

        for i in range(get_lastpower + 1):
            power[i] = 3
            if i == get_lastpower:
                power[i] = get_howmuchpower / 3.0

        price = start_value * pow(factors[0],power[0]) * pow(factors[1],power[1]) * pow(factors[2],power[2]) * pow(factors[3],power[3]) * pow(factors[4],power[4]) * 1000

        if price / 100 >= 1:
            return int(price) - int(price) % 10
        else:
            return int(price)

    def __init__(self, pos, skill, name = None, age = None, avg_skill = False, skill_exp = None, skill_season = None, injury = None, transfer_listed = None, value = None, season_salary = None):

        self.idx = Player.id_counter
        Player.id_counter += 1

        def random_name():
        #   Returns string with random name
            first = random.choice(string.ascii_uppercase)
            delimiter =  '. '
            last = random.choice(PEOPLE_NAMES)
            return str(first + delimiter + last)

        def create_skill(skill, avg_skill):
        #   Returns int with player starting skill
        #   TODO: Add age influence!
            # if avg_skill:
            #     skill_variation = int(round(PLAYER_GLOBALS["MAX_SKILL"] * 0.02, 0))
            #     random_var = random.randint(-skill_variation, skill_variation)
            #     skill += random_var
            skill_age_inf = PLAYER_GLOBALS["MAX_SKILL"] * 0.05 + skill * 0.2
            age_inf = 1 - 2 * HelperMethods.normalize(age, PLAYER_GLOBALS["MIN_AGE"], PLAYER_GLOBALS["MAX_AGE"])

            if age_inf > 0:
                skill -= skill_age_inf * age_inf

            skill = min(max(int(round(skill, 0)), PLAYER_GLOBALS["MIN_SKILL"]), PLAYER_GLOBALS["MAX_SKILL"])
            return skill

        def random_age():
        #   Returns int with random age
            age = random.gauss(PLAYER_GLOBALS["MEAN_AGE"], PLAYER_GLOBALS["STD_DEV_AGE"])
            age = min(max(int(round(age, 0)), PLAYER_GLOBALS["MIN_AGE"]), PLAYER_GLOBALS["MAX_AGE"])
            return age



        #PERSONAL DATA
        if name is None:
            name = random_name()
        self.name = name

        if age is None:
            age = random_age()
        self.age = age

        self.pos = pos

        #SKILL
        self.skill = skill

        if skill_exp is None:
            skill_exp = random.random()
        self.skill_exp = skill_exp

        if skill_season is None:
            skill_season = self.skill
        self.skill_season = skill_season

        self.skill_week = self.skill

        #TRAINING
        self.increase_per_turn = None
        self.turn_skill_change = None
        self.turn_exp_increase = None

        #CONTRACT
        if value is None:
            value = self.calc_price()
        self.value = value

        if season_salary is None:
            season_salary = self.calc_season_salary()
        self.season_salary = season_salary

        if transfer_listed is None:
            transfer_listed = False
        self.transfer_listed = transfer_listed

        #PLAYING
        if injury is None:
            injury = 0
        self.injury = injury

        self.retired = False

