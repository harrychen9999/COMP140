"""
The Kevin Bacon Game.

Replace "pass" with your code.
"""

import simpleplot
import comp140_module4 as movies

class Queue:
    """
    A simple implementation of a FIFO queue.
    """
    
    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._initialize_queue=[]
  
        

    def __len__(self):
        """
        Return number of items in the queue.
        """
        return len(self._initialize_queue)

    def __str__(self):
        """
        Returns a string representation of the queue.
        """
        return "A"
    
    def push(self, item):
        """
        Add item to the queue.
        """        
        self._initialize_queue.append(item)
        
    def pop(self):
        """
        Remove and return the least recently inserted item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
      
        return self._initialize_queue.pop(0)
      
    
    def clear(self):
        """
        Remove all items from the queue.
        """
        self._initialize_queue=[]
        return self._initialize_queue




def bfs(graph, start_node):
    """
    Performs a breadth-first search on graph starting at the 
    start_node.

    Returns a two-element tuple containing a dictionary
    associating each visited node with the order in which it 
    was visited and a dictionary associating each visited node 
    with its parent node.
    """
    queue=Queue()
    dist={}
    parent={}
#   The following sentences is used to give each node
#	initial state. Since these nodes have never been visited, 
#	therefore they can be understood as not connected to other nodes.
#	which means so far they don't have parent nodes and their distance
#	to starting node is infinity	
    for node in graph.nodes():
        dist[node]=float("inf")
        parent[node]=None 
    dist[start_node]=0
    queue.push(start_node)
#   When the queue is not empty, delete the point from the queue.
#	Then find neighbors of that node to begin next search
    for node in graph.nodes():
        if (len(queue)!=0):
            node2=queue.pop()
            for neighbor in graph.get_neighbors(node2): 
#   Since we don't want to repeat visiting the neighbor node,            
#	we here check if the distance of the neighbor node is still infinity. Infinity
#	means the neighbor node has never been visited. When visited, the distance of
#	the neighbor node equals to the distance of the node2 pluses 1(because it is one step further)
#	In such situation, the parent node of the neighbor node is node2
#	Then push the neighbor node into the queue
                if dist[neighbor]==float("inf"):
                    dist[neighbor]=dist[node2]+1
                    parent[neighbor]=node2
                    queue.push(neighbor)
    return dist, parent 

def distance_histogram(graph, node):
    """
    Given a graph and a node in that graph, returns a histogram
    (in the form of a dictionary mapping distance to counts) of
    the distances from node to every other node in the graph.
    """
    distance_counts={}
    bfs_result=bfs(graph, node)
#   bfs_result[0] is the map which maps the node with their 
#	distances to the starting node. The following sentences 
#   are used to iterate every other nodes and calculate the 
# 	differences(which are the distances)between them and given node
#   Since distance is always positive while the difference may be negative
#   check if differences are positive, if not, then transform them into positive
#   value 
    for other_node in bfs_result[0]:
            distance=bfs_result[0][node]-bfs_result[0][other_node]
            if distance<0:
                distance=0-distance
#   Instead of using default map, I choose to use the following sentences
#   to check if the variable distance is already a key of the map and 
#   assign the value zero to the distance if the output is false
# 	(which means the distance is not already a key ). If the ouput is true, 
#	is true, the value(which is the key's time) of the key distance pluses one 
            if distance not in distance_counts.keys():
                distance_counts[distance]=0
                distance_counts[distance]+=1
            else:
                distance_counts[distance]+=1
              

    return distance_counts

def find_path(graph, start_person, end_person, parents):
    """
    Finds the path from start_person to end_person in the graph, 
    and returns the path in the form:

    [(actor1, set([movie1a, ...])), (actor2, set([movie2a, ...])), ...]
    """
    actor_movie=[]
    path=[]
#   The following setences help check two special situations
#   One is the end person and the start person are same person,
#   Under such a situation,the attribute is set([]). Then translate the
#   set into a sequence, and connect it with the start person after 
#   translating the start_person into a sequence.
#   Then push the new formed sequence into the orignial empty sequence path
    if  end_person==start_person:
        actor_movie=[start_person]+[set(path)]
        actor_movie=tuple(actor_movie)
        path.append(actor_movie)
        return path
#   Another special situations is there is no end person, as a result
#   the there is no path because we can't find its parent nodes
    elif parents[end_person]==None:
        return path
    else:
# 	In the normal situation fist find the path of the last person by
#   using the following sentences
        actor_movie=[end_person]+[set(path)]
        actor_movie=tuple(actor_movie)
        path.append(actor_movie)
#   Here I use the following sentences to find the path between the node
#   named end_person and its parent node. As long as I find the path, I
#   will translate the type of the path refered by a variable named attribute
#   from set to sequence. Also I translate the type of the parent node of the end_person 
#	refered by the variable named end_person into a sequence and combine it with the
#   last sequence into one sequence. Afterwards I translate the new formed sequence
# 	into the tuple and push it into the sequence named path. In this way, I can
# 	show the path in required format. After I finish pushing the tuple into the sequence
#   named path, the value of the end_person will becomes the the value of its parent node.
#   Then keep doing such process until the end person is the same as the start person
        while end_person!=start_person:
            attribute=graph.get_attrs(parents[end_person],end_person)
            actor_movie=[parents[end_person]]+[attribute]
            actor_movie=tuple(actor_movie)
            path.append(actor_movie)
            end_person=parents[end_person]
#   Since the order of elements in my sequence is reversed to the required order,
#   here I reverse the order if elements in the sequence 
    path.reverse()
    return path
  
   

def play_kevin_bacon_game(graph, start_person, end_people):
    """
    Play the "Kevin Bacon Game" on the actors in the given 
    graph, where startperson is the "Kevin Bacon"-esque 
    actor from which the search will start and endpeople 
    is a list of end people to which the search will be 
    performed.
    
    Prints the results out.
    """
    parents=bfs(graph,start_person)[1]
    for end_person in end_people:
        path=find_path(graph, start_person, end_person, parents) 
        movies.print_path(path)
def run():
    """
    Load a graph and play the Kevin Bacon Game.
    """
    graph5000 = movies.load_graph('subgraph5000')
    
    if len(graph5000.nodes()) > 0:
        # You can/should use smaller graphs and other actors while
        # developing and testing your code.
        play_kevin_bacon_game(graph5000, 'Kevin Bacon', 
            ['Amy Adams', 'Andrew Garfield', 'Anne Hathaway', 'Barack Obama', \
             'Benedict Cumberbatch', 'Chris Pine', 'Daniel Radcliffe', \
             'Jennifer Aniston', 'Joseph Gordon-Levitt', 'Morgan Freeman', \
             'Sandra Bullock', 'Tina Fey'])
        
        # Plot distance histograms
        for person in ['Kevin Bacon', 'Stephanie Fratus']:
            hist = distance_histogram(graph5000, person)
            simpleplot.plot_bars(person, 400, 300, 'Distance', \
                'Frequency', [hist], ["distance frequency"])
 
# Uncomment the call to run below when you have completed your code.
# run()
