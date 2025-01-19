import matplotlib.pyplot as plt
import numpy as np

def plot_valuation(valuations, title, filename):
    plt.figure(figsize=(10, 6))  # Set figure size

    # Plot the valuation curve
    plt.plot(valuations, label="Valuation", color="teal", linewidth=2)

    # Add title and labels
    plt.title("Mean Valuation Over Iterations for "+title, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Iterations", fontsize=14)
    plt.ylabel("Valuation", fontsize=14)

    # Add grid for better readability
    plt.grid(alpha=0.3)

    # Add legend
    plt.legend(fontsize=12, loc='best')

    # Customize tick parameters
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Add tight layout for better spacing
    plt.tight_layout()

    plt.savefig(filename+".png", format='png')
    # plt.show()


def plot_mean_variation(valuations, nb_cities, filename=None, charasteristics=''):
    """
    Plots the mean and standard deviation of valuation data over iterations.

    Parameters:
        iterations (array-like): Array of iteration numbers.
        valuations (2D array-like): Valuations data with shape (num_runs, num_iterations).
        filename (str, optional): File path to save the plot. If None, the plot is displayed but not saved.
    """

    # Plot mean and standard deviation
    mean_values = []
    min_values = []
    max_values = []
    
    for i in range(max([len(item) for item in valuations])) :
        temp =[valuations[j][i] for j in range(len(valuations)) if len(valuations[j]) > i]
        mean_values.append(sum(temp)/len(temp))
        min_values.append(min(temp))
        max_values.append(max(temp))

    plt.figure(figsize=(10, 6))
    plt.plot(mean_values, label="Mean Valuation", color="teal", linewidth=2)
    plt.fill_between([i for i in range(max([len(item) for item in valuations]))], min_values, max_values, alpha=0.25, linewidth=0)

    # Customize the plot
    plt.title("Mean linear Valuation for " + str(nb_cities) +" cities" + charasteristics, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Iterations", fontsize=14)
    plt.ylabel("Valuation", fontsize=14)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=12, loc='best')

    # Adjust layout
    plt.tight_layout()

    # Save or display the plot
    if filename:
        plt.savefig(filename, format='png', dpi=300, bbox_inches='tight')
    else:
        plt.show()
import json
# Read the JSON file back into Python
with open("a280_n279_bounded-strongly-corr_01output.json", "r") as f:
    loaded_list_of_lists = json.load(f)

# print(loaded_list_of_lists)
plot_mean_variation(loaded_list_of_lists, 280, "a280_n279_bounded-strongly-corr_01_linear.png", " knapsack : bounded strongly corr")