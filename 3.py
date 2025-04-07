
def solve(a, b, target):
    queue = []
    visited = set()
    queue.append((0, 0, []))
    visited.add((0, 0))
    while queue:
        x, y, path = queue.pop(0)
        
        if y == target:
            return path + ["Success"]
        
        next_states = []

        next_states.append((a, y, ["Fill A"]))  # Fill A
        next_states.append((x, b, ["Fill B"]))  # Fill B
        next_states.append((0, y, ["Empty A"]))  # Empty A
        next_states.append((x, 0, ["Empty B"]))  # Empty B
        
        a_to_b = min(x, b - y)  # Pour A to B
        if a_to_b > 0:
            next_states.append((x - a_to_b, y + a_to_b, ["Pour A B"]))

        b_to_a = min(y, a - x)  # Pour B to A
        if b_to_a > 0:
            next_states.append((x + b_to_a, y - b_to_a, ["Pour B A"]))

        for state in next_states:
            new_x, new_y, action = state
            if (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append((new_x, new_y, path + action))

    return ["Err0r"]

a, b, target = map(int, input("").split())
k = 1
while a != 0 and b != 0 and target != 0:
    result = solve(a, b, target)
    print(f"Case #{k}")
    print("\n".join(result))
    print()
    k += 1
    a, b, target = map(int, input("").split())

    
    



