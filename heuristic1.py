import utils 

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
    for index, _, weight, cityKey in objects :
        if fill + weight < capacity :
            selected_objects.append((index, weight, cityKey))

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

def tour(cities) :
    # calculates a tour tha goes from one city to its closest non explored city
    tour = [1]
    cities_cpy = cities.copy()
    current_city = 1
    tour_length = 0

    while len(cities_cpy) > 1 :
        next_city = closest_city(current_city, cities_cpy)
        cities_cpy.pop(current_city)
        tour.append(next_city[0])
        tour_length += next_city[1]
        current_city = next_city[0]
    return tour, tour_length


print(tour(cities))

# print(order_objects(cities))