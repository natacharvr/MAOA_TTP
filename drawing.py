# import utils
import numpy as np
import cv2
# import heuristic1
import math

def min_max_pos(cities) :
    max_x = 0
    max_y = 0
    min_x = math.inf
    min_y = math.inf
    for _, values in cities.items() :
        max_x = max(max_x, values[0][0])
        max_y = max(max_y, values[0][1])
        min_x = min(min_x, values[0][0])
        min_y = min(min_y, values[0][1])
    return(min_x, min_y, max_x, max_y)

def make_visu(cities, tour, filename):
    min_x, min_y, max_x, max_y = min_max_pos(cities)
    size_x = max_x - min_x
    size_y = max_y - min_y
    img = np.zeros(((size_y + 50), (size_x + 50), 3), dtype = "uint8") 
    for city, values in cities.items() :
        coord_x, coord_y = values[0]
        coord_x -= min_x
        coord_y -= min_y
        cv2.circle(img, (coord_x, coord_y), 1, (255, 255, 255), 2) 


    for i in range(len(tour)-1) :
        coord_x, coord_y = cities[tour[i]][0]
        coord_x2, coord_y2 = cities[tour[i+1]][0]
        coord_x -= min_x
        coord_x2 -= min_x
        coord_y -= min_y
        coord_y2 -= min_y
        cv2.line(img,(coord_x, coord_y), (coord_x2, coord_y2), (255,i%255,i%255), 2)
    coord_x, coord_y = cities[tour[0]][0]
    coord_x2, coord_y2 = cities[tour[-1]][0]
    coord_x -= min_x
    coord_x2 -= min_x
    coord_y -= min_y
    coord_y2 -= min_y
    cv2.line(img, (coord_x, coord_y), (coord_x2, coord_y2), (255,i%255,i%255), 2)

    cv2.imshow('dark', img) 
    
    # Allows us to see image 
    # until closed forcefully 
    cv2.imwrite(filename, img)

    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
# filename = "a280_n1395_uncorr-similar-weights_05"
# titre, capacity, min_speed, max_speed, cities = utils.readFile(filename+".txt")
# tour = heuristic1.tour_with_knapsack(cities, capacity)[0]

# make_visu(cities, tour, filename+".jpg")
# tour = heuristic1.tour(cities, 1)[0]
# make_visu(cities, tour, filename+"2.jpg")
