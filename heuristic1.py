import utils 
import copy
# calculate ratio of items (value/weight), sort in ascending order
# take most objects with high ratio
# create a tour with the cities of the objects at the end of the tour
# order cities "de propche en proche" with objects at the end
titre, capacity, min_speed, max_speed, cities = utils.readFile("a280_n279_bounded-strongly-corr_01.txt")


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
    # print(type(c))

    t, tour_length = tour(c, 1)
    last = t[-1]
    cities_with_object[last] = cities[last]
    init = closest_city(last, cities_with_object)[0]
    t1, tour_length1 = tour(cities_with_object, last)

    t+=t1
    tour_length += tour_length1 + utils.calculate_distance(last, init, cities)
    return t, tour_length
# problem problem problem TODO

t, _ = tour_with_knapsack(cities, capacity)
t1, _ = tour(cities, 1)

t = t[1:]
print(t)
print(t1)
diff = 0
for i in range(len(t1)) :
    if t[i] != t1[i]:
        diff += 1
    else :
        print(i)
print("diff ", diff)
# print(order_objects(cities))