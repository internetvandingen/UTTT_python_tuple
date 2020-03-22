import random
import pickle

class Qbot:
	# class attribute Qbot.Q: dictionary is shared by all object of class Qbot
	Q = {}

	def __init__(self, mark, Q={'nr_games':0}, default_Qvalue = 1., epsilon = 0.1, alpha = 0.3, gamma = 0.9):
		self.mark = mark
		if len(Qbot.Q)==0:
			Qbot.Q = Q
		Qbot.default_Qvalue = default_Qvalue

		Qbot.epsilon = epsilon
		Qbot.alpha = alpha
		Qbot.gamma = gamma

	def get_move(self, field):
		moves = field.get_available_moves()
		state_key = self.make_and_maybe_add_key(field, moves)

		# store last state key as class attribute
		Qbot._last_state_key = state_key

		# with chance of epsilon, make random move (explore), else select from dictionary (exploit)
		if random.uniform(0, 1) < Qbot.epsilon:
			move = moves[random.randrange(len(moves))]
		else:
			Qs = Qbot.Q[state_key]
			if self.mark == 'X':
				move = self.stochastic_argminmax(Qs, max)
			elif self.mark == 'O':
				move = self.stochastic_argminmax(Qs, min)

		return move


	@classmethod
	def make_and_maybe_add_key(cls, field, moves):
		# Make a dictionary key for the current state(board + player turn)
		# if Q does not yet have it, add it to Q.

		state_key = cls.get_key(field)
		if Qbot.Q.get(state_key) is None:
			Qbot.Q[state_key] = {move:cls.default_Qvalue for move in moves}

		return state_key


	@classmethod
	def get_key(cls, field, separator = ","):
		return sum(field.board, sum(field.macroboard, ()))

	@classmethod
	def dump_dict(cls):
		nr_games = Qbot.Q['nr_games']
		filename = "dictionaries/_Q"+str(nr_games)+".p"

		with open(filename, 'wb') as outfile:
			pickle.dump(Qbot.Q, outfile, protocol=pickle.HIGHEST_PROTOCOL)
		
		# with open(filename, 'w') as outfile:
		# 	json.dump(Qbot.Q, outfile)

	def stochastic_argminmax(self, Qs, min_or_max):
		min_or_maxQ = min_or_max(list(Qs.values()))
		# If there is more than one move corresponding to the maximum Q-value, choose one at random
		if list(Qs.values()).count(min_or_maxQ) > 1:
			best_options = [move for move in list(Qs.keys()) if Qs[move] == min_or_maxQ]
			move = best_options[random.randint(0, len(best_options))-1]
		else:
			move = min_or_max(Qs, key=Qs.get)
		return move

	@classmethod
	def parse_reward(cls, whos_turn, field, move, winner):
		# move is already implemented, so get state key of before that happened
		state_key = cls._last_state_key

		# get available moves after move is implemented
		# TODO: can be faster if these moves are stored and used for next move
		moves = field.get_available_moves()

		if winner == 'X':
			expected_reward = 100.0
			cls.Q['nr_games'] += 1
		elif winner == 'O':
			expected_reward = -100.0
			cls.Q['nr_games'] += 1
		elif winner == 'D':
			expected_reward = 0.5
			cls.Q['nr_games'] += 1
		else:
			# reward is zero if game is not over, so no need to add it to expected reward
			next_state_key = cls.make_and_maybe_add_key(field, moves)
			next_Qs = cls.Q[next_state_key]

			# current player is O, and X made most recent move, so minimize value
			if whos_turn == 'O':
				expected_reward = cls.gamma * min(next_Qs.values())
			# current player is X and O made most recent move, so maximize value
			elif whos_turn == 'X':
				expected_reward = cls.gamma * max(next_Qs.values())

		change = cls.alpha * (expected_reward - cls.Q[state_key][move])
		cls.Q[state_key][move] += change