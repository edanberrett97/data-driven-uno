from functions import hand_cards_normal_domain
from functions import card_score
from play_game import N_players
from play_game import original_deck

#returns the number of cards in a player's playable cards having a certain 
#feature e.g. if their playable cards are 'wild,wild+4,r3' and the feature is
#'wild', 2 is the output
def player_possible_cards_count_features(x,feature):
    return x.count(feature)

#returns the number of cards in a player's playable cards that are normal cards
def player_possible_cards_n_normal_cards(x):
    return len([c for c in str.split(x,',') if len(c) == 2])

#returns the number of cards that every player individually holds
def all_players_n_cards(x):
    return ','.join([str(n) for n in x])

#returns the number of cards that every player except the current player
#individually holds
def all_other_players_n_cards(x):
    player = x[0]
    all_players_n_cards = str.split(x[1],',')
    return ','.join([all_players_n_cards[i] 
                     for i in range(len(all_players_n_cards)) 
                     if i+1 != player])

#returns either the minimum, maximum, or average of the number of cards 
#individually held by every player except the current player
def all_other_players_n_cards_statistics(x,statistic):
    all_other_players_n_cards = [int(n) for n in str.split(x,',')]
    if statistic == 'min':
        return min(all_other_players_n_cards)
    if statistic == 'max':
        return max(all_other_players_n_cards)
    if statistic == 'mean':
        return sum(all_other_players_n_cards)/len(all_other_players_n_cards)
    
#returns number of cards held by the player whose turn it will be m turns later
#if the direction of play doesn't change e.g. with 5 players, player 2 as 
#current player and direction being anti-clockwise, 1 turn later will be player
#1, 2 turns later will be player 5
def m_players_later_n_cards(x,m):
    direction_pre_play = x[0]
    player = x[1]
    all_players_n_cards = str.split(x[2],',')
    m_players_later_player = (player + m * direction_pre_play) % len(
                                                        all_players_n_cards) 
    if m_players_later_player == 0:
        m_players_later_player += N_players
    return all_players_n_cards[m_players_later_player - 1]

#a player's hand has a 'normal domain', which is determined by taking the full 
#original deck, removing the cards in the players hand from the original deck,
#then finding all of the normal cards in what remains where, if that card was on the top 
#of the discard pile, at least one card in the players hand would be playable 
#e.g. if the player holds just a y1, their hand's domain is ['r1', 'g1', 'b1',
#'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'r1', 'g1', 'b1', 'y1', 'y2', 
#'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'y0']; the player's hand's power is
#the size of it's domain
def hand_normal_power(x,full_deck):
    return len(hand_cards_normal_domain(str.split(x,','),full_deck))

#returns what a player's hand's power will
#be after playing a card, for each of their playable cards, then returns the 
#maximum of these
def max_possible_post_play_hand_normal_power(x):
    player_hand_pre_play = str.split(x[0],',')
    player_possible_cards = str.split(x[1],',')
    possible_post_play_hand_normal_powers = []
    if player_possible_cards != ['']:
        for c in player_possible_cards:
            player_possible_hand_post_play = player_hand_pre_play[:]
            player_possible_hand_post_play.remove(c)
            player_possible_hand_post_play_normal_power = len(
                hand_cards_normal_domain(player_possible_hand_post_play,
                                                  original_deck)
            )
            possible_post_play_hand_normal_powers.append(
                player_possible_hand_post_play_normal_power)
    if possible_post_play_hand_normal_powers != []:
        return max(possible_post_play_hand_normal_powers)
    else:
        return ''
    
#returns the number of points the cards held by a player are 
#worth in total
def hand_score(x):
    return sum([card_score(c) for c in str.split(x,',')])

##returns what a player's hand's score will
#be after playing a card, for each of their playable cards, then returns the 
#maximum of these
def min_possible_post_play_hand_score(x):
    player_hand_pre_play = str.split(x[0],',')
    player_possible_cards = str.split(x[1],',')
    possible_post_play_hand_scores = []
    if player_possible_cards != ['']:
        for c in player_possible_cards:
            player_possible_hand_post_play = player_hand_pre_play[:]
            player_possible_hand_post_play.remove(c)
            player_possible_hand_post_play = ','.join(
                                                player_possible_hand_post_play)
            player_possible_hand_post_play_score = hand_score(
                                                player_possible_hand_post_play)
            possible_post_play_hand_scores.append(
                                        player_possible_hand_post_play_score)
    if possible_post_play_hand_scores != []:
        return max(possible_post_play_hand_scores)
    else:
        return ''