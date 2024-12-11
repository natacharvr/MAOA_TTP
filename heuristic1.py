import utils 
import copy
# calculate ratio of items (value/weight), sort in ascending order
# take most objects with high ratio
# create a tour with the cities of the objects at the end of the tour
# order cities "de propche en proche" with objects at the end
# titre, capacity, min_speed, max_speed, cities = utils.readFile("a280_n279_bounded-strongly-corr_01.txt")
# titre, capacity, min_speed, max_speed, cities = utils.readFile("a280_n1395_uncorr-similar-weights_05.txt")


def order_objects(cities) :
    objects = []

    for key, value in cities.items() :
        for o in value[1] :
            ratio = utils.calculate_value_ratio(o)
            objects.append((o[0], ratio, o[2], key)) # index, ratio, weight, cityKey
    
    objects.sort(key=utils.sortSecond, reverse=True)
    return objects

def select_items(cities, capacity) :
    objects = order_objects(cities)
    selected_objects = []
    fill = 0
    for index, profit, weight, cityKey in objects :
        if fill + weight < capacity :
            selected_objects.append((index, profit, weight, cityKey))
            fill += weight
    return selected_objects

def distances_to_city(cityA, cities) :
    distances = dict()
    for city, _ in cities.items() :
        distances[city] = utils.calculate_distance(cityA, city, cities)
    return distances

def closest_city(cityA, cities) :
    if len(cities) == 1 :
        return
    distances = distances_to_city(cityA, cities)
    distances.pop(cityA)
    return min(distances.items(), key=lambda x: x[1])

def tour(cities, init) :
    # calculates a tour tha goes from one city to its closest non explored city
    tour = [init]
    cities_cpy = copy.deepcopy(cities)
    current_city = init
    tour_length = 0

    while len(cities_cpy) > 1 :
        next_city = closest_city(current_city, cities_cpy)
        cities_cpy.pop(current_city)
        tour.append(next_city[0])
        tour_length += next_city[1]
        current_city = next_city[0]
    tour_length += utils.calculate_distance(tour[0], tour[-1], cities)
    return tour, tour_length

def tour_with_knapsack(cities, capacity):
    selected_objects = select_items(cities, capacity)
    cities_with_object = dict()
    for item in selected_objects :
        cities_with_object[item[3]] = cities[item[3]]

    c = dict()
    for a in cities :
        if a not in cities_with_object :
            c[a] = cities[a]

    t, tour_length = tour(c, 1)

    last = t[-1]
    cities_with_object[last] = cities[last]
    t1, tour_length1 = tour(cities_with_object, last)

    t+=t1[1:]
    tour_length += tour_length1
    return t, selected_objects

# with our idea
# t, objects = tour_with_knapsack(cities, capacity)
# print(utils.objective_function_non_linear(cities, objects, 1, t, max_speed, min_speed, capacity))

# # without our idea
# t = tour(cities, 1)[0]
# objects = select_items(cities, capacity)

# print(utils.objective_function_non_linear(cities, objects, 1, t, max_speed, min_speed, capacity))
# without our idea is much better :(


# idée d'heuristique : on fait un bon tour, et on prend le maximum d'objets venant des derniers sommets du tour