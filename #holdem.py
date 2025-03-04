#personal project to create a version of texas hold'em
#steps/outline
#1) create a deck of card and shuffle
#2)create a list for rank of hands
#3)create a list for possible hand combination
#-- create bank
#4)make interval small blind if possible
#5)deal 2 cards from deck for player/cpu
#6)prompt for 'fold','call','raise','bet' deal flop
#7)add the turn card
#8)prompt for 'fold','raise','check'
#9)add the river card
#10)check for winner
#11)update bank

suits= ('hearts','diamonds','spades','clubs')

ranks=( 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values={'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}

from collections import Counter
import random

playing = True
bblind = True
dturn = True
driver= True

#Royal flush-A, K, Q, J, 10, all the same suit.
#2. Straight flush-Five cards in a sequence, all in the same suit.8 7 6 5 4
#3. Four of a kind-All four cards of the same rank.J J J J 7
#4. Full house-Three of a kind(same rank) with a pair(same rank).T T T 9 9
#5. Flush-Any five cards of the same suit, but not in a sequence.
#6. Straight - Five cards in a sequence, but not of the same suit.
#7. Three of a kind-Three cards (same rank)
#8. Two pair - Two different pairs(same rank).
#9. Pair - same rank
#10. High Card- highest ranking card

#----------------------------------
#creating list for rank of hands
def check_for_hand():
	pair=count(card)

import random
#---------------------------------
# create a class for card
class Card():
	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank
		
	def __str__(self):
		template= f'\t{self.rank} - {self.suit}'
		return template
		
#---------------------------------
#create a class for deck
class Deck():
	def __init__(self):
		self.cards = []
		for rank in ranks:
			for suit in suits:
				self.cards.append(Card(suit,rank))
		
	def __str__(self):
		comp = ' '
		for x in self.cards:
			comp += '\n ' + x.__str__()
		return comp
		
	def shuffle(self):
		random.shuffle(self.cards)
		
	def deal(self):
		single_card = self.cards.pop()
		return single_card
		
#create an hand object for each players hand
class Hand:
	
	def __init__(self):
		self.cards = []  # start with an empty list
		self.value = []   # start with empty list
		self.the_suits=[]
		self.aces = 0    # keep track of aces
    
	def add_card(self,card):
			
		self.cards.append(card)
		self.value.append(values[card.rank])
		self.the_suits.append(card.suit)
		
		if card.rank == 'Ace':
			self.aces += 1
			
	def __str__(self):
		comp = ' '
		for card in self.cards:
			comp += ' \n' +card.__str__()
		return comp
		
	def adjust_for_ace(self):
		
			while self.aces:
				self.aces -=1
#-----------------------------
#chips class
class Chips:
	
	def __init__(self):
		self.total = 250  # can be def or user input
		self.bet = 0
		self.small=10
        
	def add_small(self):
		self.total -=self.small
		
	def call(self):
		self.total -=self.small
		
	def win_bet(self,pot):
		value = pot.total_pot()
		self.total += value
    
	'''def lose_bet(self):
		self.total'''
		
#-----------------------------
#create the pot
class Pot():
	def __init__(self):
		self.small = 0
		self.bet = 0
		self.total = 0
		self.raised=0
		self.call_blind=0
		
	def total_pot(self):
		self.total =(self.small*2)+ self.small +self.call_blind+(self.bet*2)
		return self.total
		
	def __str__(self):
		return "pot: ",self.total
		
#----------------------------------
#take small bet
def small_bet(chips,pot):
	global playing
	#if who == 'cpu':
		#pot.small += chips.small
	#else:
		#pass
	if chips.small > chips.total:
		print(f'not enough chips. Total chips is : {chips.total}')
		playing = False
	else:
		chips.add_small()
		pot.small += chips.small
		#call function to deal 2 cards each
		print(f'player played small blind: {chips.small} chips')
		print(f'Big blind is 20 chips')
		deal_two(player_hand,house_hand,deck)
		hide_house(player_hand)
		
#---------------------------------
#function to deal 2 cards each
def deal_two(player_hand,house_hand,deck):
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())
	
	house_hand.add_card(deck.deal())
	house_hand.add_card(deck.deal())
	
#-----------------------
def hide_house(player):
	print('\n Player Hand:')
	for cards in player.cards:
		print(' ',cards)
		
	print('\n House Hand:')
	print('\t <Hidden Card>')
	print('\t <Hidden Card>')
	
#--------------------------------
def unhide_house(player,house):
	print('\n Player Hand:')
	for cards in player.cards:
		print('\t ',cards)
	
	print('\n House Hand:')
	for cards in house.cards:
		print('\t ',cards)
	print('\n')
#--------------------------------

# function to deal the flop
def deal_flop(table,deck):
	table.add_card(deck.deal())
	table.add_card(deck.deal())
	table.add_card(deck.deal())
	print('\n')
	print(f'\t  POT ==> {pot.total_pot()}  chips')
	print("flop: ",table)
	
#function to deal the turn and later river
def deal_turn(table,deck):
	table.add_card(deck.deal())
	
#---------------------------------
#func to prompt player to fold or call big blind
def big_blind(chips,pot):
	global playing
	global bblind
	while True:
		try:
			ask = input("\nFold or Call big blind. f/c: ")
		except:
			print("must be an alphabet!")
		else:
			if ask.lower() == 'f':
				playing = False
			elif ask.lower()=='c':
				if chips.small > chips.total:
					print('Not enough chips')
					playing = False
				else:
					chips.call()
					pot.call_blind +=chips.small
					deal_flop(table,deck)
					playing = True
					bblind=False
				break
			else:
				print('incorrect answer!!?')
				continue
			break

#-------------------------------
#func to prompt user to fold, check, raise or bet
def call_to_action(chips,pot):
	global playing
	global dturn
	while True:
		try:
			ask = input('(Fold) (Check) (Bet):  f/c/b: ')
		except:
			print('wrong answer selected')
		else:
			if ask.lower()=='f':
				playing = False
			elif ask.lower()=='c':
				deal_turn(table,deck)
				playing=True
				dturn=False
				break
			elif ask.lower()=='b':
				take_bet(chips,pot)
				deal_turn(table,deck)
				playing=True
				dturn=False
				break
			else:
				print('still no better answer?')
				continue
			break

#to take a bet from player
def take_bet(chips,pot):
	yeah = True
	while True:
		try:
			c = int(input('place your bet : '))
		except:
			print('must be an integer')
		else:
			if c > chips.total:
				print(f'not enough funds. Total: {chips.total} chips')
			else:
				chips.bet +=c
				chips.total-=c
				pot.bet += c
				break

#------------------------------
#implementing ranks of hand

#function to check straight
def straight(value_counter):
	t=0
	y=1
	z=5
	result = ' '
	
	val =list(value_counter)
	val.sort(reverse=True)
	if val[0]==14  and val[1] !=13:
		val.pop(0)
		val.append(1)
		
	while z<len(val):
		check=[val[t]-val[x] for x in range(y,z)]
		if check[-1] == 4:
			result='Straight'
			break
		else:
			t+=1
			y+=1
			z+=1
			result ='others'
	return result

#function to check for high card
def high_card(list_value):
	list_value.sort(reverse=True)
	high = list_value[0]
	second=list_value[1]
	third=list_value[2]
	fourth=list_value[3]
	fifth=list_value[4]
	return high,second,third,fourth,fifth

def check_flush(most_suit,list_value,list_suit):
	nsuit,ntimes=most_suit[0]
	result=' '
	t=0
	y=1
	z=5
	
	if ntimes>=5:
		match=[list_value[x] for x in range(len(list_value)) if list_suit[x] ==nsuit]
		
		match.sort(reverse=True)
		print(match)
		print(nsuit)
		val = match.copy()
		
		#check for royal flush
		if match[0] == 14 and match[1] ==13 and match[2] ==12 and match[3] ==11 and match[4] == 10:
			result='Royal flush'
		
		#check for straight flush
		elif ntimes>5:
			if match[0] == 14:
				val.remove(14)
				val.append(1)
					
				while z<=len(val):
					check=[]
					for i in range(y,z):
						check.append(val[t]-val[i])
					if check[-1] == 4:
						result='Straight flush'
						break
					else:
						t+=1
						y+=1
						z+=1	
			else:
				while z<=len(val):
					check=[]
					for i in range(y,z):
						check.append(val[t]-val[i])
					if check[-1] == 4:
						result='Straight flush'
						break
					else:
						t+=1
						y+=1
						z+=1
						
		elif match[0] - match[1] == 1 and match[1] - match[2] ==1 and match[2] - match[3] ==1 and match[3] - match[4] ==1:
			result='Straight flush'
			
		#check for flush
		else:
			result='Flush'
		return result

#check for multiple ranks
def check_rank(most_value):
	h=[]	#no. of times it occurs
	result =' '
	for x,y in most_value:
		h.append(y)
	
	#4 of a kind
	if h[0] ==4:
		result='Four of kind'
		
	#full house
	elif h[0] == h[1]==3:
		result='Full house'
	elif h[0] == 3 and h[1] == h[2] ==2:
		result='Full house'
	elif h[0] == 3 and h[1] ==2:
		result='Full house'
		
	#three of kind
	elif h[0] ==3:
		result='Three of kind'
		
	#2 pairs
	elif h[0] ==h[1]==h[2]==2:
		result='Two pairs'
	elif h[0] ==  h[1] == 2:
		result='Two pairs'
		
	#pair
	elif h[0] ==2:
		result = 'Pair'
		
	else:
		result='others'
	return result

#------------------------------
#------------------------------
#check for a pair
def check_pair(counter):
	g=[]	#value
	most_value=counter.most_common()
	for x,y in most_value:
		g.append(x)
	
	high = g[0]
	g.pop(0)
	g.sort(reverse=True)
	first=g[0]
	second=g[1]
	third=g[2]
	return high,first,second,third

#check for 2 pairs
def two_pairs(counter):
	g=[]	#card rank
	h=[]	#no. of times it occurs
	pairs=[]
	high=0
	second=0
	low=0
	most_value =counter.most_common()
	for x,y in most_value:
		g.append(x)
		h.append(y)
	'''check if we have 3 pairs add them to a new list (pairs) sort in descending order, pick the first 2 highest pairs and remove from original list(g). then sort the remaining card ranks in list(g) in descending order. pick the highest card and return to make the 5th card as high card.'''
	if h[0] ==h[1]==h[2]==2:
		pairs.append(g[0])
		pairs.append(g[1])
		pairs.append(g[2])
		pairs.sort(reverse=True)
		high=pairs.pop(0)
		second=pairs.pop(0)
		g.remove(high)
		g.remove(second)
		g.sort()
		low=g[-1]
		''' if their are only 2 pairs, add the 2 cards to a new list (two) and sort to pick the highest rank. then remove the 2 cards from original list(g) and sort (g). pick the highest card to make the 5th card.'''
	else:
		two=[]
		two.append(g[0])
		two.append(g[1])
		two.sort()
		high =two.pop()
		second=two.pop()
		g.remove(high)
		g.remove(second)
		g.sort()
		low=g[-1]
	return high,second,low

#check for 3 of a kind
def three_of_kind(counter):
	g=[]	#value
	most_value=counter.most_common()
	for x,y in most_value:
		g.append(x)
	high =g[0]
	g.pop(0)
	g.sort(reverse=True)
	first=g[0]
	second=g[1]
	return high,first,second

#check for straight
def check_straight(counter):
	high = 0
	t=0
	y=1
	z=5
	first=0
	second=0
	third=0
	fourth=0
	val =list(counter)
	val.sort(reverse=True)
	if val[0] ==14 and val[1] !=13 or val[1]==13 and val[2]!=12:
		val.remove(14)
		val.append(1)
		
		while z<len(val):
			check=[val[t] - val[x] for x in range(y,z)]
			if check[-1] == 4:
				high =val[t]
				first=val[t+1]
				second=val[t+2]
				third=val[t+3]
				fourth=val[t+4]
				break
			else:
				t+=1
				y+=1
				z+=1
		
	elif val[0]==14 and val[1]==13 and val[2]==12 and val[3]==11 and val[4]==10:
		high =14
		first=13
		second=12
		third=11
		fourth=10
	else:
		print('not straight')
	return high,first,second,third,fourth

#check for flush
def flush(most_suit,list_val,list_suit):
	nsuit,ntimes=most_suit[0]

	m=[list_val[x] for x in range(len(list_val)) if list_suit[x] ==nsuit]
	
	m.sort(reverse=True)
	high=m[0]
	first=m[1]
	second=m[2]
	third=m[3]
	fourth=m[4]
	return high,first,second,third,fourth,nsuit

#check draw for 4 of a kind
def four_of_kind(counter):
	most=counter.most_common()
	val=[]
	times=[]
	for x,y in most:
		val.append(x)
		times.append(y)
	big=val.pop(0)
	val.sort()
	return big,val[-1]

#check for full house
def full_house(most_val):
	val=[]
	times=[]
	big=0
	second=0
	for x,y in most_val:
		val.append(x)
		times.append(y)
	if times[0] == times[1]:
		if val[0] > val[1]:
			big = val[0]
			second=val[1]
		else:
			big =val[1]
			second=val[0]
	else:
		big=val.pop(0)
		if times[1] == times[2]:
			if val[0] > val[1]:
				second=val[0]
			else:
				second=val[1]
		else:
			second=val[0]
	return big,second

#check for straight flush
def straight_flush(most_suit,list_val,list_suit):
	nsuit,ntimes=most_suit[0]
	t=0
	y=1
	z=5
	high=0
	first=0
	second=0
	third=0
	fourth=0
	match=[list_value[x] for x in range(len(list_val)) if list_suit[x] ==nsuit]
	match.sort(reverse=True)
	
	val = match.copy()
	#check for straight flush
	if ntimes>5:
		if match[0] == 14:
			val.remove(14)
			val.append(1)
			print(val)
			while z<=len(val):
				check=[val[t]-val[x] for x in range(y,z)]
				if check[-1] == 4:
					high=val[t]
					first=val[t+1]
					second=val[t+2]
					third=val[t+3]
					fourth=val[t+4]
					break
				else:
					t+=1
					y+=1
					z+=1	
		else:
			while z<=len(val):
				check=[val[t]-val[x] for x in range(y,z)]
				if check[-1] == 4:
					high=match[t]
					first=match[t+1]
					second=match[t+2]
					third=match[t+3]
					fourth=match[t+4]
					break
				else:
					t+=1
					y+=1
					z+=1
						
	else:
		if match[0] - match[1] == 1 and match[1] - match[2] ==1 and match[2] - match[3] ==1 and match[3] - match[4] ==1:
			
			high=match[0]
			first=match[1]
			second=match[2]
			third=match[3]
			fourth=match[4]
	return high,first,second,third,fourth,nsuit
#------------------------------	
#------------------------------

def whos_turn(player,house):
	who=' '
	if turn == True:
		who = 'user'
	else:
		who = 'cpu'
	return who

#-------------------------------
def player_wins(pot,chips):
	chips.win_bet(pot)
	print(f'Chips total: {chips.total}')
	
def player_lose(chips):
	print(f'Chips total: {chips.total} ')
	
#implement the chips class here
chips = Chips()

house_check =0
player_check=0

while True:
	print('\n '*50)
	#print welcome message here
	bold="TEXAS HOLD'EM POKER"
	a="welcome to a game of holdem poker"
	b=f"Player starts with 250 chips! left: {chips.total}"
	c="you will be playing against the CPU. Good Luck!!"
	print(bold.center(len(c)+12,' '))
	print(a.center(len(c)+12,' '))
	print(b.center(len(c)+12,' '))
	print(c.center(len(c)+12,' '))
	print('\n')
	#-----end of welcome message-----
	
	card = Card('cb','2')
	deck = Deck()
	deck.shuffle()
	pot = Pot()
	
	player_hand= Hand()
	house_hand= Hand()
	table=Hand()
	small_bet(chips,pot)
	if playing == False:
		break
	while playing:
		big_blind(chips,pot)
		if playing ==False:
			print('\nPlayer Folds!')
			break
		else:
			call_to_action(chips,pot)
			print('\n')
			print(f'\t  POT ==> {pot.total_pot()} chips')
			print(table)
			if playing == False:
				print('\nPlayer Folds!')
				player_lose(chips)
				break
			else:
				call_to_action(chips,pot)
				print('\n'*100)
				print(f'\t  POT ==> {pot.total_pot()} chips')
				print(table)
				unhide_house(player_hand,house_hand)
				if playing ==False:
					print('\nPlayer Folds!')
					player_lose(chips)
					break
		
		#for player
		for_table=table.value
		for_player=player_hand.value
		for_player.extend(for_table)
		still_player =player_hand.the_suits
		still_table =table.the_suits
		still_player.extend(still_table)
		
		player_val = Counter(for_player)
		player_suit=Counter(still_player)
		most_val_player=player_val.most_common(3)
		most_suit_player=player_suit.most_common(1)
		
		for_dct =zip(for_player,still_player)
		for_dct = list(for_dct)
		#print(for_dct)
		
		#----------------------------
		#values and suit returned after game play
	
		#----------------------------
		#----------------------------
		#calling func for rankings
		flushed=check_flush(most_suit_player,for_player,still_player)
		ranked=check_rank(most_val_player)
		straighted=straight(player_val)
		a1,b1,c1,d1,e1 = high_card(for_player)
		
		#--------------------
		#check rank
		while True:
			if flushed == 'Royal flush':
				print('Player: best hand-- ROYAL FLUSH!!!')
				player_check =10
			elif flushed == 'Straight flush':
				print('Player: best hand --STRAIGHT FLUSH')
				player_check =9
			elif ranked == 'Four of kind':
				print('Player: best hand--FOUR OF A KIND!!!')
				player_check=8
			elif ranked == 'Full house':
				print('Player: best hand --FULL HOUSE!!')
				player_check =7
			elif flushed == 'Flush':
				print('Player: best hand --FLUSH!!')
				player_check=6
			elif straighted=='Straight':
				print('Player: best hand --STRAIGHT!')
				player_check=5
			elif ranked =='Three of kind':
				print('Player: best hand --THREE OF A KIND!!')
				player_check=4
			elif ranked =='Two pairs':
				print('Player: best hand --TWO PAIRS!!')
				player_check=3
			elif ranked =='Pair':
				print('Player: best hand --A PAIR!')
				player_check = 2
			else:
				print('Player: best hand --High Card!')
				player_check=1
			break
			
		#---------------------------
		#---------------------------
		#for cpu
		#for house
		for_table=table.value
		for_house=house_hand.value
		for_house.extend(for_table)
		still_house =house_hand.the_suits
		still_table =table.the_suits
		still_house.extend(still_table)
		
		house_val = Counter(for_house)
		house_suit=Counter(still_house)
		most_val_house=house_val.most_common(3)
		most_suit_house=house_suit.most_common(1)
		
		for_dct =zip(for_house,still_house)
		for_dct = list(for_dct)
	
		#----------------------------
		#----------------------------
		#calling func for rankings
		flushed=check_flush(most_suit_house,for_house,still_house)
		ranked=check_rank(most_val_house)
		straighted=straight(house_val)
		a2,b2,c2,d2,e2 = high_card(for_house)
		
		#--------------------
		#check rank
		while True:
			if flushed == 'Royal flush':
				print('House: best hand -- ROYAL FLUSH!!!')
				house_check=10
			elif flushed == 'Straight flush':
				print('House: best hand --STRAIGHT FLUSH')
				house_check=9
			elif ranked == 'Four of kind':
				print('House: best hand --FOUR OF A KIND!!!')
				house_check=8
			elif ranked == 'Full house':
				print('House: best hand --FULL HOUSE!!')
				house_check=7
			elif flushed == 'Flush':
				print('House: best hand --FLUSH!!')
				house_check =6
			elif straighted=='Straight':
				print('House: best hand --STRAIGHT!')
				house_check=5
			elif ranked =='Three of kind':
				print('House: best hand --THREE OF A KIND!!')
				house_check=4
			elif ranked =='Two pairs':
				print('House: best hand --TWO PAIRS!!')
				house_check=3
			elif ranked =='Pair':
				print('House: best hand --A PAIR!')
				house_check=2
			else:
				print('House: best hand --High Card!')
				house_check=1
			break
			
		#-------------------------
		#check for winner with checks
		if player_check > house_check:
			if player_check == 10:
				print('Player wins with Royal Flush!!')
			elif player_check==9:
				print('Player wins with Straight Flush!!')
			elif player_check == 8:
				print('Player wins with Four of a Kind!!')
			elif player_check == 7:
				print('Player wins with Full House!!')
			elif player_check == 6:
				print('Player wins with Flush!!')
			elif player_check == 5:
				print('Player wins with Straight!!')
			elif player_check == 4:
				print('Player wins with Three of a Kind!')
			elif player_check == 3:
				print('Player wins with Two Pairs!!')
			elif player_check == 2:
				print('Player wins with a Pair!!')
			else:
				print('Player wins with High Card')
			player_wins(pot,chips)
				
		elif player_check==house_check:
			if player_check ==10: #Royal flush
				print('We have a tie with Royal Flush')
			elif player_check ==9: #straight flush
				a1,b1,c1,d1,e1,s1= straight_flush( most_suit_player,for_player,still_player)
				a2,b2,c2,d2,e2,s2= straight_flush( most_suit_house,for_house,still_house)
				if a1==a2:
					if b1==b2:
						if c1==c2:
							print('We have a tie with Straight Flush')
						elif c1>c2:
							print('Player wins with Straight Flush!!')
							player_wins(pot,chips)
						else:
							print('House wins with Straight Flush!!')
							player_lose(chips)
					elif b1>b2:
						print('Player wins with Straight Flush!!')
						player_wins(pot,chips)
					else:
						print('House wins with Straight Flush')
						player_lose(chips)
				elif a1>a2:
					print('Player wins with Straight Flush')
					player_wins(pot,chips)
				else:
					print('House wins with Straight Flush')
					player_lose(chips)
			elif player_check==8: #Four of a kind
				b1,s1= four_of_kind(player_val)
				b2,s2= four_of_kind(house_val)
				if b1 ==b2:
					if s1 ==s2:
						print('We have a tie with Four of Kind')
					elif s1>s2:
						print('player wins with Four of kind')
						player_wins(pot,chips)
					else:
						print('House wins with Four of Kind')
						player_lose(chips)
				elif b1>b2:
					print('Player wins with Four of Kind')
					player_wins(pot,chips)
				else:
					print('House wins with Four of a Kind')
					player_lose(chips)
			elif player_check==7: #full house
				b1,s1 = full_house(most_val_player)
				b2,s2 =full_house(most_val_house)
				if b1 ==b2:
					if s1 ==s2:
						print('We have a tie with Full House')
					elif s1>s2:
						print('player wins with Full House')
						player_wins(pot,chips)
					else:
						print('House wins with Full House')
						player_lose(chips)
				elif b1>b2:
					print('Player wins with Full House')
					player_wins(pot,chips)
				else:
					print('House wins with Full House')
					player_lose(chips)
			elif player_check == 6: #flush
				a1,b1,c1,d1,e1,s1= flush(most_suit_player,for_player,still_player)
				a2,b2,c2,d2,e2,s2= flush(most_suit_house,for_house,still_house)
				if a1 ==a2:
					if b1 ==b2:
						if c1==c2:
							if d1==d2:
								if e1==e2:
									print('We have a tie with Flush')
								elif e1>e2:
									print('player wins with Flush')
									player_wins(pot,chips)
								else:
									print('House wins with Flush')
									player_lose(chips)
							elif d1>d2:
								print('Player wins with Flush')
								player_wins(pot,chips)
							else:
								print('House wins with Flush')
								player_lose(chips)
						elif c1>c2:
							print('Player wins with Flush')
							player_wins(pot,chips)
						else:
							print('House wins with Flush')
							player_lose(chips)
					elif b1>b2:
						print('Player wins with Flush')
						player_wins(pot,chips)
					else:
						print('House wins with Flush')
						player_lose(chips)
				elif a1>a2:
					print('Player wins with Flush')
					player_wins(pot,chips)
				else:
					print('House wins with Flush')
					player_lose(chips)
			elif player_check == 5: #Straight
				a1,b1,c1,d1,e1 = check_straight(player_val)
				a2,b2,c2,d2,e2 = check_straight(house_val)
				if a1 == a2:
					if b1==b2:
						if c1==c2:
							print('We have a tie with Straight')
						elif c1 > c2:
							print('Player wins with Straight')
							player_wins(pot,chips)
						else:
							print('House wins with Straight')
							player_lose(chips)
					elif b1 > b2:
						print('Player wins with Straight')
						player_wins(pot,chips)
					else:
						print('House wins with Straight')
						player_lose(chips)
				elif a1 > a2:
					print('Player wins with Straight')
					player_wins(pot,chips)
				else:
					print('House wins with Straight')
					player_lose(chips)
			elif player_check == 4: #Three of a kind
				a1,b1,c1 = three_of_kind(player_val)
				a2,b2,c2 = three_of_kind(house_val)
				if a1 ==a2:
					if b1 ==b2:
						if c1 ==c2:
							print('We have a tie with Three of Kind')
						elif c1>c2:
							print('player wins with Three of kind')
							player_wins(pot,chips)
						else:
							print('House wins with Three of Kind')
							player_lose(chips)
					elif b1>b2:
						print('Player wins with Three of Kind')
						player_wins(pot,chips)
					else:
						print('House wins with Three of a Kind')
						player_lose(chips)
				elif a1>a2:
					print('Player wins with Three of Kind')
					player_wins(pot,chips)
				else:
					print('House wins with Three of a Kind')
					player_lose(chips)
			elif player_check==3: #two pairs
				b1,s1,l1 = two_pairs(player_val)
				b2,s2,l2 = two_pairs(house_val)
				if b1 ==b2:
					if s1 ==s2:
						if l1==l2:
							print('We have a tie with Two Pairs')
						elif l1>l2:
							print('player wins with Two Pairs')
							player_wins(pot,chips)
						else:
							print('House wins with Two Pairs')
							player_lose(chips)
					elif s1>s2:
						print('Player wins with Two Pairs')
						player_wins(pot,chips)
					else:
						print('House wins with Two Pairs')
						player_lose(chips)
				elif b1>b2:
					print('Player wins with Two Pairs')
					player_wins(pot,chips)
				else:
					print('House wins with Two Pairs')
					player_lose(chips)
			elif player_check == 2: #a pair
				a1,b1,c1,d1 = check_pair(player_val)
				a2,b2,c2,d2 = check_pair(house_val)
				if a1 ==a2:
					if b1 ==b2:
						if c1==c2:
							if d1==d2:
								print('We have a tie with a Pair')
							elif d1>d2:
								print('player wins with a Pair')
								player_wins(pot,chips)
							else:
								print('House wins with a Pair')
								player_lose(chips)
						elif c1>c2:
							print('Player wins with a Pair')
							player_wins(pot,chips)
						else:
							print('House wins with a Pair')
							player_lose(chips)
					elif b1>b2:
						print('Player wins with a Pair')
						player_wins(pot,chips)
					else:
						print('House wins with a Pair')
						player_lose(chips)
				elif a1>a2:
					print('Player wins with a Pair')
					player_wins(pot,chips)
				else:
					print('House wins with a Pair')
					player_lose(chips)
			elif player_check==1:
				if a1 == a2:
					if b1 == b2:
						if c1 == c2:
							if d1==d2:
								if e1==e2:
									print('We have a tie with High Card')
								elif e1>e2:
									print('player wins with High Card')
									player_wins(pot,chips)
								else:
									print('House wins with High Card')
									player_lose(chips)
							elif d1>d2:
								print('Player wins with High Card')
								player_wins(pot,chips)
							else:
								print('House wins with High Card')
								player_lose(chips)
						elif c1>c2:
							print('Player wins with High Card')
							player_wins(pot,chips)
						else:
							print('House wins with High Card')
							player_lose(chips)
					elif b1>b2:
						print('Player wins with High Card')
						player_wins(pot,chips)
					else:
						print('House wins with High Card')
						player_lose(chips)
				elif a1>a2:
					print('Player wins with High Card')
					player_wins(pot,chips)
				else:
					print('House wins with High Card')
					player_lose(chips)
		else:
			if house_check == 10:
				print('House wins with Royal Flush!!')
			elif house_check==9:
				print('House wins with Straight Flush!!')
			elif house_check == 8:
				print('House wins with Four of a Kind!!')
			elif house_check == 7:
				print('House wins with Full House!!')
			elif house_check == 6:
				print('House wins with Flush!!')
			elif house_check == 5:
				print('House wins with Straight!!')
			elif house_check == 4:
				print('House wins with Three of a Kind!')
			elif house_check == 3:
				print('House wins with Two Pairs!!')
			elif house_check == 2:
				print('House wins with a Pair!!')
			else:
				print('House wins with High Card')
			player_lose(chips)
		break
	play_again = input("\n\t\t"+"play again? y/n: ")
	if play_again.lower() == 'y':
		playing=True
		continue
	else:
		break
