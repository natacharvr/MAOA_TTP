import code_heuristiques.utils as utils 
import copy
import time
# calculate ratio of items (value/weight), sort in ascending order
# take most objects with high ratio
# create a tour with the cities of the objects at the end of the tour
# order cities "de propche en proche" with objects at the end
titre, capacity, min_speed, max_speed, renting_ratio, cities = utils.readFile("fnl4461_n4460_bounded-strongly-corr_01.txt")

def order_objects(cities) :
    """
    Orders objects by their ratio value/weight
    returns a list of tuples (index, ratio, weight, cityKey)
    cities is a dictionary where an entry  is key (int) : [(pos_x, pos_y), [(object_index, profit, weight), ...]]
    """
    objects = []

    for key, value in cities.items() :
        for o in value[1] :
            ratio = utils.calculate_value_ratio(o)
            objects.append((o[0], ratio, o[2], key)) # index, ratio, weight, cityKey
    
    objects.sort(key=utils.sortSecond, reverse=True)
    return objects

def select_items(cities, capacity) :
    """
    Selects objects by their ratio value/weight, the most interesting objects first, and takes the most objects possible
    it only takes an object if it fits in the knapsack
    cities is a dictionary where an entry  is key (int) : [(pos_x, pos_y), [(object_index, profit, weight), ...]]
    capacity (int) the maximum capacity of the knapsack
    """
    objects = order_objects(cities)
    selected_objects = []
    fill = 0
    for index, profit, weight, cityKey in objects :
        if fill + weight < capacity :
            selected_objects.append((index, profit, weight, cityKey))
            fill += weight
    return selected_objects

def distances_to_city(cityA, cities) :
    """
    Returns a dictionnary of the distances from cityA to all the other cities
    cities is a dictionary where an entry  is key (int) : [(pos_x, pos_y), [(object_index, profit, weight), ...]]
    cityA is the index of the city
    """
    distances = dict()
    for city, _ in cities.items() :
        distances[city] = utils.calculate_distance(cityA, city, cities)
    return distances

def closest_city(cityA, cities) :
    """
    Returns the closest city from cityA in cities
    cities is a dictionary where an entry  is key (int) : [(pos_x, pos_y), [(object_index, profit, weight), ...]]
    cityA is the index if the city
    """
    if len(cities) == 1 :
        return
    distances = distances_to_city(cityA, cities)

    # we remove cityA from the dictionnary because it is at distance zero from itself
    distances.pop(cityA)
    return min(distances.items(), key=lambda x: x[1])

def tour(cities, origin) :
    """
    Calculates a tour that goes from one city to its closest non explored city
    cities is a dictionary where an entry  is key (int) : [(pos_x, pos_y), [(object_index, profit, weight), ...]]
    origin is the index of the first city of the tour
    """
    tour = [origin]
    cities_cpy = copy.deepcopy(cities)
    current_city = origin
    tour_length = 0

    # as long as there are unvisited cities
    while len(cities_cpy) > 1 : # we put strict because at every iteration the current_city is still in the dict
        next_city = closest_city(current_city, cities_cpy)
        cities_cpy.pop(current_city)
        tour.append(next_city[0])
        tour_length += next_city[1]
        current_city = next_city[0]
    
    # we add the distance from the last city to the origin
    tour_length += utils.calculate_distance(tour[0], tour[-1], cities)
    return tour, tour_length

def tour_with_knapsack_non_linear(cities, capacity):
    """
    Calculates the most interesting objects and constructs a tour that goes to the closest 
    neighbor and finishes by the cities with objects
    cities is a dictionary where an entry  is key (int) : [(pos_x, pos_y), [(object_index, profit, weight), ...]]
    capacity (int) the maximum capacity of the knapsack
    """
    selected_objects = select_items(cities, capacity)
    cities_with_object = dict()
    for item in selected_objects :
        cities_with_object[item[3]] = cities[item[3]]

    # construct a new dict of the cities that have no objects to construct a tour over these
    c = dict()
    for a in cities :
        if a not in cities_with_object :
            c[a] = cities[a]

    t, tour_length = tour(c, 1)

    # add at the end of the tour the cities with objects
    last = t[-1]
    cities_with_object[last] = cities[last]
    t1, tour_length1 = tour(cities_with_object, last)

    t+=t1[1:]
    tour_length += tour_length1
    return t, selected_objects


t, objects = tour_with_knapsack_non_linear(cities, capacity)
print(utils.objective_function_non_linear(cities, objects, renting_ratio, t, max_speed, min_speed, capacity))
