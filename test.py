import time
import sys
import numpy as np
from pprint import pprint
import pickletools

from util import *
import player_randombot as R
import player_human as H
import player_qbot as Q
import engine as E
import visualisation as vis


def test_functions():
	field = Field()

	def get_tuple():
		for i in range(9):
			yield tuple(i*9+j for j in range(9))

	field.board = tuple(get_tuple())

	print('board:')
	pprint(field.board)

	transformf = field.rot90

	original = (((0,0), (0,1), (0,2)),  ((1,0), (1,1), (1,2)),  ((2,0), (2,1), (2,2)))
	original = transformf(original)
	x = 0
	print('microboards:')
	pprint(field._get_microboard(original[x][0]))
	pprint(field._get_microboard(original[x][1]))
	pprint(field._get_microboard(original[x][2]))
	print('doel:')
	pprint(field.board[0:3])
	
	def get_tuples(x):
		rows = ()
		for y in range(3):
			rows += tuple(zip(*field._get_microboard(original[x][y])))
		return field.flipurdl(rows)
	
	newboard = ()
	print('resultaat:')
	for x in range(3):
		newboard += tuple(get_tuples(x))

	pprint(newboard)




	# if transformf != None:
	# 	print(transformf.__name__)
	# 	field.macroboard = transformf(field.macroboard)
	# 	# self.board = transformf(self.board)
	# 	# keep track of original positions of microboards
	# 	original = (((0,0), (0,1), (0,2)),  ((1,0), (1,1), (1,2)),  ((2,0), (2,1), (2,2)))
	# 	original = transformf(original)
	# 	print('transformation coordinates: ', original)
	# 	def get_tuples():
	# 		for x in range(3):
	# 			for i,j,k in (field._get_microboard(original[x][0]), field._get_microboard(original[x][1]), field._get_microboard(original[x][2])):
	# 				yield i+j+k
	# 	field.board = tuple(get_tuples())
	# 	print('board after transformation:')
	# 	pprint(field.board)
	# else:
	# 	print('no transformation')



	# b = ((1,2,3), (4,5,6), (7,8,9))
	# b = ((2, 1, 0), (2, 0, 0), (0, 0, 0))

	# print("None")
	# print(b)
	# print(field.get_score(b))
	# for i in [field.rot90, field.rot180, field.rot270, field.fliplr, field.flipud, field.flipuldr, field.flipurdl]:
	# 	print(i.__name__)
	# 	print(i(b))
		# print(tuple(field.get_score(i(b))))
	

	# field.board = ((1, 1, 1, 0, 2, 0, 1, 1, 1), (1, 1, 1, 1, 0, 1, 1, 1, 1), (1, 1, 1, 1, 0, 2, 1, 1, 1), (2, 2, 2, 1, 1, 1, 2, 2, 2), (2, 2, 2, 1, 1, 1, 2, 2, 2), (2, 2, 2, 1, 1, 1, 2, 2, 2), (1, 1, 2, 1, 0, 1, 1, 1, 1), (2, 2, 0, 0, 0, 0, 1, 1, 1), (0, 2, 2, 2, 2, 1, 1, 1, 1))
	# field.macroboard = ((1, 9, 1), (2, 1, 2), (9, 9, 1))
	# pprint(field.board)
	# print(field.macroboard)

	# field.rearrange()
	# pprint(field.board)
	# print(field.macroboard)

	# print(field._is_full(b))
	# print(field.get_winner(b))
	
	# x = 0
	# y = 4
	# i = x//3
	# j = y//3
	# field.parse_move('X',(x,y))
	# print(field._is_full(field.get_macroboard()))
	# print(field.get_winner(field.get_macroboard()))

	# pprint(field.is_in_active_microboard(6,2))
	# pprint(field.get_available_moves())
	


def test_qbot():
	field = Field()

	qbot = Q.Qbot('X')
	qbot.dump_dict()

	move = qbot.get_move(field)
	print('move: ', move)

	qbot.dump_dict()

def test_plot():
	vis.plot_last()


if __name__ == '__main__':
	# test_functions()

	test_plot()

	# test_qbot()

	# pX = H.Human('X')
	# pO = H.Human('O')
	# pX = R.Randombot('X')
	# pO = R.Randombot('O')
	# engine = E.Engine(pX,pO)
	# engine.run(transform = True)
	# engine.print_result()
	
	# pX = H.Human('X')
	# pX = Q.Qbot('X')
	# pO = Q.Qbot('O')
	# engine = E.Engine(pX, pO)
	# engine.run(train = True)
	# engine.print_result()

	# pO.dump_dict()