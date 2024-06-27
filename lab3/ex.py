import random
import math
from plot import plot_graph
from collections import deque
import heapq

def generate_cities(n, range_min=-100, range_max=100):
    return [(random.uniform(range_min, range_max), random.uniform(range_min, range_max)) for _ in range(n)]

def get_distance(city1, city2):

    distance_x = pow((city1[0] - city2[0]), 2)
    distance_y = pow((city1[1] - city2[1]), 2)

    distance = math.sqrt(distance_x + distance_y)
    return distance

def create_graph(cities, full_connectivity=True):
    graph = {}
    n = len(cities)
    
    for i in range(n):
        graph[i] = []
        for j in range(n):
            if i != j:
                distance = get_distance(cities[i], cities[j])
                if full_connectivity or random.random() <= 0.8:
                    graph[i].append((j, distance))
    
    return graph


def tsp_bfs(graph, start):
    n = len(graph)
    queue = deque([(start, [start], 0)])
    min_cost = float('inf')
    min_path = None

    while queue:
        current_city, path, cost = queue.popleft()

        if len(path) == n:
            return_cost = get_distance(cities[current_city], cities[start])
            total_cost = cost + return_cost
            if total_cost < min_cost:
                min_cost = total_cost
                min_path = path + [start]
            continue

        for neighbor, edge_cost in graph[current_city]:
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor], cost + edge_cost))
    
    return min_path, min_cost

def tsp_dfs(graph, start):
    n = len(cities)
    stack = [(start, [start], 0)]
    min_cost = float('inf')
    min_path = None

    while stack:
        current_city, path, cost = stack.pop()
        
        if len(path) == n:
            return_cost = get_distance(cities[current_city], cities[start])
            total_cost = cost + return_cost
            if total_cost < min_cost:
                min_cost = total_cost
                min_path = path + [start]
            continue

        for neighbor, edge_cost in graph[current_city]:
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor], cost + edge_cost))
    
    return min_path, min_cost

def minimum_spanning_tree(graph):
    n = len(graph)
    mst = []
    visited = [False] * n

    # cost, from node, to node
    min_heap = [(0, 0, 0)]

    total_cost = 0

    while min_heap:
        cost, from_node, to_node = heapq.heappop(min_heap)
        if visited[to_node]:
            continue
        visited[to_node] = True
        if from_node != to_node:
            mst.append((from_node, to_node, cost))
            total_cost += cost
        for neighbor, edge_cost in graph[to_node]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (edge_cost, to_node, neighbor))
    
    return mst, total_cost

def create_graph_and_mst(cities, start):
    graph = {i: [] for i in range(len(cities))}
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            distance = get_distance(cities[i], cities[j])
            graph[i].append((j, distance))
            graph[j].append((i, distance))

    mst, total_cost = minimum_spanning_tree(graph)

    mst_graph = {i: [] for i in range(len(cities))}
    for edge in mst:
        from_node, to_node, cost = edge
        mst_graph[from_node].append((to_node, cost))
        mst_graph[to_node].append((from_node, cost))

    
    n = len(mst_graph)
    visited = [False] * n
    path = []
    
    def dfs(node):
        visited[node] = True
        path.append(node)
        for neighbor, _ in mst_graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    dfs(start)
    path.append(start)

    return mst_graph, path ,total_cost
    
def greedy_search(graph, start):
    n = len(cities)
    path = [start]
    total_cost = 0
    current_city = start
    visited = [False] * n
    visited[start] = True

    while len(path) < n:
        next_city = None
        min_cost = float('inf')
        for neighbour, edge_cost in graph[current_city]:
            if not visited[neighbour] and edge_cost < min_cost:
                next_city = neighbour
                min_cost = edge_cost
        
        path.append(next_city)
        visited[next_city] = True
        total_cost += min_cost
        current_city = next_city

    total_cost += get_distance(cities[-1], cities[start])
    path.append(start)

    return path, total_cost

def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start], 0

    front_queue = deque([start])
    back_queue = deque([goal])
    
    front_visited = {start: 0}
    back_visited = {goal: 0}
    
    front_parent = {start: None}
    back_parent = {goal: None}
    
    while front_queue and back_queue:
        if front_queue:
            current = front_queue.popleft()
            for neighbor, cost in graph[current]:
                if neighbor not in front_visited:
                    front_queue.append(neighbor)
                    front_visited[neighbor] = front_visited[current] + cost
                    front_parent[neighbor] = current
                    if neighbor in back_visited:
                        return reconstruct_path(front_parent, back_parent, neighbor, start, goal), front_visited[neighbor] + back_visited[neighbor]

        if back_queue:
            current = back_queue.popleft()
            for neighbor, cost in graph[current]:
                if neighbor not in back_visited:
                    back_queue.append(neighbor)
                    back_visited[neighbor] = back_visited[current] + cost
                    back_parent[neighbor] = current
                    if neighbor in front_visited:
                        return reconstruct_path(front_parent, back_parent, neighbor, start, goal), front_visited[neighbor] + back_visited[neighbor]

    return None, float('inf')

def reconstruct_path(front_parent, back_parent, meet_node, start, goal):
    path = []
    node = meet_node
    while node is not None:
        path.append(node)
        node = front_parent[node]
    path.reverse()
    
    node = back_parent[meet_node]
    while node is not None:
        path.append(node)
        node = back_parent[node]
    
    return path


cities = generate_cities(10)
graph_full = create_graph(cities, full_connectivity=True)
graph_partial = create_graph(cities, full_connectivity=False)
start_city = 0
end_city = 9
plot_graph(cities, graph_full, "Full Connectivity Graph")

path_bfs, cost_bfs = tsp_bfs(graph_full, start_city)
print(f"BFS TSP path: {path_bfs}, Cost: {cost_bfs:.2f}")
plot_graph(cities, graph_full, "BFS", tsp_path=path_bfs)

path_dfs, cost_dfs = tsp_dfs(graph_full, start_city)
print(f"DFS TSP path: {path_dfs}, Cost: {cost_dfs:.2f}")
plot_graph(cities, graph_full, "DFS", tsp_path=path_dfs)


mst_graph, path_mst, total_cost = create_graph_and_mst(cities, start_city)
print(f"Full Connectivity MST: {path_mst}, Total Cost: {total_cost:.02f}")
plot_graph(cities, graph_full, "Minimal Spanning Tree", tsp_path=path_mst)

path_greedy, cost_greedy = greedy_search(graph_full, start_city)
print(f"GREEDY TSP path: {path_greedy}, Cost: {cost_greedy:.2f}")
plot_graph(cities, graph_full, "Greedy", tsp_path=path_greedy)

path_bidirectional, cost_biderectional = bidirectional_search(graph_partial, start_city, end_city)
print(f"BIDIRECTIONAL SEARCH path: {path_bidirectional}, Cost: {cost_biderectional:.2f}")
plot_graph(cities, graph_full, "BIDIRECTIONAL SEARCH", tsp_path=path_bidirectional)
