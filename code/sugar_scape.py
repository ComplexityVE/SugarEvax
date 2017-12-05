import matplotlib.pyplot as plt
import numpy as np

from Cell2D import Cell2D, Cell2DViewer
from SugarscapeViewer import SugarscapeViewer
from agent import Agent
import random
import copy

def make_locs(n, m):
	"""Makes array where each row is an index in an `n` by `m` grid.

	n: int number of rows
	m: int number of cols

	returns: NumPy array
	"""
	left = np.repeat(np.arange(m), n)
	right = np.tile(np.arange(n), m)
	return np.transpose([left, right])

def make_visible_locs(vision):
	"""Computes the kernel of visible cells.
	vision: int distance
	"""
	def make_array(d):
		"""Generates visible cells with increasing distance."""
		a = np.array([[-d, 0], [d, 0], [0, -d], [0, d]])
		np.random.shuffle(a)
		return a

	arrays = [make_array(d) for d in range(1, vision+1)]
	return np.vstack(arrays)

def make_neighbors_locs():
	""" Makes array of neighbors"""
	neighbors = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
	np.random.shuffle(neighbors)
	return neighbors

class Sugarscape(Cell2D):
	"""Represents an Epstein-Axtell Sugarscape."""

	def __init__(self, n, taxation, mating_env=True, redistribution=False, **params):
		"""Initializes the attributes.

		n: number of rows and columns
		params: dictionary of parameters
		"""
		self.n = n
		self.params = params
		self.total_welfare = 0
		self.taxation = taxation
		self.mating_env = mating_env
		self.redistribution = redistribution

		# track variables
		self.agent_count_seq = []
		self.agent_metabolism_seq = []

		# make the capacity array
		self.capacity = self.make_capacity()

		# initially all cells are at capacity
		self.array = self.capacity.copy()

		# make the agents
		self.agents = []
		self.occupied = set()
		self.agent_loc_dict = {}
		self.make_agents()

		# Stuff to keep track of for graphing
		self.vision = [np.mean([agent.vision for agent in self.agents])]
		self.curr_mean_wealth = np.mean([agent.sugar for agent in self.agents])
		self.wealth = [self.curr_mean_wealth]
		self.low_sugar = sum([1 for agent in self.agents if agent.sugar<=self.curr_mean_wealth])
		self.metabolism = [np.mean([agent.metabolism for agent in self.agents])]
		self.get_welfare_brackets()

	def make_capacity(self):
		"""Makes the capacity array."""

		# compute the distance of each cell from the peaks.
		x = np.arange(self.n)
		rows, cols = np.meshgrid(x, x, indexing='ij')

		# each cell in `rows` contains its own `i` coordinate
		# each cell in `cols` contains its `j` coordinate
		dist1 = np.hypot(rows-15, cols-15)
		dist2 = np.hypot(rows-35, cols-35)

		# each cell in `dist` contains its distance to the closer peak
		dist = np.minimum(dist1, dist2)

		# cells in the capacity array are set according to dist from peak
		a = np.zeros((self.n, self.n), np.float)
		a[dist<21] = 1
		a[dist<16] = 2
		a[dist<11] = 3
		a[dist<6] = 4

		return a

	def make_agents(self):
		"""Makes the agents."""

		# determine where the agents start and generate locations
		#n, m = self.params.get('starting_box', self.array.shape)
		#locs = make_locs(n, m)
		#np.random.shuffle(locs)
		# make the agents
		num_agents = self.params.get('num_agents', 400)

		for i in range(num_agents):
			self.add_agent()

		# keep track of which cells are occupied
		self.occupied = set(agent.loc for agent in self.agents)

	def grow(self):
		"""Adds sugar to all cells and caps them by capacity."""
		grow_rate = self.params.get('grow_rate', 1)
		self.array = np.minimum(self.array + grow_rate, self.capacity)

	def look_around(self, center, vision):
		"""Finds the visible cell with the most sugar.

		center: tuple, coordinates of the center cell
		vision: int, maximum visible distance

		returns: tuple, coordinates of best cell
		"""
		# find all visible cells
		locs = make_visible_locs(vision)
		locs = (locs + center) % self.n

		# convert rows of the array to tuples
		locs = [tuple(loc) for loc in locs]

		# select unoccupied cells
		empty_locs = [loc for loc in locs if loc not in self.occupied]

		# if all visible cells are occupied, stay put
		if len(empty_locs) == 0:
			return center

		# look up the sugar level in each cell
		t = [self.array[loc] for loc in empty_locs]

		# find the best one and return it
		# (in case of tie, argmax returns the first, which
		# is the closest)
		i = np.argmax(t)
		return empty_locs[i]

	def harvest(self, loc):
		"""Removes and returns the sugar from `loc`.

		loc: tuple coordinates
		"""
		sugar = self.array[loc]
		self.array[loc] = 0
		return sugar

	def step(self):
		"""Executes one time step."""
		replace = self.params.get('replace', False)
		if self.redistribution:
			self.get_welfare_brackets()

		# loop through the agents in random order
		random_order = np.random.permutation(self.agents)
		for agent in random_order:
			# mark the current cell unoccupied
			self.occupied.remove(agent.loc)
			del self.agent_loc_dict[agent.loc]


			if agent.sugar <= self.curr_mean_wealth:
				self.low_sugar += 1

			# execute one step
			agent.step(self)

			# if the agent is dead, remove from the list
			if agent.is_starving() or agent.is_old():
				self.agents.remove(agent)
			else:
				# otherwise mark its cell occupied
				self.agent_loc_dict[agent.loc] = agent
				self.occupied.add(agent.loc)


		# update the time series
		self.agent_count_seq.append(len(self.agents))
		metabolisms = [agent.metabolism for agent in self.agents]
		self.agent_metabolism_seq.append(np.mean(metabolisms))

		# grow back some sugar
		self.grow()

		if self.mating_env:
			# initialize mating
			self.mating()

		# update array of values for graphing
		self.vision.append(np.mean([agent.vision for agent in self.agents]))
		self.curr_mean_wealth = np.mean([agent.sugar for agent in self.agents])
		self.wealth.append(self.curr_mean_wealth)
		self.metabolism.append(np.mean([agent.metabolism for agent in self.agents]))

		taxes = [agent.get_tax() for agent in self.agents]
		self.total_welfare = sum(taxes)
		self.total_welfare = self.total_welfare - (self.total_welfare*.15)

		return len(self.agents)

	def get_welfare(self, agent):
		if len(self.agents) == 0:
			return 0
		if self.redistribution:
			bracket_width = self.curr_mean_wealth / 3
			if agent.sugar <= self.curr_mean_wealth-bracket_width:
				return self.bracket1_welfare
			elif agent.sugar <= self.curr_mean_wealth:
				return self.bracket2_welfare
			elif agent.sugar <= self.curr_mean_wealth+bracket_width:
				return self.bracket3_welfare
			return 0
		else:
			return self.total_welfare / len(self.agents)

	def get_welfare_brackets(self):
		bracket_width = self.curr_mean_wealth / 3
		bracket1 = sum([1 for agent in self.agents if agent.sugar<=self.curr_mean_wealth-bracket_width])
		bracket2 = sum([1 for agent in self.agents if agent.sugar<=self.curr_mean_wealth and agent.sugar>self.curr_mean_wealth-bracket_width])
		bracket3 = sum([1 for agent in self.agents if agent.sugar<=self.curr_mean_wealth+bracket_width and agent.sugar>self.curr_mean_wealth])
		if bracket1 == 0:
			self.bracket1_welfare = 0
		else:
			self.bracket1_welfare = (self.total_welfare*.5)/bracket1
		if bracket2 == 0:
			self.bracket2_welfare = 0
		else:
			self.bracket2_welfare = (self.total_welfare*.3)/bracket2
		if bracket3 == 0:
			self.bracket3_welfare = 0
		else:
			self.bracket3_welfare = (self.total_welfare*.2)/bracket3

	def mating(self):
		""" mates agents and creates new babies """
		random_order = np.random.permutation(self.agents)
		self.mating_pairs = {}

		# for each agent, find all possible mates in its neighbors
		for agent in random_order:
			if agent.can_mate:
				self.find_mate(agent)

		prev_set = self.mating_pairs
		# create sets of agents that can mate at the same time
		# mate them, and generate new set until no more matings possible
		while self.mating_pairs:

			mating_set = self.mating_set()
			self.mate_agents(mating_set)
			if prev_set == self.mating_pairs:
				break

			prev_set = self.mating_pairs


	def mating_set(self):
		""" generates all possible simulatenous matings"""
		mating_set=[]
		already_mated = []


		#TODO: rename this to mean what it is (single agent or pairs?)
		for agent in self.mating_pairs:
			# updates the agents ability to mate
			agent.mating_conditions()
			# if agent not in already_mated and agent.can_mate:
			if agent.can_mate:
				# if only one possible mating
				if len(self.mating_pairs[agent])==1:
					mate = self.mating_pairs[agent][0]
					# check if mate can mate
					mate.mating_conditions()
					# if mate not in already_mated and mate.can_mate:
					if mate.can_mate:
						already_mated.append(agent)
						already_mated.append(mate)
						mating_set.append((agent,mate))
					# remove both agents no matter if they mated or not
					# bc if they didn't, that means they can't anymore
					self.mating_pairs[mate].remove(agent)
					self.mating_pairs[agent].remove(mate)

				# if more than one possibility
				elif len(self.mating_pairs[agent])>1:
					mates = copy.copy(self.mating_pairs[agent])

					# randomly loop through all mateable neighbors until
					# one is found or none can mate
					for i in range(len(self.mating_pairs[agent])):
						mate = random.choice(mates)
						mates.remove(mate)
						mate.mating_conditions()
						if mate.can_mate==True:
							#if mate not in already_mated:
							already_mated.append(agent)
							already_mated.append(mate)
							self.mating_pairs[mate].remove(agent)
							self.mating_pairs[agent].remove(mate)
							mating_set.append((agent,mate))
							break


		# removes all agents that no longer have any partners
		self.mating_pairs = {k:v for k,v in self.mating_pairs.items() if v!=[]}
		return mating_set

	def find_mate(self, agent):
		"""Finds the neighbors that can mate
		"""
		# find all the neighbors
		locs = make_neighbors_locs()
		locs = (locs + agent.loc) % self.n

		# convert rows of the array to tuples
		locs = [tuple(loc) for loc in locs]

		# select occupied cells
		occupied_locs = [loc for loc in locs if loc in self.occupied]

		for loc in occupied_locs:
			try:
				if self.agent_loc_dict[loc].can_mate and agent.sex != self.agent_loc_dict[loc].sex:
					if self.mating_pairs.get(agent) == None:
						self.mating_pairs[agent] = []

					self.mating_pairs[agent] += [self.agent_loc_dict[loc]]
			except(KeyError):
				# this means it is a neighbor which does not have an agent (tis unoccupied)
				pass

	def find_baby_site(self,agents):
		""" find location for baby to be born """
		for agent in agents:
			# find all visible cells
			locs = make_visible_locs(1)
			locs = (locs + agent.loc) % self.n

			# convert rows of the array to tuples
			locs = [tuple(loc) for loc in locs]

			# select unoccupied cells
			empty_locs = [loc for loc in locs if loc not in self.occupied]

			# if all visible cells are occupied, then do nothing
			if len(empty_locs) == 0:
				pass
			else:
				# randomly choose a place for baby from possibilities
				i = random.choice(empty_locs)
				return i
		# if no empty location was found return None
		return None

	def mate_agents(self, mating_set):
		""" mates a pair of agents"""

		for mate_pair in mating_set:
			mate1 = mate_pair[0]
			mate2 = mate_pair[1]
			loc = self.find_baby_site(mate_pair)
			if loc != None:
				params = {}
				# both parents donate half of their initial sugars
				mate1.sugar -= mate1.init_sugar/2
				mate2.sugar -= mate2.init_sugar/2

				# sets the parameters for baby
				params['sugar'] = (mate1.init_sugar+mate2.init_sugar)/2
				params['death_age'] = random.choice([mate1.lifespan,mate2.lifespan])
				params['metabolism'] = random.choice([mate1.metabolism,mate2.metabolism])
				params['vision'] = random.choice([mate1.vision,mate2.vision])
				params['child'] = random.choice([mate1.beg_reproduction_age,mate2.beg_reproduction_age])
				self.add_baby(loc,params, True)


	def add_baby(self, loc, params, baby=False):
		"""Generates a new agent.

		returns: new Agent
		"""
		new_agent = Agent(loc, self.taxation, self.mating_env,params,baby)
		self.agents.append(new_agent)
		self.agent_loc_dict[new_agent.loc] = new_agent
		self.occupied.add(new_agent.loc)
		return new_agent

	def add_agent(self):
		"""Generates a new random agent.
		returns: new Agent
		"""
		new_agent = Agent(self.random_loc(), self.taxation, self.mating_env, self.params)
		self.agents.append(new_agent)
		self.agent_loc_dict[new_agent.loc] = new_agent
		self.occupied.add(new_agent.loc)
		return new_agent

	def random_loc(self):
		"""Choose a random unoccupied cell.

		returns: tuple coordinates
		"""
		while True:
			loc = tuple(np.random.randint(self.n, size=2))
			if loc not in self.occupied:
				return loc

	def plot_populations(self, my_label):
		plt.xlabel('Time')
		plt.ylabel('Average Population')
		plt.plot(self.agent_count_seq, label=my_label)
		plt.legend()

	def plot_avg_metabolisms(self):
		plt.plot(self.agent_metabolism_seq)



if __name__ == '__main__':
	env = Sugarscape(50, True, False, True, num_agents=400)
	for i in range(800):
		env.step()
	env.plot_populations("Taxation")
	env = Sugarscape(50, False, False, True, num_agents=400)
	for i in range(800):
		env.step()
	env.plot_populations("No Taxation")
	plt.title("Population with No Evolution")
	'''
	plt.show()

	# env = Sugarscape(50, num_agents=400)
	#
	# for i in range(800):
	#  	env.step()
	#
	# plt.subplot(2, 2, 1)
	# plt.plot(env.population)
	# plt.xlabel('Time')
	# plt.ylabel('Average Population')
	#
	# plt.subplot(2, 2, 2)
	# plt.plot(env.wealth)
	# plt.xlabel('Time')
	# plt.ylabel('Average Wealth')
	#
	# plt.subplot(2, 2, 3)
	# plt.plot(env.vision)
	# plt.xlabel('Time')
	# plt.ylabel('Average Vision')
	#
	# plt.subplot(2, 2, 4)
	# plt.plot(env.metabolism)
	# plt.xlabel('Time')
	# plt.ylabel('Average Metabolism')
	# plt.show()
