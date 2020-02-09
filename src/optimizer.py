
from components.optimizer.population import Population
from components.mapping.point import Point
from components.mapping.map import Map
import pickle as pkl
######################## Params ##########################
n_generations = 100
n_pop = 5000
crossover_rate = 0.4
mutation_rate = 0.2
n_buses = 2
start_position = 0

with open('../points.pkl','rb') as points_file:
    points = pkl.load(points_file)

if __name__ == "__main__":
    _map = Map(points)
    opt = Population(n_pop,crossover_rate,mutation_rate,n_buses,_map,start_position)
    best = None
    n_best = (int) (n_pop - n_pop*(crossover_rate + mutation_rate))

    for g in range(n_generations):
        opt.natural_selection()
        offspring = opt.binary_tournament()
        mutations = opt.mutation(offspring)
        opt.pop[n_best:n_pop] = offspring + mutations
        best = opt.pop[0]
        print(best.fitness_value)
        
    
    


    




