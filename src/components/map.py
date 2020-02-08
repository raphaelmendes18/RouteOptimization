import numpy as np
from route import Route
from point import Point
import random
class Map:

    '''
    The map is an adjacency matrix of all points, thus the Map
    '''
    def __init__(self, points):
        self.adj_mat = np.empty(shape=(len(points),len(points)), dtype=Route)
        self.points = points
    
    def fill_adj_mat(self):
        '''
        Initialize with random values
        '''
        shape = self.adj_mat.shape[0]
        for i in range(shape):
            for j in range(shape):
                self.adj_mat[i,j] = Route(self.points[i], self.points[j])

    def get_distance_between_points(self, i, j)
        return self.adj_mat[i,j]._get_distance()
