from point import Point
import random
import numpy as np
class DNA:
    
    def __init__(self, n_buses, _map, start_position, routes = None):
        self.n_buses = n_buses
        self.map = _map
        self.start_position = start_position
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
        routes_cost = np.zeros(shape=self.routes.shape[0],dtype=float)
        for idx,r in enumerate(self.routes):
            routes_cost[idx] = DNA.get_route_cost(r)

        return max(routes_cost)      

    def get_route_cost(r):
        cost = 0.0
        for i in range(len(r)-1):
            cost += self.map.get_distance_between_points(r[i], r[i+1])
        return cost

    def mutation(self, n_perm = 4):
        '''
        Mutation will be a set of permutations between 2 routes
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
        encoded = self.encode()
        idx_of_city = np.where(encoded == k)[0][0]
        
        if idx_of_city == len(encoded):
            return self.start_position
        else:
            return encoded[idx_of_city + 1]

    def former_city(self, k):
        encoded = self.encode()
        idx_of_city = np.where(encoded == k)[0][0]
        
        if idx_of_city == 0:
            return self.start_position
        else:
            return encoded[idx_of_city - 1]

    def encode(self):

        return np.flatten(self.routes)
    
    def decode(self, encoded_dna):

        route = -1
        routes = np.array([np.array([]) for i in range(self.map.shape[0])])
        for idx, el in encoded_dna:
            if el == self.start_position:
                route += 1
                routes[route] = np.append(routes[route], el)

        return routes

    def crossover(parent_1, parent_2, mark, _map):

        encoded_parent_1 = np.unique(parent_1.encode())
        encoded_parent_2 = np.unique(parent_2.encode())

        length = len(encoded_parent_1)

        k = encoded_parent_1[random.randint(1,length-1)]

        result = np.array([0,k])

        while length > 1:
            if mark == 'latter':
                x = parent_1.latter_city(k)
                y = parent_2.latter_city(k)
            elif mark == 'former':
                x = parent_1.former_city(k)
                y = parent_2.former_city(k)

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

            child_2_encoded = np.append(result[0],np.random.permutation(results[1:len(results)]))

            child_1 = DNA(parent_1.n_buses, parent_1.map, parent_1.start_position, routes = parent_1.decode(result))
            child_2 = DNA(parent_1.n_buses, parent_1.map, parent_1.start_position, routes = parent_1.decode(child_2_encoded))

            return child_1, child_2


















