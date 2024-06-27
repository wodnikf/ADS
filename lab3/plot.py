import matplotlib.pyplot as plt

def plot_graph(cities, graph, title, tsp_path=None):
    plt.figure(figsize=(8, 8))
    plt.title(title)
    for i, city in enumerate(cities):
        plt.plot(city[0], city[1], 'o', markersize=10, label=f'City {i}')
        plt.text(city[0], city[1], f' {i}', fontsize=12, ha='right')
    
    for i, neighbors in graph.items():
        for neighbor, distance in neighbors:
            x_values = [cities[i][0], cities[neighbor][0]]
            y_values = [cities[i][1], cities[neighbor][1]]
            plt.plot(x_values, y_values, 'b-', alpha=0.5)

    if tsp_path:
        for i in range(len(tsp_path) - 1):
            x_values = [cities[tsp_path[i]][0], cities[tsp_path[i + 1]][0]]
            y_values = [cities[tsp_path[i]][1], cities[tsp_path[i + 1]][1]]
            plt.plot(x_values, y_values, 'r-', linewidth=2)
    
    plt.xlim(-110, 110)
    plt.ylim(-110, 110)
    plt.legend()
    plt.grid(True)
    #plt.show()
    plt.savefig(title)
