# 演算法分析機測
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系

import numpy as np
import cv2
import copy

def isNumber( string ) : # 確認字串是否全為數字
    for i in string :
        asciiCode = ord(i)
        if (( asciiCode < 48 ) or ( asciiCode > 57 )) :
            return False
    return True

def DP( differ, direct, wid, high ) : # 使用dynamic programming 決定最佳裂隙
    lst = dict() # 儲存前一 行 or 列節點的最優cost以及對應的路徑

    if ( direct == "1" ) : # 如果為水平拼貼
        for i in range(high) : # 先建立每個高一個list，儲存目前到此點的最佳cost&路徑
            lst[i] = [differ[(0,i)] ,{ 0 : i }] # 先放 x = 0 的那排

        for i in range(wid): # 從最左排一路算到最右
            tmp = dict() # 用於儲存目前到此點的最佳cost&路徑 (lst是紀錄前一排的)
            for k in range(high): # 一個一個高算
                successor = [[], lst[k], []] # 儲存左上、正左方、左下的點的lst資訊
                
                if ( k != 0 ) :#如果左上存在點(=不為頂部)
                    successor[0] = lst[k-1]

                if ( k != (high - 1) ) :#如果左下存在點(=不為底部)
                    successor[2] = lst[k+1]

                # 先假定為正左方，畢竟一定會存在
                final = 1 
                cost = successor[1][0]

                # 看cost決定要連結到哪一個節點
                for m in range (0, 3, 2 ) :
                    if ( successor[m] != [] ) :
                        if ( successor[m][0] < cost ) :
                            cost = successor[m][0]
                            final = m

                #將最後結果更新至tmp，並加上目前節點
                tmp[k] = [ (cost + differ[(i,k)]), copy.deepcopy(lst[k-1+final][1]) ]
                tmp[k][1][i] = k 
                 

            # 當此行完成，便將覆蓋lst供下一行使用
            lst = copy.deepcopy(tmp)

        # 最後一行跑完之後，取出cost最小者，即為最佳seam
        result = 0
        cost = lst[0][0]
        for i in range(1, high):
            if ( lst[i][0] < cost ) :
                result = i
    else : # 如果為垂直拼貼，相似於水平，只是長寬立場調換(會因重疊改變的為寬)，故不贅述
        for i in range(wid) :
            lst[i] = [differ[(i,0)] ,{ 0 : i }]

        for i in range(high):
            tmp = dict()
            for k in range(wid):
                successor = [[], lst[k], []]
                
                if ( k != 0 ) :
                    successor[0] = lst[k-1]

                if ( k != (wid - 1) ) :
                    successor[2] = lst[k+1]

                final = 1
                cost = successor[1][0]
                for m in range (0, 3, 2 ) :
                    if ( successor[m] != [] ) :
                        if ( successor[m][0] < cost ) :
                            cost = successor[m][0]
                            final = m

                tmp[k] = [ (cost + differ[(k,i)]), copy.deepcopy(lst[k-1+final][1]) ]
                tmp[k][1][i] = k
                 


            lst = copy.deepcopy(tmp)

        result = 0
        cost = lst[0][0]
        for f in range(1, wid):
            if ( lst[f][0] < cost ) :
                result = f

    # 回傳最佳seam
    return lst[result][1]


def main():
    imgName = "" # 紀錄檔案的名字
    direction = "" #紀錄要水平還是垂直拼接
    percent = "" # 紀錄要重疊多少比例

    # 輸入設定
    while ( True ) : #輸入正確格式檔案名稱
        imgName = (input("請輸入影像檔：")).strip()
        if ( len(imgName.split(".")) != 2 ) :
            print( "!!檔名輸入錯誤!!" )
        else:
            break


    while ( True ) : #輸入拼貼方向
        direction = (input("請輸入拼貼方向 (1)水平、(2)垂直：")).strip()
        if ( direction != "1" and direction != "2" ) :
            print( "!!請輸入1或是2!!" )
        else:
            break
    
    while ( True ) :  #輸入重疊比例(介於 20% ~ 30% )
        percent = (input("請輸入重疊比例 (%)：")).strip()
        
        if ( isNumber(percent) ) :
            if ( int(percent) < 20 or  int(percent) > 30 ) :
                print( "!!重疊比例需介於 20% ~ 30%之間!!" )
            else:
                break
        else:
            print( "!!請輸入數字!!" )

    #讀檔與初始設定
    img = cv2.imread(imgName, -1) # 讀案
    height, width = img.shape[:2] # 取得影像長寬
    difference = dict() # 儲存重疊區域上下影像 rgb 的歐氏距離(key是座標，value是距離)
    sean = dict() # 儲存拼貼縫隙座標( key 是 不會因拼貼變動的長/寬(從0開始)，值對應的寬/長座標)
    canvas_h = height #拼貼後的圖片長(暫時用原始值替代)
    canvas_w = width #拼貼後的圖片寬(暫時用原始值替代)
    heightUP = 0 #用於水平拼貼，紀錄未重疊的高/2
    widthUP = 0 #用於垂直拼貼，紀錄未重疊的寬/2

    # 處理水平與垂直拼貼
    if ( direction == "1" ) : #如果水平拼貼
        heightUP = int(( height * (1 - ( int(percent) / 100 )) )// 1) # 計算原圖除去重疊區域的長度
        y = 0 # 紀錄第二張圖片現在的座標(高)到哪裡

        #計算重疊區域的歐式距離
        for i in range( heightUP -1, height ) : # 從第一張圖重疊邊界往下算
            for k in range( 0, width ) : # 逐一算整列的歐式距離並儲存
                num = 0

                #計算rgb三色差
                for m in range(3):
                    num += (int(img[i, k][m]) - int(img[y, k][m]) ) ** 2

                num = num ** 0.5 # 開根號得到距離
                difference[(k, y)] = num # 以第二張圖的座標為key儲存歐式距離

            y += 1 # 往下個高算

        seam = DP(difference, direction, width, y ) # 呼叫DP取得最佳縫隙
        canvas_h = canvas_h + heightUP # 拼貼後的圖片長

    else :
        widthUP = int(( width * (1 - ( int(percent) / 100 )) )// 1) # 計算原圖除去重疊區域的寬
        x = 0 # 紀錄第二張圖片現在的座標(寬)到哪裡

        #計算重疊區域的歐式距離
        for i in range( widthUP -1, width ) : # 從第一張圖重疊邊界往右算
            for k in range( 0, height ) : # 逐一算整行的歐式距離並儲存
                num = 0
                
                #計算rgb三色差
                for m in range(3):
                    num += (int(img[k, i][m]) - int(img[k, x][m]) ) ** 2

                num = num ** 0.5 # 開根號得到距離
                difference[(x,k)] = num  # 以第二張圖的座標為key儲存歐式距離

            x += 1 # 往下個寬算

        seam = DP(difference, direction, x, height ) # 呼叫DP取得最佳縫隙
        canvas_w = canvas_w + widthUP # 拼貼後的圖片寬


    # 先建畫布，依據重疊的方式貼上兩張圖
    canvas1 = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
    canvas2 = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    if ( direction == "1") :
        canvas1[:height, :width] = img
        canvas2[heightUP: , :width] = img
    else:
        canvas1[:height, :width] = img
        canvas2[:height , widthUP:] = img

    #建立遮罩
    mask = np.zeros((canvas_h, canvas_w), dtype=np.uint8)

    if ( direction == "1") :
        for i in range(canvas_w):
            h = seam[i] + heightUP
            mask[:h, i] = 255
    else :
        for i in range(canvas_h):
            w = seam[i] + widthUP
            mask[i, :w] = 255

    #放上遮罩，讓圖片根據裂隙顯示為上層或下層圖片
    mask3 = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    output = canvas1 * (mask3 / 255.0) + canvas2 * (1 - mask3 / 255.0) # 產出接合canvas1放上遮罩+ canvas2放相反區域遮罩的圖片

    #輸出圖片、顯示圖片
    output = output.astype(np.uint8)
    imgName = imgName.split(".")[0]+"_result.bmp"
    cv2.imwrite(imgName , output)
    cv2.imshow(imgName , output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
