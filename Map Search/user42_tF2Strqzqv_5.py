"""
Map Search
"""

import comp140_module7 as maps
  
class Queue:
    """
    A simple implementation of a FIFO queue.
    """
    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return number of items in the queue.
        """
        return len(self._items)

    def __str__(self):
        """
        Return a string representing the queue.
        """
        return str(self._items)

    def push(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)
    
    def pop(self):
        """
        Return and remove least recently inserted item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
        return self._items.pop(0)
    
    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []

class Stack:
    """
    A simple implementation of a LIFO stack.
    """
    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return number of items in the queue.
        """
        return len(self._items)

    def __str__(self):
        """
        Return a string representing the queue.
        """
        return str(self._items)

    def push(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)
    
    def pop(self):
        """
        Return and remove least recently inserted item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
        return self._items.pop(-1)
    
    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []
    
def bfs_dfs(graph, rac_class, start_node, end_node):
    """
    Performs a breadth-first search or a depth-first search on graph
    starting at the start_node.  The rac_class should either be a
    Queue class or a Stack class to select BFS or DFS.

    Completes when end_node is found or entire graph has been
    searched.

    Returns a dictionary associating each visited node with its parent
    node.
    """
    
    rac=rac_class()
    dist = {}
    parent = {}
# The following statements are used to initialize the parent and distance   
    for node in graph.nodes():
        dist[node] = float('inf')
        parent[node] = None

    dist[start_node] = 0
    rac.push(start_node)
# The following statements are used to implement bfs or dfs
# search based on the recipe given for BFS search
    while len(rac)!=0:
        node = rac.pop()
        nbrs = graph.get_neighbors(node)
        for nbr in nbrs:
            if dist[nbr] == float('inf'):
                    dist[nbr] = dist[node] + 1
                    parent[nbr] = node
                    rac.push(nbr)
# The following statemtns are used to determine when to finish                   
                    if nbr==end_node:
                        return parent
                    
                
    return parent 

def dfs(graph, start_node, end_node, parent):
    """
    Performs a recursive depth-first search on graph starting at the
    start_node.

    Completes when end_node is found or entire graph has been
    searched.

    Modifies parent dictionary to associate each visited node with its 
    parent node.  Assumes that parent initially has one entry that
    associates the original start_node with None.
    """
    nbrs=graph.get_neighbors(start_node)
    key=parent.keys()
#   The variable counter will be used as a condition later
#   whose value will represent whether a certain element is 
#   in the map parent or not
    counter=0
    for element1 in nbrs:
        if parent.has_key(element1)==False:
                counter=1
#   The following statement represents the base case: start_node=end_node
#   or the entire graph has been explored
    if start_node==end_node or counter==0:
        return parent
    else:
        for nbr in nbrs:
            if nbr not in key:
                parent[nbr]=start_node
                dfs(graph,nbr,end_node,parent)
        return parent        
          
#print dfs(maps.load_test_graph('grid'), 'A', 'I', {'A': None}) 
#print maps.load_test_graph('grid')
def getkey(value,dict1):
    """
    This function is used to return the corresponding key for 
    the given value in a given dictionary 
    """
    for element in dict1.items():
        if element[1]==value:
            return element[0]
            
def astar(graph, start_node, end_node,
          edge_distance, straight_line_distance):
    """
    Performs an A* search on graph starting at start_node.

    edge_distance and straigh_line_distance are functions that take
    two nodes and a graph and return a distance.  edge_distance should
    return the actual distance between two neighboring nodes.
    straigh_line_distance should return the heuristic distance between
    any two nodes in the graph.

    Completes when end_node is found or entire graph has been
    searched.

    Returns a dictionary associating each visited node with its parent
    node.
    """
#   The following statements are used to initialize the openset, 
# 	closedset,gcost, hcost and parent
    openset = []
    closedset = []
    openset.append(start_node)
    gcost = {start_node: 0}
    hcost = {start_node: straight_line_distance(start_node, end_node, graph)}
    parent = {start_node: None}
#   while the openset is not empty
    while len(openset) != 0:        
        minnode = openset[0]
        minf = gcost[minnode] + hcost[minnode]
        for node in openset:
# 	the following statements are used to check if the fcost is smaller 
#   than the minimum value, if so update the fcost 
            fost = gcost[node] + hcost[node]
            if fost < minf:
                minnode = node
                minf = fost
#   if minnode is the end_node, end             
        if minnode == end_node:
            break
#   if minnode is not the end_node, remove minnode from the openset and add
#   it to the closedset
        openset.remove(minnode)
        closedset.append(minnode)
        for nbr in graph.get_neighbors(minnode):
# 	the following statements are used to get the new gcost for the nbr node          
            newgcost = gcost[minnode] + edge_distance(minnode, nbr, graph)
            if nbr in openset:
#   the following situation is when newgcost<gcost of nbr when nbr in openset        
                if newgcost < gcost[nbr]:
                    gcost[nbr] = newgcost
                    parent[nbr] = minnode
#   the followingg situations are nbr both not in openset and not in closeset             
            elif (nbr not in openset) and (nbr not in closedset):
                openset.append(nbr)
                parent[nbr] = minnode
                hcost[nbr] = straight_line_distance(nbr, end_node, graph)
                gcost[nbr] = newgcost
    return parent             
# You can replace functions/classes you have not yet implemented with
# None in the call to "maps.start" below and the other elements will
# work.
maps.start(bfs_dfs, Queue, Stack, dfs, astar)
