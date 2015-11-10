# -*- coding: latin_1 -*-
import Config

class DBCreator(object):

    def __init__(self):
        self.competitions = []
        self.teams = []
        self.managers = []
        self.players = []
        self.conn = sqlite3.connect('Data.db')

    def create_database(self):

        with self.conn:

            cur = self.conn.cursor()

            cur.execute("CREATE TABLE Competition (CID INTEGER PRIMARY KEY, Name TEXT, Type TEXT, Format TEXT, Season INT, TotalTeamNumbers INT)")
            cur.execute("CREATE TABLE Match (MID INTEGER PRIMARY KEY, Week INT, CID INTEGER, HomeTID INTEGER, AwayTID INTEGER, FOREIGN KEY(CID) REFERENCES competition(CID), FOREIGN KEY(HomeTID) REFERENCES team(TID), FOREIGN KEY(AwayTID) REFERENCES team(TID))")
            cur.execute("CREATE TABLE Team (TID INTEGER PRIMARY KEY, Name TEXT, Nation INT, AvgSkill INT, Stadium TEXT, Money INT, UNIQUE (Name))")
    #        cur.execute("CREATE TABLE Agent (AID INTEGER PRIMARY KEY, Name TEXT, Randomness INT, Flexibility INT, FirstOffer INT, UNIQUE (Name))")
            cur.execute("CREATE TABLE Player (PID INTEGER PRIMARY KEY, FirstName TEXT DEFAULT 'John', LastName TEXT DEFAULT 'Doe', Nation INT DEFAULT '0', Age INT DEFAULT '16', Position INT DEFAULT '0', Skill INT DEFAULT '0', AppSkill INT DEFAULT '0', Form INT DEFAULT '20', AppForm INT DEFAULT '5', Fitness INT DEFAULT '500', AppFitness INT DEFAULT '5', Salary INT DEFAULT '0', Price INT DEFAULT '0', Contract INT DEFAULT '0', TotalGames INT DEFAULT '0', TotalGoals INT DEFAULT '0', SeasonGames INT DEFAULT '0', SeasonGoals INT DEFAULT '0', YellowCards INT DEFAULT '0', RedCards INT DEFAULT '0', Tstatus INT DEFAULT '0', Istatus INT DEFAULT '0', Sstatus INT DEFAULT '0', TID INTEGER, AID INTEGER, FOREIGN KEY(TID) REFERENCES team(TID), FOREIGN KEY(AID) REFERENCES agent(AID))")
            cur.execute("CREATE TABLE Staff (SID INTEGER PRIMARY KEY, FirstName TEXT DEFAULT 'John', LastName TEXT DEFAULT 'Doe', Skill INT DEFAULT '0', Salary INT DEFAULT '0', Contract INT DEFAULT '0', Role INT DEFAULT '0', TID INTEGER, FOREIGN KEY(TID) REFERENCES team(TID))")
            cur.execute("CREATE TABLE participatesIn (TID INTEGER, CID INTEGER, FOREIGN KEY(TID) REFERENCES team(TID),  FOREIGN KEY(CID) REFERENCES team(CID))")
