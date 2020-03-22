from pprint import pprint


class Human:
	def __init__(self, mark):
		self.mark = mark

	def get_move(self, field):
		moves = field.get_available_moves()
		pprint(field.get_board())
		print(field.get_macroboard())
		print("Player "+self.mark+", choose any of the available moves (0-"+str(len(moves)-1)+") or pass:\n")
		print(moves)
		mv = input()
		try:
			return moves[int(mv)]
		# catch non integer and out of range inputs
		except (ValueError, IndexError):
			return None