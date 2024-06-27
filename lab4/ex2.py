from plot import *

class MinHeap:
    def __init__(self, arr=None):
        self.heap = []
        if arr:
            self.heap = arr.copy()
            for i in range(len(self.heap))[::-1]:
                self._sift_down(i)

    def _sift_up(self, i):
        parent = (i - 1) // 2
        while i != 0 and self.heap[i].frequency < self.heap[parent].frequency:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent
            parent = (i - 1) // 2

    def _sift_down(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        
        if left < len(self.heap) and self.heap[left].frequency < self.heap[smallest].frequency:
            smallest = left
        if right < len(self.heap) and self.heap[right].frequency < self.heap[smallest].frequency:
            smallest = right
            
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._sift_down(smallest)

    def insert(self, element):
        self.heap.append(element)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            return None
        min_val = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._sift_down(0)
        return min_val

    def length(self):
        return len(self.heap)
    
    def print_heap(self):
        for node in self.heap:
            print(f"{node.character}{node.frequency}", end=" ")
        print()



class PriorityQueue:
    def __init__(self):
        self.queue = MinHeap()

    def enqueue(self, element):
        self.queue.insert(element)

    def dequeue(self):
        return self.queue.extract_min()

    def is_empty(self):
        return len(self.queue.heap) == 0


class Node:
    def __init__(self, character, frequency, left=None, right=None):
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency


def print_nodes(node):
    print(node.character, node.frequency, end=" LR \n")

def get_frequency(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
            
    return frequency


def build_tree(text):
    frequency = get_frequency(text)
    pq = PriorityQueue()

    for char, freq in frequency.items():
        pq.enqueue(Node(char, freq))
        

    while pq.queue.length() > 1:
        # print("new interation")
        # pq.queue.print_heap()
        left = pq.dequeue()
        # print_nodes(left)
        # pq.queue.print_heap()
        right = pq.dequeue()
        # print_nodes(right)
        # pq.queue.print_heap()
        # print()
        
        new_node = Node(left.character + right.character, left.frequency + right.frequency, left, right)
        
        pq.enqueue(new_node)

    return pq.dequeue()


def huffman_code(node, prefix="", code={}):
    if node is not None:
        if node.character is not None:
            code[node.character] = prefix
        huffman_code(node.left, prefix + "0", code)
        huffman_code(node.right, prefix + "1", code)
    return code

def replace_text(text, dictionary):
    for key, value in dictionary.items():
        text = text.replace(key, value)
    
    return text

input_text = "Ilovedatastructures"
root_node = build_tree(input_text)
codes = huffman_code(root_node)

print("Huffman Codes:")
table = {}
for char, code in codes.items():
    if len(char) == 1:
        table[char] = code

print("Table of Huffman Codes:")
print(table)

print("\nEncoded text:")
text = replace_text(input_text, table)
print(text)
compression_ratio = (len(text) / (8 * len(input_text))) * 100
print("Compression Ratio: {:.2f}%".format(compression_ratio))

draw_huffman_tree(root_node)
