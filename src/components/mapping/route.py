import numpy as np


class Route:

    '''
    A route is a path from point A to point B measured in 
    distance and time
    '''
    def __init__(self, A, B):
        self.start = A
        self.end = B               

    def _get_distance(self):
        ''' 
        Euclidean Distance
        '''
        return np.linalg.norm(self.start.coordinates-self.end.coordinates)
        





