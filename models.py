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
        
        for g in self.get_groups():
            for p in g.get_players():
                # randomizing tossed coin values in first round
                if self.round_number == 1:
                    p.participant.vars["random_tossing"] = coin_results.copy()
                    random.shuffle(p.participant.vars["random_tossing"])
                
                # assigning coin values
                index = self.round_number - 1 # index for getting respective coin result
                p.real_coin_value = p.participant.vars["random_tossing"][index]
                

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