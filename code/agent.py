import numpy as np

class Agent:

    def __init__(self, loc, taxation, params):
        """Creates a new agent at the given location.

        loc: tuple coordinates
        params: dictionary of parameters
        """
        self.loc = tuple(loc)
        self.age = 0
        self.taxation = taxation

        # extract the parameters
        max_vision = params.get('max_vision', 6)
        max_metabolism = params.get('max_metabolism', 4)
        min_lifespan = params.get('min_lifespan', 99998)
        max_lifespan = params.get('max_lifespan', 100000)
        min_sugar = params.get('min_sugar', 5)
        max_sugar = params.get('max_sugar', 25)

        # choose attributes
        self.vision = np.random.random_integers(max_vision)
        self.metabolism = np.random.uniform(1, max_metabolism)
        self.lifespan = np.random.uniform(min_lifespan, max_lifespan)
        self.sugar = np.random.uniform(min_sugar, max_sugar)

    def step(self, env):
        """Look around, move, and harvest.

        env: Sugarscape
        """
        self.calculate_tax()
        self.redistribute_wealth(env.get_welfare())
        self.loc = env.look_around(self.loc, self.vision)
        if self.taxation:
            self.sugar = self.sugar + env.harvest(self.loc) - self.metabolism - self.tax + self.welfare
        else:
            self.sugar = self.sugar + env.harvest(self.loc) - self.metabolism
        self.age += 1

    def is_starving(self):
        """Checks if sugar has gone negative."""
        return self.sugar < 0

    def is_old(self):
        """Checks if lifespan is exceeded."""
        return self.age > self.lifespan

    def get_wealth(self):
        return self.sugar

    def redistribute_wealth(self, welfare):
        self.welfare = welfare

    def calculate_tax(self):
        if self.sugar <= 5:
            self.tax = self.sugar * .3
        elif self.sugar > 5 and self.sugar <= 12:
            self.tax = 1.5 + ((self.sugar-5)*.4)
        elif self.sugar >12 and self.sugar <= 20:
            self.tax = 4.8 + ((self.sugar-12)*.5)
        else:
            self.tax = 10 + ((self.sugar-20)*.6)

    def get_tax(self):
        self.calculate_tax()
        return self.tax
