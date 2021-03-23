# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:12:48 2019

@author: frani
"""
class Node(object): 
    def __init__(self, name): 
        """Assumes name is a string""" 
        self.name = name 
    def getName(self): 
        return self.name 
    def __str__(self): 
        return self.name
class Edge(Node): 
    def __init__(self, src, dest): 
        """Assumes src and dest are nodes""" 
        self.src = src 
        self.dest = dest       
    def getSource(self): 
        return self.src 
    def getDestination(self): 
        return self.dest 
    def __str__(self): 
        return Node.getName(self.src) + "->"+ Node.getName(self.dest)

class Digraph(object):
    "edges is a dict mapping each node to a list of its children"
    def __init__(self):
        self.edges = {}
    def addNode(self, node): 
        if node in self.edges:
            raise ValueError('Duplicate node') 
        else: 
            self.edges[node] = []
    def addEdge(self, edge): 
        src = edge.getSource() 
        dest = edge.getDestination() 
        if not (src in self.edges and dest in self.edges): 
            raise ValueError('Node not in graph') 
        self.edges[src].append(dest)
    def childrenOf(self, node): 
        return self.edges[node]
    def hasNode(self, node): 
        return node in self.edges
    def getNode(self, name): 
        for n in self.edges: 
            if n.getName() == name: 
                return n 
        raise NameError(name)
    def __str__(self): 
        result = '' 
        for src in self.edges: 
            for dest in self.edges[src]: 
                result = result + src.getName() + '->' + dest.getName() + '\n' 
        return result[:-1] #omit final newline
class Graph(Digraph): 
    def addEdge(self, edge):
        Digraph.addEdge(self, edge) 
        rev = Edge(edge.getDestination(), edge.getSource()) 
        Digraph.addEdge(self, rev)

def buildCityGraph(): 
    g = Graph() 
    for name in ('Boston', 'Providence', 'New York', 'Chicago', 'Denver', 'Phoenix', 'Los Angeles'): #Create 7 nodes 
        g.addNode(Node(name))

    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence'))) 
    g.addEdge(Edge(g.getNode('Boston'),g.getNode ('New York'))) 
    g.addEdge(Edge(g.getNode('Providence'),g.getNode ('Boston'))) 
    g.addEdge(Edge(g.getNode('Providence'),g.getNode ('New York'))) 
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago'))) 
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver'))) 
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix'))) 
    g.addEdge(Edge(g.getNode('Denver'), g.getNode("New York"))) 
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix'))) 
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g

e=buildCityGraph()
print(e)

        
#nodes = []
#nodes.append(Node("ABC")) # nodes[0]
#nodes.append(Node("ACB")) # nodes[1]
#nodes.append(Node("BAC")) # nodes[2]
#nodes.append(Node("BCA")) # nodes[3]
#nodes.append(Node("CAB")) # nodes[4]
#nodes.append(Node("CBA")) # nodes[5]
#
#g = Graph()
#for n in nodes:
#    g.addNode(n)
#g.addEdge(Edge(nodes[0], nodes[1]))
#g.addEdge(Edge(nodes[0], nodes[2]))
#g.addEdge(Edge(nodes[1], nodes[4]))
#g.addEdge(Edge(nodes[2], nodes[3]))
#g.addEdge(Edge(nodes[3], nodes[5]))
#g.addEdge(Edge(nodes[4], nodes[5]))

#print(g)
        
class WeightedEdge(Edge):
    def __init__(self, src, dest, weight):
        # Your code here
        Edge.__init__(self,src,dest)
        self.weight=weight
    def getWeight(self):
        return self.weight
    def __str__(self):
        return Edge.__str__(self)+"("+str(self.getWeight()) +")" 

#c=WeightedEdge("A","B",3)
#c.__str__()