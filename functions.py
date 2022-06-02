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
