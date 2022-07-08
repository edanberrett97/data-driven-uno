from play_game import original_deck
from play_game import N_players
from dataframe_functions import player_possible_cards_count_features
from dataframe_functions import player_possible_cards_n_normal_cards
from dataframe_functions import all_players_n_cards
from dataframe_functions import all_other_players_n_cards
from dataframe_functions import all_other_players_n_cards_statistics
from dataframe_functions import m_players_later_n_cards
from dataframe_functions import max_possible_post_play_hand_normal_power
from dataframe_functions import hand_normal_power
from dataframe_functions import hand_score
from dataframe_functions import min_possible_post_play_hand_score

#EXPLAIN THIS FUNCTION
def features_useful_columns(df):
    
    count_feature_types = [
        'wild',
        'wild+4',
        'skip',
        'reverse',
        '+2',
    ]
        
    #to get the number of cards in the current player's playable cards having a 
    #certain feature e.g. if their playable cards are 'wild,wild+4,r3' and the 
    #feature is 'wild', 2 is the output
    for feature in count_feature_types:
        df['player_n_possible_' + feature + '_cards_pre_play'] = df[
            'player_possible_cards'].apply(lambda x:
                               player_possible_cards_count_features(x,feature))
           
    #to get the number of wild cards in the current player's playable cards 
    #that are not wild+4 cards
    df['player_n_possible_wild_(not_+4)_cards_pre_play'] = (
            df['player_n_possible_wild_cards_pre_play'] - 
            df['player_n_possible_wild+4_cards_pre_play']
        )
    
    #to get the number of cards in the current player's playable cards that are 
    #normal cards
    df['player_n_possible_normal_cards_pre_play'] = df[
        'player_possible_cards'].apply(
            lambda x:player_possible_cards_n_normal_cards(x))
    
    #to get the number of cards that every player individually holds
    players_n_cards_pre_play_columns = ['player_'+str(i+1)+'_n_cards_pre_play' 
                                                    for i in range(N_players)]
    df['all_players_n_cards_pre_play'] = df[
            players_n_cards_pre_play_columns].apply(all_players_n_cards,axis=1)
    
    #to get the number of cards that every player except the current player
    #individually holds        
    df['all_other_players_n_cards_pre_play'] = df[[
            'player',
            'all_players_n_cards_pre_play'
        ]].apply(all_other_players_n_cards,axis=1)
    
    #to get the minimum, maximum, and average (in separate columns) of the 
    #number of cards individually held by every player except the current 
    #player
    for s in ['min','max','mean']:
        df[s + '_all_other_players_n_cards_pre_play'] = df[
            'all_other_players_n_cards_pre_play'].apply(
                lambda x:all_other_players_n_cards_statistics(x,s))
    
    #to get, in separate columns for m in {1 to N_players - 1}, the number of 
    #cards held by the player whose turn it will be m turns later if the 
    #direction of play doesn't change e.g. with 5 players, player 2 as current 
    #player and direction being anti-clockwise, 1 turn later will be player 1, 
    #2 turns later will be player 5
    for i in range(N_players - 1): 
        df[str(i+1) + '_players_later_n_cards_pre_play'] = df[[
                'direction_pre_play',
                'player',
                'all_players_n_cards_pre_play'
            ]].apply(m_players_later_n_cards,m=i+1,axis=1)
        
    #a player's hand has a 'normal domain', which is determined by taking the 
    #full original deck, removing the cards in the players hand from the 
    #original deck, then finding all of the normal cards in what remains where, 
    #if that card was on the top of the discard pile, at least one card in the 
    #players hand would be playable e.g. if the player holds just a y1, their 
    #hand's domain is ['r1', 'g1', 'b1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 
    #'y8', 'y9', 'r1', 'g1', 'b1', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 
    #'y8', 'y9', 'y0']; the player's hand's power is the size of it's domain; 
    #this is to get the current player's hand's power post play
    df['player_hand_post_play_normal_power'] = df[
            'player_hand_post_play'
        ].apply(lambda x:hand_normal_power(x,original_deck))
    
    #to get, of what the current player's hand's power will
    #be after playing a card, for each of their playable cards, the maximum 
    #value
    df['player_max_possible_post_play_hand_normal_power'] = df[[
            'player_hand_pre_play',
            'player_possible_cards'
        ]].apply(max_possible_post_play_hand_normal_power,axis=1)
    
    #to get the number of points the cards held by the current player post play 
    #are worth in total
    df['player_hand_post_play_score'] = df[
            'player_hand_post_play'
        ].apply(lambda x:hand_score(x))
    
    #to get, of what the current player's hand's score will
    #be after playing a card, for each of their playable cards, the minimum 
    #value
    df['player_min_possible_post_play_hand_score'] = df[[
            'player_hand_pre_play',
            'player_possible_cards'
        ]].apply(min_possible_post_play_hand_score,axis=1)
    
    #all of the columns that will ultimately prove useful (MAYBE DEFINE 'USEFUL')
    interesting_columns = [
        'game',
        'turn',
        'direction_pre_play',
        'player',
        'player_n_cards_pre_play',
        'played_card',
        'challenge',
        'trade_player'
    ]
    interesting_columns += ['player_n_possible_' + feature + '_cards_pre_play'
                                            for feature in count_feature_types]
    interesting_columns += [
        'player_n_possible_wild_(not_+4)_cards_pre_play',
        'player_n_possible_normal_cards_pre_play'
    ]
    interesting_columns += [s + '_all_other_players_n_cards_pre_play' 
                                                for s in ['min','max','mean']] 
    interesting_columns +=  [str(i+1) + '_players_later_n_cards_pre_play'
                                                 for i in range(N_players - 1)]
    interesting_columns += [
        'player_hand_post_play_normal_power',
        'player_max_possible_post_play_hand_normal_power',
        'player_hand_post_play_score',
        'player_min_possible_post_play_hand_score'
    ]
                                 
    return df[interesting_columns]

