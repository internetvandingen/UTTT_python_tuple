import random

class Randombot:
	def __init__(self, mark):
		self.mark = mark

	def get_move(self, field):
		moves = field.get_available_moves()
		move = random.choice(moves)
		# print("Bot placed mark "+self.mark+" at "+str(move[0])+","+str(move[1]))
		return move