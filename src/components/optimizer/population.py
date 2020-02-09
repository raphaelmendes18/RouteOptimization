from components.mapping.map import Map
from components.optimizer.dna import DNA
import copy
import numpy as np
import random
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
        self.map = _map
        self._initialize_pop(n_buses, start_position)
    
    def _initialize_pop(self, n_buses, start_position):
        self.pop = []
        
        for i in range(self.n_pop):
            self.pop.append(DNA(n_buses, self.map, start_position))

    def natural_selection(self):
        '''
        Calculate Fitness
        Sort population
        '''
        for p in self.pop:
            p.fitness()

        self.pop.sort(key=lambda p: p.fitness_value, reverse=False)

    def binary_tournament(self):

        offspring_num = (int) (self.n_pop*self.crossover_rate)
        n_best = (int) (self.n_pop - self.n_pop*(self.crossover_rate + self.mutation_rate))

        mating_pool = self.pop[0:n_best]
        
        offspring = []

        for i in range(int (offspring_num/2)):
            # Select 2 Parents in 1x1 mini tournaments
            parents_1 = random.sample(mating_pool, k = 2)
            if parents_1[0].fitness_value < parents_1[1].fitness_value:
                parent_1 = parents_1[0]
            else: 
                parent_1 = parents_1[1]
            parents_2 = random.sample(mating_pool, k = 2)
            if parents_2[0].fitness_value < parents_2[1].fitness_value:
                parent_2 = parents_2[0]
            else: 
                parent_2 = parents_2[1]    
            child_1, child_2 = DNA.crossover(parent_1, parent_2, mark='latter', _map = self.map)
            
            offspring.append(child_1)
            offspring.append(child_2)
        
        return offspring

    def mutation(self, offspring):

        n_best = (int) (self.n_pop - self.n_pop*(self.crossover_rate + self.mutation_rate))

        mating_pool = self.pop[0:n_best]

        mutation_pool = mating_pool + offspring
        mutated_list = []
        for i in range(int (self.n_pop*self.mutation_rate)):
            # Pick one dna from mutation pool
            mutated_dna = copy.deepcopy(random.sample(mutation_pool, k = 1)[0])
            # Operates mutation
            mutated_dna.mutation()
            # Reset fitness_value
            mutated_dna.fitness_value = np.inf
            mutated_list.append(mutated_dna)

        return mutated_list

