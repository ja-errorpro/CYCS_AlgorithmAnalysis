# 演算法分析機測Add commentMore actions
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系

import cv2
import os
import random
import bisect
import heapq
import numpy as np
from operator import attrgetter
from collections import deque

# ------------------ 圖片邊緣分析 ------------------
class ImageAnalysis:
    bestMatchList = []
    dissimilarityList = []
    @classmethod
    def analysis(cls, pieces):
        n = len(pieces)
        # 四個方向都要存
        cls.bestMatchList     = [[[]     for _ in range(4)] for _ in range(n)]
        cls.dissimilarityList = [[[None  for _ in range(4)] for _ in range(n)] for _ in range(n)]

        def update(firstPiece, secondPiece, dir):
             revDir = (dir + 2) % 4
             dissimilarity = cls.calcDissim(firstPiece.edge(dir), secondPiece.edge(revDir))
             cls.dissimilarityList[firstPiece.id][secondPiece.id][dir] = dissimilarity
             cls.bestMatchList[firstPiece.id][dir].append((dissimilarity, secondPiece.id))
             cls.bestMatchList[secondPiece.id][revDir].append((dissimilarity, firstPiece.id))

        # 四個方向都要計算一次
        for a in range(n):
            for b in range(a + 1, n):
                for c in range(4):
                    update(pieces[a], pieces[b], c)
                    update(pieces[b], pieces[a], c)

        # 把 bestMatchList 排序
        for a in range(n):
           for b in range(4):
              cls.bestMatchList[a][b].sort(key=lambda x: x[0])

    @staticmethod
    def calcDissim(edge1, edge2):
        # simple squared-difference
        diff = edge1.astype(np.int32) - edge2.astype(np.int32)
        return int((diff*diff).sum())

    @classmethod
    def getDissimilarity(cls, a, b, d):
        return cls.dissimilarityList[a][b][d]
    @classmethod
    def getBestMatch(cls, a, d):
        return cls.bestMatchList[a][d][0][1]

# ------------------ 單一拼圖解 --------------------------------
class PuzzleSolution:
    def __init__(self, pieces, row, col, shuffle=True):
        self.row, self.col = row, col
        self.pieces = pieces.copy()
        if shuffle:
            random.shuffle(self.pieces)
        self.id2idx = {p.id:i for i,p in enumerate(self.pieces)}
        self.fitness = 0
        self.calcFitness()

    def calcFitness(self):
        s = 0
        for r in range(self.row):
            for c in range(self.col-1):
                a = self.pieces[r*self.col+c].id
                b = self.pieces[r*self.col+c+1].id
                s = s + ImageAnalysis.getDissimilarity(a,b,0)
        for r in range(self.row-1):
            for c in range(self.col):
                a = self.pieces[r*self.col+c].id
                b = self.pieces[(r+1)*self.col+c].id
                s = s + ImageAnalysis.getDissimilarity(a,b,1)
        # 把越低 dissimilarity 轉成越高 fitness
        self.fitness = 1_000_000_000 / (s+1)

    def getFitness(self): return self.fitness
    def size(self):      return len(self.pieces)
    def getPieceById(self, pid):
        return next(p for p in self.pieces if p.id==pid)
    def edge(self, pid, d):
        idx = self.id2idx[pid]
        r,c = divmod(idx, self.col)
        if d==0 and c<self.col-1: return self.pieces[idx+1].id
        if d==1 and r<self.row-1: return self.pieces[idx+self.col].id
        if d==2 and c>0:          return self.pieces[idx-1].id
        if d==3 and r>0:          return self.pieces[idx-self.col].id

    def toImage(self):
        # 重建整張圖
        rows = []
        for r in range(self.row):
            row_imgs = [p.img for p in self.pieces[r*self.col:(r+1)*self.col]]
            rows.append(np.hstack(row_imgs))
        return np.vstack(rows)

# ------------------ 兩親交配操作 ------------------------------
class Crossover:
    def __init__(self, p1, p2):
        self.parents = (p1,p2)
        self.row, self.col = p1.row, p1.col
        N = p1.size()
        self.kernel = [None]*N     # kernel[pieceId] = (y,x)
        self.vis    = set()        # 已放位置
        self.queue  = []           # priority queue，存放待擴展的 (權重, (pid, (y,x)), _)

    def initKernel(self):
        pid = random.choice(self.parents[0].pieces).id
        # 從中心開始，這樣上下左右都能均衡生長，不會被 child() 丢棄
        start_y = self.row  // 2
        start_x = self.col  // 2
        self._addToKernel(pid, (start_y, start_x))

    def run(self):
        self.initKernel()
        while self.queue:
            weight, (pid,pos), dirinfo = heapq.heappop(self.queue)
            if pos in self.vis or self.kernel[pid] is not None: continue
            self._addToKernel(pid,pos)

    def child(self):
        """
        從 kernel 生成一个合法排列：
        1) 把 kernel 中有效位置的 pid 放到對應格子；
        2) 再按父二的順序把剩餘 pid 填滿空格；
        3) 最後如果還剩，再按父一順序補上。
        """
        N = len(self.kernel)
        total = self.row * self.col

        # 1) 準備用来裝 pid 的線性數組
        R = [None] * total
        placed = set()

        # 2) 先把 kernel 有效的放進去
        coords = [pos for pos in self.kernel if pos is not None]
        if coords:
            ys = [y for y,x in coords]
            xs = [x for y,x in coords]
            minY, minX = min(ys), min(xs)
            for pid, pos in enumerate(self.kernel):
                if pos is None: 
                    continue
                y, x = pos
                y0, x0 = y - minY, x - minX
                # 只有落在 [0,rows)×[0,cols) 範圍内才放
                if 0 <= y0 < self.row and 0 <= x0 < self.col:
                    idx = y0 * self.col + x0
                    R[idx] = pid
                    placed.add(pid)

        # 3) 父二剩下的 pid 依序填空格
        free_slots = [i for i,v in enumerate(R) if v is None]
        parent2_ids = [p.id for p in self.parents[1].pieces]
        for pid in parent2_ids:
            if pid not in placed and free_slots:
                R[free_slots.pop(0)] = pid
                placed.add(pid)

        # 4) 如果還剩（保險起見），再按父一順序補上
        parent1_ids = [p.id for p in self.parents[0].pieces]
        for pid in parent1_ids:
            if pid not in placed and free_slots:
                R[free_slots.pop(0)] = pid
                placed.add(pid)

        # 5) 最後的 sanity check：所有位置都填滿
        assert all(x is not None for x in R), "仍有空位，child() 逻辑有误"

        # 6) 把 pid 序列轉回 ImagePiece 列表
        pieces = [self.parents[0].getPieceById(pid) for pid in R]
        return PuzzleSolution(pieces, self.row, self.col, shuffle=False)


    def _addToKernel(self, pid, pos):
        self.kernel[pid] = pos
        self.vis.add(pos)
        # 推入對列：四个方向
        order = [2,1,0,3]
        for d in order:
            ny = pos[0] + (d==1) - (d==3)
            nx = pos[1] + (d==0) - (d==2)
            # 只考虑將来可能落在拼圖内的點
            if 0 <= ny < self.row and 0 <= nx < self.col:
                neigh = ImageAnalysis.getBestMatch(pid, d)
                heapq.heappush(self.queue, (
                    ImageAnalysis.getDissimilarity(pid, neigh, d),
                    (neigh, (ny,nx)),
                    None
                ))

# ------------------ GA 主流程 ----------------------------------
class GeneticAlgorithm:
    def __init__(self, pieces, row, col, pop_size=200):
        self.row, self.col = row, col
        # 初始化 population
        self.solutions = [PuzzleSolution(pieces, row, col) for _ in range(pop_size)]

    def rouletteSelection(self, k=2):
        fits = [s.getFitness() for s in self.solutions]
        prefix = np.cumsum(fits)
        def pick():
            x = random.random()*prefix[-1]
            return self.solutions[bisect.bisect_left(prefix, x)]
        return pick(), pick()

    def evolution(self, generations=15):
        best = None
        plot_win = None

        for g in range(generations):
            # 精英保留：先把族群按 fitness 排序，直接保留最好的兩個
            self.solutions.sort(key=attrgetter("fitness"), reverse=True)
            newpop = self.solutions[:2]

            # 其餘靠交配＋少量變異產生
            while len(newpop) < len(self.solutions):
                p1,p2 = self.rouletteSelection()
                co = Crossover(p1,p2)
                co.run()
                child = co.child()
                newpop.append(child)

            self.solutions = newpop
            current = max(self.solutions, key=attrgetter("fitness"))


            best = current

        return best

# ------------------ 輔助：把 OpenCV 讀圖轉成 Image 物件 ------------
class ImagePiece:
    def __init__(self, img, id):
        self.img, self.id = img, id
    def edge(self, d):
        if d==0: return self.img[:,-1]  #右邊緣
        if d==1: return self.img[-1]    #下邊緣
        if d==2: return self.img[:,0]   #左邊緣
        if d==3: return self.img[0]     #上邊緣

# ------------------ main 程式 -----------------------------------
def main():
    path = input("請輸入影像檔: ").strip()

    img = cv2.imread(path)[:,:,::-1]  # BGR→RGB
    
    # 切塊
    pieces = []
    tile = 120
    h,w = img.shape[:2]
    rows,cols = h//tile,w//tile
    id=0
    for r in range(rows):
        for c in range(cols):
            y = r*tile
            x = c*tile
            pieces.append(ImagePiece(img[y:y+tile, x:x+tile], id))
            id+=1

    # 分析邊緣相似度
    ImageAnalysis.analysis(pieces)

    # 執行 GA
    ga = GeneticAlgorithm(pieces, rows, cols, pop_size=100)
    best = ga.evolution(generations=30)

    # 輸出結果
    out = path.rsplit('.',1)[0] + "_result." + path.rsplit('.',1)[1]
    res_img = best.toImage()[:,:,::-1]  # RGB→BGR
    cv2.imwrite(out, res_img)
    print("輸出影像檔:", out)

if __name__ == '__main__':
    main()
