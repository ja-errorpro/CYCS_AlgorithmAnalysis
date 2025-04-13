# 演算法分析機測
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系
def init(list_size):
    return list(range(list_size))

#將兩點指向同一root
def combine(root,s1,s2):
    root[findroot(root,s1)] = findroot(root,s2)
    
#find root of set
def findroot(root, sett):
    if root[sett] != sett:
        root[sett] = findroot(root,root[sett])
    return root[sett]

#檢查相鄰節點是超出邊界
def inbounds(x,y,high,weight):
    if x >=0 and x < high:
        if y >=0 and y < weight:
            return True
        else:
            return False
    else:
        return False
    
def main():
    id_image = 1
    while True:
        high, weight = map(int,input().split())
        if (high == 0) and (weight == 0):
            break

        image = [];

        for i in range(high):
            row = list(map(int,input().strip()))
            image.append(row)

        root = init(high * weight) # 將圖從二維變一維，初始化每一點為各自的起點
        direct = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)] # 8個方位

        #合併pixel
        for x in range(high):
            for y in range(weight):
                if image[x][y] == 1:
                    for x1,y1 in direct:
                        neighbor_x = x + x1
                        neighbor_y = y + y1
                        if inbounds(neighbor_x,neighbor_y,high,weight) and image[neighbor_x][neighbor_y] == 1 :
                             combine(root, x*weight + y , neighbor_x * weight + neighbor_y)
        #計算面積
        area = {}
        for x in range(high):
            for y in range(weight):
                if image[x][y] == 1:
                    componnent_root = findroot(root,x*weight + y)
                    area[componnent_root] = area.get(componnent_root,0)+1

        #編列輸出順序表
        order_of_root = []
        s2 = set()
        for x in range(high):
            for y in range(weight):
                if image[x][y] == 1:
                    temp = findroot(root,x*weight+y)
                    if temp not in s2:
                        s2.add(temp)
                        order_of_root.append(temp)
                        
        num_of_component = len(order_of_root)
        print(f"Image #{id_image}")
        print(f"Number of Connected Components = {num_of_component}")

        for i, temp in enumerate(order_of_root):
            print(f"Connected Component #{i+1} Area = {area[temp]}")
        id_image += 1 
            
    
if __name__ == "__main__":
    main()
    
