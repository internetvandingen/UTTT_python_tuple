import numpy as np

# DEBUG
# from pprint import pprint


# Field class:
# 	board, total (9x9)
# 	microboard, one of 9 smaller 3x3 boards
# 	macroboard. the 3x3 board containing the status of all 9 microboards

# move is a tuple of coordinates (x,y)
class Field:
	# integer representations of different type of states a cell can be in (used in transformation functions)
	_markX = 1
	_markO = 2
	_draw = 8
	_empty = 0
	_available = 9
	


	def __init__(self):
		# initialize for _empty board, all cells in macroboard are available.
		self.board = ((self._empty,)*9,)*9
		self.macroboard = ((self._available,)*3,)*3
		self.heuristics = ((0,)*3,)*3

	def parse_move(self, mark, move, transform = False):
		if mark=='X':
			markint = self._markX
		elif mark=='O':
			markint = self._markO
		else:
			raise Exception("Wrong mark given: "+mark+" should be 'X' or 'O'.")


		move_x, move_y = move

		# check if move is valid (in right microboard and cell should be empty)
		if (self.is_in_active_microboard(move_x, move_y) and self.board[move_x][move_y] == self._empty):
			# update board
			updated_row = self.board[move_x][:move_y] + (markint,) + self.board[move_x][move_y+1:]
			self.board = self.board[:move_x] + (updated_row,) + self.board[move_x+1:]

			
			# update macroboard
			changed_index = (move_x//3, move_y//3)
			next_move_index = (move_x%3, move_y%3)
			
			macroboard_changed = self.get_winner(self._get_microboard(changed_index))
			if macroboard_changed == None:
				macroboard_changed = self._empty
			else:
				# TRANSFORM
				if transform:
					# microboard is over, so fill it with (empty or corresponding) cells
					def get_tuple():
						for i in range(9):
							if i//3 == changed_index[0]:
								yield self.board[i][:changed_index[1]*3] + (macroboard_changed,)*3 + self.board[i][(changed_index[1]*3+3):]
							else:
								yield self.board[i]

					self.board = tuple(get_tuple())
				# TRANSFORM


			if next_move_index == changed_index:
				macroboard_next_move = macroboard_changed
			else:
				macroboard_next_move = self.macroboard[next_move_index[0]][next_move_index[1]]

			if macroboard_next_move in (self._empty, self._available):
				# replace mb_next_move with _mb_available
				macroboard_next_move = self._available
				# replace other values with _mb_unfinished or actual value
				replace_value = self._empty
			else:
				# mb_next_move is occupied, leave it as is
				# macroboard_next_move = macroboard_next_move
				# replace other values with _mb_available or actual value
				replace_value = self._available
			
			def get_tuples(i, j, replace_value):
				if (i,j) == next_move_index:
					return macroboard_next_move
				tocheck = macroboard_changed if (i,j)==changed_index else self.macroboard[i][j]
				if tocheck in (self._available, self._empty):
					return replace_value
				else:
					return tocheck

			self.macroboard = tuple(tuple(get_tuples(i, j, replace_value) for j in range(3)) for i in range(3))

			# TRANSFORM
			if transform:
				# after all is done, we rearrange the board
				self.rearrange(changed_index)
			# TRANSFORM

		else:
			raise Exception("Player "+mark+" tried to play an invalid move: "+str(x)+","+str(y))

	# ---------------------------------------------- TRANSFORM ----------------------------------------------
	def rearrange(self, index):
		# DEBUG
		# print('board before transformation:')
		# pprint(self.board)

		# If microboard is not finished yet, transform it
		if (self.macroboard[index[0]][index[1]] in (self._empty, self._available)):
			microboard = self._get_microboard(index)
			transformf = self.transform_board(microboard)
			if transformf != None:
				transformed_microboard = transformf(microboard)
				def get_tuple():
					for k in range(9):
						if k//3 == index[0]:
							yield self.board[k][:index[1]*3] + transformed_microboard[k%3] + self.board[k][(index[1]*3+3):]
						else:
							yield self.board[k]
				self.board = tuple(get_tuple())

		# DEBUG
		# print('board after microboard transformation')
		# pprint(self.board)

		# Get transform function board from heuristics
		def get_tuple():
			for i in range(3):
				if i == index[0]:
					yield self.heuristics[i][:index[1]] + (self.get_microboard_heuristic(self._get_microboard((i, index[1]))), ) + self.heuristics[i][index[1]+1:]
				else:
					yield self.heuristics[i]
		self.heuristics = tuple(get_tuple())

		transformf = self.transform_board(self.heuristics)

		# transform board and macroboard
		if transformf != None:
			self.macroboard = transformf(self.macroboard)

			# keep track of original positions of microboards
			original = (((0,0), (0,1), (0,2)),  ((1,0), (1,1), (1,2)),  ((2,0), (2,1), (2,2)))
			original = transformf(original)

			def get_tuples(x):
				rows = ()
				for y in range(3):
					rows += tuple(zip(*self._get_microboard(original[x][y])))
				return self.flipurdl(rows)

			newboard = ()
			
			for x in range(3):
				newboard += tuple(get_tuples(x))
			self.board = newboard
		# DEBUG
		#	print('transformation function: ', transformf.__name__)
		# 	print('resultaat:')
		# 	print('board after transformation:')
		# 	pprint(self.board)
		# else:
		# 	print('no transformation')

	def transform_board(self, board):
		# checks which transformation has the highest score and returns this function
		# calculate current score of board
		best_score = sum(self.get_score(board))
		best_i = 7

		functions = [self.rot90, self.rot180, self.rot270, self.fliplr, self.flipud, self.flipuldr, self.flipurdl, None]
		for i in range(7):
			new = sum(self.get_score(functions[i](board)))
			if (new > best_score):
				best_score = new
				best_i = i

		# if original state isnt the best, return the best transformation
		return functions[best_i]

	def get_score(self, m):
		# returns score that is unique for this transformation, given no symmetry
		n = len(m)
		for i in range(n):
			for j in range(n):
				yield m[i][j]*(i+1)**3*j**3

	def get_microboard_heuristic(self, m):
		# returns heuristic of microboard that is independent of any of the 8 transformations
		# 3 for middle, 5 for corners and 7 for edges
		total = 0
		for coord in [(0,0),(2,0),(0,2),(2,2)]:
			total += m[coord[0]][coord[1]]*5
		for coord in [(0,1),(1,0),(1,2),(2,1)]:
			total += m[coord[0]][coord[1]]*7
		total += m[1][1]*3
		return total

	# # transformation functions, all return a copy
	def rot90(self, m):
		return tuple(reversed(tuple(zip(*m))))
	def rot180(self, m):
		return self.rot90(self.rot90(m))
	def rot270(self, m):
		return tuple(zip(*reversed(m)))
	def flipud(self, m):
		return tuple(reversed(m))
	def flipurdl(self, m):
		return tuple(zip(*m))
	def flipuldr(self, m):
		return self.flipud(self.rot270(m))
	def fliplr(self, m):
		return self.rot270(self.flipurdl(m))

	
	# ---------------------------------------------- TRANSFORM ----------------------------------------------

	def _get_microboard(self, pos):
		# returns copy of microboard selected by pos = (0-2, 0-2)
		def get_tuples():
			for x in range(pos[0]*3, pos[0]*3+3):
				yield self.board[x][pos[1]*3:(pos[1]*3+3)]

		return tuple(get_tuples())

	def get_winner(self, microboard):
		# determines winner for 3x3 tuple
		# check rows
		for x in range(3):
			if self._has_3_in_a_line(microboard[x]):
				return microboard[x][0]
		# check columns
		for y in range(3):
			if self._has_3_in_a_line([i[y] for i in microboard]):
				return microboard[0][y]

		# check diagonals
		if self._has_3_in_a_line([microboard[i][i] for i in range(3)]):
			return microboard[0][0]
		if self._has_3_in_a_line([microboard[2 - i][i] for i in range(3)]	):
			return microboard[0][2]

		# draw
		if self._is_full(microboard):
			return self._draw

		# otherwise, unfinished
		return None

	def _has_3_in_a_line(self, line):
		return all(x == self._markO for x in line) | all(x == self._markX for x in line)

	def _is_full(self, microboard):
		return not(any(self._available in row or self._empty in row for row in microboard))

	def get_available_moves(self):
		moves = []
		for y in range(9):
			for x in range(9):
				if (self.is_in_active_microboard(x,y) and (self.board[x][y] == self._empty)):
					moves.append((x,y))
		return moves

	def is_in_active_microboard(self, x, y):
		if self.macroboard[x//3][y//3] == self._available:
			return True
		else:
			return False

	def get_board(self):
		return self.board

	def get_macroboard(self):
		return self.macroboard