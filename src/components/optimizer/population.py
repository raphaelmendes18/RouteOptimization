from map import Map
from dna import DNA
class Population:
    '''
    The Population orchestrates the solutions by optimizing them using Genetic Algorithm
    Operators:
        * Natural Selection: Select n_best solutions for the mating pool
        * Mating Pool: Fittest to be used to generate offsprint
        * Binary Tournament: Pick 2 parents from mating pool - return the best(fittest)
        * Generate Offspring: Generate n_pop*crossover_rate children solutions
        * Mutation: Generate n_pop*mutation_rate mutated solutions from n_best + n_pop*crossover_rate
    '''
    
    def __init__(self, n_pop, crossover_rate, mutation_rate, n_buses, _map, start_position):
        try:
            assert isinstance(n_pop, int)
            assert isinstance(crossover_rate, float)
            assert isinstance(mutation_rate, float)
            assert isinstance(n_buses, int)
            assert isinstance(_map, Map)
            assert isinstance(start_position, int)
        except AssertionError:
            raise AssertionError('Error Creating Population Object - Unexpected Types')
        
        self.n_pop = n_pop
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate 
        self._initialize_pop(n_buses, _map, start_position)

    def _initialize_pop(self, n_buses, _map, start_position):
        self.pop = []
        
        for i in range(n_pop):
            self.pop.append(DNA(n_buses, _map, start_position))

    def natural_selection(self):

        n_best = self.n_pop - self.n_pop(crossover_rate + mutation_rate)

        for p in self.pop:
            p.fitness()

        self.pop.sort(key=lambda x: p.fitness, reverse=True)
        

