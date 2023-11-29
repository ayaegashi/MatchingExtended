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


class Sim:
    def __init__(self):
        self.participants = set()
        num_women = 10
        num_men = 10
        num_nb = 10
        total = num_women  + num_nb + num_men

        sexualities = list(chain.from_iterable(combinations([FEMALE, MALE, NONBINARY], r) for r in range(1, 4)))

        for i in range(total):
            # generate gender
            if i < num_women:
                gender = FEMALE
            elif i < num_women + num_nb:
                gender = NONBINARY
            else:
                gender = MALE

            # generate sexuality
            sexuality_id = random.randint(0,len(sexualities)-1)
            participant = ParticipantTruthful(i, gender, sexualities[sexuality_id])
            self.participants.add(participant)

        for participant in self.participants:
            participant.generate_preference_order(self.participants)


    def runMatch(self):

        set_proposed_to = set()
        # iterating through all participants
        print("in run match")
        for participant in self.participants:
            print("in for loop")
            
            proposer = participant
    
                
            next_choice = proposer.preference_order_list[proposer.ask_rank]

            # iterating through preference list of proposer, switching to anyone rejected due to current proposer
            while next_choice not in set_proposed_to and proposer.ask_rank < proposer.cutoff:
                print("in while loop")
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
        # if next_choice.paired_with is None:
        #     return True 
        print("in proposal_accepted")
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
            
new_simulation = Sim()
new_simulation.runMatch()

print("truthful sim")
for participant in new_simulation.participants:
    print("PARTICIPANT " + str(participant.id))
    if participant.paired_with:
        print("matched with " + str(participant.paired_with.id))
    else:
        print("no match")

        





# def parse_strategic(args):
#     # might not work
#     for c in args:
#         s = c.split(',')
#         name, count = s
#     return count


# def main(args):
#     usage_msg = "Usage:  %prog [options] PeerClass1[,count] PeerClass2[,count] ..."
#     parser = OptionParser(usage=usage_msg)

#     def usage(msg):
#         print(("Error: %s\n" % msg))
#         parser.print_help()
#         sys.exit()

#     parser.add_option("--numWomen",
#                       dest="num_women", default=5, type="int",
#                       help="Set number of women in simulation")

#     parser.add_option("--numNonBinary",
#                       dest="num_nb", default=5, type="int",
#                       help="Set number of nonbinary people in simulation")

#     parser.add_option("--numMen",
#                       dest="num_men", default=5, type="int",
#                       help="Set number of men in simulation")

#     (options, args) = parser.parse_args()

#     # leftover args are class names, with optional counts:
#     # "Peer Seed[,4]"

#     if len(args) == 0:
#         # default
#         strategic_count = 0
#     else:
#         try:
#             strategic_count = parse_strategic(args)
#         except ValueError as e:
#             usage(e)

#     configure_logging(options.loglevel)
#     config = Params()

#     config.add("num_women", options.num_women)
#     config.add("num_nb", options.blocks_nb)
#     config.add("num_men", options.max_men)

#     sim = Sim(config)
#     sim.run_sim()


# if __name__ == "__main__":
#     # The next two lines are for profiling...
#     import cProfile

#     cProfile.run('main(sys.argv)', 'out.prof')
# #    main(sys.argv)