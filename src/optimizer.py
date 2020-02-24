
from components.optimizer.population import Population
from components.mapping.point import Point
from components.mapping.map import Map, OpenApiMap
import pickle as pkl
import pandas as pd
######################## Params ##########################
n_generations = 10
n_pop = 500
n_best = 200
crossover_rate = 0.4
mutation_rate = 0.2
n_buses = 3
start_position = 0

# with open('../points.pkl','rb') as points_file:
#     points = pkl.load(points_file)

df_points = pd.read_csv('../input/points.csv', sep=',')
points = df_points.apply(lambda p: Point(p.LATITUDE, p.LONGITUDE), axis = 1)

if __name__ == "__main__":
    results = []
    _map = OpenApiMap(points)
    opt = Population(n_pop,crossover_rate,mutation_rate,n_best,n_buses,_map,start_position)
    best = None
    opt.natural_selection()
    for g in range(n_generations):
        offspring = opt.binary_tournament()
        mutations = opt.mutation(offspring)
        opt.pop[n_best:n_pop] = offspring + mutations
        opt.natural_selection()
        for p in opt.pop:
            results.append([g, p.fitness_value[0], p.fitness_value[1]])

    pd.DataFrame(results,columns=['generation','max_trip','total_trip']).to_csv('../results.csv', index=False)
    with open('../graph.pkl', 'wb') as graph_file:
        adj_mat = _map.adj_mat
        import numpy as np
        mat = np.zeros(shape=(adj_mat.shape[0],adj_mat.shape[0]))
        for i in range(adj_mat.shape[0]):
            for j in range(adj_mat.shape[0]):
                mat[i,j] = adj_mat[i,j]
            
        pkl.dump(mat,graph_file)
    with open('../routes.pkl', 'wb') as routes_file:
        solutions = opt.pop[0:n_best]
        pkl.dump([s.encode() for s in solutions], routes_file)