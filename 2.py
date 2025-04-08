
def dfs(graph, node, visited, path):
    visited[node] = True
    path.append(node)

    if len(path) == len(graph):
        if path[0] in graph[node]: # end
            return path + [path[0]]
        else:  # backtrack
            path.pop()
            visited[node] = False
            return None

    for neighbor in graph[node]: # bf
        if not visited[neighbor]:
            result = dfs(graph, neighbor, visited, path)
            if result:
                return result

    path.pop()
    visited[node] = False
    return None

def solve(graph): # Complexity: O(n!)
    visited = [False] * (len(graph) + 1) # initial: all nodes are unvisited
    path = []

    for node in range(1, len(graph) + 1):
        if not visited[node]:
            result = dfs(graph, node, visited, path)
            if result:
                return result

    return []


u, v = map(int, input().split())
while u != 0 and v != 0:
    graph = {}
    for i in range(1, u + 1):
        graph[i] = []
    for i in range(v):
        x, y = map(int, input().split())
        graph[x].append(y)
        graph[y].append(x)

    result = solve(graph)
    print(*result)
    u, v = map(int, input().split())