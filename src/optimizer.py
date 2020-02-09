
from components.optimizer.population import Population
from components.mapping.point import Point
from components.mapping.map import Map
import pickle as pkl
import pandas as pd
######################## Params ##########################
n_generations = 20
n_pop = 1000
crossover_rate = 0.8
mutation_rate = 0.2
n_buses = 10
start_position = 0

with open('../points.pkl','rb') as points_file:
    points = pkl.load(points_file)

if __name__ == "__main__":
    results = []
    _map = Map(points)
    opt = Population(n_pop,crossover_rate,mutation_rate,n_buses,_map,start_position)
    Qt = Population(n_pop,crossover_rate,mutation_rate,n_buses,_map,start_position).pop
    best = None
    n_best = (int) (n_pop - n_pop*(crossover_rate + mutation_rate))

    for g in range(n_generations):
        opt.natural_selection(Qt)
        best = opt.pop[0]
        offspring = opt.binary_tournament()
        mutations = opt.mutation(offspring)
        Qt = offspring + mutations

        for p in opt.pop:
            results.append([g, p.fitness_value[0], p.fitness_value[1]])
    
    pd.DataFrame(results,columns=['generation','max_trip','total_trip']).to_csv('../results.csv', index=False)
        
    
    


    




