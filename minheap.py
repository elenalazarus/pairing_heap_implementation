import math


class Heap:
    def __init__(self):
        self.heap_size = 0
        self.ar = []
        self.largest = 0

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2


class MinHeap(Heap):
    def min_heapify(self, i):
        p = self.left(i)
        q = self.right(i)
        if p < len(self.ar) and self.ar[p] < self.ar[i]:
            self.largest = p
        else:
            self.largest = i
        if q < len(self.ar) and self.ar[q] < self.ar[self.largest]:
            self.largest = q
        if self.largest != i:
            self.ar[i], self.ar[self.largest] = self.ar[self.largest], self.ar[
                i]
            self.min_heapify(self.largest)

    def build_min_heap(self):
        for i in range(len(self.ar) // 2 - 1, -1, -1):
            self.min_heapify(i)


class MaxHeap(Heap):
    def max_heapify(self, i):
        p = self.left(i)
        q = self.right(i)
        if p < len(self.ar) and self.ar[p] > self.ar[i]:
            self.largest = p
        else:
            self.largest = i
        if q < len(self.ar) and self.ar[q] > self.ar[self.largest]:
            self.largest = q
        if self.largest != i:
            self.ar[i], self.ar[self.largest] = self.ar[self.largest], self.ar[
                i]
            self.max_heapify(self.largest)

    def build_max_heap(self):
        for i in range(len(self.ar) // 2, -1, -1):
            try:
                self.max_heapify(i)
            except IndexError:
                continue


class Median:
    def __init__(self):
        self.min_heap = MinHeap()
        self.max_heap = MaxHeap()

    def get_median(self):
        if len(self.min_heap.ar) == len(self.max_heap.ar):
            return self.max_heap.ar[0], self.min_heap.ar[0]
        elif len(self.min_heap.ar) < len(self.max_heap.ar):
            return self.max_heap.ar[0]
        else:
            return self.min_heap.ar[0]

    def get_maxheap_elements(self):
        return self.max_heap.ar

    def get_minheap_elements(self):
        return self.min_heap.ar

    def add_element(self, value):
        if len(self.min_heap.ar) == len(self.max_heap.ar) == 0:
            self.max_heap.ar.append(value)
            self.max_heap.build_max_heap()
        elif value < self.max_heap.ar[0]:
            self.max_heap.ar.append(value)
            self.max_heap.build_max_heap()
        elif value > self.max_heap.ar[0]:
            self.min_heap.ar.append(value)
            self.min_heap.build_min_heap()

        if len(self.max_heap.ar) - len(self.min_heap.ar) == 2:
            self.min_heap.ar.append(self.max_heap.ar[0])
            self.max_heap.ar.pop(0)
            self.min_heap.build_min_heap()
            self.max_heap.build_max_heap()

        elif len(self.min_heap.ar) - len(self.max_heap.ar) == 2:
            self.max_heap.ar.append(self.min_heap.ar[0])
            self.min_heap.ar.pop(0)
            self.min_heap.build_min_heap()
            self.max_heap.build_max_heap()


class Node:
    def __init__(self, val):
        self.val = val
        self.children = []


class PairingMinHeap:
    def __init__(self):
        self.root = None

    def find_min(self):
        if self.root is not None:
            return self.root.val

    def merge(self, root1, root2):
        if root1 is None:
            return root2
        elif root2 is None:
            return root1
        elif root1.val < root2.val:
            root1.children.append(root2)
            return root1
        else:
            root2.children.append(root1)
            return root2

    def insert(self, val):
        self.root = self.merge(self.root, Node(val))

    def delete_min(self):
        if self.root is None:
            raise ValueError("Heap is empty!")
        else:
            self.root = self.merge_pairs(self.root.children)

    def merge_pairs(self, l):
        if len(l) == 0:
            return None
        elif len(l) == 1:
            return l[0]
        else:
            return self.merge(self.merge(l[0], l[1]),
                              self.merge_pairs(l[2:]))


class PairingMaxHeap:
    def __init__(self):
        self.root = None

    def find_min(self):
        if self.root is not None:
            return self.root.val

    def merge(self, root1, root2):
        if root1 is None:
            return root2
        elif root2 is None:
            return root1
        elif root1.val > root2.val:
            root1.children.append(root2)
            return root1
        else:
            root2.children.append(root1)
            return root2

    def insert(self, val):
        self.root = self.merge(self.root, Node(val))

    def delete_max(self):
        if self.root is None:
            raise ValueError("Heap is empty!")
        else:
            self.root = self.merge_pairs(self.root.children)

    def merge_pairs(self, l):
        if len(l) == 0:
            return None
        elif len(l) == 1:
            return l[0]
        else:
            return self.merge(self.merge(l[0], l[1]),
                              self.merge_pairs(l[2:]))


class PairingMedian:
    def __init__(self):
        self.min_heap = PairingMinHeap()
        self.max_heap = PairingMaxHeap()

    def get_median(self):
        if self.min_heap.root is None:
            return self.max_heap.root.val
        elif self.max_heap.root is None:
            return self.min_heap.root.val
        elif len(self.get_minheap_elements()) == len(
                self.get_maxheap_elements()):
            return self.max_heap.root.val, self.min_heap.root.val
        elif len(self.get_minheap_elements()) < len(
                self.get_maxheap_elements()):

            return self.max_heap.root.val
        else:

            return self.min_heap.root.val

    def bfs(self, root):
        res = []
        if (root == None):
            return []
        queue = [i for i in root.children]
        res += [root.val]
        while (queue != []):
            current = queue.pop(0)
            res += [current.val]
            queue += [i for i in current.children]
        return res

    def get_maxheap_elements(self):
        lst = self.bfs(self.max_heap.root)
        return lst

    def get_minheap_elements(self):
        lst = self.bfs(self.min_heap.root)
        return lst

    def add_element(self, value):
        if self.min_heap.root is None and self.max_heap.root is None:
            self.max_heap.insert(value)
        elif value < self.max_heap.root.val:
            self.max_heap.insert(value)
        elif value > self.max_heap.root.val:
            self.min_heap.insert(value)
        print(self.get_maxheap_elements())
        print(self.get_minheap_elements())
        if self.min_heap.root is None and self.max_heap.root is not None:
            if len(self.get_maxheap_elements()) == 2:
                self.min_heap.insert(self.max_heap.root.val)
                self.max_heap.delete_max()
        elif self.max_heap.root is None and self.min_heap.root is not None:
            if len(self.get_minheap_elements()) == 2:
                self.max_heap.insert(self.min_heap.root.val)
                self.min_heap.delete_min()
        elif self.max_heap.root is not None and self.min_heap.root is not None:
            if len(self.get_maxheap_elements()) - len(
                    self.get_minheap_elements()) == 2:
                self.min_heap.insert(self.max_heap.root.val)
                self.max_heap.delete_max()
            elif len(self.get_minheap_elements()) - len(
                    self.get_maxheap_elements()) == 2:
                self.max_heap.insert(self.min_heap.root.val)
                self.min_heap.delete_min()


if __name__ == "__main__":
    h = PairingMedian()
    h.add_element(10)
    h.add_element(4)
    h.add_element(3)
    h.add_element(6)
    h.add_element(9)
    h.add_element(25)

    # # print(h.get_maxheap_elements())
    # # print(h.get_minheap_elements())

    # # print()
    h.add_element(1)
    print(h.get_maxheap_elements())
    print(h.get_minheap_elements())
    print(h.get_median())
