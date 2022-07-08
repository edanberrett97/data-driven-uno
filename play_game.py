from functions import eligible_cards
from functions import eligible_plus_cards
from play_from_state import play_from_state
import random
import numpy as np
import pandas as pd
import copy 

#setting some parameters for the game
colours = ['r','g','b','y']
N = 9
N_duplicates = 2
N_zeros = 1
N_players = 5
start_cards_per_player = 5
N_wild = 2
N_action = 2
actions = ['_skip','_reverse','_+2']
#creating a list of all the cards in the deck
all_number_cards = [c + str(j+1) 
                    for c in colours
                    for j in range(N)] * N_duplicates
all_number_cards += [c + '0' for c in colours] * N_zeros
all_wild_cards = ['wild','wild+4'] * N_wild
all_action_cards = [c + a
                    for c in colours
                    for a in actions] * N_action
original_deck = all_number_cards + all_wild_cards + all_action_cards

def play_game(game):

    #table to add data from each turn to
    turns = {
        'game':[],
        'turn':[],
        'direction_pre_play':[],
        'player':[],
        'player_hand_pre_play':[],
        'jump_in_player':[],
        'player_n_cards_pre_play':[]
    }
    turns.update({
        'player_'+str(i+1)+'_hand_pre_play':[] for i in range(N_players)
    })
    turns.update({
        'player_'+str(i+1)+'_n_cards_pre_play':[] for i in range(N_players)
    })
    turns.update({
        'player_possible_cards':[],
        'player_possible_plus_cards':[],
        'played_card':[],
        'challenge':[],
        'wild_card_chosen_colour':[],
        'trade_player':[],
        'player_hand_post_play':[]
    })
    turns.update({
        'player_'+str(i+1)+'_hand_post_play':[] for i in range(N_players)
    })
    turns.update({
        'branch_winner':[],
        'branch_winner_score':[]
    })

    #game starts with original deck which is then shuffled
    deck = original_deck[:]
    random.shuffle(deck)
    #a selection of cards to supply each players hand and start the discard
    #pile with one card
    initial_drawn_cards = deck[:N_players*start_cards_per_player+1]
    
    #the selection of cards is removed from the deck and shared across the 
    #players' hands as well as one being placed face up to start the discard
    #pile
    deck = deck[N_players*start_cards_per_player+1:] 
    player_hands = {'player_'+str(i+1):
                    list(initial_drawn_cards)[start_cards_per_player*i:
                                      start_cards_per_player*(i+1)]
                    for i in range(N_players)}
    discard_pile = [initial_drawn_cards[-1]]
    
    #some dynamic game parameters
    #when end becomes False, the game ends
    end = False
    #the total number of turns that have been taken in the game
    turn = 0
    #the total number of steps that have been made in the clockwise direction 
    #(when play is moving anti-clockwise, n_cycles decreases by 1 per turn)
    n_cycles = 0
    #direction is 1 if play is moving clockwise, -1 if it is moving 
    #anti-clockwise
    direction = 1
    #wild_card_chosen_colour becomes the colour chosen by the player if they
    #play a wild card, and persists until another card is played
    wild_card_chosen_colour = ''
    #wild_card_last_played becomes True if a wild card is played, and only 
    #becomes False once a non-wild card is played
    wild_card_last_played = False
    #last_plus_four_turn is the last turn where a wild+4 was played
    last_plus_four_turn = 0
    #illegal_plus_four becomes True if a player plays a wild+4 when they could 
    #have played a different card, and persists until another wild+4 is played
    illegal_plus_four = False
    #n_cards_to_pick_up accumulates the number of cards on a "+" card whenever 
    #one is played, and also accumulates 2 if a player incorrectly challenges a
    #played wild+4 card, only returning to 0 once a player can't play any card
    #or incorrectly challenges a played wild+4 card, and is forced to pick up 
    #n_cards_to_pick_up cards
    n_cards_to_pick_up = 0
    #discard_pile_flip is False by default and becomes True whenever the deck 
    #becomes empty after a player's turn, at which point the discard pile is 
    #flipped over to replenish the deck; it returns to False at the end of the 
    #next turn
    discard_pile_flip = False
    #loop_count accumulates 1 whenever the deck and discard pile are both empty
    #and a player is unable to play a card; it returns to zero whenever a card 
    #is played; if it exceeds N_players, then this means the game will continue
    #indefinitely, so end is set to True if this becomes the case
    loop_count = 0
    #drawn_wpf_card_played is True if a wild+4 card is played immediately after
    #being drawn; this is so that the next player knows not to challenge as 
    #they will have seen that the wild+4 was the only card the previous player
    #could have played; drawn_wpf_card_played returns to False after the 
    #decision to not challenge has been made
    drawn_wpf_card_played = False
    
    #players keep taking turns until end becomes True
    while end == False:

        state = {
            'deck':deck[:],
            'player_hands':{p:player_hands[p][:] for p in player_hands},
            'discard_pile':discard_pile[:],
            'end':end,
            'turn':turn,
            'n_cycles':n_cycles,
            'direction':direction,
            'wild_card_chosen_colour':wild_card_chosen_colour,
            'wild_card_last_played':wild_card_last_played,
            'last_plus_four_turn':last_plus_four_turn,
            'illegal_plus_four':illegal_plus_four,
            'n_cards_to_pick_up':n_cards_to_pick_up,
            'discard_pile_flip':discard_pile_flip,
            'loop_count':loop_count,
            'drawn_wpf_card_played':drawn_wpf_card_played
        }
        
        #the player and previous player (out of 1 to N_players) can be 
        #determined from n_cycles like so
        previous_player = (n_cycles - direction) % N_players + 1
        player = n_cycles % N_players + 1
        
        leaf = play_from_state(game,copy.deepcopy(state),colours,N_players)
        branch_winner = leaf[0]
        branch_winner_score = leaf[1]

        #the hands of each player before anything happens this turn
        player_hands_pre_play = {p:player_hands[p][:] for p in player_hands}
        player_hand_pre_play = player_hands['player_'+str(player)][:]
        direction_pre_play = direction #and direction before anything happens
        
        #if a player has a card with the same number and colour as that on the 
        #top of the discard pile, they can play that card (jump in) even if it 
        #isn't their turn, if they are fast enough, with play then continuing 
        #to their left or right depending on the current direction; whether a
        #jump-in occurs is modelled by jump_in being chosen randomly, and if it
        #is True, the option for a jump-in to occur being given; if a jump-in
        #occurs, then it will be considered to be everything that happened in
        #the turn
        jump_in = np.random.choice([True,False])
        #if the discard pile isn't empty, the card on the top of the discard 
        #pile is a number card, and there is the possibility of a jump-in
        if (discard_pile != [] 
            and len(discard_pile[-1]) == 2 
            and jump_in == True):
            #all players that hold a card identical to that on the top of the
            #discard pile
            jump_in_players = [p for p in player_hands 
                               if discard_pile[-1] in player_hands[p]] 
            #if there are any players that could jump in
            if jump_in_players != []:
                #randomly select one of them; only the fastest one can jump in
                jump_in_player = np.random.choice(jump_in_players)
                int_jump_in_player = int(str.split(jump_in_player,'_')[-1])
                #the played card for the turn is the card held by the player 
                #who jumped in that is identical to that on the top of the 
                #discard pile; no cards need to be drawn this turn
                played_card = discard_pile[-1]
                n_drawn_cards = 0
                #adjust n_cycles so that it is as if play had continued in the 
                #current direction from the player whose turn it was to the 
                #player who jumped in 
                n_cycles += (int_jump_in_player - player) % N_players 
                previous_player = (n_cycles - direction) % N_players + 1 
                player = n_cycles % N_players + 1 
            else:
                #if no players can jump in, then no jump-in occurs
                jump_in_player = ''
                jump_in = False
        else:
            jump_in_player = ''
            jump_in = False

        #cards that the current player is allowed to play are determined here,
        #assuming that they don't have to pick up any cards
        if ((discard_pile != [] 
            and 'wild' in discard_pile[-1]) 
            or discard_pile == []): 
            if wild_card_last_played == False:
                #if the top of the discard pile is a wild card, but 
                #wild_card_last_played is False, this is either how the game 
                #started or because the deck was previously empty and the 
                #discard pile was flipped to replenish the deck, with the first 
                #card to start the discard pile being a wild card; so the 
                #current player can play any card
                player_possible_cards = player_hand_pre_play
            else:
                #otherwise if the discard pile top is a wild card, the cards
                #allowed to be played are wild cards and cards the same colour
                #as that chosen by the player that played the wild card
                player_possible_cards = eligible_cards(player_hand_pre_play,
                                                   wild_card_chosen_colour+'*')
        else:
            #cards allowed to be played otherwise
            player_possible_cards = eligible_cards(player_hand_pre_play,
                                                           discard_pile[-1])
        #any "+" cards allowed to be played, if the discard pile top card is a 
        #"+" card
        if discard_pile != []:
            player_possible_plus_cards = eligible_plus_cards(
                                        player_hand_pre_play,discard_pile[-1])
        else:
            player_possible_plus_cards = []

        #if the previous player played a wild+4, the current player can 
        #challenge it's use as one can only be played if the player has no 
        #other allowed cards that they could play  
        if (discard_pile != []
            and discard_pile[-1] == 'wild+4' 
            #top of discard pile needs to be a wild+4, but this also needs
            #to not be the result of a discard pile flip or the game 
            #starting this way, in order for it to have been the card that
            #the previous player played 
            and discard_pile_flip == False 
            and turn != 0
            #should be wild+4 that wasn't played immediately after being drawn,
            #as challenging this would always be incorrect
            and drawn_wpf_card_played == False 
            #checking wild+4 was played in previous turn, not earlier
            and turn - last_plus_four_turn == 1): 
            #current player may or may not challenge
            challenge = np.random.choice([True,False])
        else:
            #no challenge if wild card wasn't played
            challenge = False
        #now that challenge decision has been made, no longer need a record of 
        #whether the wild+4 was played immediately after being drawn
        drawn_wpf_card_played = False
        #if current player correctly challenges
        if challenge == True and illegal_plus_four == True:
            #previous player has to pick up n_cards_to_pick_up cards from the
            #deck (n_cards_to_pick_up will have accumulated 4 when they played 
            #the wild+4)
            previous_player_n_drawn_cards = n_cards_to_pick_up
            #set this to 0 as accumulated cards will now be picked up 
            n_cards_to_pick_up = 0
        #if current player incorrectly challenges
        if challenge == True and illegal_plus_four == False:
            #previous player has to pick up no cards; 2 cards are added to 
            #n_cards_to_pick_up and current player will be forced to pick up
            #this many cards (see below)
            previous_player_n_drawn_cards = 0
            n_cards_to_pick_up += 2 
        #if current player doesn't challenge, then previous player doesn't have
        #to pick up any cards and n_cards_to_pick_up remains the same
        if challenge == False:
            previous_player_n_drawn_cards = 0
            
        #if there was a jump-in, this effectively cancels the turn for the 
        #current player, so only as long as jump_in is False, and there are no
        #cards to pick up, the current player can continue their turn with 
        #complete freedom
        if n_cards_to_pick_up == 0 and jump_in == False:
            #if player has any cards that are allowed to be played
            if player_possible_cards != []:
                #randomly choose one of them to play; current player doesn't 
                #have to draw any cards this turn
                played_card = np.random.choice(player_possible_cards)
                n_drawn_cards = 0
                #any allowed cards held that aren't wild+4 cards
                player_possible_nwpf_cards = [c for c in player_possible_cards
                                              if c != 'wild+4']
                #illegal for a wild+4 to be played when a different card could 
                #have been played
                if (played_card == 'wild+4' 
                    and player_possible_nwpf_cards != []): 
                    illegal_plus_four = True
                else:
                    illegal_plus_four = False                
            #if player can't play any of their cards
            else:
                #the player won't play any card this turn and will have to pick 
                #one up from the deck
                played_card = ''
                n_drawn_cards = 1
                #the previous player has to draw a certain number of cards 
                #(possibly 0) before the current player draws their card; here,
                #we determine what card the current player will draw after the
                #previous player has drawn
                #
                #if the deck has more cards than previous_player_n_drawn_cards,
                #then the current player will pick up the card that is 
                #previous_player_n_drawn_cards into the deck, as the previous
                # player will have picked up previous_player_n_drawn_cards
                #from the deck first
                if len(deck) > previous_player_n_drawn_cards:
                    player_drawn_card = deck[previous_player_n_drawn_cards]
                #otherwise, if the deck and discard pile combined have more 
                #cards than previous_player_n_drawn_cards, the current player 
                #will pick up the card that is 
                #(previous_player_n_drawn_cards-len(deck)) into the discard 
                #pile, as the previous player will have picked up all cards
                #from the deck, and that many cards from the bottom of the 
                #discard pile too
                elif (len(deck) + len(discard_pile) > 
                                                previous_player_n_drawn_cards):
                    player_drawn_card = discard_pile[
                                    previous_player_n_drawn_cards-len(deck)] 
                #otherwise, the previous player will pick up all cards from the
                #deck and discard pile, so the current player won't be able to 
                #pick up a card
                else:
                    player_drawn_card = '' 
                    played_card = ''
                #if drawn card is allowed to be played, that is if it is the 
                #same colour as wild_card_chosen_colour, or allowed to be 
                #played given the card on top of the discard pile
                if (player_drawn_card != ''
                    and (player_drawn_card[0] == wild_card_chosen_colour 
                        or (discard_pile != [] 
                            and eligible_cards([player_drawn_card],
                                   discard_pile[-1]) == [player_drawn_card]))):
                    #then the drawn card will be played immediately
                    played_card = player_drawn_card
                    #if drawn and subsequently played card was a wild+4, then
                    #need a record of this so that next player doesn't 
                    #challenge when doing so would obviously be incorrect
                    if played_card == 'wild+4':
                        drawn_wpf_card_played = True
        
        #again only if a jump-in hasn't occurred, which would have effectively 
        #cancelled the turn for the current player, we can now check what 
        #happens if there are cards to pick up
        elif jump_in == False:
            if (discard_pile != []
                and '+' in discard_pile[-1] 
                and player_possible_plus_cards != []
                #if current player didn't incorrectly challenge a wild+4  
                and [challenge,illegal_plus_four] != [True,False]): 
                #if the discard pile top card is a "+" card, and the current 
                #player hasn't just incorrectly challenged a played wild+4 card 
                #then they may play another "+" card if it has the same number
                #of required cards to pick up; randomly choose one if there are 
                #any that can be played; current player has to draw no cards
                #this turn
                played_card = np.random.choice(player_possible_plus_cards)
                n_drawn_cards = 0
                if played_card == 'wild+4': 
                    #not possible for this to be illegal as it is the only card 
                    #that the player is allowed to play in this case
                    illegal_plus_four = False
            else:
                played_card = ''
                n_drawn_cards = n_cards_to_pick_up
                n_cards_to_pick_up = 0
       
        #previous player has to pick up previous_player_n_drawn_cards cards,
        #current player has to pick up n_drawn_cards cards
        players_n_drawn_cards = {previous_player:previous_player_n_drawn_cards,
                               player:n_drawn_cards}
        #first element is list of cards previous player draws, second element 
        #is list of cards current player draws
        players_drawn_cards = []
        #for each of the above two players (previous player first as they will
        #need to draw cards first if they played an illegal wild+4)
        for p in players_n_drawn_cards:
            #if the deck contains at least as many cards as those the player 
            #needs to pick up, then take that many cards from the deck and add
            #them to the player's hand
            if len(deck) >= players_n_drawn_cards[p]:
                p_drawn_cards = deck[:players_n_drawn_cards[p]]
                player_hands['player_'+str(p)] += p_drawn_cards
                deck = deck[players_n_drawn_cards[p]:]
            #if the deck doesn't contain enough cards, add the whole deck to 
            #the player's hand, then take any additional cards that need to be
            #picked up from the bottom of the discard pile and also add them to
            #the player's hand (because the discard pile would be flipped to
            #replenish the deck anyway once the deck becomes empty)
            else:
                #number of cards that need to picked up from bottom of the
                #discard pile
                n_discard_pick_up = players_n_drawn_cards[p] - len(deck)
                p_drawn_cards = deck + discard_pile[:n_discard_pick_up]
                deck = []
                discard_pile =  discard_pile[n_discard_pick_up:]
                player_hands['player_'+str(p)] += p_drawn_cards 
            players_drawn_cards.append(p_drawn_cards)
        #if current player played a card, remove it from their hand and add it
        #to the top of the discard pile; this can include a single card that 
        #they have picked up but can now play, as all drawing has now been 
        #performed
        if played_card != '':
            player_hands['player_'+str(player)].remove(played_card)
            discard_pile.append(played_card)
        
        if deck == [] and discard_pile == [] and played_card == '': 
            loop_count += 1
        if played_card != '':
            loop_count = 0
        if loop_count > N_players:
            end = True
            
        #check if the deck is empty, in which case the discard pile needs to be
        #flipped over to replenish the deck, and if a wild card wasn't last 
        #played, the top card of the result must be flipped over to start a new 
        #discard pile
        if deck == [] and discard_pile != []:
            discard_pile_flip = True
            #flip the discard pile over to replenish the deck
            deck = discard_pile
            #only if wild_card_last_played is False, as if it is True, the 
            #chosen colour can be used for the next player to determine whether
            #they can play any cards
            if wild_card_last_played == False:
                #take the top card from the deck and flip it over to start the
                #discard pile again
                discard_pile = [deck[0]]
                deck = deck[1:]
                if '+' in discard_pile[-1]:
                    #if the flipped over card is a "+" card, then 
                    #n_cards_to_pick_up becomes the number of cards the card 
                    #requires to be picked up; it is not added to because 
                    #if the deck has become empty, n_cards_to_pick_up must be / 
                    #have become zero as either a card was picked up or 
                    #n_cards_to_pick_up were picked up in order for the deck to
                    #become empty
                    n_cards_to_pick_up = int(discard_pile[-1][-1])
            else:
                discard_pile = []
        else:
            discard_pile_flip = False

        #effects if played card was any kind of special card
        if played_card == 'wild+4':
            last_plus_four_turn = turn
        if 'wild' in played_card:
            #player chooses a colour that next card played has to be if 
            #they played a wild card
            wild_card_chosen_colour = np.random.choice(colours)
            wild_card_last_played = True
        #the chosen colour persists until another card is played
        elif played_card != '':
            wild_card_chosen_colour = ''
            wild_card_last_played = False
        if 'skip' in played_card:
            #at the end of the turn, there is another 
            #"n_cycles += direction", so this results in the next player 
            #being the player two after the current player, in the direction of
            #play
            n_cycles += direction
        if 'reverse' in played_card:
            #switches the direction
            direction *= -1
        if '+' in played_card:
            #if a "+" card was played, add the number of cards the card says to 
            #pick up to n_cards_to_pick_up 
            n_cards_to_pick_up += int(played_card[-1])
        if '7' in played_card:
            #if a 7 was played, the current player has to trade hands with 
            #a player of their choice
            current_player_hand = player_hands['player_'+str(player)][:]
            #randomly choose one of the players that isn't the current 
            #player
            trade_player = np.random.choice([p for p in player_hands
                                         if p != 'player_'+str(player)])
            trade_player_hand = player_hands[trade_player][:]
            #switch hands of current player with player chosen for trade
            player_hands['player_'+str(player)] = trade_player_hand
            player_hands[trade_player] = current_player_hand
        else:
            trade_player = ''
        if '0' in played_card:
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
                                    
        #if a game has lasted this long, then it is almost certainly stuck in a
        #loop, so end it
        if turn > 10000:
            end = True
            
        #the hands of each player at the end of this turn
        player_hands_post_play = {p:player_hands[p][:] for p in player_hands}
        player_hand_post_play = player_hands['player_'+str(player)][:]
                
        #adding data from current turn to game data
        column_variables = {
            'game':game,
            'turn':turn,
            'direction_pre_play':direction_pre_play,
            'player':player,
            'player_hand_pre_play':','.join(player_hand_pre_play),
            'jump_in_player':jump_in_player,
            'player_n_cards_pre_play':len(player_hand_pre_play)
        }
        column_variables.update({
            p+'_hand_pre_play':','.join(player_hands_pre_play[p]) 
                                             for p in player_hands_pre_play
        })
        column_variables.update({
            p+'_n_cards_pre_play':len(player_hands_pre_play[p]) 
                                             for p in player_hands_pre_play
        })
        column_variables.update({
            'player_possible_cards':','.join(player_possible_cards),
            'player_possible_plus_cards':','.join(player_possible_plus_cards),
            'played_card':played_card,
            'challenge':challenge,
            'wild_card_chosen_colour':wild_card_chosen_colour,
            'trade_player':trade_player,
            'player_hand_post_play':','.join(player_hand_post_play)
        })
        column_variables.update({
            p+'_hand_post_play':','.join(player_hands_post_play[p]) 
                                             for p in player_hands_post_play
        })
        column_variables.update({
            'branch_winner':branch_winner,
            'branch_winner_score':branch_winner_score
        })
        for c in column_variables:
            turns[c].append(column_variables[c])
            
        #end the game if any player's hand is empty
        if [] in [player_hands[p] for p in player_hands]:
            end = True

        turn += 1
        n_cycles += direction
            
    return pd.DataFrame(turns)
