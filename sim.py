#!/usr/bin/env python

"""
Simulates one file being shared amongst a set of peers.  The file is divided into a set of pieces, each comprised of some number of blocks.  There are two types of peers:
  - seeds, which start with all the pieces.
  - regular peers, which start with no pieces.

The simulation proceeds in rounds.  In each round, peers can request pieces from other peers, and then decide how much to upload to others.  Once every peer has every piece, the simulation ends.
"""

from optparse import OptionParser
import sys
from itertools import chain, combinations
import random

from truthful import ParticipantTruthful
from strategic import ParticipantStrategic


# Genders
FEMALE = 0
MALE = 1
NONBINARY = 2

def coin_flip(p):
    return 0 if random.random() < p else 1

class Sim:
    def __init__(self, options):
        self.participants = set()
        self.avg_utility = 0
        num_women = options.num_women
        num_men = options.num_men
        num_nb = options.num_nb
        self.num_participants = num_women  + num_nb + num_men
        self.percent_match = 0

        sexualities = list(chain.from_iterable(combinations([FEMALE, MALE, NONBINARY], r) for r in range(1, 4)))
        weights = []
        if options.flex:
            weights = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.52]
        else:
            weights = [1/7]*7

        for i in range(self.num_participants):
            # generate gender
            if i < num_women:
                gender = FEMALE
            elif i < num_women + num_nb:
                gender = NONBINARY
            else:
                gender = MALE

            # generate sexuality
            sexuality = random.choices(sexualities, weights, k=1)[0]
            
            if coin_flip(options.percent_truthful) == 1:
                participant = ParticipantStrategic(i, gender, sexuality)
            else:
                participant = ParticipantTruthful(i, gender, sexuality)
            self.participants.add(participant)

        for participant in self.participants:
            participant.generate_preference_order(self.participants)


    def runMatch(self):
        set_proposed_to = set()
        # iterating through all participants
        for participant in self.participants:     
            proposer = participant

            next_choice = proposer.preference_order_list[proposer.ask_rank]

            # iterating through preference list of proposer, switching to anyone rejected due to current proposer
            while next_choice not in set_proposed_to and proposer.ask_rank < proposer.cutoff:
                # print("in while loop")
                # Proposer proposing to next choice
                if self.proposal_accepted(proposer, next_choice):
                     
                    if next_choice in set_proposed_to:
                        # switch to proposer who was just rejected due to previous proposer
                        proposer = next_choice.just_rejected
                        # shift down rank to ask becasue just rejected
                        proposer.ask_rank += 1
                        next_choice = proposer.preference_order_list[proposer.ask_rank]

                    else:
                        # keep track of who has been proposed to before
                        set_proposed_to.add(next_choice)

                else:
                    # iterate proposer ask rank, ask down list
                    proposer.ask_rank += 1

    
    
    def proposal_accepted(self, proposer, next_choice):
        # if not paired with anyone yet, accepts first offer
        current_next_choice_pair_id = next_choice.paired_with.id if next_choice.paired_with is not None else -1
        for i in range(next_choice.cutoff):
            # see which id is encountered first in preference list of person proposed to
            if next_choice.preference_order_list[i].id == proposer.id:
                # new proposal wins; keep track of previous match who was rejected and create new pairing
                if next_choice.paired_with is not None:
                    next_choice.just_rejected = next_choice.paired_with
                    next_choice.just_rejected.paired_with = None
                next_choice.paired_with = proposer
                proposer.paired_with = next_choice
                return True
            elif next_choice.preference_order_list[i].id == current_next_choice_pair_id:
                # previous proposer is ranked more highly than current
                return False

        # new proposer not possible matchings for the proposed  
        return False

    def calc_avg_utility(self):
        total_utility = 0
        for participant in self.participants:
            total_utility += participant.calculate_utility(participant.paired_with, self.num_participants)
        self.avg_utility = total_utility / self.num_participants


    def check_if_stable(self):
        for participant in self.participants:

            for i in range(participant.ask_rank):
                preferred_to_match = participant.preference_order_list[i]
                preferred_to_match_ask_rank = preferred_to_match.ask_rank
                if participant in preferred_to_match.preference_order_list[:preferred_to_match_ask_rank]:
                    return False
                
        return True
            
    def print_results(self):

        count_match = 0
        print("Match results")
        print("------------------------------")
        for participant in self.participants:
            if participant.paired_with:
                count_match += 1
                print("Participant " + str(participant.id) + " matched with Participant " + str(participant.paired_with.id))
            else:
                print("Participant " + str(participant.id) + " unmatched")
        print("------------------------------")

        self.percent_match = count_match  / self.num_participants
        print("Average utility among participants: " + str(self.avg_utility))
        print("% Match: " + str(self.percent_match * 100) + "%")


            



def main(args):
    usage_msg = "Usage:  %prog [options] PeerClass1[,count] PeerClass2[,count] ..."
    parser = OptionParser(usage=usage_msg)

    def usage(msg):
        print(("Error: %s\n" % msg))
        parser.print_help()
        sys.exit()

    parser.add_option("--numWomen",
                      dest="num_women", default=5, type="int",
                      help="Set number of women in simulation")

    parser.add_option("--numNonBinary",
                      dest="num_nb", default=5, type="int",
                      help="Set number of nonbinary people in simulation")

    parser.add_option("--numMen",
                      dest="num_men", default=5, type="int",
                      help="Set number of men in simulation")
    
    parser.add_option("--checkStability",
                      dest="check_stability", default=False, action="store_true",
                      help="Set whether or not you want to check for stability")
    
    parser.add_option("--numReps",
                      dest="num_reps", default=1, type="int",
                      help="Set the number of repetitions")
    
    parser.add_option("--percentTruthful",
                      dest="percent_truthful", default=1, type="float",
                      help="Set the percentage of agents who are truthful.")
    
    parser.add_option("--flex",
                      dest="flex", default=False, action="store_true",
                      help="Set whether or not you want to weight towards pansexual participants.")

    (options, args) = parser.parse_args()
    print(options)
    
    utilities = []
    percent_matches = []
    stabilities = []
    for i in range(options.num_reps):
        sim = Sim(options)
        sim.runMatch()
        sim.calc_avg_utility()
        sim.print_results()
        utilities.append(sim.avg_utility)
        percent_matches.append(sim.percent_match * 100)

        if options.check_stability:
            print("Checking Stability")
            print(sim.check_if_stable())
            stable = sim.check_if_stable()
            stabilities.append(stable)
        
    # Print results:
    if options.check_stability:
        print(sum(stabilities) * 100 / len(stabilities), "percent of simulations resulted in a stable matching.")
    print("The utility across runs was", sum(utilities) / len(utilities))
    print("The average percent match", sum(percent_matches) / len(percent_matches))


if __name__ == "__main__":
    # The next two lines are for profiling...
    import cProfile

    cProfile.run('main(sys.argv)', 'out.prof')
#    main(sys.argv)