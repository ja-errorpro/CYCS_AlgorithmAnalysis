# 演算法分析機測
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系
import copy
def sameString ( string, target ) :
    lengthT = len(target)
    for i in range ( 0, len(string) - lengthT + 1, 1 ) :
        if ( lengthT == 1 ) :
            if ( string[i] == target ) :
                return i
        elif ( string[i: i + lengthT - 1 ] == target ) :
            return i

    return -1

def skipEmpty(string) :
    tmp = ""
    for i in string :
        if ( ( i != ("\n") ) and ( i != ("\t") ) and ( i != (" ") ) ) :
            tmp += i

    return tmp

def allNumber(idx) :
    for i in idx :
        val = ord(i)
        if ( ( int(val) < 48 ) | ( int(val) > 57 ) ) :
            return False

    return True

def whickFunct( string, func1, func2 ) :
    name = string.split("(")[0]
    if ( name == func1 ) :
        return 0
    else :
        return 1

def parsePoly(string) : # 分解多項式(公式)
    equalSeperate = string.split("=") # 先用等號分解函式名字和多項式
    returnResult = [] # 儲存分解結果
    if ( len(equalSeperate) == 2 ) : # 如果以等號為界能將其一分為二
        equlaLeft = equalSeperate[0].split("(") # 左邊以左括弧為界線，區分函數與變數名字
        if ( len(equlaLeft) == 2 ) : # 若能將其一分為二
            returnResult.append( equlaLeft[0]) # 將函式名字存入於 idx 0
            returnResult.append( equlaLeft[1][0:-1] ) #將變數名字從入於 idx 0 
        else :
            return ["-"] # 否則回傳錯誤

        equlaRight = (equalSeperate[1]).split("+") # 以加號分解函式部分
        containLst = [] # 儲存函式最終分解結果
        for i in equlaRight : # 一個一個檢查與拆成正確格式

            tmp = []
            tmpStr = i
            preIndex = 0
            for k in range(len(i)) :
                if (i[k] == "-") & (k != 0):
                    tmp.append( i[preIndex: k])
                    preIndex = k
                    
            if ( preIndex != len(i) - 1 ) or (len(i) == 1):
                tmp.append( i[preIndex:])

            for k in tmp : # 接著開始分解記錄成正確格式
                idx = sameString ( k, returnResult[1] ) # 以變數為界線，區分係數和次方
                if ( idx == -1 ) : # 若找不著，代表此為常數
                    if not (( k[0] == "-" ) or ( allNumber(k[0]) ) ) :#檢查此項是否全為數字或負號+數字
                        if( len(k) > 1 ) :
                            if( not allNumber(k[1:]) ) :
                                return ["-"] # 不符合則回傳報錯
                        elif ( k[0] == "-" ) :
                            return ["-"]
                    containLst.append([int(k), 0 ]) # 正確則將分解好的項目加入函式列表中
                else : #如果找的著
                    varEnd = idx + len(returnResult[1]) # 該index加上變數長度
                    coefficient = 0 #擷取係數
                    if ( k[0:idx] == "" ) :
                        coefficient = 1
                    elif (( idx == 1) and ( k[0] == "-" )) :
                        coefficient = -1
                    else :
                        coefficient = 0
                        if  ( k[0] == "-" ) :
                            coefficient = int(k[1:idx])
                            coefficient *= -1
                        else :
                            coefficient = int(k[0:idx])
                        
                    if ( varEnd == len(k) ) : # 如果結果等於該項目長度
                        containLst.append([coefficient, 1 ]) #代表為1次項，故沒有"^"
                    elif ( k[varEnd] == "^" ): # 剩下的變數後面一定有東西，看是否為次方符號
                            lst = [coefficient] #擷取係數
                            lst.append( int(k[varEnd+1:]) ) #擷取次方項
                            containLst.append(lst) #把該項加入
                    else : #都不是則回傳錯誤訊息
                        return ["-"]

        returnResult.append(containLst) # 分解完函數後加入回傳lst中
        return returnResult # 回傳結果
    else: # 無法一分為二，則回傳錯誤訊息
        return ["-"]

def honer( funct, var ) : # 用於把數字帶入的多項式是解, funct 是該多項式，var 是帶入值
    prePower = funct[0][1]  # 前一個項的次方
    num = funct[0][0] # 初始化為第一項的係數
    first = True
    for i in range( 0, len(funct), 1 ) : # 再把整個多項式帶入完前
        if prePower == 0  : # 若前項是常數，代表整個多項式是常數，故直接return 值就好
            return [funct[0][0], 0 ]
        elif ( len(funct) == 1 ): # 若只有一項
            return [num * (var**prePower), 0] # 直接計算本項結果並回傳
        elif ( i != 0 ) : # 若並非第一項
            num = num * (var**(prePower - funct[i][1] )) + funct[i][0]  # 數值為前數 * (上次方 - 下次方)的變數次方，再加上此項係數
            prePower = funct[i][1] # 更新prepower為此項

    return [num, 0]

def concatAndInsert( funct, item ) : # 將目標加入方程式中
    for i in range ( 0, len(funct) ,  1 ) : # 每項都看過
        if ( item[1] == funct[i][1] ) : # 如果次方一樣
            funct[i][0] += item[0]  # 就係數加起來
            return funct
        elif ( i == 0 ) & ( funct[0][1] < item[1] ) : # 如果為第一位，且次方項小於目標
            funct.insert( i, item ) # 就將目標插入第一項
            return funct
        elif ( i >= 0 ) & ( i + 1 < len(funct) ) : # 如果前有後皆項次
            if ( funct[i+1][1] < item[1] ) & ( funct[i][1] > item[1] ) : # 如果後面的項次，次方小於目標;前面的項次，次方大於目標 i> target > i+1
                funct.insert( i+1, item ) #就將目標插入兩者之間
                return funct
        
    funct.append( item ) #整個跑完都沒發現可插入的idx，故直接插入最面
    return funct            
            

def polyArithmatic( element, operator ) : #暫時默認變數相同
    rst = element[0] # 儲存結果
    i = 1
    while ( i != len(element) ) :
        tmp = rst
        multiRst = []
        for k in element[i] : # 迴圈將兩者每項相乘
            if ( operator == "*" ) : # 若為乘法
                for m in tmp : # 迴圈將兩者每項相乘
                    power = m[1]+k[1] # 次方相加
                    value = m[0]*k[0] # 係數相乘
                    rst = concatAndInsert( multiRst, [ value, power ] ) #結果為將結果插入結果式子中
            elif (( operator == "+" ) or ( operator == "-" ))  : # 若為加減
                if ( operator == "-" ) :# 負數，要處理係數為負號
                    k[0] = k[0] * (-1)

                rst = concatAndInsert( rst, k )

        i += 1

    finalRst = []
    for k in range(len(rst)) : # 用於檢查係數為0的項次，將其從回傳結果中去除
        if ( rst[k][0] != 0 ) :
            finalRst.append(rst[k])

    if ( finalRst == [] ) : # 如果全0，則回傳0
        return [[ 0, 0 ]]
    else : # 如果還有係數不為零的項次，則回傳結果
        return finalRst

def parseByOperator( string, operator ) :
    lst = []
    tmpStr = ""
    preIdx = -1
    for i in range(len(string)) :
        if (string[i] == operator ) & (preIdx != -1) :
            if ( operator == "-" ) & ( string[preIdx] == "("):
                tmpStr += string[i]
                preIdx = i
            else :
                lst.append(tmpStr)
                tmpStr = ""
        else :
            tmpStr += string[i]
            preIdx = i

    if ( tmpStr != "" ) :
        lst.append(tmpStr)

    return lst

def arithmaticrResult( string, funct, functString ) : # 輸入為 計算式,公式, 公式字串
    operatorLst = [ "+", "-", "*" ] # 運算子列表

    for i in operatorLst : # 以各種運算子試圖分解計算式
        parseLst = parseByOperator( string, i ) # 儲存分解結果
        if ( len(parseLst) >= 2 ): # 如果可被分解
            isPara = False
            for k in parseLst :
                if k[-1] == "(" :
                    isPara = True
                    break
            if ( not isPara ) :
                return dealing( parseLst, funct, i ) # 呼叫dealing處理運算

    # 如果只有一個
    parseLst = string.split("(") # 切分出函式名與變數名
    idx = whickFunct( parseLst[0], funct[0][0], funct[1][0] ) #看到底是哪個函式
    var = parseLst[1].split(")")[0] # 取出變數
    
    if ( var == funct[idx][1] ) : # 若變數是未知數
        return funct[idx][2] # 直接回傳此函式str
    else :
        return [honer( funct[idx][2], int(var) )] # 否則呼叫honer去求值
    
def dealing( parseLst, funct, operator ) : # 取得運算結果
    idx = [] # 儲存到底是哪一個函式
    bringIn = [] # 儲存把函式替換函式名或honer的結果
    for i in range( len(parseLst) ) : # 每一個看
        parse = parseLst[i].split("(")
        var = parse[1].split(")")[0] #取得變數名或數字
        idx = whickFunct( parse[0], funct[0][0], funct[1][0] ) # 得知是哪一個function
        if( funct[idx][1] == var ) : # 若變數等於括號中的string
            tmpLst = copy.deepcopy(funct[idx][2])
            bringIn.append(tmpLst) # 把函式內容抓進lst中
        else : # 若不等於，代表是數字，就需要honer
            bringIn.append([honer( funct[idx][2], int(var) ) ])

    return polyArithmatic( bringIn, operator )

def main() :
    # counter = 1 # 計數器
    errorOccur = False # 代表錯誤有無發生
    funct = [] # 存放函式
    formula = [] # 存放多項運算式
    functString = [] # 存放函式的完整字串
    result = [] # 存放結果
    
    string = skipEmpty(input()) # 輸入
    while (( string != "0" ) and not errorOccur ): # 若不為結束且錯誤無發生
        if ( string == "" ) : # 如果並未輸入，就開始新的回合
            if ( len(funct) < 2 ) :
                string = skipEmpty(input()) # 輸入
            else :
                string = skipEmpty(input())
            continue
        elif ( len(funct) < 2 ) : # 函式lst小於2代表函式尚未輸入完畢
            tmp = parsePoly(string) # 暫存輸入(函式)的分解結果
            if ( tmp[0][0] != "-" ) : # 為負號代表錯誤發生，反之無
                funct.append(tmp) # 新增函式
                functString.append(string.split("=")[1]) # 新增函式字串

                if ( len(funct) > 1 ) : # 若已有兩個函式
                    if ( funct[0][0] == funct[1][0] ) : # 名字相同，會導致之後計算錯誤
                        print( "\n!!two functions are the same!!" )
                        errorOccur = True
                        break
            else :
                print( "\n!!the function enter is wrong!!" ) #錯誤發生
                errorOccur = True
                break
        else : # 除外皆是多項計算式
            formula.append( string )
            result.append( arithmaticrResult( string, funct, functString ) ) # 呼叫arithmaticrResult處理

        if ( len(funct) < 2 ) :
            string = skipEmpty(input()) # 輸入
        else :
            string = skipEmpty(input())
            
    if not ( ( errorOccur ) or ( len(funct) != 2 ) or (len(formula) == 0) ) : # 若錯誤未發生 且 有兩個函式 且 有多項方程式，則需要輸出
        variableName = funct[0][1]
        #print(formula)
        for i in range (len(formula)) :
            print(formula[i] , end = " = " )

            for k in range (len(result[i])) :
                thisItem = result[i][k]
                if ( thisItem[0] != 0 ) :
                    tmpVar = thisItem[0]
                    if ( k != 0 ) & ( tmpVar > 0 ) :
                        print( "+", end = "" )


                    coefficient = ""


                    if ( thisItem[0] == -1) :
                        coefficient = "-"
                    elif ( thisItem[0] != 1) :
                        if ( thisItem[0] < 0 ) :
                            coefficient = "-" + str(thisItem[0] * (-1))
                        else :
                            coefficient = str(thisItem[0])
                    
                    if ( thisItem[1] == 0 ) :
                        if ( thisItem[0] == -1) :
                            print( "-1", end = "" )
                        elif ( k == 0 ) & ( thisItem[0] == 0 ) :
                            print( "0", end = "" )
                        else :
                            print( coefficient, end = "" )
                    elif ( thisItem[1] == 1 ) :
                        print( coefficient, end = variableName + "" )
                    else :
                        print( coefficient, end = "" + variableName + "^" )
                        print( thisItem[1], end = "" )
                elif ( k == 0 ) & ( thisItem[0] == 0 ) :
                    print( "0" )

            print()
            
        
                
main()


