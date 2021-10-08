# 记录链接的顶点以及每一条边的权重
class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    # 添加从一个顶点到另一个的连接
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])
    
    # 返回邻接表中的所有顶点
    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    # 返回从当前顶点到以参数传入的顶点之间的边的权重
    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    # 返回图中所有顶点的名字
    def getVertices(self):
        return self.vertList.keys()
    
    # 遍历图中的所有顶点对象
    def __iter__(self):
        return iter(self.vertList.values())


if __name__ == "__main__":
    g = Graph()
    for i in range(6):
        g.addVertex(i)