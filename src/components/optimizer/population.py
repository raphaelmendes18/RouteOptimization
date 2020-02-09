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

    def natural_selection(self, Qt):
        '''
        Calculate Fitness
        Sort population
        '''

        self.pop = self.pop + Qt
        aux_pop = []
        for p in self.pop:
            p.fitness()

        pareto_frontiers = self.non_dominant_sorting()
        crowd_values = self.crowd_sorting(pareto_frontiers)

        def custom_sort(pareto_frontiers, crowd_values):
            sorted_pop = []
            for f in pareto_frontiers:
                sorted_pop += sorted(f, key = lambda x: crowd_values[x])
            return sorted_pop

        sorted_pop = custom_sort(pareto_frontiers, crowd_values)

        for p in sorted_pop:
            aux_pop.append(self.pop[p])

        self.pop = aux_pop[0:self.n_pop]
        

    def binary_tournament(self):

        offspring_num = (int) (self.n_pop*self.crossover_rate)
        n_best = (int) (self.n_pop)

        mating_pool = self.pop[0:n_best]
        
        offspring = []

        for i in range(int (offspring_num/2)):
            # Select 2 Parents in 1x1 mini tournaments
            parent_1 = random.sample(mating_pool, k = 1)[0]
            parent_2 = random.sample(mating_pool, k = 1)[0]
        
            child_1, child_2 = DNA.crossover(parent_1, parent_2, mark='latter', _map = self.map)
            
            offspring.append(child_1)
            offspring.append(child_2)
        
        return offspring

    def mutation(self, offspring):

        n_best = (int) (self.n_pop)

        mating_pool = self.pop[0:n_best]

        mutation_pool = mating_pool + offspring
        mutated_list = []
        for i in range(int (self.n_pop*self.mutation_rate)):
            # Pick one dna from mutation pool
            mutated_dna = copy.deepcopy(random.sample(mutation_pool, k = 1)[0])
            # Operates mutation
            mutated_dna.mutation()
            # Reset fitness_value
            mutated_dna.fitness_value = [np.inf,np.inf]
            mutated_list.append(mutated_dna)

        return mutated_list

    def non_dominant_sorting(self):
        
        pareto_frontiers = []
        dominance_list = [] 
        remaining = self.n_pop*2
        pop = [i for i in range(self.n_pop*2)]
        '''
        Create List of Dominations By for each individual
        '''
        for i in range(self.n_pop*2):
            dominated_by = []
            for j in range(self.n_pop*2):
                if Population.a_dominates_b(self.pop[j], self.pop[i]):
                    dominated_by.append(j)
            dominance_list.append(dominated_by)

        while remaining > 0:
            ''' 
            Create Empty Frontier
            '''
            frontier = []
            '''
            Iterate over population of individuals without frontiers
            '''
            for p in pop:
                '''
                if not dominated by any other points
                then should be added to frontier
                '''
                
                if len(dominance_list[p]) == 0:
                    frontier.append(p)
                    remaining -= 1

            pareto_frontiers.append(frontier)
            '''
            Remove Points recently added to frontier from population
            '''
            
            pop = [p for p in pop if p not in frontier]
            
            
            '''
            Update list of dominance by removing previous frontiers points
            '''
            for p in pop:
                for f in frontier:
                    try:
                        dominance_list[p].remove(f)
                    except ValueError:
                        continue
                    
        return pareto_frontiers

    def crowd_sorting(self, pareto_frontiers):
        '''
        Crowd Sorting needs to be calculated across objectives
        '''
        num_objectives = len(self.pop[0].fitness_value)
        '''
        Store the values, the index of the crowd_sorting_values is associated with the pop index in self.pop
        '''
        crowd_sorting_values = [[] for i in range(self.n_pop*2)]
        '''
        For Normalization Purposes, need to get min and max for each objective
        '''
        boundaries = []
        for i in range(num_objectives):
            max_value = max(self.pop, key = lambda p: p.fitness_value[i]).fitness_value[i]
            min_value = min(self.pop, key = lambda p: p.fitness_value[i]).fitness_value[i]
            boundaries.append((min_value,max_value))

        '''
        Calculate Crowd Sorting among frontiers by first sorting on objective        
        '''
        for frontier in pareto_frontiers:
            for i in range(num_objectives):
                sorted_frontier = sorted(frontier, key = lambda p: self.pop[p].fitness_value[i])     
                for idx, p in enumerate(sorted_frontier):
                    if idx == 0 or idx == len(sorted_frontier)-1:
                        crowd_value = np.inf
                    else:
                        min_value, max_value = boundaries[i]
                        crowd_value = (self.pop[sorted_frontier[idx+1]].fitness_value[i] - self.pop[sorted_frontier[idx-1]].fitness_value[i])/(max_value - min_value) 

                    crowd_sorting_values[p].append(crowd_value)
        
        return [sum(cs) for cs in crowd_sorting_values]
                    


    def a_dominates_b(a, b):
        dominates = True
        for idx in range(len(a.fitness_value)):
            dominates = dominates & (a.fitness_value[idx] < b.fitness_value[idx])

        return dominates
            





