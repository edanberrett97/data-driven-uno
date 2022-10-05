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

all_columns = [
    'game',
    'round',
    'turn',
    'player',
    'previous_player_played_wild_plus_four',
    'challenge',
    'correct_challenge',
    #'wild_card_chosen_colour':[], #MAY INCLUDE THIS FEATURE LATER - AND MAYBE ALSO STUFF TO DO WITH DISCARD PILE TOP CARD
    'trade_player_relative_position',
    'player_current_score',
    'player_n_cards_pre_play',
    'player_n_cards_post_play',
    'player_n_cards_pre_card_play',
    'player_n_cards_post_card_play',
    'player_n_cards_pre_trade',
    'player_n_cards_post_trade',
]
for t in card_types:
    all_columns += [
        'player_n_' + t + '_cards_pre_play',
        'player_n_' + t + '_cards_post_play',
        'player_n_' + t + '_cards_pre_card_play',
        'player_n_' + t + '_cards_post_card_play',
        'player_n_' + t + '_cards_pre_trade'
    ]
all_columns += [
    'player_n_unique_numbers_or_actions_pre_play',
    'player_n_unique_numbers_or_actions_post_play',
    'player_n_unique_numbers_or_actions_pre_card_play',
    'player_n_unique_numbers_or_actions_post_card_play',
    'player_n_unique_numbers_or_actions_pre_trade',
    'player_n_unique_colours_pre_play',
    'player_n_unique_colours_post_play',
    'player_n_unique_colours_pre_card_play',
    'player_n_unique_colours_post_card_play',
    'player_n_unique_colours_pre_trade',
    'player_hand_score_pre_play',
    'player_hand_score_post_play',
    'player_hand_score_pre_card_play',
    'player_hand_score_post_card_play',
    'player_hand_score_pre_trade'
]
for t in card_types:
    all_columns.append('played_card_is_' + t)
for i in range(N_players - 1):
    all_columns += [
        str(i+1) + '_players_later_pre_play_n_cards', #SOLVED I THINK?>#MAYBE THIS SHOULD ACCOUNT FOR IF PREVIOUS PLAYER HAS PICKED UP ILLEGAL WILD+4 PENALTY CARDS
        str(i+1) + '_players_later_post_play_n_cards', 
        str(i+1) + '_players_later_pre_card_play_n_cards',
        str(i+1) + '_players_later_post_card_play_n_cards', 
        str(i+1) + '_players_later_n_cards_post_trade',
        str(i+1) + '_players_later_pre_play_current_score', 
        str(i+1) + '_players_later_post_play_current_score',
        str(i+1) + '_players_later_current_score_pre_trade',
        str(i+1) + '_players_later_current_score_post_trade'
    ]
all_columns.append('previous_player_won_play_from_state_game')

identifier_columns = [
        'game',
        'round',
        'turn',
        'player'
    ]

trade_model_X_columns = [
        'challenge',
        'trade_player_relative_position',
        #MAYBE SHOULD ADD PREVIOUS PLAYER PLAYED WILD PLUS FOUR?
        'player_n_cards_pre_trade',
        'player_n_cards_post_trade',
        'player_current_score',
    ]
for t in card_types:
    trade_model_X_columns.append('player_n_' + t + '_cards_pre_trade')
trade_model_X_columns += [
        'player_n_unique_numbers_or_actions_pre_trade',
        'player_n_unique_colours_pre_trade',
        'player_hand_score_pre_trade'
    ]
for i in range(N_players - 1):
    trade_model_X_columns.append(
                                str(i+1) + '_players_later_n_cards_post_trade')
    trade_model_X_columns.append(
                        str(i+1) + '_players_later_current_score_post_trade')
    
#
play_non_zero_card_model_X_columns = [
        'challenge',
        'player_n_cards_post_play',
        'player_current_score',
    ]
for t in card_types:
    play_non_zero_card_model_X_columns.append(
                                        'player_n_' + t + '_cards_post_play')
play_non_zero_card_model_X_columns += [
        'player_n_unique_numbers_or_actions_post_play',
        'player_n_unique_colours_post_play',
        'player_hand_score_post_play'
    ]
for i in range(N_players - 1):
    play_non_zero_card_model_X_columns.append(
                                str(i+1) + '_players_later_n_cards_post_play')
    play_non_zero_card_model_X_columns.append(
                        str(i+1) + '_players_later_current_score_post_play')
    
play_zero_card_model_X_columns = [
        'challenge',
        'player_n_cards_pre_play',
        'player_current_score',
    ]
for t in card_types:
    play_card_model_X_columns.append('player_n_' + t + '_cards_pre_play')
play_card_model_X_columns += [
        'player_n_unique_numbers_or_actions_pre_play',
        'player_n_unique_colours_pre_play',
        'player_hand_score_pre_play'
    ]
for i in range(N_players - 1):
    play_card_model_X_columns.append(
                                str(i+1) + '_players_later_n_cards_post_trade')
    play_card_model_X_columns.append(
                        str(i+1) + '_players_later_current_score_post_trade')
    