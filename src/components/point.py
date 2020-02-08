

class Point:
    ''' 
    Class representing a point in space
    '''
    def __init__(self, name, x, y):
        self.name = name
        self.coordinates = np.array([x,y])

    