#!/usr/bin/python

import random

class Participant:
    def __init__(self, id, gender, sexuality):
        self.id = id
        self.gender = gender
        self.sexuality = sexuality
        self.desirability = random.randint(0,100)
        self.preference_order_list = []
        self.cutoff = -1

    def preference_order(self, agents):
        # Need to match on own sexuality, other agent's sexuality
        not_attracted = []
        attracted = []
        for agent in agents:
            if agent.gender in self.sexuality:
                attracted.push(agent)
            else:
                not_attracted.push(agent)

        attracted = sorted(attracted, lambda x: abs(self.desirability - x.desirability), reverse=True)
        self.preference_order_list = attracted + not_attracted
        self.cutoff = len(attracted)