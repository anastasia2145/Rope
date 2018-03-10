#python 3
import sys

class Node:
    def __init__(self, key, size, left, right, parent):
        (self.key, self.size, self.left, self.right, self.parent) = (key, size, left, right, parent)
        
    def offset(self):
        if self.left:
            return self.left.size + 1
        return 1
        
        
# пересчет весов для узла
def update(v):
    if v is None:
        return

    v.size = 1 + (v.left.size if v.left != None else 0) + (v.right.size if v.right != None else 0)

    if v.left != None:
        v.left.parent = v        
    if v.right != None:
        v.right.parent = v
        
    

def smallRotation(v):
    parent = v.parent
    if parent is None:
        return

    grandparent = v.parent.parent
    if parent.left == v:
        m = v.right
        v.right = parent
        parent.left = m
    else:
        m = v.left
        v.left = parent
        parent.right = m

    update(parent)
    update(v)

    v.parent = grandparent
    if grandparent != None:
        if grandparent.left == parent:
            grandparent.left = v
        else:
            grandparent.right = v


def bigRotation(v):
    if v.parent.left == v and v.parent.parent.left == v.parent:
        # Zig-zig
        smallRotation(v.parent)
        smallRotation(v)
    elif v.parent.right == v and v.parent.parent.right == v.parent:
        # Zig-zig
        smallRotation(v.parent)
        smallRotation(v)
    else:
        # Zig-zag
        smallRotation(v)
        smallRotation(v)

# Splay узла. Делает его новым Root
def splay(v):
    if v is None:
        return None

    while v.parent != None:
        if v.parent.parent is None:
            smallRotation(v)
            break
        bigRotation(v)
    return v

def find(root, key):   
    v = root
    
    while True:
        if v is None:
            return None
        if v.offset() == key:
            return splay(v)
        if v.offset() > key:
            v = v.left
        else:
            key -= v.offset()
            v = v.right


def split(root, key):
    result = find(root, key)
    
    if result is None: 
        if key == 0:
            return (None, root)
        else:
            return (root, None)

    left = result
    right = result.right
    left.right = None
    if right != None:
        right.parent = None

    update(left)
    update(right)

    return (left, right)


def merge(left, right):
    if left == None:
        return right
    if right == None:
        return left
    while right.left != None:
        right = right.left
    right = splay(right)
    right.left = left
    update(right)
    return right


class Rope:
    def __init__(self, S):
        self.res = None
        self.root = None
        for s in S:
            self.insert(s)

    def insert(self, x):
        if self.root == None:
            self.root = Node(x, 1, None, None, None)
        else:
            new_node = Node(x, self.root.size + 1, self.root, None, None)
            self.root.parent = new_node
            self.root = new_node
        return self

    def result(self):
        self.res = []
        self.inOrderTraversal(self.root)
        return ''.join(self.res)

    def process(self, i, j, k):
        (middle, right) = split(self.root, j + 1)
        (left, middle) = split(middle, i)
        erased = merge(left, right)
        (left, right) = split(erased, k)
        self.root = merge(merge(left, middle), right)
        return self

    # def inOrderTraversal(self, v):
        # if v == None:
            # return
        # self.inOrderTraversal(v.left)
        # self.res.append(v.key)
        # self.inOrderTraversal(v.right)
    #Итеративный
    def inOrderTraversal(self, root):
        if not root:
            return

        stack = []
        node = root
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                self.res.append(node.key)
                node = node.right

                
                
rope = Rope(sys.stdin.readline().strip())
q = int(sys.stdin.readline())
for _ in range(q):
    i, j, k = map(int, sys.stdin.readline().strip().split())
    rope.process(i, j, k)
print(rope.result())