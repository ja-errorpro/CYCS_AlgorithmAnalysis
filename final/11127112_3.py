# 演算法分析機測
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系

X = Y = 8
dx = [-1, 1, -2, 2, -2, 2, -1, 1]
dy = [-2, -2, -1, -1, 1, 1, 2, 2]

while True:
    visited = [[False] * (Y + 1) for _ in range(X + 1)]
    dis = [[0] * (Y + 1) for _ in range(X + 1)]

    start, end = input().split()
    if start == "0" and end == "0":
        break
    start_x = ord(start[0]) - ord('a') + 1
    start_y = int(start[1])
    end_x = ord(end[0]) - ord('a') + 1
    end_y = int(end[1])

    ans = 0

    # parent = [[None] * (Y + 1) for _ in range(X + 1)]
    bfsx = [start_x]
    bfsy = [start_y]
    visited[start_x][start_y] = True
    while bfsx:
        x = bfsx.pop(0)
        y = bfsy.pop(0)
        
        if x == end_x and y == end_y:
            ans = dis[x][y]
            break
        
        for i in range(8):
            nx, ny = x + dx[i], y + dy[i]
            if 1 <= nx <= X and 1 <= ny <= Y and not visited[nx][ny]:
                visited[nx][ny] = True
                dis[nx][ny] = dis[x][y] + 1
                # parent[nx][ny] = (x, y)
                bfsx.append(nx)
                bfsy.append(ny)

    print(ans)
    '''
    if ans > 0 or (start_x == end_x and start_y == end_y):
        path = []
        cx, cy = end_x, end_y
        while (cx, cy) != (start_x, start_y):
            path.append((cx, cy))
            cx, cy = parent[cx][cy]
        path.append((start_x, start_y))
        path = path[::-1]
        print("Path:", end=' ')
        for px, py in path:
            print(f"{chr(ord('a') + px - 1)}{py}", end=' ')
        print()
    else:
        print("No path found")
    '''

