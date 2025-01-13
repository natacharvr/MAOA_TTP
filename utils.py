import math

def readFile(fileName) :
    # reads from fileName
    # returns titre, capacity, min_speed, max_speed, cities
    # cities is a dictionary xhere an entry  is key (int) : [(pos_x, pos_y), [(index, profit, weight), ...]]
    file = open(fileName, "r")

    lines = file.readlines()

    titre = lines[0].split()[2]
    nb_cities = (int)(lines[2].split()[1])

    capacity = (int)(lines[4].split()[3])
    nb_items = (int)(lines[3].split()[3])
    min_speed = (float)(lines[5].split()[2])
    max_speed = (float)(lines[6].split()[2])
    renting_ratio = (float)(lines[7].split()[2])

    cities = dict()
    for i in range(10, nb_cities+10, 1) :
        a,x, y = lines[i].split()
        cities[(int)(a)] = [((int)(x),(int)(y)), []]

    indice_items = 11 + nb_cities
    for i in range(indice_items, indice_items+nb_items, 1):
        a,b,c,d = lines[i].split()
        item = ((int)(a),(int)(b),(int)(c))
        cities[(int)(d)][1].append(item)
        # print(cities[(int)(d)])
    return titre, capacity, min_speed, max_speed, renting_ratio, cities

_, _, _, _, _, cities = readFile("a280_n279_bounded-strongly-corr_01.txt")

def calculate_distance(cityA, cityB, cities) :
    # a simple function to calculate the distance from cityA to cityB (the index of the cities)
    # print("cities", cities)
    if cityA == cityB : return 0
    posxA, posyA = cities[cityA][0]
    posxB, posyB = cities[cityB][0]
    #print(posxA, posyA, posxB, posyB)
    return math.sqrt((posxB -posxA)**2 + (posyB - posyA)**2)

# print(calculate_distance(125,124, cities))

def calculate_value_ratio(object):
    profit = object[1]
    weight = object[2]
    return profit/weight

def sortSecond(val):
        return val[1]

def objective_function_linear(cities, knapsack_content, K, tour) : 
    # knapsack_content is a list of tuples (index, profit, weight, cityKey)
    # tour is a list of the idex of the cities
    first_term = 0
    for item in knapsack_content :
          first_term += item[1]
    
    second_term = 0
    weight = 0
    for i in range(len(tour)-1) :
        for item in knapsack_content:
            if item[3] == tour[i] :
                weight += item[2] 
        second_term += calculate_distance(tour[i], tour[i+1], cities) * weight
    second_term += calculate_distance(tour[0], tour[-1], cities) * weight

    return first_term - K * second_term

def objective_function_non_linear(cities, knapsack_content, R, tour, vmax, vmin, capacity) :
    first_term = 0
    for item in knapsack_content :
          first_term += item[1]

    v = (vmax - vmin) / capacity
    second_term = 0
    weight = 0
    for i in range(len(tour)-1) :
        for item in knapsack_content:
            if item[3] == tour[i] :
                weight += item[2] 
        second_term += calculate_distance(tour[i], tour[i+1], cities) / (vmax - v * weight)
    second_term += calculate_distance(tour[0], tour[-1], cities) / (vmax - (v * weight))
    return first_term - R * second_term