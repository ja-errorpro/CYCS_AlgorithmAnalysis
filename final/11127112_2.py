# 演算法分析機測Add commentMore actions
# 學號: 11127112 / 11127122 / 11127137
# 姓名: 莊沛儒 / 胡沛頎 / 黃乙家
# 中原大學資訊工程系

class Node:
    def __init__(self,frequence,char=None,left=None,right=None):
        self.frequence = frequence
        self.char = char
        self.left = left
        self.right= right
def build_huffman_tree(freq_map):
    heap = [Node(frequence,char) for char,frequence in freq_map.items()]

    while len(heap)>1:
        heap.sort(key = lambda x: x.frequence)
        left = heap.pop(0)
        right = heap.pop(0)
        merge = Node(left.frequence + right.frequence, None)
        merge.left = left
        merge.right = right
        heap.append(merge)
    return heap[0]

def generate_codes(self):
    codes = {}
    def traverse(node,code=''):
        if node:
            if node.char:
                codes[node.char] = code
            traverse(node.left, code + '0')
            traverse(node.right,code + '1')

    traverse(self)
    return codes

def decode_bitstring(self, bitstring):
    decode_text = ''
    current_node = self
    for bit in bitstring:
        if bit == '0':
            current_node = current_node.left
        elif bit == '1':
            current_node = current_node.right
        if current_node.char is not None:
            decode_text += current_node.char
            current_node = self
    return decode_text
        
def main():
    case_number = 1
    while True:
        try:
            line = input().strip()
            if line == '0':
                break
            n = int(line)
            freq_map = {}
            for _ in range(n):
                parts = input().strip().split()
                char = parts[0]
                freq = int(parts[1])
                freq_map[char] = freq
            bitstring = input().strip()

            root = build_huffman_tree(freq_map)
            code_map = generate_codes(root)
            decoded = decode_bitstring(root, bitstring)

            print(f'Huffman Codes #{case_number}')
            for char in sorted(code_map):  # 字母排序輸出
                print(f'{char} {code_map[char]}')

            print(f'Decode = {decoded}')
            case_number += 1

            print()
        except EOFError:
            break

if __name__ == "__main__":
    main()
