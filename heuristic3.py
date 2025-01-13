import math 
import utils

def calculate_matrix(cities) :
    matrix = [[math.inf for _ in range(len(cities)+1)] for _ in range(len(cities)+1)]

    # every city is in a group (to avoid building tours that do not contain every city)
    matrix[0][0] = ("", 0) # an empty cell at the top left corner
    for i in range(1, len(cities)+1) :
        # the title of a line/column is a tuple of the name of the city and the group in which it is 
        matrix[i][0] = (i,0) # title of row (city index starts at 0)
        matrix[0][i] = (i,0) # title of column
    
    for i in range(1, len(cities)+1) :
        for j in range(i, len(cities)+1):
            d = utils.calculate_distance(i, j, cities)
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix

def remove_line(matrix, line_name):
    # Find the row index to remove
    row_index = next((i for i, row in enumerate(matrix) if row[0][0] == line_name), None)
    if row_index is not None:
        del matrix[row_index]

def remove_column(matrix, column_name):
    # Find the column index to remove
    column_index = next((i for i, title in enumerate(matrix[0]) if title[0] == column_name), None)
    if column_index is not None:
        for row in matrix:
            del row[column_index]

# matrix = [[("",0), (1,0), (2,0)], [(1,0), 1, 2], [(2,0), 3, 4]]

def print_matrix(matrix) : 
    for row in matrix :
        print(row, '\n')


def find_group(matrix, city) :
    for row in matrix :
        if row[0][0] == city: 
            return row[0][1]
    for line in matrix[0] :
        if line[0] == city :
            return line[1]
    # print(matrix, city)

def change_city_group(matrix, city, group) :
    for i in range(len(matrix)):
        # Check if the first element of the tuple matches the city
        if matrix[i][0][0] == city:
            matrix[i][0] = (city, group)  # Update row title
        if matrix[0][i][0] == city:
            matrix[0][i] = (city, group)  # Update column title

def merge_groups(matrix, group1, group2):
    """
    Merges two groups in the matrix by changing the group of all cities in the larger group
    to the group of the smaller one.
    
    Parameters:
        matrix (list): The matrix with row and column titles as tuples.
        group1 (int): The first group.
        group2 (int): The second group.
    """
    # Determine which group has the smaller and larger group number
    if group1 > group2:
        smaller_group, larger_group = group2, group1
    else:
        smaller_group, larger_group = group1, group2
    
    # Change all cities in the larger group to the smaller group
    for i in range(1, len(matrix)):  # Start from 1 to skip the header row
        if matrix[i][0][1] == larger_group:  # Check if the city belongs to the larger group
            city = matrix[i][0][0]  # Get the city index

            # Update the row
            matrix[i][0] = (city, smaller_group)

            # Update the column (first row)
            for j in range(1, len(matrix[i])):  # Loop over columns
                if matrix[0][j][0] == city:  # Find the city in the first row
                    matrix[0][j] = (city, smaller_group)  # Change the city group in the header


def find_smallest_distance(matrix):
    min_distance = math.inf
    min_position = (None, None)

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            # Skip the diagonal elements where i == j (distance to itself)
            # if i != j:
            if matrix[i][0][0] != matrix[0][j][0] : 
                city_i_group = matrix[i][0][1]  # Extract the group of city i
                city_j_group = matrix[0][j][1]  # Extract the group of city j

                # Skip pairs of cities in the same group (except group 0)
                if city_i_group != city_j_group or city_i_group == 0:
                    if matrix[i][j] < min_distance:
                        min_distance = matrix[i][j]
                        # Access city names from the first row and first column
                        min_position = (matrix[i][0][0], matrix[0][j][0])

    return min_distance, min_position

def build_path(matrix):
    int_group = 0
    path = []
    total_distance = 0

    while True:
        # print("heehe")
        # print_matrix(matrix)
        min_distance, (city1, city2) = find_smallest_distance(matrix)
        # print(min_distance, (city1, city2))
        # if min_distance == math.inf :
        #     break
        
        # Add the current pair to the path
        path.append((city1, city2))
        total_distance += min_distance
        
        # Merge the two cities' groups
        group1 = find_group(matrix, city1) # we add 1 to skip the headers
        group2 = find_group(matrix, city2)
        # if one city is not in a group yet, we just add it to the group
        if group1 == 0 and group2 != 0 :
            change_city_group(matrix, city1, group2)
        elif group2 == 0 and group1 != 0 : 
            change_city_group(matrix, city2, group1)

        # if neither cities are in a group, we create a new group
        elif group1 == group2 == 0 :
            int_group += 1
            change_city_group(matrix, city1, int_group)
            change_city_group(matrix, city2, int_group)

        # if both cities are in different groups, we merge the groups
        else :
            merge_groups(matrix, group1, group2)
        
        # Remove the row and column of the intersection (only once, theother intersection is forbidden by the groups)
        remove_line(matrix, city1)
        remove_column(matrix, city2)
        
        # Check if all cities are in the same group (other than 0)
        # groups = {matrix[i][0][1] for i in range(1, len(matrix))}
        # if len(groups) == 1 and 0 not in groups:
        if len(matrix) == 2 and len(matrix[0]) == 2:
            # print_matrix(matrix)
            # print("hehe")
            break
    
    return path, total_distance

def extract_tour_from_edges(edges):
    # Initialize an empty list to store the tour order of cities
    cities_in_order = []

    # Create a map that connects each city to its neighbors
    city_map = {}

    # Populate the city_map with the edges
    for city1, city2 in edges:
        if city1 not in city_map:
            city_map[city1] = []
        if city2 not in city_map:
            city_map[city2] = []
        city_map[city1].append(city2)
        city_map[city2].append(city1)

    # Start from the first city in the edges list (or any city in the cycle)
    current_city = next(city for city, neighbors in city_map.items() if len(neighbors) == 1)
    
    # Add the starting city to the tour
    cities_in_order.append(current_city)


    # Traverse the cities in the cycle
    while len(city_map) > len(cities_in_order):
        # Get the neighbors of the current city
        neighbors = city_map[current_city]
        
        # We move to the neighbor that is not the one we came from
        if len(neighbors) > 1 :
            next_city = neighbors[0] if neighbors[1] == cities_in_order[-1] else neighbors[1]
        else : 
            next_city = neighbors[0]
        
        # Add the next city to the tour
        cities_in_order.append(next_city)
        
        city_map[current_city].remove(next_city)
        city_map[next_city].remove(current_city)
        # Move to the next city
        current_city = next_city
    
    return cities_in_order


# Example matrix with city names in the first row and first column
# matrix = [
#     [("", 0), ("A", 0), ("B", 0), ("C", 0), ("D", 0)],  # First row: city names and titles
#     [("A", 0), 0, 2, 3, 1],  # First column: city 0
#     [("B", 0), 2, 0, 4, 1],  # First column: city 1
#     [("C", 0), 3, 4, 0, 3],  # First column: city 2
#     [("D", 0), 1, 1, 3, 0]
# ]

# min_distance, cities = find_smallest_distance(matrix)
# print(f"Smallest distance: {min_distance} between cities {cities}")

# merge_groups(matrix, 1, 0)
# change_city_group(matrix, cities[0], 1)
# change_city_group(matrix, cities[1], 1)

# remove_column(matrix, cities[0])
# remove_line(matrix, cities[1])
# print_matrix(matrix)
# print(build_path(matrix))
titre, capacity, min_speed, max_speed, renting_ratio, cities = utils.readFile("fnl4461_n4460_bounded-strongly-corr_01.txt")

matrix = calculate_matrix(cities)
print("here")
# print_matrix(matrix)
edges, length = build_path(matrix)
print(length)
# print(extract_tour_from_edges(edges))