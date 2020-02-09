from components.mapping.point import Point
from random import randint
import pickle as pkl

number_of_points = 150

min_range_x = 10
max_range_x = 500

min_range_y = 10
max_range_y = 500

points_list = [Point(x=randint(min_range_x,max_range_x), y=randint(min_range_y,max_range_y)) for i in range(number_of_points)]
with open('../points.pkl', 'wb') as points_file:
    pkl.dump(points_list, points_file)


