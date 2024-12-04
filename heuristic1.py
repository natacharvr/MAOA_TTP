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


print(order_objects(cities))