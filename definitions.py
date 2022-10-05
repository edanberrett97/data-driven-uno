#setting some parameters for the game
colours = ['r','g','b','y']
N = 9
N_duplicates = 1
N_zeros = 1
N_players = 3
start_cards_per_player = 2
N_wild = 1
N_action = 1
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

all_columns_places = [
    'game',
    'round',
    'turn',
    'player',
    'previous_player_played_wild_plus_four',
    'challenge-T,P',
    'correct_challenge',
    #'wild_card_chosen_colour':[], #MAY INCLUDE THIS FEATURE LATER - AND MAYBE ALSO STUFF TO DO WITH DISCARD PILE TOP CARD
    'trade_player_relative_position-T',
    'player_current_score-T,P',
    'player_n_cards_pre_play',
    'player_n_cards_post_play-P',
    'player_n_cards_pre_card_play',
    'player_n_cards_post_card_play',
    'player_n_cards_pre_trade-T',
    'player_n_cards_post_trade-T',
]
for t in card_types:
    all_columns_places += [
        'player_n_' + t + '_cards_pre_play',
        'player_n_' + t + '_cards_post_play',
        'player_n_' + t + '_cards_pre_card_play',
        'player_n_' + t + '_cards_post_card_play-P',
        'player_n_' + t + '_cards_pre_trade-T'
    ]
all_columns_places += [
    'player_n_unique_numbers_or_actions_pre_play',
    'player_n_unique_numbers_or_actions_post_play',
    'player_n_unique_numbers_or_actions_pre_card_play',
    'player_n_unique_numbers_or_actions_post_card_play-P',
    'player_n_unique_numbers_or_actions_pre_trade-T',
    'player_n_unique_colours_pre_play',
    'player_n_unique_colours_post_play',
    'player_n_unique_colours_pre_card_play',
    'player_n_unique_colours_post_card_play-P',
    'player_n_unique_colours_pre_trade-T',
    'player_hand_score_pre_play',
    'player_hand_score_post_play',
    'player_hand_score_pre_card_play',
    'player_hand_score_post_card_play-P',
    'player_hand_score_pre_trade-T'
]
for t in card_types:
    all_columns_places.append('played_card_is_' + t + '-P')
for i in range(N_players - 1):
    all_columns_places += [
        str(i+1) + '_players_later_pre_play_n_cards', #SOLVED I THINK?>#MAYBE THIS SHOULD ACCOUNT FOR IF PREVIOUS PLAYER HAS PICKED UP ILLEGAL WILD+4 PENALTY CARDS
        str(i+1) + '_players_later_post_play_n_cards-P', 
        str(i+1) + '_players_later_pre_card_play_n_cards',
        str(i+1) + '_players_later_post_card_play_n_cards', 
        str(i+1) + '_players_later_n_cards_post_trade-T',
        str(i+1) + '_players_later_pre_play_current_score', 
        str(i+1) + '_players_later_post_play_current_score-P',
        str(i+1) + '_players_later_pre_card_play_current_score', 
        str(i+1) + '_players_later_post_card_play_current_score',
        str(i+1) + '_players_later_current_score_post_trade-T'
    ]
all_columns_places.append('previous_player_won_play_from_state_game')

all_columns = [str.split(c,'-')[0] for c in all_columns_places]    
trade_model_X_columns = [str.split(c,'-')[0] 
                                     for c in all_columns_places if 'T' in c]
play_card_model_X_columns = [str.split(c,'-')[0] 
                                     for c in all_columns_places if 'P' in c]
