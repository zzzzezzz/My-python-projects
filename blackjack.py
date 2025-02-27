import random

suits= ('Hearts','Diamonds','Spades','Clubs')
ranks=( 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values={'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
playing= True
still_playing=True


#create and instance of each type of card
class Card:
	
	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank
		
	def __str__(self):
		return self.rank+ " of " + self.suit
		

#create a deck to represent all 52 cards
class Deck:
	
	def __init__(self):
		self.deck = []  # start with an empty list
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank))
	
	def __str__(self):
		deck_comp = ' '
		
		for card in self.deck:
			deck_comp  += '\n ' + card.__str__()
		return 'the deck has: ' + deck_comp
			

	def shuffle(self):
		random.shuffle(self.deck)
        
	def deal(self):
		single_card = self.deck.pop()
		return single_card
		
#create an hand object for each players hand
class Hand:
	
	def __init__(self):
		self.cards = []  # start with an empty list
		self.value = 0   # start with zero value
		self.aces = 0    # keep track of aces
    
	def add_card(self,card):
			
		self.cards.append(card)
		self.value += values[card.rank]
		
		if card.rank == 'Ace':
			self.aces += 1
			
	def __str__(self):
		comp = ' '
		for card in self.cards:
			comp += '\n ' +card.__str__()
		return "the hand has : " + comp
		
	def adjust_for_ace(self):
		
			while self.value > 21 and self.aces:
				self.value -= 10
				self.aces -=1
				
#to keep track of chips
class Chips:
	
	def __init__(self):
		self.total = 100  # can be def or user input
		self.bet = 0
        
	def win_bet(self):
		self.total += self.bet
    
	def lose_bet(self):
		self.total -= self.bet
				
#func for taking player bet
def take_bet(chips):
	
	while True:
		
		try:
			chips.bet = abs(int(input('pls, enter your bet: ')))
		except :
			print('bet must be a non decimal num')
		else:
			if abs(chips.bet) > chips.total:
				print('cant exceed total: ',chips.total)
			
			else:
				break
			
#func to take a hit player/dealer
def hit(deck,hand):
	
	hand.add_card(deck.deal())
	hand.adjust_for_ace()
	
#prompt use to hit or stand
def hit_or_stand(deck,hand):
	
	global playing  # to control a while loop
	
	while True:
		
		player_choice = input('do you want to hit or stand. enter "h/s" ')
		
		if player_choice.lower()== 'h':
			hit(deck,hand)
			
		elif player_choice.lower()=='s':
			print('player stands! Dealer is playing')
			playing = False
			
		else:
			print('please type a correct choice')
			continue
		break

#show player/cpu hand with one cpu hidden
def show_some(player,dealer):
	#for dealer
	print("\n Dealer's hand")
	print("  <card hidden> ")
	print(' ', dealer.cards[1])
	
	print("\n Player's hand")
	for card in player.cards:
		print(' ', card)

#show all cards and value
def show_all(player,dealer):
    
    print("\n Dealer's hand")
    for card in dealer.cards:
    	print(' ',card)
    print(dealer.value)
    
    print("\n Player's hand")
    for card in player.cards:
    	print(' ', card)
    print(player.value)
    
    
#for end game situations
def player_busts(player,chips):
   
    chips.lose_bet()
    print('\nplayer Bust!')

def player_wins(player,dealer,chips):
	
    chips.win_bet()
    print('\nPlayer Wins!')

def dealer_busts(dealer,player,chips):
	
	chips.win_bet()
	print('\nDealer Bust!')
    
def dealer_wins(dealer,player,chips):
	
    chips.lose_bet()
    print('\nDealer Wins!')
    
def push(player,dealer):
	
	print('\nPUSH!')
    
    
#GAME PLAY!!!

#setup player chips
player_chips = Chips()

while True:
    # Print an opening statement
	print("\t welcome to blackjack")
	print("\t aim for a 21 to win")
	
    
    # Create & shuffle the deck, deal two cards to each player
	deck = Deck()
	deck.shuffle()
    
    #player instance
	player = Hand()
	player.add_card(deck.deal())
	player.add_card(deck.deal())
	
	#dealer instance
	dealer = Hand()
	dealer.add_card(deck.deal())
	dealer.add_card(deck.deal())

    # Set up the Player's chips
    
    # Prompt the Player for their bet
	take_bet(player_chips)
   
    # Show cards (but keep one dealer card hidden)
	show_some(player,dealer)
 
	while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
		hit_or_stand(deck,player)
        
        # Show cards (but keep one dealer card hidden)
		show_some(player,dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
		if player.value > 21:
			show_all(player,dealer)
			player_busts(player,player_chips)
			break
		

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    
	if player.value <= 21:
		
		while dealer.value <17:
			hit(deck,dealer)
			
	    # Show all cards
		show_all(player, dealer)
	    
	    # Run different winning scenarios
		#player wins
		if player.value <=21 and player.value > dealer.value:
			player_wins(player,dealer,player_chips)
		
		#dealer bust
		elif dealer.value > 21:
			dealer_busts(player,dealer,player_chips)
			
		#dealer wins
		elif dealer.value > player.value:
			dealer_wins(player,dealer,player_chips)
				
		#push
		else:
			push(player,dealer)
	    
	    # Inform Player of their chips total
	print(f"Total chips remaining: {player_chips.total}")
	
	if player_chips.total ==0:
		print('out of chips!!!')
		break
	    
	 # Ask to play again
	 	
	play_again = input("play again? y/n: ")
	if play_again.lower() == 'y':
		playing=True
		continue
	else:
		break
    

#d = Deck()
#d.shuffle()

#player = Hand()
#player.add_card(d.deal())
#player.add_card(d.deal())
#print(player)
#print(player.value)
