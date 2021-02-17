Preeth Kanamangala
PK9297

1. We want to use the stack data struct here because we want to keep
expanding the most recently added node in DFS to get the deepest we can
into the tree. We basically keep running an iteration of removing the most
recent node on the fringe (only if it hasn't been visited before), checking
if it's the goal state, expanding its successors, and adding them to the fringe. 
We also have another stack data struct we use to hold the move we took to get to 
any node. When we expand successors, we add the move it took to get to there to 
this cumulative list. The next 3 algorithms have this exact same implementation
with their relevant differences explained.

2. The only difference between BFS and DFS in the implementation is that we
use a queue instead of a stack because we want to expand layer by layer, which
requires that we look at the nodes added to the fringe in chronological order.

3. The only difference between UCS and BFS is that we order nodes in the fringe
by the total cost it took to get there, which we need a PriorityQueue to do.
This also means that we had to extract and store the cost information of each successor
node when we expand a certain node, and keep track of the total cost for each path.

4. The only difference between A-STAR and UCS is that instead of just ordering nodes
by cost in the fringe, we want to order and store them by cost PLUS heuristic.

5. For this successor function, we basically went through each possible directon
and returned a position for it. In between, we made sure that this position wasn't
a wall, and we updated the visited corners list if this position hasn't been visited
before and is a corner. We then append all this infomation into a list of successors
that we return.

6. We did this heuristic very explicitly. First, we compiled a list of unvisited corners.
Then, logically, we just want to see what the closest node is and use manhattanDistance to get
to it. This is guarenteed to be less than the MazeDistance. Then, we want to go from that node
to the next closest node. We keep doing this until we run out of unvisited corners. This basically
mimics the path that pacman would take IF there were no walls and therefore provides a good
sense of where to go since there are walls.

7. This heuristic is more simple. We know that, worst case, the pacman has the travel the 
MazeDistance to the furthest food item. Best case, it could get every single other food item
on the exact path to that furthest item. Therefore, we can just take the max of all the 
MazeDistances to each food item. 

8. We want to just pass this problem to BFS because we want to just GREEDILY eat the closest
dot. BFS looks at each node layer by layer, as in it will always look at the closest nodes first.
This is exactly what we want, so the previously written BFS will solve it for us. 