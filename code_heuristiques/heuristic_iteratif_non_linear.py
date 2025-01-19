import utils
import random
import time
import heuristic_gloutonne_non_linear

MAX_ITERATIONS = 10000
MAX_TIME = 120

# we will try to optimize the tour rather than the knapsack

def optimize_tour(cities, renting_ratio, type="simple"):
    """
    Calculates a tour and knapsack with the glutton method and tries to optimize it
    There are three methods : simple, with length and 2-opt
    simple : exchanges cities randomly and keeps the change if it improves the solution
    with length : finds the longest edge of the tour and exchanges with a random other city of the tour, only keeps the chaneg if it is better 
    2-opt : iteratively improves the tour, and selects a knapsack interesting from the end of the tour. Keeps if change is better
    """
    # tour, _ = heuristic_gloutonne_non_linear.tour(cities, 1)
    # knapsack_content = heuristic_gloutonne_non_linear.select_items(cities, capacity, tour)
    tour, knapsack_content = heuristic_gloutonne_non_linear.tour_with_knapsack_non_linear(cities, capacity)

    #we timeout after 10 minutes or when the best value did not change in 10 000 iterations
    match type:
        case "simple":
            valuation = utils.objective_function_non_linear(cities, knapsack_content, renting_ratio, tour, max_speed, min_speed, capacity)
            print(valuation)
            log_valuation = [valuation]
            counter = 0
            best_tour = tour
            start = time.time()
            while (time.time() - start < MAX_TIME) and counter < MAX_ITERATIONS : # TODO change here the timeoout
                new_tour = randomize_tour(tour)
                val = utils.objective_function_non_linear(cities, knapsack_content, renting_ratio, new_tour, max_speed, min_speed, capacity)
                # only keep the change if it improves the solution
                if val > valuation :
                    print(val)
                    valuation = val
                    counter = 0
                    best_tour = new_tour
                else : 
                    counter += 1
                log_valuation.append(valuation)
            return best_tour, log_valuation, knapsack_content
        
        # TODO can we exchange with closest neighbor ?
        case "with_length":
            # we calculate the length of each edge for easier computation
            tour_distance = []
            for i in range(len(tour)) : 
                tour_distance.append((tour[i], utils.calculate_distance(tour[i], tour[(i+1)%len(tour)], cities)))
            tour = tour_distance
            # if(type(tour[0]) == int):
            #     raise Exception("Give a list of cities with the distance to the next one")
            
            valuation = utils.objective_function_non_linear(cities, knapsack_content, renting_ratio, [val for (val, _) in tour], max_speed, min_speed, capacity)
            log_valuation = [valuation]
            counter = 0
            best_tour = tour
            start = time.time()
            while (time.time() - start < MAX_TIME) and counter < MAX_ITERATIONS : # TODO change here the timeoout
                new_tour = randomize_longest_edge(tour, cities, counter/MAX_ITERATIONS)
                val = utils.objective_function_non_linear(cities, knapsack_content, renting_ratio, [val for (val,_) in new_tour], max_speed, min_speed, capacity)
                
                # only keep the change if it improves the solution
                if val > valuation :
                    print(val)
                    valuation = val
                    counter = 0
                    best_tour = new_tour
                else : 
                    counter += 1
                log_valuation.append(valuation)
            return best_tour, log_valuation, knapsack_content
         
        case "2-opt":
            best_tour_length = utils.calculate_tour_len(tour, cities)
            valuation = utils.objective_function_non_linear(cities, knapsack_content, renting_ratio, tour, max_speed, min_speed, capacity)
            print(valuation)
            log_valuation = [valuation]
            counter = 0
            best_tour = tour
            start = time.time()
            improved = False

            while (time.time() - start < MAX_TIME) and counter < MAX_ITERATIONS:
                for i in range(0, len(tour)) :
                    for j in range(i+1, len(tour)) :
                        new_tour = two_opt_swap(tour, i, j)
                        tour_length = utils.calculate_tour_len(new_tour, cities)
                        if tour_length < best_tour_length :
                            new_knapsack_content = heuristic_gloutonne_non_linear.select_items(cities, capacity, new_tour, min(100*counter/MAX_ITERATIONS, 0.99))
                            val = utils.objective_function_non_linear(cities, new_knapsack_content, renting_ratio, new_tour, max_speed, min_speed, capacity)
                            if val > valuation :
                                print(val)
                                tour = new_tour
                                knapsack_content = new_knapsack_content
                                valuation = val
                                best_tour = new_tour
                                improved = True
                                counter = 0
                                break
                    if improved :
                        break
                counter += 1
                # print(counter)
                log_valuation.append(valuation)
            return best_tour, log_valuation, knapsack_content

def randomize_tour(tour) :
    """ 
    Randomly exchanges cities in a tour
    tour is a list of index of cities
    """
    nb_cities = len(tour)
    # probas = [1-1/nb_cities, 1/nb_cities]
    probas = [0.7, 0.3]
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


def randomize_longest_edge(tour, cities, proba) :
    """
    randomly exchanges cities in the tour (up to 100 exchanges)

    tour is a list of tuples (cityIndex, distance to next city)
    proba is the probability to NOT select the longest edge to exchange it (if not selected, will select the next edge with proba)
    """
    nb_cities = len(tour)
    # probas = [1-1/nb_cities, 1/nb_cities]
    
    # on sort les edges en taille decroissante
    sorted_cities = sorted(tour,key=lambda city: city[1],reverse=True)
    probas = [proba, 1-proba]
    for _ in range(10) :
        for i in range(0, nb_cities) :
                # we swap the longest edge with probability of 1-proba
                choice = random.choices([0,1], probas)
                if choice :
                    city1 = sorted_cities[i]

                    city2_index = random.randint(0,nb_cities-1)
                    city2 = tour[city2_index]
                    
                    # we swap the two cities
                    city1_index = -1
                    for j in range(len(tour)) :
                        if tour[j][0] == city1[0] :
                            city1_index = j
                            break
                    tour[city1_index] = city2
                    tour[city2_index] = city1

                    # we recalculate the length of the new edges selected
                    tour[(i-1)%len(tour)] = (tour[(i-1)%len(tour)][0],utils.calculate_distance(tour[i][0], tour[(i-1)%len(tour)][0], cities))
                    tour[i] = (tour[i][0], utils.calculate_distance(tour[i][0], tour[(i+1)%len(tour)][0], cities))
                    tour[city2_index] = (tour[city2_index][0], utils.calculate_distance(tour[city2_index][0], tour[(city2_index+1)%len(tour)][0], cities))
                    tour[(city2_index-1)%len(tour)] = (tour[(city2_index-1)%len(tour)][0], utils.calculate_distance(tour[city2_index][0], tour[(city2_index-1)%len(tour)][0], cities))
                    break
    return tour

def two_opt_swap(tour, i, k):
                """ 
                Swaps the tour to create a new tour by reversing the order of the cities between i and k 
                """
                new_tour = tour[0:i]
                new_tour.extend(reversed(tour[i:k + 1]))
                new_tour.extend(tour[k + 1:])
                return new_tour

# t, objects = heuristic_gloutonne_non_linear.tour_with_knapsack_non_linear(cities, capacity)
# objects = heuristic_gloutonne_non_linear.select_items(cities, capacity)
# t, _ = heuristic_gloutonne_non_linear.tour(cities, 1)
# print(t)


import json
filenames = ["a280_n279_bounded-strongly-corr_01", "a280_n1395_uncorr-similar-weights_05", "fnl4461_n4460_bounded-strongly-corr_01"]

for filename in filenames :
    print(filename)
    titre, capacity, min_speed, max_speed, renting_ratio, cities = utils.readFile("datas/"+filename+".txt")

    b_log = []
    for i in range(10) : 
        print(i)
        tour,b,knapsack = optimize_tour(cities, renting_ratio, "2-opt")
        b_log.append(b)
    title = str(len(tour)) + " cities"
    # b = []
    # for i in range(max([len(item) for item in b_log])) :
    #     temp =[b_log[j][i] for j in range(len(b_log)) if len(b_log[j]) > i]
    #     b.append(sum(temp)/len(temp))

    # plots.plot_valuation(b, title, filename+"test")
    print(b_log)
    with open(filename+"output.json", "w") as f:
        json.dump(b_log, f)
    
