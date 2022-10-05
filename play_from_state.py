from functions import eligible_cards
from functions import eligible_plus_cards
from functions import hand_score
import numpy as np

def play_from_state(game,state,colours,N_players):
    deck = state['deck']
    player_hands = state['player_hands']
    discard_pile = state['discard_pile']
    end = state['end']
    turn = state['turn']
    n_cycles = state['n_cycles']
    direction = state['direction']
    wild_card_chosen_colour = state['wild_card_chosen_colour']
    wild_card_last_played = state['wild_card_last_played']
    last_plus_four_turn = state['last_plus_four_turn']
    illegal_plus_four = state['illegal_plus_four']
    n_cards_to_pick_up = state['n_cards_to_pick_up']
    discard_pile_flip = state['discard_pile_flip']
    loop_count = state['loop_count']
    drawn_wpf_card_played = state['drawn_wpf_card_played']

    while end == False:

        previous_player = (n_cycles - direction) % N_players + 1
        player = n_cycles % N_players + 1
        
        player_hand_pre_play = player_hands['player_'+str(player)][:]
        
        jump_in = np.random.choice([True,False])
        if (discard_pile != [] 
            and len(discard_pile[-1]) == 2 
            and jump_in == True):
            jump_in_players = [p for p in player_hands 
                               if discard_pile[-1] in player_hands[p]] 
            if jump_in_players != []:
                jump_in_player = np.random.choice(jump_in_players)
                int_jump_in_player = int(str.split(jump_in_player,'_')[-1])
                played_card = discard_pile[-1]
                n_drawn_cards = 0 
                n_cycles += (int_jump_in_player - player) % N_players 
                previous_player = (n_cycles - direction) % N_players + 1 
                player = n_cycles % N_players + 1 
            else:
                jump_in_player = ''
                jump_in = False
        else:
            jump_in_player = ''
            jump_in = False

        if ((discard_pile != [] 
            and 'wild' in discard_pile[-1]) 
            or discard_pile == []): 
            if wild_card_last_played == False:
                player_possible_cards = player_hand_pre_play
            else:
                player_possible_cards = eligible_cards(player_hand_pre_play,
                                                   wild_card_chosen_colour+'*')
        else:
            player_possible_cards = eligible_cards(player_hand_pre_play,
                                                           discard_pile[-1])
        if discard_pile != []:
            player_possible_plus_cards = eligible_plus_cards(
                                        player_hand_pre_play,discard_pile[-1])
        else:
            player_possible_plus_cards = []

        if (discard_pile != []
            and discard_pile[-1] == 'wild+4' 
            and discard_pile_flip == False 
            and turn != 0
            and drawn_wpf_card_played == False 
            and turn - last_plus_four_turn == 1): 
            challenge = np.random.choice([True,False])
        else:
            challenge = False
        drawn_wpf_card_played = False
        if challenge == True and illegal_plus_four == True:
            previous_player_n_drawn_cards = n_cards_to_pick_up
            n_cards_to_pick_up = 0
        if challenge == True and illegal_plus_four == False:
            previous_player_n_drawn_cards = 0
            n_cards_to_pick_up += 2 
        if challenge == False:
            previous_player_n_drawn_cards = 0
            
        if n_cards_to_pick_up == 0 and jump_in == False:
            if player_possible_cards != []:
                played_card = np.random.choice(player_possible_cards)
                n_drawn_cards = 0
                player_possible_nwpf_cards = [c for c in player_possible_cards
                                              if c != 'wild+4']
                if (played_card == 'wild+4' 
                    and player_possible_nwpf_cards != []): 
                    illegal_plus_four = True
                else:
                    illegal_plus_four = False                
            else:
                played_card = ''
                n_drawn_cards = 1
                if len(deck) > previous_player_n_drawn_cards:
                    player_drawn_card = deck[previous_player_n_drawn_cards]
                elif (len(deck) + len(discard_pile) > 
                                                previous_player_n_drawn_cards):
                    player_drawn_card = discard_pile[
                                    previous_player_n_drawn_cards-len(deck)] 
                else:
                    player_drawn_card = '' 
                    played_card = ''
                if (player_drawn_card != ''
                    and (player_drawn_card[0] == wild_card_chosen_colour 
                        or (discard_pile != [] 
                            and eligible_cards([player_drawn_card],
                                   discard_pile[-1]) == [player_drawn_card]))):
                    played_card = player_drawn_card
                    if played_card == 'wild+4':
                        drawn_wpf_card_played = True
        
        elif jump_in == False:
            if (discard_pile != []
                and '+' in discard_pile[-1] 
                and player_possible_plus_cards != []
                and [challenge,illegal_plus_four] != [True,False]): 
                played_card = np.random.choice(player_possible_plus_cards)
                n_drawn_cards = 0
                if played_card == 'wild+4': 
                    illegal_plus_four = False
            else:
                played_card = ''
                n_drawn_cards = n_cards_to_pick_up
                n_cards_to_pick_up = 0
       
        players_n_drawn_cards = {previous_player:previous_player_n_drawn_cards,
                               player:n_drawn_cards}
        players_drawn_cards = []
        for p in players_n_drawn_cards:
            if len(deck) >= players_n_drawn_cards[p]:
                p_drawn_cards = deck[:players_n_drawn_cards[p]]
                player_hands['player_'+str(p)] += p_drawn_cards
                deck = deck[players_n_drawn_cards[p]:]
            else:
                n_discard_pick_up = players_n_drawn_cards[p] - len(deck)
                p_drawn_cards = deck + discard_pile[:n_discard_pick_up]
                deck = []
                discard_pile =  discard_pile[n_discard_pick_up:]
                player_hands['player_'+str(p)] += p_drawn_cards 
            players_drawn_cards.append(p_drawn_cards)
        if played_card != '':
            player_hands['player_'+str(player)].remove(played_card)
            discard_pile.append(played_card)
        
        if deck == [] and discard_pile == [] and played_card == '': 
            loop_count += 1
        if played_card != '':
            loop_count = 0
        if loop_count > N_players:
            end = True
            
        if deck == [] and discard_pile != []:
            discard_pile_flip = True
            deck = discard_pile
            if wild_card_last_played == False:
                discard_pile = [deck[0]]
                deck = deck[1:]
                if '+' in discard_pile[-1]:
                    n_cards_to_pick_up = int(discard_pile[-1][-1])
            else:
                discard_pile = []
        else:
            discard_pile_flip = False

        if played_card == 'wild+4':
            last_plus_four_turn = turn
        if 'wild' in played_card:
            wild_card_chosen_colour = np.random.choice(colours)
            wild_card_last_played = True
        elif played_card != '':
            wild_card_chosen_colour = ''
            wild_card_last_played = False
        if 'skip' in played_card:
            n_cycles += direction
        if 'reverse' in played_card:
            direction *= -1
        if '+' in played_card:
            n_cards_to_pick_up += int(played_card[-1])
        if '7' in played_card:
            current_player_hand = player_hands['player_'+str(player)][:]
            trade_player = np.random.choice([p for p in player_hands
                                         if p != 'player_'+str(player)])
            trade_player_hand = player_hands[trade_player][:]
            player_hands['player_'+str(player)] = trade_player_hand
            player_hands[trade_player] = current_player_hand
        else:
            trade_player = ''
        if '0' in played_card:
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
                      
        if turn > 10000:
            winner = 'player_1' #THIS NEEDS TO BE CHANGED
            score = 500 #NEED TO IDENTIFY THE CORRECT SOLUTION HERE
            end = True
            
        if [] in [player_hands[p] for p in player_hands]:
            for p in player_hands:
                if player_hands[p] == []:
                    winner = p
            end = True
            score = sum([hand_score(player_hands[p]) for p in player_hands])

        turn += 1
        n_cycles += direction

    return winner,score
