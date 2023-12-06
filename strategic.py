#!/usr/bin/python

import random
# import uuid

class ParticipantStrategic:
    def __init__(self, id, gender, sexuality):
        self.id = id
        self.gender = gender
        self.sexuality = sexuality
        self.desirability = random.randint(0,100)
        self.preference_order_list = []
        self.cutoff = -1
        self.paired_with = None
        self.just_rejected = None
        self.ask_rank = 0

    def preference_order(self, agents):
        # Need to match on own sexuality, other agent's sexuality
        not_attracted = []
        attracted = []
        for agent in agents:
            if agent.gender in self.sexuality and agent.id != self.id:
                attracted.append(agent)
            else:
                not_attracted.append(agent)

        attracted = sorted(attracted, lambda x: abs(self.desirability - x.desirability), reverse=True)
        self.preference_order_list = attracted + not_attracted
        self.cutoff = len(attracted)

    def calculate_utility(self, match):
        if match not in self.preference_order_list:
            return 0
        for p in self.preference_order_list:
            if match == p:
                return match.desirability