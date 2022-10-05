from definitions import (
    card_types,
    trade_model_X_columns,
    play_card_model_X_columns
)
from functions import (
    count_hand_cards_of_type,
    m_players_later_n_cards,
    m_players_later_score,
    count_distinct_numbers_or_actions_in_hand,
    count_distinct_colours_in_hand,
    hand_score
)
import pandas as pd
import numpy as np

#
def make_decision(data,model,THINGY):
    predictions = model.predict_proba(data)
    predictions = [p[1] for p in predictions]
    
    if THINGY == 1:
    
        return np.argmax(predictions)
    
    if THINGY == -1:
        
        return np.argmin(predictions)

#When a player plays a 7, they must trade hands with another player. This 
#function will determine the best player to trade with based on the predicted
#game outcome, for each trade, according to a model making predictions from:
    #whether the player challenged earlier in their turn
    #MAYBE WILD_CARD_CHOSEN_COLOUR AND OTHER DISCARD VARIABLES
    #the position of the potential trade player relative to the player
    #

##all_options_predictions = pd.DataFrame({c:[] for c in trade_model_X_columns})

def choose_trade_player(player,
                        hand_pre_trade,
                        direction_pre_trade,
                        player_hands_pre_trade,
                        player_scores,
                        challenge,
                        model,
                        THINGY
                        ):
    options_predictions = {c:[] for c in trade_model_X_columns}
    possible_trade_players = [p for p in player_hands_pre_trade
                                      if int(str.split(p,'_')[-1]) != player]
    #
    for trade_player in possible_trade_players:
        trade_player_relative_position = direction_pre_trade * (
                int(str.split(trade_player,'_')[-1]) - player
            ) % len(player_hands_pre_trade)
        row_values = {
                'challenge':challenge,
                #wild_card_chosen_colour
                'trade_player_relative_position':
                                                trade_player_relative_position,
                'player_n_cards_pre_trade':len(hand_pre_trade),
                'player_n_cards_post_trade':len(
                                        player_hands_pre_trade[trade_player]),
                'player_current_score':player_scores['player_' + str(player)]   
            }
        for t in card_types:
            row_values.update({'player_n_' + t + '_cards_pre_trade':
                               count_hand_cards_of_type(hand_pre_trade,t)})
        row_values.update({
            'player_n_unique_numbers_or_actions_pre_trade':
                count_distinct_numbers_or_actions_in_hand(
                                                    hand_pre_trade),
            'player_n_unique_colours_pre_trade':
                    count_distinct_colours_in_hand(hand_pre_trade),
            'player_hand_score_pre_trade':hand_score(hand_pre_trade)
         })
        for i in range(len(player_hands_pre_trade) - 1):
            row_values.update({str(i+1) + '_players_later_n_cards_post_trade':
                m_players_later_n_cards(direction_pre_trade,
                                        player,
                                        player_hands_pre_trade,
                                        i+1)})
            row_values.update({str(i+1) + '_players_later_current_score_post_trade':
                m_players_later_score(direction_pre_trade,
                                      player,
                                      player_scores,
                                      i+1)})
        row_values.update({str(trade_player_relative_position) + 
                   '_players_later_n_cards_post_trade':len(hand_pre_trade)})
        for v in row_values:
            options_predictions[v].append(row_values[v])
    options_predictions = pd.DataFrame(options_predictions)
    
    ##global all_options_predictions
    ###all_options_predictions = all_options_predictions.iloc[0:0]
    ##all_options_predictions = all_options_predictions.append(options_predictions)
    ##print(all_options_predictions)
    
    return possible_trade_players[make_decision(options_predictions,model,THINGY)]


#
def choose_card_to_play(player,
                        possible_cards,
                        hand_pre_play,
                        direction_pre_play,
                        player_hands_pre_play,
                        player_scores,
                        model):
    options_predictions = {c:[] for c in play_card_model_X_columns}
    sevens = [c for c in possible_cards if '7' in c]
    for card in possible_cards:
        #THE PLAYERS HAND WILL LOOK DIFFERENT DEPENDING ON WHICH 7 IS PLAYED, 
        row_values = {
                'challenge':
            }

#
def correct_challenge_probability(player,
                                  hand_pre_play,
                                  direction_pre_play,
                                  player_hands_pre_play,
                                  player_scores,
                                  model):
    challenge_options_predictions = {
            'challenge':1,
            'player_n_cards_pre_play':len(hand_pre_play)
        }
    
    challenge_options_predictions = {
            'challenge':[],
            'player_n_cards_pre_play':[]
        }
    for i in range(len(player_hands_pre_play) - 1):
        challenge_options_predictions.update({
            str(i+1) + '_players_later_n_cards_pre_play':
                                                    m_players_later_n_cards(
                                                        direction_pre_play,
                                                        player,
                                                        player_hands_pre_play,
                                                        i+1
                                                        ),
            str(i+1) + '_players_later_current_score':
                                                    m_players_later_score(
                                                        direction_pre_play,
                                                        player,
                                                        player_scores,
                                                        i+1
                                                        )
        })
    challenge_options_predictions = pd.DataFrame(
                                            challenge_options_predictions)
    return model.predict_proba(challenge_options_predictions)[0][1]

#
def make_decision_CALLTHISSOMETHINGELSE(player,
                  possible_cards,
                  hand_pre_play,
                  direction_pre_play,
                  player_hands_pre_play,
                  player_scores,
                  model,
                  challenge_model,
                  decision_type,
                  previous_player_played_wild_plus_four=False):
    
    decision_types = ['card_to_play','whether_to_challenge','player_to_trade_with']
    
    #IF WILD+4 NOT PLAYED BY PREVIOUS PLAYER:
    #1. FOR EACH PLAYABLE CARD, PREDICT THE OUTCOME OF PLAYING IT
    #2. FOR EACH PLAYABLE CARD THAT IS A 7, THIS WILL NEED TO BE DONE BY CONSIDERING
    #EVERY OTHER PLAYER AND THE OUTCOME OF TRADING HANDS WITH THEM
    #3. CHOOSE THE CARD WITH HIGHEST PREDICTED OUTCOME
    
    #IF WILD+4 PLAYED BY PREVIOUS PLAYER:
    #1. PREDICT PROBABILITY OF SUCCESSFUL CHALLENGE BASED ON PRE-PLAY VARIABLES AND SEPARATE MODEL P(SC)
    #2. DETERMINE WHICH CARD WILL BE PLAYED ASSUMING SUCCESSFUL CHALLENGE AND GET PREDICTED OUTCOME OF PLAYING IT P(SCPC)
    #3. GET PREDICTED OUTCOME ASSUMING UNSUCCESSFUL CHALLENGE P(UC)
    #4. GET PREDICTED OUTCOME OF NOT CHALLENGING P(NC)
    #5. PREDICTED OUTCOME OF CHALLENGING IS P(C) = P(SC)*P(SCPC) + (1-P(SC))*P(UC)
    #6. SO CHOOSE WHETHER TO CHALLENGE OR NOT BASED ON GREATEST OUT OF P(NC) AND P(C)
    #7. NEED THIS APPROACH BECAUSE PREDICTING OUTCOME OF CHALLENGE BASED ON PRE-PLAY 
    #VARIABLES WITHOUT CONSIDERING WHAT PLAYER WILL DO IF CHALLENGE IS SUCCESSFUL WILL
    #UNDERESTIMATE POTENTIAL BENEFIT OF CHALLENGING
    
    if previous_player_played_wild_plus_four == True:
        P_correct_challenge = correct_challenge_probability(player,
                                          hand_pre_play,
                                          direction_pre_play,
                                          player_hands_pre_play,
                                          player_scores,
                                          challenge_model)
    
    card_types = [
        'number',
        'wild',
        'wild+4',
        'skip',
        'reverse',
        '+2',
        '0',
        '7'
    ]
    options_predictions = {
            'challenge':[],
            #'wild_card_chosen_colour':[], #MAY INCLUDE THIS FEATURE LATER
            'trade_player':[],
            'player_n_cards_post_play':[],
            'player_current_score':[],
        }
    for t in card_types:
        options_predictions.update({'player_n_' + t + '_cards_post_play':[]})
    options_predictions.update({
        'player_n_unique_numbers_or_actions_post_play':[],
        'player_n_unique_colours_post_play':[],
        'player_hand_score_post_play':[]
    })
    for t in card_types:
        options_predictions.update({'played_card_is_' + t:[]})
    for i in range(len(player_hands_pre_play) - 1):
        options_predictions.update({str(i+1) + '_players_later_n_cards':[]})
        options_predictions.update({
                                str(i+1) + '_players_later_current_score':[]})
    
    for pc in possible_cards:
        
        potential_hand_post_play = [c for c in possible_cards if c != pc]
        potential_player_hands_post_play = player_hands_pre_play
        potential_player_hands_post_play[
                            'player_' + str(player)] = potential_hand_post_play
        
        #determine the consequences of playing the card pc here
        potential_direction_post_play = direction_pre_play
        if 'reverse' in pc:
            potential_direction_post_play *= -1
        next_player_n_cards_to_pick_up = 0
        if '+' in pc:
            next_player_n_cards_to_pick_up += int(pc[-1])
        #this determines whether to remove the player's knowledge of their hand
        #post play - if they are considering playing a 7 or 0, they shouldn't 
        #be given knowledge of the player's hand they trade with, as they can 
        #only know this once they actually play the card
        obscure_potential_hand_knowledge = False
        if '7' in pc:
            obscure_potential_hand_knowledge = True
            #if a 7 was played, the current player has to trade hands with 
            #a player of their choice
            player_potential_hand_post_play = potential_hand_post_play[:]
            #randomly choose one of the players that isn't the current 
            #player NO, CHECK ALL AVAILABLE OPTIONS IN THIS CASE
            for pl in [p for p in potential_player_hands_post_play 
                                               if p != 'player_'+str(player)]:
                trade_player = pl
                trade_player_hand = player_hands[trade_player][:]
            #switch hands of current player with player chosen for trade
            player_hands['player_'+str(player)] = trade_player_hand
            player_hands[trade_player] = current_player_hand
        else:
            trade_player = ''
        if '0' in pc:
            obscure_potential_hand_knowledge = True
            #if a 0 was played, every player passes their hand to the next
            #player in the current direction of play; so if the direction 
            #is clockwise, player_2 gets player_1's hand, ..., player_1 
            #gets player_N_players's hand; if the direction is 
            #anti-clockwise, player_1 gets player_2's hand, ..., 
            #player_N_players gets player_1's hand; this is achieved by
            #taking the list [player_1,...,player_N_players] and altering 
            #it to either be [player_2,...,player_N_players,player_1]
            #(clockwise) or [player_N_players,player_1,...,player_2]
            #(anti-clockwise), then performing an index-wise pairing with
            #[player_1's hand,...,player_N_players's hand]
            ordered_player_hands = [p for p in player_hands]
            if direction == -1:
                ordered_player_hands.reverse()
            ordered_player_hands.append(ordered_player_hands[0])
            ordered_player_hands.remove(ordered_player_hands[0])
            if direction == -1:
                ordered_player_hands.reverse()
            new_player_hands = {ordered_player_hands[i]:
                                [player_hands[p] for p in player_hands][i]
                                    for i in range(N_players)}
            player_hands = new_player_hands
        
        #REMINDER: PLAYER MUST NOT SEE OTHER PLAYER HAND IF POTENTIAL PLAYED CARD IS 0 OR 7 - SHOULD JUST TAKE AVERAGE OF ALL CASES EXCLUDING KNOWLEDGE OF CARDS IN NEW HAND FROM SWAP
        
        row_values = {
            #'challenge':challenge**2, #WILL INCLUDE THESE 3 FEATURES LATER
            #'wild_card_chosen_colour':wild_card_chosen_colour,
            #'trade_player':trade_player,
            'player_n_cards_post_play':len(potential_hand_post_play),
            'player_current_score':player_scores['player_' + str(player)],
        }
        for t in card_types:
            row_values.update({
                'player_n_' + t + '_cards_post_play':
                        count_hand_cards_of_type(potential_hand_post_play,t)
            })
        row_values.update({
            'player_n_unique_numbers_or_actions_post_play':
                count_distinct_numbers_or_actions_in_hand(
                                                    potential_hand_post_play),
            'player_n_unique_colours_post_play':
                    count_distinct_colours_in_hand(potential_hand_post_play),
            'player_hand_score_post_play':hand_score(potential_hand_post_play)
        })
        for t in card_types:
            row_values.update({
                'played_card_is_' + t:card_type_is_type(pc,t)
            })
        for i in range(len(player_hands_pre_play) - 1):
            row_values.update({str(i+1) + '_players_later_n_cards':
                m_players_later_n_cards(potential_direction_post_play,
                                        player,
                                        potential_player_hands_post_play,
                                        i+1)})
            row_values.update({str(i+1) + '_players_later_current_score':
                m_players_later_score(potential_direction_post_play,
                                      player,
                                      player_scores,
                                      i+1)})

        for v in row_values:
            options_predictions[v].append(row_values[v])
        
    
    
    
    
    
    