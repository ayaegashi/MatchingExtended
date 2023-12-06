#!/usr/bin/python

import random

class ParticipantStrategic:
    def __init__(self, id, gender, sexuality):
        self.id = id
        self.gender = gender
        self.sexuality = sexuality
        self.desirability = random.randint(0,100)
        self.preference_order_list = []
        self.true_preference_order = []
        self.cutoff = -1
        self.paired_with = None
        self.just_rejected = None
        self.ask_rank = 0

    def generate_preference_order(self, agents):
        # Need to match on own sexuality, other agent's sexuality, and sort by desirability of matches
        not_attracted = []
        attracted = []
        for agent in agents:
            if agent.gender in self.sexuality and agent.id != self.id:
                attracted.append(agent)
            else:
                not_attracted.append(agent)

        attracted = sorted(attracted, key=lambda x: abs(self.desirability - x.desirability), reverse=True)
        self.preference_order_list = attracted + not_attracted

        true_attracted = sorted(attracted, key=lambda x: x.desirability, reverse=True)
        self.true_preference_order = true_attracted + not_attracted

        self.cutoff = len(attracted)

    def calculate_utility(self, match, maxUtil):
        if match not in self.true_preference_order:
            return 0
        for p in self.true_preference_order:
            if match == p:
                return maxUtil
            maxUtil -= 1