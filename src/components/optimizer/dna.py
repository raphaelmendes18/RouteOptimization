from point import Point
from map import Map
import random
import numpy as np
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
            assert isinstance(start_position), int)
            assert isinstance(_map, Map)
        except AssertionError:
            raise AssertionError('Error Creating DNA Object - Unexpected Types')

        self.n_buses = n_buses
        self.map = _map
        self.start_position = start_position
        self.fitness = np.inf
        if routes == None:
            self.routes = initialize_routes()
        else:
            self.routes = routes
    
    def initialize_routes(self):

        routes = np.array([np.array([]) for i in range(self.map.shape[0])])
        for r in routes:
            r[0] = self.start_position #Start Position
        
        visited_stops = numpy.zeros((self._map.shape[0]), dtype=bool)
        
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
        if self.fitness != np.inf:
            routes_cost = np.zeros(shape=self.routes.shape[0],dtype=float)
            for idx,r in enumerate(self.routes):
                routes_cost[idx] = DNA.get_route_cost(r)

            self.fitness = max(routes_cost)      

    def get_route_cost(r):
        cost = 0.0
        for i in range(len(r)-1):
            cost += self.map.get_distance_between_points(r[i], r[i+1])
        return cost

    def mutation(self, n_perm = 4):
        '''
        Mutation will be a set of permutations between 2 random routes
        '''
        for i in range(n_perm):
            route_1 = random.sample(self.routes,k=1)[0]
            route_2 = random.sample(self.routes,k=1)[0]
            if len(route_1) > 1:
                pos_1 = random.randint(1,len(route_1)-1)
                if len(route_2) > 1:  
                    pos_2 = random.randint(1,len(route_2)-1)

                    aux = route_1[pos_1]
                    route_1[pos_1] = route_2[pos_2]
                    route_2[pos_2] = aux
                else:
                    route_2 = np.append(route_2,route_1[pos_1])
                    route_1 = np.delete(route_1,pos_1)
            else:
                if len(route_2) > 1:  
                    pos_2 = random.randint(1,len(route_2)-1)
                    
                    route_1 = np.append(route_1, route_2[pos_2])
                    route_2 = np.delete(route_2,pos_2)
                else:
                    pass

    def latter_city(self, k):
        '''
        Identify the stop that comes after stop K
        '''
        encoded = self.encode()
        idx_of_city = np.where(encoded == k)[0][0]
        
        if idx_of_city == len(encoded):
            return self.start_position
        else:
            return encoded[idx_of_city + 1]

    def former_city(self, k):
        '''
        Identify the stop that comes before stop K
        '''
        encoded = self.encode()
        idx_of_city = np.where(encoded == k)[0][0]
        
        if idx_of_city == 0:
            return self.start_position
        else:
            return encoded[idx_of_city - 1]

    def encode(self):
        '''
        Encode the routes into a single array
        to make it easier to manipulate and operate
        crossover.
        '''
        return np.flatten(self.routes)
    
    def decode(self, encoded_dna):
        '''
        Decode the encoded array into the matrix of routes
        '''
        route = -1
        routes = np.array([np.array([]) for i in range(self.map.shape[0])])
        for idx, el in encoded_dna:
            if el == self.start_position:
                route += 1
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
        encoded_parent_1 = np.unique(parent_1.encode())
        encoded_parent_2 = np.unique(parent_2.encode())

        length = len(encoded_parent_1)

        # get a random K
        k = encoded_parent_1[random.randint(1,length-1)]

        # result will store the child 1
        result = np.array([parent_1.start_position,k])

        while length > 1:
            if mark == 'latter':
                x = parent_1.latter_city(k)
                y = parent_2.latter_city(k)
            elif mark == 'former':
                x = parent_1.former_city(k)
                y = parent_2.former_city(k)

            # Find K in parents and remove.
            idx_of_k_parent_1 = np.where(parent_1 == k)[0][0]
            encoded_parent_1 = np.delete(encoded_parent_1,idx_of_k_parent_1)

            idx_of_k_parent_2 = np.where(parent_2 == k)[0][0]
            encoded_parent_2 = np.delete(encoded_parent_2,idx_of_k_parent_2)
            
            dx = _map.get_distance_between_points(k, x)
            dy = _map.get_distance_between_points(k, y)

            if dx < dy:
                k = x
            else:
                k = y

            length = len(encoded_parent_1)

            result = np.append(result, k)

            #child 2 generation based on random permutation of Child 1/Result
            child_2_encoded = np.append(result[0],np.random.permutation(result[1:len(result)]))

            child_1 = DNA(parent_1.n_buses, parent_1.map, parent_1.start_position, routes = parent_1.decode(result))
            child_2 = DNA(parent_1.n_buses, parent_1.map, parent_1.start_position, routes = parent_1.decode(child_2_encoded))

            return child_1, child_2



















