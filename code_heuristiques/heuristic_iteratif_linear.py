import utils
import random
import time
import heuristic_gloutonne_linear
import matplotlib.pyplot as plt

MAX_ITERATIONS = 10000
FILENAME = "datas/a280_n279_bounded-strongly-corr_01.txt"
titre, capacity, min_speed, max_speed, renting_ratio, cities = utils.readFile(FILENAME)

# we will try to optimize the knaosack and the tour created

def select_items_linear_proba(objects, capacity, proba) :
    """
    Selects objects by their ratio (value/weight)/distance_to_origin, the most interesting objects first, and takes the most objects possible
    it only takes an object if it fits in the knapsack
    objects is a list of objects ordered by interest (higher to lower)
    capacity (int) the maximum capacity of the knapsack
    proba is the probablity in [0,1] to take an object when it fits
    """
    selected_objects = []
    fill = 0
    for index, profit, weight, cityKey in objects :
        choice = random.choices([0,1], [proba, 1-proba])[0]
        if fill + weight < capacity and  choice: 
            selected_objects.append((index, profit, weight, cityKey))
            fill += weight
    return selected_objects

def optimize_tour(cities, renting_ratio):
    """
    Calculates a solution with glutton algo and tries to optimize the objective function by changing randomly the
    knapsack and therefore the associated tour
    """
    origin = 1

    current_tour, knapsack_content = heuristic_gloutonne_linear.tour_with_knapsack_linear(cities, capacity)
    valuation = utils.objective_function_linear(cities, knapsack_content, renting_ratio, current_tour)
    log_valuation = [valuation]

    #we timeout after 10 minutes or when the best value did not change in 10 000 iterations
    objects = heuristic_gloutonne_linear.order_objects_by_value_and_distance(cities, origin)

    counter = 0
    best_tour = current_tour
    start = time.time()
    while (time.time() - start < 120) and counter < MAX_ITERATIONS : # TODO change here the timeoout
        # TODO proba is okay ? When we have not moved in some time, we change more the knapsack proba
        new_tour, knapsack_content = randomize_tour_linear(cities, current_tour, capacity, objects, counter/MAX_ITERATIONS)
        val = utils.objective_function_linear(cities, knapsack_content, renting_ratio, new_tour)
        # only keep the change if it improves the solution
        if val > valuation :
            print(val)
            valuation = val
            counter = 0
            best_tour = new_tour
        else : 
            counter += 1
        log_valuation.append(valuation)
    return best_tour, log_valuation        

def randomize_tour_linear(cities, current_tour, capacity, objects, proba) :
    """ 
    Selects an interesting knapsack with randomness and modifies the tour 
    to finish by the cities with picked objects
    """
    # select objects with given proba
    selected_objects = select_items_linear_proba(objects, capacity, proba)

    # exctract the cities with objects 
    cities_with_object = dict()
    for item in selected_objects :
        cities_with_object[item[3]] = cities[item[3]]
    # remove the cities with objects to add them at the end
    for city, _ in cities_with_object.items() :
        current_tour.remove(city)

    # add at the end of the tour the cities with objects
    last = current_tour[-1]
    cities_with_object[last] = cities[last]
    t1, _ = heuristic_gloutonne_linear.tour(cities_with_object, last)

    current_tour+=t1[1:]
    return current_tour, selected_objects

# t, objects = heuristic_gloutonne_linear.tour_and_len_with_knapsack(cities, capacity)
# print(t)
# print("HERE \n")
# randomize_longest_edge(t)
tour,b = optimize_tour(cities, renting_ratio)
plt.plot(b)
plt.show()
print(b)
f = open("output_iteratif_a280_n279_bounded-strongly-corr_01.txt", 'w')


# other idea : we try to break the longest distance
# we select (probably) the city wit the longest distance to travel and swap it with another city at random
# we need to use a lisr of tuples with (origin, distance to travel) ordered, the we have only two distances to recalculate at each step
# probleme de avec quoi relier (genre si on prends l'arete la plus grande, comment choisir quelle autre arete pour ameliorer?)

### INFOS SUPPLEMENTAIRES ###
# Comment comparer (valeur finale, temps d'exec, prendre en compte que le truc de la competition est faite en java et non python)
# visualisation des donnees au choix (villes, items, chemins) utiliser des tableaux et figures
# commenter le code rajouter le lien vers le code dans le rapport
# Ecrire les algos en pseudo-code et en anglais si on veut
# rendu au plus tard le 20 janvier