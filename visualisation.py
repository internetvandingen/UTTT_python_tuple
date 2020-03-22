import matplotlib.pyplot as plt
import re
import json
import time
from os import listdir
from pprint import pprint

def plot_winrates(res, title = ''):

	games = [i[0] for i in res]
	winrate = [i[1] for i in res]
	winratex = [i[2] for i in res]
	winrateo = [i[3] for i in res]
	plt.plot(games, winrate, 'ko-', label = 'Winrate')
	plt.plot(games, winratex, 'ro--', label = 'Winrate as X', alpha = 0.5, markersize = 4)
	plt.plot(games, winrateo, 'bo--', label = 'Winrate as O', alpha = 0.5, markersize = 4)
	plt.ylabel('Winrate')
	plt.xlabel('Number of games')
	plt.ylim([0, 1])
	plt.title(title)
	plt.legend()
	plt.show()

def save(results, dir = 'dictionaries/'):
	# save results from games over time in directory dir
	filename = time.strftime(dir + "results_%Y-%m-%d_%H%M%S.json")
	with open(filename, 'w') as outfile:
		json.dump(results, outfile)

def load(file):
	# loads and returns results using json
	with open(file) as json_data:
		data = json.load(json_data)

	return data
	


def plot_last(dir = 'dictionaries/'):
	# scans the temp folder
	files = listdir(dir)

	if (len(files)>0):
		resultfiles = []
		for i in files:
			if re.match(r'^results_', i):
				resultfiles.append(i)

		if (len(resultfiles)>0):
			# selects most recent file
			files.sort()

			# loads the data from it
			data = load(dir+resultfiles[-1])

			print('Loaded file: ' + resultfiles[-1])

			# plots the data
			plot_winrates(data)
		else:
			print('No files beginning with "results_" in ' + dir)
	else:
		print('No files available in /' + dir + '/')
