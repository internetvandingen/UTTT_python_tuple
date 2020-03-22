import time
import sys
import datetime
import numpy as np
import pickle
import json

from util import *
import player_randombot as R
import player_human as H
import player_qbot as Q
import engine as E
import visualisation as vis

def play_randbot_randbot(nr_games = 1):
	pX = R.Randombot('X')
	pO = R.Randombot('O')
	play_set_games(nr_games, pX, pO)

def play_randbot_human():
	# You play against the random bot
	pX = H.Human('X')
	pO = R.Randombot('O')
	engine = E.Engine(pX,pO)
	engine.run()
	engine.print_result()

def play_human_human():
	pX = H.Human('X')
	pO = H.Human('O')
	engine = Engine(pX,pO)
	engine.run()
	engine.print_result()

def play_set_games(nr_games, pX, pO, transform = False):
	# plays nr_games for pX against pO and prints the results
	results = []
	engine = E.Engine(pX,pO)

	start = time.time()
	for j in range(100):
		jst = time.time()
		for i in range(nr_games//100):
			engine.run(transform = transform)
			results.append(engine.get_result())
		jend = time.time()
		sys.stdout.write("\r%d%%, %d seconds remaining" % ((j+1), (99-j)*(jend-jst)))
		sys.stdout.flush()
	
	end = time.time()
	print("\n"+str(len(results))+" games played in "+str(round(end-start,3))+" seconds ("+str(round(len(results)/(end-start),3))+" games/s)" )
	print("PlayerX wins: {}, PlayerO wins: {}, draws: {}".format(results.count('X'), results.count('O'), results.count('D')))


def train_qdict(nr_games, pX, pO, report_winrate = False):
	engine = E.Engine(pX, pO)

	winrates = []

	print("Start on " + str(datetime.datetime.now()))
	start = time.time()
	for j in range(1, nr_games+1):
		sys.stdout.write( "\r%d/%d" % (j, nr_games) )
		sys.stdout.flush()
		engine.run(train = True, transform = True)
		if j%5000 == 0:
			if report_winrate:
				winrates.append([j] + test_qdict(Q.Qbot.Q, 1000))
			Q.Qbot.dump_dict()
	
	end = time.time()
	print("\nFinished on " + str(datetime.datetime.now()))
	
	dt = end-start
	dhour = int(dt//(60*60))
	dt = dt-dhour*60*60
	dmin = int(dt//60)
	dt = dt-dmin*60
	dsec = round(dt, 3)
	
	print("Operation took "+str(dhour)+" hours, " + str(dmin) + " minutes and " + str(dsec) + " seconds.")

	print("\n"+str(nr_games)+" games played")

	vis.save(winrates)

	vis.plot_winrates(winrates, title = 'Winrate over time vs random player')



def test_qdict(Qdict, nr_games):

	xresults = []
	# play as X against random O
	pX = Q.Qbot(mark = 'X', Q = Qdict, epsilon = 0)
	pO = R.Randombot('O')
	engine = E.Engine(pX, pO)
	for i in range(nr_games//2):
		engine.run(train = False, transform = True)
		xresults.append(engine.get_result())

	oresults = []
	pX = R.Randombot('X')
	pO = Q.Qbot(mark = 'O', Q = Qdict, epsilon = 0)
	engine = E.Engine(pX, pO)
	for i in range(nr_games//2):
		engine.run(train = False, transform = True)
		oresults.append(engine.get_result())

	winratex = (xresults.count('X') + xresults.count('D')/2) / nr_games*2
	winrateo = (oresults.count('O') + oresults.count('D')/2) / nr_games*2
	winrate = winratex/2. + winrateo/2.

	print('\nwinrate as X: ', round(winratex, 6))
	print('winrate as O: ', round(winrateo, 6))
	print('winrate: ', round(winrate, 6))

	return [winrate, winratex, winrateo]



if __name__ == '__main__':
	# play_randbot_human()
	# play_human_human()

	nr_games = 100000


	pX = Q.Qbot(mark = 'X') #, Q = Qdictionary)
	pO = Q.Qbot(mark = 'O')
	train_qdict(nr_games = nr_games, pX = pX, pO = pO, report_winrate = True)


	# with open('dictionaries/_Q1000.p', 'rb') as handle:
	# 	Qdict = pickle.load(handle)

	# winrate = test_qdict(Qdict, 1000)
	


	# pX = R.Randombot('X')
	# pO = R.Randombot('O')
	# play_set_games(nr_games,pX,pO, transform = True)

	# play_randbot_randbot(nr_games)