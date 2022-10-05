import numpy as np
import pandas as pd

#this function finds all cards in the list hand_cards that are allowed to be 
#played if the top of the discard pile is discard_pile_card
def eligible_cards(hand_cards,discard_pile_card):
    #all wild cards are automatically allowed
    eligible = [c for c in hand_cards if 'wild' in c]
    #check each card in hand_cards
    for c in hand_cards:
        #exclude all action cards and wild cards in this consideration
        if '_' not in c and 'wild' not in c:
            #if card is same colour as discard_pile_card
            if (c[0] == discard_pile_card[0] 
                #or same number
                or c[1] == discard_pile_card[1]):
                    #card is allowed to be played
                    eligible.append(c)
        #now just consider action cards
        elif 'wild' not in c:
            #only the colours need to be the same in this case
            if c[0] == discard_pile_card[0]:
                    #card is allowed to be played
                    eligible.append(c)
            #checking if card is same type of action card as discard_pile_card
            elif '_' in discard_pile_card:
                if str.split(c,'_')[-1] == str.split(
                                                    discard_pile_card,'_')[-1]:
                    #card is allowed to be played
                    eligible.append(c)
    return eligible

#this function finds all "+2" or "+4" cards in the list hand_cards that are 
#allowed to be played if the top of the discard pile is discard_pile_card and 
#discard_pile_card is a "+2" or "+4" card
def eligible_plus_cards(hand_cards,discard_pile_card):
    #if discard_pile_card is a "+2" or "+4" card
    if '+' in discard_pile_card:
        #if discard_pile_card is a "+2" then allowed cards are all "+2" cards;
        #similarly for "+4"
        eligible = [c for c in hand_cards if c[-2:] == discard_pile_card[-2:]]
    else: 
        #otherwise don't consider any to be allowed, any allowed cards will
        #already be included in the output of eligible_cards
        eligible = [] 
    return eligible

#this function returns the number of points a card is worth
def card_score(card):
    if 'wild' in card:
        return 50
    elif '_' in card:
        return 20
    elif len(card) == 2:
        return int(card[1])
    else:
        return 0

#this function returns the number of points the cards held by a player are 
#worth in total
def hand_score(hand_cards):
    return sum([card_score(c) for c in hand_cards])

#returns all normal cards from full_deck (with all cards from hand_cards removed) 
#where if that card was on the top the deck, at least one of the card from a
#player's hand hand_cards would be playable; a rough proxy for the probability
#that the player will be able to play one of their cards when it is next their
#turn 
def hand_cards_normal_domain(hand_cards,full_deck):
    full_deck_normal_cards = [dc for dc in full_deck if len(dc) == 2]
    domain_unique = []
    for hc in hand_cards:
        if 'wild' in hc:
            domain_unique += [dc for dc in full_deck_normal_cards]
        elif '_' in hc:
            domain_unique += [dc for dc in full_deck_normal_cards if 
                                                              dc[0] == hc[0]]
        elif hc != '':
            domain_unique += [dc for dc in full_deck_normal_cards if 
                                              dc[0] == hc[0] or dc[1] == hc[1]]
    domain_unique = set(domain_unique)
    domain = [c for c in full_deck if c in domain_unique]
    for c in hand_cards:
        if len(c) == 2:
            domain.remove(c)
    return domain
    
#
def count_hand_cards_of_type(hand_cards,type):
    if type == 'number':
        return len([c for c in hand_cards if len(c) == 2])
    if type == 'wild':
        return len([c for c in hand_cards if 'wild' in c and '+4' not in c])
    else:
        return len([c for c in hand_cards if type in c])
    
#
def count_distinct_numbers_or_actions_in_hand(hand_cards):
    number_cards = [c for c in hand_cards if len(c) == 2]
    action_cards = [c for c in hand_cards if len(str.split(c,'_')) == 2]
    unique_numbers = set([c[-1] for c in number_cards])
    unique_actions = set([str.split(c,'_')[-1] for c in action_cards])
    n_unique_numbers_or_actions = len(unique_numbers) + len(unique_actions)
    return n_unique_numbers_or_actions

#
def count_distinct_colours_in_hand(hand_cards):
    non_wild_cards = [c for c in hand_cards if 'wild' not in c]
    unique_colours = set([c[0] for c in non_wild_cards])
    return len(unique_colours)

#
def card_type(card):
    if card != '':
        if len(card) == 2 and card[-1] not in ['0','7']:
            return 'number'
        if '_' in card:
            return str.split(card,'_')[-1]
        if card[-1] in ['0','7']:
            return card[-1]
        if 'wild+4' in card:
            return 'wild+4'
        else:
            return 'wild'
    else:
        return 'None'
    
#
def delta(x,y):
    if x == y:
        return 1
    else:
        return 0
    
#
def card_type_is_type(card,type):
    return delta(card_type(card),type)

#
def m_players_later(direction_pre_play,player,N,m):
    return (player + m * direction_pre_play) % N

#returns number of cards held by the player whose turn it will be m turns later
#if the direction of play doesn't change e.g. with 5 players, player 2 as 
#current player and direction being anti-clockwise, 1 turn later will be player
#1, 2 turns later will be player 5
def m_players_later_n_cards(direction_pre_play,player,player_hands,m):
    m_players_later_player = (player + m * direction_pre_play) % len(
                                                                player_hands) 
    #print(m_players_later_player,'a')
    if m_players_later_player == 0:
        m_players_later_player += len(player_hands)
    #print(m_players_later_player,'b')
    return len(player_hands['player_' + str(m_players_later_player)])

#
def m_players_later_score(direction_pre_play,player,player_scores,m):
    m_players_later_player = (player + m * direction_pre_play) % len(
                                                                player_scores) 
    #print(m_players_later_player,'a')
    if m_players_later_player == 0:
        m_players_later_player += len(player_scores)
    #print(m_players_later_player,'b')
    return player_scores['player_' + str(m_players_later_player)]

