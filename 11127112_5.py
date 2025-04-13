# 演算法分析機測
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系

import queue

direction = [('E', 0, 1), ('W', 0, -1), ('S', 1, 0), ('N', -1, 0) ] # 方向( 字串、 column  vector, row vector )
MoveTrails = {'E': 'e', 'W': 'w', 'S': 's', 'N': 'n'} # 人走的方向(小寫)
 
def checkElementRight(string) : # 檢查輸入中是否全為迷宮會出現的元素
    tmp = ""
    for i in string :
        if ( ( i == ("#") ) or ( i == (".") ) or ( i == ("T") ) or ( i == ("S") ) or ( i == ("B") ) ) :
            tmp += i

    return tmp

def NotOutOfBound( position, mazeSize ) : # 檢查該位置會不會超出迷宮邊界
    for i in range( 2 ) :
        if  ( not ( 0 <= position[i] < mazeSize[i] ) ) :
            return False

    return True
    

def findWayByBFS(maze, mazeSize, start, target, box ) : # 跑BFS來尋找可能的路徑
    visited = set() # 儲存曾經走過的點
    q = queue.Queue() 
    q.put( (start, box, "", 0 ) ) # 將起始位置與路徑、步數放入
    visited.add( (start, box) ) # 將一開始位置放入

    while not q.empty() : # 若queue中還有可探索的路徑可以走
        positionP, positionB, trails, step = q.get() # 取得該筆路徑

        if ( positionB == target ) : #若箱子已到終點，返回這一路徑
            return trails

        for direct, vecR, vecC in direction : #若無，四方探索
            nextPositionP = (positionP[0] + vecR, positionP[1] + vecC) # 往該方向走一步

            if ( not NotOutOfBound( nextPositionP, mazeSize ) ) : # 若超maze size 返回
                continue
            elif ( maze[nextPositionP[0]][nextPositionP[1]] == "#" ) : # 若該格為牆壁，返回
                continue


            if ( nextPositionP == positionB  ) : # 若下一格為箱子，試著推動
                nextPositionB = ( positionP[0] + vecR * 2 , positionP[1] + vecC* 2 ) # 讓箱子朝該方向走一步
                if ( NotOutOfBound( nextPositionB, mazeSize ) ) : # 若無超maze size 
                    if (maze[nextPositionB[0]][nextPositionB[1]] != "#") and ( (nextPositionP, nextPositionB) not in visited ): # 若不為牆，且之前沒有這麼移動過
                        visited.add( (nextPositionP, nextPositionB) ) # 加入已拜訪的點
                        q.put( (nextPositionP, nextPositionB, trails+direct, step+1) ) # 放入queue 中視為有潛力的路線

            else : #若只是人移動
                if ( nextPositionP, positionB ) not in visited : # 沒走過的話
                    visited.add( (nextPositionP, positionB) ) # 加入已拜訪的點 
                    q.put( (nextPositionP, positionB, trails+MoveTrails[direct], step+1) ) # 放入queue 中視為有潛力的路線

    return "Impossible" # 若已經跑遍所有可能的路，則視為不可行
            

def main() :
    result = [] # 儲存路徑結果
    string = input() #輸入
    tmpLst = string.split(" ") # 一開始以空白分裂字串，以取得maze 的 column 與 row 數
    error = False  # 代表錯誤是否發生
    size = [] # 儲存 maze 的 column 與 row 
    
    for i in tmpLst : # 逐一加入
        size.append( int(i) )

    if ( len(size) != 2 ) : # 若查度不合法則錯誤發生
        error = True
            
    while ( (size[0] != 0) & (size[1] != 0) ) and ( not error ): # 當結束00與錯誤沒發生的狀況下繼續跑
        maze = [] # 初始化迷宮

        for i in range ( size[0] ) : # 輸入迷宮地形
            string = input()
            if ( ( len(string) != size[1] ) and ( checkElementRight(string) )) : # 若寬度不相符或是有不屬於迷宮的字元，視為錯誤
                error = True
                break
            else : # 無錯則加入
                maze.append(list(string) )

        if ( ( not error ) and (len(maze) == size[0] ) ): # 若錯誤無發生與寬度相符
            start = tuple()
            box = tuple()
            target = tuple()

            for k in range ( size[0] ) : # 記錄下 起點、箱子位置、終點
                for m in range ( size[1] ) :
                    if maze[k][m] == "S" :
                        start = (k,m)
                        maze[k][m] = "."
                    elif maze[k][m] == "B" :
                        box = (k,m)
                        maze[k][m] = "."
                    elif maze[k][m] == "T" :
                        target = (k,m)
                        maze[k][m] = "."

            
            result.append( findWayByBFS(maze, size, start, target, box ) ) # 開始用bfs尋找解方

        # 輸入長寬
        string = input()
        tmpLst = string.split(" ")
        error = False 
        size = []
    
        for i in tmpLst :
            size.append( int(i) )

        if ( len(size) != 2 ) :
            error = True


    # 若錯誤並未發生，則輸出
    if ( not error ) :
        for i in range ( len(result) ) :
            print(f"Maze #{i+1}")
            print(result[i], end = "\n\n")
 
 
if __name__ == "__main__":
    main()        

                        
        

        
 
