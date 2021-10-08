from graph.graph import Graph
from collections import deque


# 为词梯问题构建单词关系图
def buildGraph(wordFile):
    d = {}
    g = Graph()
    wfile = open(wordFile, 'r')
    # 创建词桶
    for line in wfile:
        word = line[:-1]
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i+1:]
            if bucket in d:
                d[bucket].append(word)
            else:
                d[bucket] = [word]
    # 为同一个桶中的单词添加顶点和边
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1, word2)
    return g


def bfs(g, start):
    start.setDistance(0)
    start.setPred(None)
    q = deque()
    q.append(start)
    while (q.size() > 0):
        currentVert = q.popleft()
        for nbr in currentVert.getConnections():
            if (nbr.getColor() == 'white'):
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                q.append(nbr)
        currentVert.setColor('black')




if __name__ == "__main__":
    g = buildGraph()
    