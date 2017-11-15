class FitnessLandscape:
    def __init__(self, N):
        """Create a fitness landscape.
        
        N: number of dimensions
        """
        self.N = N
        self.set_values()
        
    def set_values(self):
        self.one_values = np.random.random(self.N)
        self.zero_values = np.random.random(self.N)

    def random_loc(self):
        """Choose a random location."""
        # in NumPy versions prior to 1.11, you might need
        #return np.random.randint(2, size=self.N).astype(np.int8)
        return np.random.randint(2, size=self.N, dtype=np.int8)
    
    def fitness(self, loc):
        """Evaluates the fitness of a location.
        
        loc: array of N 0s and 1s
        
        returns: float fitness
        """
        fs = np.where(loc, self.one_values, self.zero_values)
        return fs.mean()
    
    def distance(self, loc1, loc2):
        return np.sum(np.logical_xor(loc1, loc2))