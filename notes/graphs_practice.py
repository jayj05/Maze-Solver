graph = [None]

class AdjNode:
    def __init__(self, vertex):
        self.vertex = vertex 
        self.next = None 

node = AdjNode(1)
node.next = graph[0]
graph[0] = node

node = AdjNode(2)
node.next = graph[0]
graph[0] = node

node = AdjNode(3)
node.next = graph[0]
graph[0] = node

for i in range(1):
    temp = graph[i]
    while temp:
        print(temp.vertex)
        temp = temp.next

