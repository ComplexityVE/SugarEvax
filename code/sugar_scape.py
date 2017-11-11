import matplotlib.pyplot as plt
import numpy as np

from Cell2D import Cell2D, Cell2DViewer
from SugarscapeViewer import SugarscapeViewer
from agent import Agent


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

class Sugarscape(Cell2D):
    """Represents an Epstein-Axtell Sugarscape."""

    def __init__(self, n, taxation, **params):
        """Initializes the attributes.

        n: number of rows and columns
        params: dictionary of parameters
        """
        self.n = n
        self.params = params
        self.total_welfare = 0
        self.taxation = taxation

        # track variables
        self.agent_count_seq = []

        # make the capacity array
        self.capacity = self.make_capacity()

        # initially all cells are at capacity
        self.array = self.capacity.copy()

        # make the agents
        self.make_agents()

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
        n, m = self.params.get('starting_box', self.array.shape)
        locs = make_locs(n, m)
        np.random.shuffle(locs)

        # make the agents
        num_agents = self.params.get('num_agents', 400)
        self.agents = [Agent(locs[i], self.taxation, self.params)
                       for i in range(num_agents)]

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
        total_welfare = 0
        replace = self.params.get('replace', False)

        # loop through the agents in random order
        random_order = np.random.permutation(self.agents)
        for agent in random_order:

            # mark the current cell unoccupied
            self.occupied.remove(agent.loc)

            total_welfare += agent.get_tax()

            # execute one step
            agent.step(self)

            # if the agent is dead, remove from the list
            if agent.is_starving() or agent.is_old():
                self.agents.remove(agent)
                if replace:
                    self.add_agent()
            else:
                # otherwise mark its cell occupied
                self.occupied.add(agent.loc)

        # update the time series
        self.agent_count_seq.append(len(self.agents))

        # grow back some sugar
        self.grow()
        self.total_welfare = total_welfare
        return len(self.agents)

    def get_welfare(self):
        if len(self.agents) == 0:
            return 0
        return self.total_welfare / len(self.agents)

    def add_agent(self):
        """Generates a new random agent.

        returns: new Agent
        """
        new_agent = Agent(self.random_loc(), self.params)
        self.agents.append(new_agent)
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

    def plot_populations(self):
        plt.plot(self.agent_count_seq)



if __name__ == '__main__':
    env = Sugarscape(50, True, num_agents=400)
    for i in range(800):
        env.step()
    env.plot_populations()
    env = Sugarscape(50, False, num_agents=400)
    for i in range(800):
        env.step()
    env.plot_populations()
    plt.show()
