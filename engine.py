from util import *
import player_qbot as Q

class Engine:
	_markX = None
	_markO = None
	_draw = None

	def __init__(self, playerX, playerO):
		self.playerX = playerX
		self.playerO = playerO
		self.winner = None
		

	def run(self, train = False, transform = False):
		self.whos_turn = 'X'
		field = Field()

		# get integer representations of player marks
		self._markX = field._markX
		self._markO = field._markO
		self._draw = field._draw

		self.winner = None
		while(self.winner==None):
			if self.whos_turn=='X':
				move = self.playerX.get_move(field)
				if move == None:
					print("player X has passed")
					self.winner = self._markO
					break
				field.parse_move(self.whos_turn, move, transform)
				self.whos_turn='O'
			else:
				move = self.playerO.get_move(field)
				if move == None:
					print("player O has passed")
					self.winner = self._markX
					break
				field.parse_move(self.whos_turn, move, transform)
				self.whos_turn='X'
			self.winner = field.get_winner(field.get_macroboard())
			if train:
				# Q learning section, only works if playerX is class Qbot
				Q.Qbot.parse_reward(whos_turn = self.whos_turn, field = field, move = move, winner = self.get_result())




	def get_result(self):
		if (self.winner==self._markX):
			return 'X'
		elif (self.winner==self._markO):
			return 'O'
		elif (self.winner==self._draw):
			return 'D'
		else:
			return None

	def print_result(self):
		if self.winner == self._markX:
			w = 'win for player X'
		elif self.winner == self._markO:
			w = 'win for player O'
		elif self.winner == self._draw:
			w = 'draw'
		else:
			print("Game is not finished yet...")
		print("The game resulted in a "+w)