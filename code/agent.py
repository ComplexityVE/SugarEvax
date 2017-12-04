import numpy as np
import random

class Agent:

    def __init__(self, loc, taxation, mating, params, baby=False):
        """Creates a new agent at the given location.

        loc: tuple coordinates
        params: dictionary of parameters
        """
        self.loc = tuple(loc)
        self.age = 0
        self.taxation = taxation
        self.mating = mating

        min_end_child_m = params.get('min_end_child_m', 50)
        max_end_child_m = params.get('max_end_child_m', 60)

        min_end_child_f = params.get('min_end_child_f', 40)
        max_end_child_f = params.get('max_end_child_f', 50)

        # if this is a product of an agent mating
        if baby == True:
            self.vision = params.get('vision')
            self.metabolism = params.get('metabolism')
            self.lifespan = params.get('death_age')
            self.sugar = params.get('sugar')
            self.beg_reproduction_age = params.get('child')

        # if this is the initial generating of agents
        else:
            min_beg_child = params.get('min_beg_child', 12)
            max_beg_child = params.get('max_beg_child', 15)
            # extract the parameters
            min_metabolism = params.get('min_metabolism', 1)
            max_metabolism = params.get('max_metabolism', 4)

            min_vision = params.get('min_vision', 1)
            max_vision = params.get('max_vision', 6)

            if self.mating:
                min_sugar = params.get('min_sugar', 50.0)
                max_sugar = params.get('max_sugar', 100.0)
                min_death = params.get('min_death', 60)
                max_death = params.get('max_death', 100)
            else:
                min_sugar = params.get('min_sugar', 5.0)
                max_sugar = params.get('max_sugar', 25.0)
                min_death = params.get('min_death', 998800)
                max_death = params.get('max_death', 1000000)

            # choose attributes
            self.vision = np.random.random_integers(min_vision,max_vision)
            self.metabolism = np.random.uniform(min_metabolism, max_metabolism)
            self.lifespan = np.random.uniform(min_death, max_death)
            self.sugar = np.random.uniform(min_sugar, max_sugar)

            self.beg_reproduction_age = np.random.uniform(min_beg_child, max_beg_child)

        self.init_sugar = 0
        self.sex = random.choice(['female','male'])
        if self.sex == 'female':
            self.end_reproduction_age = np.random.uniform(min_end_child_f, max_end_child_f)
        else:
            self.end_reproduction_age = np.random.uniform(min_end_child_m, max_end_child_m)
        self.can_mate = False
        self.can_mate_age = False
        self.can_mate_sugar = False

    def step(self, env):
        """Look around, move, and harvest.

        env: Sugarscape
        """
        self.calculate_tax()
        self.redistribute_wealth(env.get_welfare(self))
        self.loc = env.look_around(self.loc, self.vision)
        if self.taxation:
            self.sugar = self.sugar + env.harvest(self.loc) - self.metabolism - self.tax + self.welfare
        else:
            self.sugar = self.sugar + env.harvest(self.loc) - self.metabolism
        self.age += 1
        self.mating_conditions()

    def is_starving(self):
        """Checks if sugar has gone negative."""
        return self.sugar < self.metabolism

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

    def mating_conditions(self):
        if (self.age>=self.beg_reproduction_age) and (self.age <=self.end_reproduction_age):
            self.can_mate_age = True
        else:
            self.can_mate_age = False
        if (self.sugar>= self.init_sugar):
            self.can_mate_sugar = True
        else:
            self.can_mate_sugar = False
        if self.can_mate_age==True and self.can_mate_sugar==True:
            self.can_mate = True
        else:
            self.can_mate = False
