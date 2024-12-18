import utils
import random
import time
import heuristic1
import matplotlib.pyplot as plt

MAX_ITERATIONS = 10000

titre, capacity, min_speed, max_speed, renting_ratio, cities = utils.readFile("a280_n279_bounded-strongly-corr_01.txt")

# we will try to optimize the tour rather than the knapsack

def optimize_tour(cities, knapsack_content, renting_ratio, tour, type="simple"):
    
    #we timeout after 10 minutes or when the best value did not change in 10 000 iterations
    match type:
        case "simple":
            valuation = utils.objective_function_linear(cities, knapsack_content, renting_ratio, tour)
            log_valuation = [valuation]
            counter = 0
            best_tour = tour
            start = time.time()
            while (time.time() - start < 60) and counter < MAX_ITERATIONS : 
                new_tour = randomize_tour(tour)

                val = utils.objective_function_linear(cities, knapsack_content, renting_ratio, new_tour)
                if val > valuation :
                    print(val)
                    valuation = val
                    counter = 0
                    best_tour = new_tour
                else : 
                    counter += 1
                log_valuation.append(valuation)
            return best_tour, log_valuation
        
        case "with_length":
            
            if(type(tour[0]) == int):
                raise Exception("Give a list of cities with the distance to the next one")
            
            valuation = utils.objective_function_linear(cities, knapsack_content, renting_ratio, tour)
            log_valuation = [valuation]
            counter = 0
            best_tour = tour
            start = time.time()
            while (time.time() - start < 60) and counter < MAX_ITERATIONS : 
                new_tour = randomize_longest_edge(tour)
                val = utils.objective_function_linear(cities, knapsack_content, renting_ratio, new_tour)
                if val > valuation :
                    print(val)
                    valuation = val
                    counter = 0
                    best_tour = new_tour
                else : 
                    counter += 1
                log_valuation.append(valuation)
            return best_tour, log_valuation            

def randomize_tour(tour) :
    nb_cities = len(tour)
    # probas = [1-1/nb_cities, 1/nb_cities]
    probas = [0.7, 0.3]
    for a in range(10) :
        for i in range(1, nb_cities) :
                # we swap two cities with probability of 1/n
                proba = random.choices([0,1], probas)
                if proba :
                    city1 = tour[i]
                    # city1 = random.randint(0, nb_cities)
                    city2_index = random.randint(1,nb_cities-1)
                    city2 = tour[city2_index]
                    
                    # we swap the two cities
                    tour[i] = city2
                    tour[city2_index] = city1
    return tour


def randomize_longest_edge(tour) :
    nb_cities = len(tour)
    # probas = [1-1/nb_cities, 1/nb_cities]
    
    # on sort les edges en taille decroissante
    sorted_cities = sorted(tour,key=lambda city: city[1],reverse=True)
    print(sorted_cities)
    probas = [0.7, 0.3]
    for _ in range(10) :
        for i in range(1, nb_cities) :
                # we swap two cities with probability of 1/n
                proba = random.choices([0,1], probas)
                if proba :
                    city1,_ = sorted_cities[1]
                    # city1 = random.randint(0, nb_cities)
                    city2_index = random.randint(1,nb_cities-1)
                    city2 = tour[city2_index]
                    
                    # we swap the two cities
                    tour[i] = city2
                    tour[city2_index] = city1
    return tour



t, objects = heuristic1.tour_and_len_with_knapsack(cities, capacity)
print(t)
print("HERE \n")
randomize_longest_edge(t)

# _,b = optimize_tour(cities, objects, renting_ratio, t)
# plt.plot(b)
# plt.show()
# print(b)

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