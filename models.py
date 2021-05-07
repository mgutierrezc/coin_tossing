from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

author = 'Marco Gutierrez'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'coin_tossing'
    players_per_group = None
    num_rounds = 5
    instructions_template = name_in_url + "/Instructions.html"

    # parameters for coin tossing
    head_value = "Cara"
    tail_value = "Sello"
    head_payment = c(10)
    coin_choices = [head_value, tail_value]
    num_heads = 2 # number of times a coin should be heads
    


class Subsession(BaseSubsession):
    def creating_session(self):
        # defining all possible coin results
        coin_results = [Constants.head_value if iteration < Constants.num_heads else Constants.tail_value for iteration in range(Constants.num_rounds)]
        if self.round_number == 1:
            self.session.vars["lies_accum"] = 0
            for round_num in range(1, Constants.num_rounds + 1):
                self.session.vars[f"lies_round_{round_num}"] = 0

            print(f"initial value lies accum = {self.session.vars['lies_accum']}")

        for g in self.get_groups():
            for p in g.get_players():
                # randomizing tossed coin values in first round
                if self.round_number == 1:
                    p.participant.vars["random_tossing"] = coin_results.copy()
                    random.shuffle(p.participant.vars["random_tossing"])
                
                # assigning coin values
                index = self.round_number - 1 # index for getting respective coin result
                p.real_coin_value = p.participant.vars["random_tossing"][index]

    def vars_for_admin_report(self):
        num_players = len(self.get_players())

        lies = [p.player_is_lying for p in self.get_players()]
        # storing current number of lies
        self.session.vars[f"lies_round_{self.round_number}"] = sum(lies)

        # obtaining the accumulated number of lies
        for round_num in range(1, Constants.num_rounds + 1):
            self.session.vars["lies_accum"] += self.session.vars[f"lies_round_{round_num}"]

        print(f"round {self.round_number} lies accum = {self.session.vars['lies_accum']}")
        # proporcion de mentiras por ronda
        # promedio de mentiras acumulado

        if lies:
            return {
                'avg_lies': str(round(sum(lies)*100/num_players, 1)) + "%",
                'accum_lies_avg': str(round(self.session.vars["lies_accum"]/num_players, 1)),
            }
        else:
            return {
                'avg_lies': '(no data)',
                'accum_lies_avg': '(no data)'
            }
           

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_final_payoffs(self):
        """
        Choses a random app for paying the player

        Input: None
        Output: None
        """

        apps = self.session.config["app_sequence"][:-1]
        print("app sequence without last app", apps)
        random.shuffle(apps)
        self.chosen_app = apps[0]
        self.participant.payoff = self.participant.vars["payoff_"+self.chosen_app]

    chosen_app = models.StringField()

    heads_or_tails = models.StringField(doc="The player declares if the tossed coin was heads or tails", 
                                        choices=Constants.coin_choices,
                                        verbose_name="Por favor, indica qué resultado muestra el dado")
    number_of_heads = models.IntegerField(doc="Number of times the player declared heads",
                                          initial=0)
    real_coin_value = models.StringField(doc="Real value of coin after being tossed")
    player_is_lying = models.IntegerField(initial=0, doc="0 is not lying, 1 it is")