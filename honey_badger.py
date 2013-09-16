import random
import math

class Player:
    def __init__(self):

        # variables for a tit for 2 tats
        self.c_prob_to_deviate = 0.1  # a constant,  a probability to deviate from tic for 2 tacs tactics
        self.opponets_choice_last_round = [] # list of opponents choices in the last round
        self.opponets_choice_penult_round = [] # list of opponents choices in the penultimate round
        self.opponets_rep_last_round = [] # a dictionary of opponents reputation in the last round to try match
        self.to_deviate = [] #decision to deviate from tic-for-tac tactics
        
        # variables for a local search
        self.targeted_reputation = 0.9  #  what must be my reputation as measured in this round only
        self.min_rounds_per_step = 5  # minimum number of rounds in one search step
        self.rounds_left_in_current_stage = self.min_rounds_per_step # how many more round I must stay in this step
        self.step_type = 'h'   # 'h' when moving reputation up, 's' when moving reputation down
        self.is_stable = True  # if now is the stable period?
        self.last_gain_average = 3.0 # how much food (excluding award) I gained in the last stable period in a round on average per opponent
        self.gaining_now = 0.0 # how much food (excluding award) I have gained so far in the stable period, on average per opponent
        self.step_size = 0.2 # how large is a search step
        
        self.number_choices = 0  # how many choices I (and each remaining player) have made so far in a game
        self.max_reputation_var = 1.0 # how much reputation can vary from choices in one round
       
    def tit_for_tat(self, round_number, current_food, current_reputation, m,  player_reputations):
        hunt_decisions = []
        to_deviate_new = []
        if self.to_deviate == []:
            self.to_deviate = [False for x in self.opponets_choice_last_round]
        for i in range(len(player_reputations)):
            # rematch opponents from previous rounds
            matching_player_last = min(range(len(self.opponets_choice_last_round)), key=lambda j: abs(self.opponets_choice_last_round[j][0] - player_reputations[i]))
            matching_player_penult = min(range(len(self.opponets_choice_penult_round)), key=lambda j: abs(self.opponets_choice_penult_round[j][0] - self.opponets_choice_last_round[matching_player_last][0]))
            response = 'h' if self.opponets_choice_last_round[matching_player_last][1] == 'h' or self.opponets_choice_penult_round[matching_player_penult][1] == 'h' else 's' # a tit for 2 tats
            if self.to_deviate[matching_player_last] and self.opponets_choice_last_round[matching_player_last][1] == 'h':
                response = 's' # keep slacking since no retaliation
                to_deviate_new.append(True)
            else:
                to_deviate = random.random() < self.c_prob_to_deviate # try to see if opponents cares to retaliate or start to cooperate
                if to_deviate:
                    response = 'h' if response == 's' else 's'
                to_deviate_new.append(to_deviate)
            hunt_decisions.append(response)
        self.to_deviate = to_deviate_new
        self.rounds_left_in_current_stage = self.min_rounds_per_step
        self.gaining_now = 0.0
        self.is_stable = True
        return hunt_decisions   

    def local_search(self, round_number, current_food, current_reputation, m, player_reputations):
        if not self.is_stable:
            # reputation is changing
            if (self.step_type == 's' and current_reputation <= self.targeted_reputation) or \
                (self.step_type == 'h' and current_reputation >= self.targeted_reputation):
                # target achieved!
                self.rounds_left_in_current_stage = self.min_rounds_per_step
                self.gaining_now = 0.0
                self.is_stable = True
            else:
                # keep moving
                hunt_decisions = [self.step_type for x in player_reputations] 
        elif self.is_stable and self.rounds_left_in_current_stage == 0:
                # was gathering statistics, now time to evaluate and make a step
                self.is_stable = False # start moving again
                if (self.step_type == 'h') == (self.gaining_now > self.last_gain_average):
                    self.targeted_reputation = (1.0 + self.step_size) * current_reputation
                    self.step_type = 'h'
                else:
                    self.targeted_reputation = (1.0 - self.step_size) * current_reputation
                    self.step_type = 's'
                self.targeted_reputation = max(min(self.targeted_reputation, 1.0 - self.step_size / 3), self.step_size / 3)
                if self.last_gain_average > self.gaining_now: 
                    # make local search slower over time to stabilize
                    self.min_rounds_per_step += int(5) 
                    self.step_size *= 0.5
                self.last_gain_average = self.gaining_now
                hunt_decisions = [self.step_type for x in player_reputations] 
        if self.is_stable and self.rounds_left_in_current_stage > 0:
            # keep gathering statistics
            self.rounds_left_in_current_stage -= 1
            number_of_slacks_this_round = int(round((1.0 - current_reputation) * len(player_reputations), 0)) # keep reputation stable over data collection periods
            # 'hunt' number_of_slacks_this_round worst players in this round
            if number_of_slacks_this_round == len(player_reputations):
                epsilon = -1.0
            else:
                epsilon = sorted(map(lambda x:abs(x - current_reputation), player_reputations))[number_of_slacks_this_round] # how far to the worst of the best players
            hunt_decisions = ['s' if abs(x - current_reputation) < epsilon else 'h' for x in player_reputations]
        return hunt_decisions

    def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
        if len(player_reputations) == 2: 
            #if two players then always slacker
            hunt_decisions = ['s' for x in player_reputations] 
        elif all((rep < current_reputation - self.max_reputation_var) or 
            (rep > current_reputation + self.max_reputation_var) for rep in player_reputations):
            hunt_decisions = self.tit_for_tat(round_number, current_food, current_reputation, m, player_reputations)
        else:
            hunt_decisions = self.local_search(round_number, current_food, current_reputation, m, player_reputations)

        self.number_choices += len(player_reputations)
        self.max_reputation_var = float(len(player_reputations)) / self.number_choices
        self.opponets_rep_last_round = player_reputations        
        return hunt_decisions

    def hunt_outcomes(self, food_earnings):
        self.opponets_choice_penult_round = self.opponets_choice_last_round 
        self.opponets_choice_last_round = [(self.opponets_rep_last_round[i], 'h' if food_earnings[i] >= 0 else 's') for i in range(len(food_earnings))]
        if self.is_stable:
            self.gaining_now += sum(food_earnings) / float(len(food_earnings)) / float(self.min_rounds_per_step)

    def round_end(self, award, m, number_hunters):
        pass # do nothing
