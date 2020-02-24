import numpy as np
from components.mapping.route import Route
from components.mapping.point import Point
import random
import requests
import json
class Map:

    '''
    The map is an adjacency matrix of all points, thus the Map
    '''
    def __init__(self, points):
        self.adj_mat = np.empty(shape=(len(points),len(points)), dtype=Route)
        self.points = points
        self.fill_adj_mat()
    def fill_adj_mat(self):
        '''
        Initialize with random values for distances
        '''
        shape = self.adj_mat.shape[0]
        for i in range(shape):
            for j in range(shape):
                self.adj_mat[i,j] = Route(self.points[i], self.points[j])

    def get_distance_between_points(self, i, j):
        return self.adj_mat[i,j]._get_distance()

class OpenApiMap(Map):
    
    def fill_adj_mat(self):
        url = 'https://api.openrouteservice.org/v2/matrix/driving-car'

        api_token = '5b3ce3597851110001cf6248c92a8f952cf540049f8b8450065eeacb'
        payload = f'''{{
            "locations" : {[[p.coordinates[1],p.coordinates[0]] for p in self.points]},
            "metrics":["distance"],
            "units":"km"
        }}'''
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': '5b3ce3597851110001cf6248c92a8f952cf540049f8b8450065eeacb',
            'Content-Type': 'application/json; charset=utf-8'
        }

        print('Calling Api')
        response = requests.post(url=url,data=payload, headers=headers)
        print("Finished Calling Api")
        matrix_response = response.json()['distances']
        shape = self.adj_mat.shape[0]
        for i in range(shape):
            for j in range(shape):
                self.adj_mat[i,j] = matrix_response[i][j]
    def get_distance_between_points(self, i, j):
        return self.adj_mat[i,j]