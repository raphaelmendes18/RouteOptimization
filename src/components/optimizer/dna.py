from components.mapping.point import Point
from components.mapping.map import Map
import random
import numpy as np
import copy
class DNA:
    '''
    The DNA represents a solution to the problem,
    the solution for the Multi Traveller Salesman Problem is encoded
    as a matrix of n_buses x number_of_stops.
    The entire set of stops and the distance between each stop is represented
    as the map.
    Constraint: They start from same start_position
    '''
    def __init__(self, n_buses, _map, start_position, routes = None):

        try:
            assert isinstance(n_buses, int)
            assert isinstance(start_position, int)
            assert isinstance(_map, Map)
        except AssertionError:
            raise AssertionError('Error Creating DNA Object - Unexpected Types')

        self.n_buses = n_buses
        self.map = _map
        self.start_position = start_position
        self.fitness_value = np.inf
        if routes == None:
            self.routes = self.initialize_routes()
        else:
            self.routes = routes
    
    def initialize_routes(self):

        routes = np.empty(shape=self.n_buses, dtype=object)
        for i in range(len(routes)):
            routes[i] = np.array(self.start_position)
        
        visited_stops = np.zeros((self.map.adj_mat.shape[0]), dtype=bool)
        
        '''
        All buses start from the same start position
        '''
        visited_stops[self.start_position] = True

        while any(not s for s in visited_stops): #Checks if Non-Visited Stops still exist
            # Get available stops
            non_visited_stops = [idx for idx, s in enumerate(visited_stops) if s==False]
            
            # Pick one stop randomly
            stop = random.sample(non_visited_stops, k=1)[0]
            
            # Pick one route randomly
            route = random.randint(0,len(routes)-1)
            
            # Add stop to route
            routes[route] = np.append(routes[route], stop)
            
            # Update Visited Stops
            visited_stops[stop] = True
        return routes

    
    def fitness(self):
        '''
        The fitness function will calculate the max route
        '''
        
        if self.fitness_value == np.inf:
            routes_cost = np.zeros(shape=self.routes.shape[0],dtype=float)
            for idx,r in enumerate(self.routes):
                routes_cost[idx] = DNA.get_route_cost(r, self.map)

            self.fitness_value = max(routes_cost)      

    def get_route_cost(r,_map):
        cost = 0.0
        for i in range(r.size-1):
            cost += _map.get_distance_between_points(r[i], r[i+1])
        return cost

    def mutation(self, n_perm = 4):
        '''
        Mutation will be a set of permutations between 2 random routes
        '''
        for i in range(n_perm):
            route_1 = self.routes[random.randint(0, len(self.routes)-1)]
            route_2 = self.routes[random.randint(0, len(self.routes)-1)]
            
            if route_1.size > 1:
                pos_1 = random.randint(1,route_1.size-1)
                if route_2.size > 1:  
                    pos_2 = random.randint(1,route_2.size-1)

                    aux = route_1[pos_1]
                    route_1[pos_1] = route_2[pos_2]
                    route_2[pos_2] = aux
                else:
                    route_2 = np.append(route_2,route_1[pos_1])
                    route_1 = np.delete(route_1,pos_1)
            else:
                if route_2.size > 1:  
                    pos_2 = random.randint(1,route_2.size-1)
                    
                    route_1 = np.append(route_1, route_2[pos_2])
                    route_2 = np.delete(route_2,pos_2)
                else:
                    pass

    def latter_city(encoded, k):
        '''
        Identify the stop that comes after stop K
        '''
        idx_of_city = np.where(encoded == k)[0][0]
        if idx_of_city == len(encoded)-1:
            return encoded[0]
        else:
            return encoded[idx_of_city + 1]

    def former_city(encoded, k):
        '''
        Identify the stop that comes before stop K
        '''
        idx_of_city = np.where(encoded == k)[0][0]
        
        if idx_of_city == 0:
            return encoded[len(encoded) - 1]
        else:
            return encoded[idx_of_city - 1]

    def encode(self):
        '''
        Encode the routes into a single array
        to make it easier to manipulate and operate
        crossover.
        '''
        aux = np.zeros(shape=0,dtype=int)
        for r in self.routes:
            aux = np.append(aux,r)
        
        return aux
    
    def decode(self, encoded_dna):
        '''
        Decode the encoded array into the matrix of routes
        '''
        route = -1
        routes = np.empty(shape=self.n_buses, dtype=object)
        for i in range(len(routes)):
            routes[i] = np.array(self.start_position)
        
        for idx, el in enumerate(encoded_dna):
            if el == self.start_position:
                route += 1
            else:
                routes[route] = np.append(routes[route], el)
        
        return routes

    def crossover(parent_1, parent_2, mark, _map):
        '''
        The crossover operation will generate two offspring
        the first offspring is generated by starting from position
        K then filling the child array based on each parents distance to the next point

        E.g.
        P_1:0->2->3->0->4->1
        P_2:0->3->2->4->0->1

        if K = 3 and mark = latter
        for P_1 latter will be 0
        for P_2 latter will be 2

        remove K from P_1 and P_2

        dx = distance of K->0
        dy = distance of K->2

        dx is less than dy.
        so, the new K will be 0, loops until P_1 and P_2 are empty

        Child 2 is a random permutation of child 1.
        '''

        # Get Encoded parents and remove repeated starting 
        # positions
        encoded_parent_1 = parent_1.encode()
        encoded_parent_1 = encoded_parent_1[1:len(encoded_parent_1)]
        encoded_parent_2 = parent_2.encode()
        encoded_parent_2 = encoded_parent_2[1:len(encoded_parent_2)]
        
        length = len(encoded_parent_1)

        # get a random K
        k = encoded_parent_1[random.randint(0,length-1)]

        # result will store the child 1
        result = np.array([parent_1.start_position,k])

        while length > 1:
            if mark == 'latter':
                x = DNA.latter_city(encoded_parent_1, k)
                y = DNA.latter_city(encoded_parent_2, k)
            elif mark == 'former':
                x = DNA.former_city(encoded_parent_1, k)
                y = DNA.former_city(encoded_parent_2, k)

            # Find K in parents and remove.
            # print('----')
            # print(k)
            # print(encoded_parent_1)
            idx_of_k_parent_1 = np.where(encoded_parent_1 == k)[0]
            encoded_parent_1 = np.delete(encoded_parent_1,idx_of_k_parent_1)
            # print(k)
            # print(encoded_parent_2)
            idx_of_k_parent_2 = np.where(encoded_parent_2 == k)[0]
            encoded_parent_2 = np.delete(encoded_parent_2,idx_of_k_parent_2)
            
            dx = _map.get_distance_between_points(k, x)
            dy = _map.get_distance_between_points(k, y)

            if dx < dy:
                k = x
            else:
                k = y
            
            length = len(encoded_parent_1)
            result = np.append(result, k)
    
            # print(result)

        #child 2 generation based on random permutation of Child 1/Result
        
        child_2_encoded = np.append(result[0],np.random.permutation(result[1:len(result)]))

        child_1 = DNA(parent_1.n_buses, parent_1.map, parent_1.start_position, routes = parent_1.decode(result))
        
        child_2 = DNA(parent_1.n_buses, parent_1.map, parent_1.start_position, routes = parent_1.decode(child_2_encoded))
        
        return child_1, child_2



















