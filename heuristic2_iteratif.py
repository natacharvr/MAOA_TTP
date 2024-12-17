import utils
import random
import time
import heuristic1
import matplotlib.pyplot as plt

MAX_ITERATIONS = 10000

titre, capacity, min_speed, max_speed, renting_ratio, cities = utils.readFile("a280_n279_bounded-strongly-corr_01.txt")

# we will try to optimize the tour rather than the knapsack

def optimize_tour(cities, knapsack_content, renting_ratio, tour):
    valuation = utils.objective_function_linear(cities, knapsack_content, renting_ratio, tour)
    log_valuation = [valuation]
    counter = 0
    best_tour = tour
    start = time.time()

    #we timeout after 10 minutes or when the best value did not change in 10 000 iterations
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
t, objects = heuristic1.tour_with_knapsack(cities, capacity)
t = [i for i in cities.keys()]
print(t)
print(randomize_tour(t))
_,b = optimize_tour(cities, objects, renting_ratio, t)
plt.plot(b)
plt.show()
# print(b)

# other idea : we try to break the longest distance
# we select (probably) the city wit the longest distance to travel and swap it with another city at random
# we need to use a lisr of tuples with (origin, distance to travel) ordered, the we have only two distances to recalculate at each step