# 演算法分析機測
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系

W = int(input())
n = int(input())

w = []
v = []
for i in range(n):
    w_i, v_i = map(lambda x: int(x), input().split())
    w.append(w_i)
    v.append(v_i)

dp = [0 for _ in range(W + 1)]
path = [[False for _ in range(W+1)] for _ in range(n + 1)]


for i in range(n):
    for j in range(W, w[i] - 1, -1):
        # dp[j] = max(dp[j], dp[j - w[i]] + v[i])
        if dp[j] < dp[j - w[i]] + v[i]:
            dp[j] = dp[j - w[i]] + v[i]
            path[i][j] = True

print('Total Value =', dp[W])

# backtrack
items = []
for i in range(n - 1, -1, -1):
    if path[i][W]:
        items.append(i + 1)
        W -= w[i]
print('Take Items', end=' ')
print(*items[::-1], sep=',')