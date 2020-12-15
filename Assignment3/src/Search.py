import maze_helper as helper
from pyTree.Tree import Tree as Tree
from queue import Queue,LifoQueue, PriorityQueue
import math
import copy

def Find_Children(maze, Node):                          # A function use to find all the options for each round of searching
    option = []
    West = [Node[0], Node[1]-1]
    North = [Node[0]-1, Node[1]]
    East = [Node[0], Node[1] + 1]
    South = [Node[0]+ 1, Node[1]]

    if(helper.look(maze, West) != 'X'): option.append(West)
    if(helper.look(maze, East) != 'X'): option.append(East)
    if(helper.look(maze, North) != 'X'): option.append(North)
    if(helper.look(maze, South) != 'X'): option.append(South)
    
    return option

def Find_Distance(NodeonTree,Root):
    Total = 0
    while(NodeonTree != Root):
        NodeonTree = NodeonTree.getParent()
        Total = Total + 1
    return Total

def getResult(maze):                    # It is a function that find final numbers of path cost and area explored
    Result = []
    Cost = 0
    Explored = 0
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if(maze[i][j] == 'P' or maze[i][j] == 'G'):
                Cost = Cost + 1
                Explored = Explored + 1
            elif(maze[i][j] == '.'):
                Explored = Explored + 1
    Result.append(Cost)
    Result.append(Explored)
    return Result

def BFS_Search(maze, vis):
    Start = helper.find_pos(maze, what = "S")
    End = helper.find_pos(maze, what = "G")                 #   Set start point and end point
    Result = []
    MaxFrontier = 1
    MaxDepth = 1
    if(Start == End):                                       # If Start is End
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        return Result
    q = Queue(maxsize=(len(maze)*len(maze[0])))             # It is a FIFO queue
    q.put(Start)
    
    Root = Tree(Start)                                      # Use a tree to store all the paths

    while(q.empty() == False):
        if(q.qsize() > MaxFrontier):
            MaxFrontier = q.qsize()
            
        Node = q.get()                                      # Get a node from queue
        NodeonTree = Root.getNode(Node)
        
        depth = Find_Distance(NodeonTree, Root)
        if(MaxDepth < depth):                               # Find the depth of the node
            MaxDepth = depth
            
        children = Find_Children(maze,Node)
        if(vis == True):                                    # Show paths for each round
            if(Node != Start):
                maze[Node[0]][Node[1]] = 'P'                
                helper.show_maze(maze)
                maze[Node[0]][Node[1]] = '.'
            else:
                helper.show_maze(maze)
        for e in children:
            if (e == End):
                newTreeNode = Tree(e)
                NodeonTree.addChild(newTreeNode)
                tempNode = newTreeNode.getParent()
                while(tempNode != Root):
                    maze[tempNode.data[0]][tempNode.data[1]] = 'P'
                    tempNode = tempNode.getParent()                 # Rebuild the path based on the tree                    
                Result = getResult(maze)
                Result.append(MaxFrontier)
                Result.append(MaxDepth)
                return Result
            if(Root.getNode(e) == None):
                newTreeNode = Tree(e)
                maze[e[0]][e[1]] = '.'
                NodeonTree.addChild(newTreeNode)                    # Add child to the tree and to the queue
                q.put(e)
                
    Result.append("Path not found")
    Result.append("Path not found")                             # If no path founded
    Result.append("Path not found")
    Result.append("Path not found")                             # If no path founded
    return Result


def DFS_Search(maze, vis):
    Start = helper.find_pos(maze, what = "S")
    End = helper.find_pos(maze, what = "G")
    Result = []
    MaxFrontier = 1
    MaxDepth = 1
    
    if(Start == End):
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        return Result
    
    q = LifoQueue(maxsize= (len(maze)*len(maze[0])))            # It is a LIFO queue, or called stack
    q.put(Start)
    
    Root = Tree(Start)

    while(q.empty() == False):
        if(q.qsize() > MaxFrontier):
            MaxFrontier = q.qsize()
            
        Node = q.get()
        NodeonTree = Root.getNode(Node)
        
        depth = Find_Distance(NodeonTree, Root)
        if(MaxDepth < depth):                               # Find the depth of the node
            MaxDepth = depth
        
        children = Find_Children(maze,Node)
        if(vis == True):
            if(Node != Start):
                maze[Node[0]][Node[1]] = 'P'
                helper.show_maze(maze)
                maze[Node[0]][Node[1]] = '.'
            else:
                helper.show_maze(maze)
        for e in children:
            if (e == End):
                newTreeNode = Tree(e)
                NodeonTree.addChild(newTreeNode)
                tempNode = newTreeNode.getParent()
                while(tempNode != Root):
                    maze[tempNode.data[0]][tempNode.data[1]] = 'P'
                    tempNode = tempNode.getParent()                 # Rebuild the path based on the tree                    
                Result = getResult(maze)
                Result.append(MaxFrontier)
                Result.append(MaxDepth)
                return Result
            if(Root.getNode(e) == None):
                newTreeNode = Tree(e)
                maze[e[0]][e[1]] = '.'
                NodeonTree.addChild(newTreeNode)                    # Add child to the tree and to the queue
                q.put(e)
                
    Result.append("Path not found")
    Result.append("Path not found")                             # If no path founded
    Result.append("Path not found")
    Result.append("Path not found")
    return Result


def Get_layer(TreeNode, Root):
    layer = 0
    while(TreeNode != Root):
        layer = layer + 1
        TreeNode = TreeNode.getParent()
    return layer

def Find_DLS_Children(maze, Node, NodeonTree, Root):
    option = []
    West = [Node[0], Node[1]-1]
    North = [Node[0]-1, Node[1]]
    East = [Node[0], Node[1] + 1]
    South = [Node[0]+ 1, Node[1]]
    
    tempNodeW = Root.getNode(West)
    tempNodeE = Root.getNode(East)              
    tempNodeN = Root.getNode(North)
    tempNodeS = Root.getNode(South)
    OldDistance = Find_Distance(NodeonTree, Root) + 1
    if(helper.look(maze, West) != 'X'):                     
        if(tempNodeW != None):
             if(Find_Distance(tempNodeW,Root) > OldDistance):           # If the node is on the tree but with higher distance
                Root.delNode(West)
                option.append(West)
        else:
            option.append(West)
    if(helper.look(maze, East) != 'X'): 
        if(tempNodeE != None):
             if(Find_Distance(tempNodeE,Root) > OldDistance):
                Root.delNode(East)
                option.append(East)
        else:
            option.append(East)
    if(helper.look(maze, North) != 'X'): 
        if(tempNodeN != None):
             if(Find_Distance(tempNodeN,Root) > OldDistance):
                Root.delNode(North)
                option.append(North)
        else:
            option.append(North)
    if(helper.look(maze, South) != 'X'): 
        if(tempNodeS != None):
             if(Find_Distance(tempNodeS,Root) > OldDistance):
                Root.delNode(South)
                option.append(South)
        else:
            option.append(South)
    return option


def DLS_Search(maze,vis,depth):
    Start = helper.find_pos(maze, what = "S")
    End = helper.find_pos(maze, what = "G")
    Result = []
    MaxFrontier = 1
    MaxDepth = 1                                    # The maximum number will always show with longest distance

    if(Start == End):
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        return Result
    
    q = LifoQueue(maxsize= (len(maze)*len(maze[0])))                # It is a LIFO queue like DFS
    Root = Tree(Start)
    q.put(Root)
    layer = 0
    
    while(q.empty() == False):
        if(q.qsize() > MaxFrontier):
            MaxFrontier = q.qsize()
            
            
        NodeonTree = q.get()
        Node = NodeonTree.data
        layer = Get_layer(NodeonTree, Root)
        
        if(layer > MaxDepth):
            MaxDepth = layer
        
        if(layer < depth):
            children = Find_DLS_Children(maze,Node,NodeonTree,Root)
            if(vis == True):
                if(Node != Start):
                    maze[Node[0]][Node[1]] = 'P'
                    helper.show_maze(maze)
                    maze[Node[0]][Node[1]] = '.'
                else:
                   helper.show_maze(maze)
            for e in children:
                if (e == End):
                    newTreeNode = Tree(e)
                    NodeonTree.addChild(newTreeNode)
                    tempNode = newTreeNode.getParent()
                    while(tempNode != Root):
                        maze[tempNode.data[0]][tempNode.data[1]] = 'P'
                        tempNode = tempNode.getParent()                 # Rebuild the path based on the tree                    
                    Result = getResult(maze)
                    Result.append(MaxFrontier)
                    Result.append(MaxDepth)
                    return Result
                newTreeNode = Tree(e)
                maze[e[0]][e[1]] = '.'
                NodeonTree.addChild(newTreeNode)                    # Add child to the tree and to the queue
                q.put(newTreeNode)
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    return Result
    
    
def IDS_Search(maze, vis):
    result = []
    result.append("Path not found")
    result.append("Path not found")
    i = 1                                             # i is started in 1
    while(result[0] == "Path not found"):               # i is the layer and the upper bound of IDS to avoid the program stuck in loop
        result = DLS_Search(maze, vis, i)
        i = i + 1
    return result

    
###################################################################################################

def Find_Child(maze, Node, End, Dtype, Visited):
    West = [Node[0], Node[1]-1]
    North = [Node[0]-1, Node[1]]
    East = [Node[0], Node[1] + 1]
    South = [Node[0]+ 1, Node[1]]
    BestNode = [-1,-1]
    BestDistance = 0
    if(helper.look(maze, West) != 'X' and West not in Visited):         # Find Children with best h(n)
        if(West == End):
            return West
        else:
            maze[West[0]][West[1]] = '.'
            Distance = 0
            if(Dtype == "MA"):
                Distance = abs(West[0] - End[0]) + abs(West[1] - End[1])
            elif(Dtype == "EU"):
                Distance =  math.sqrt((abs(West[0] - End[0]))**2 + (abs(West[1] - End[1]))**2)  
            if(Distance <= BestDistance or BestDistance == 0):
                BestNode = West
                BestDistance = Distance
    if(helper.look(maze, East) != 'X' and East not in Visited):
        if(East == End):
            return East
        else:
            maze[East[0]][East[1]] = '.'
            Distance = 0
            if(Dtype == "MA"):
                Distance = abs(East[0] - End[0]) + abs(East[1] - End[1])
            elif(Dtype == "EU"):
                Distance =  math.sqrt((abs(East[0] - End[0]))**2 + (abs(East[1] - End[1]))**2)
            if(Distance <= BestDistance or BestDistance == 0):
                BestNode = East
                BestDistance = Distance
    if(helper.look(maze, North) != 'X'and North not in Visited): 
        if(North == End):
            return North
        else:
            maze[North[0]][North[1]] = '.'
            Distance = 0
            if(Dtype == "MA"):
                Distance = abs(North[0] - End[0]) + abs(North[1] - End[1])
            elif(Dtype == "EU"):
                Distance =  math.sqrt((abs(North[0] - End[0]))**2 + (abs(North[1] - End[1]))**2)
            if(Distance <= BestDistance or BestDistance == 0):
                BestNode = North
                BestDistance = Distance
    if(helper.look(maze, South) != 'X' and South not in Visited): 
        if(South == End):
            return South
        else:
            maze[South[0]][South[1]] = '.'
            Distance = 0
            if(Dtype == "MA"):
                Distance = abs(South[0] - End[0]) + abs(South[1] - End[1])
            elif(Dtype == "EU"):
                Distance =  math.sqrt((abs(South[0] - End[0]))**2 + (abs(South[1] - End[1]))**2)
            if(Distance <= BestDistance or BestDistance == 0):
                BestNode = South
                BestDistance = Distance        # Best Node is a list with the best child nearby and the number of area explored
    return BestNode
    
    
    

def GBFS_Search(maze, vis, Dtype):
    Start = helper.find_pos(maze, what = "S")
    End = helper.find_pos(maze, what = "G")
    Result = []
    Visited = []
    PathCost = 0
    AreaExplored = 0
    MaxFrontier = 1
    MaxDepth = 1
    
    if(Start == End):
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        return Result
    
    Path = LifoQueue(maxsize= (len(maze)*len(maze[0])))
    Path.put(Start)
    Visited.append(Start)
    
    while(Path.empty != False):
        if(Path.qsize() > MaxFrontier):
            MaxFrontier = Path.qsize()
        Node = Path.get()
        NewNode = Find_Child(maze,Node,End,Dtype, Visited)
        if(NewNode[0] != -1):
            if(NewNode == End):
                Result = getResult(maze)
                Result.append(MaxFrontier)
                Result.append(Result[0])
                return Result
            else:
                Visited.append(NewNode)
                Path.put(Node)
                Path.put(NewNode)
                maze[NewNode[0]][NewNode[1]] = 'P'
                if(vis == True):
                    helper.show_maze(maze)
        else:
            maze[Node[0]][Node[1]] = '.'
            Node = Path.get()
            maze[Node[0]][Node[1]] = 'P'
            Path.put(Node)
            if(vis == True):
                helper.show_maze(maze)
                
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    return Result
       
###################################################################################################

def Find_F_Distance(maze, Node, Root, NodeonTree, End, Dtype):                 # A function for f(n)
    Total = 0
    while(NodeonTree != Root):
        NodeonTree = NodeonTree.getParent()
        Total = Total + 1

    if(Dtype == "MA"):
        Total = Total  + abs(Node[0] - End[0]) + abs(Node[1] - End[1])
    elif(Dtype == "EU"):
        Total = Total  +  math.sqrt((abs(Node[0] - End[0]))**2 + (abs(Node[1] - End[1]))**2)
        
    return Total

def Find_A_Star_Children(maze, Node, Root, NodeonTree, End, Dtype):
    Children = []
    
    NewPath = []
    Visited = 0
    while(NodeonTree != Root):
        NewPath.append(NodeonTree.data)
        NodeonTree = NodeonTree.getParent()
        Visited = Visited + 1
    NewPath.append(NodeonTree.data)
    Visited = Visited + 1                   # Rebuild the path based on the node on tree
    
    West = [Node[0], Node[1]-1]
    if(helper.look(maze, West) != 'X' and West not in NewPath):
        Children.append(West)
        
    North = [Node[0]-1, Node[1]]
    if(helper.look(maze, North) != 'X' and North not in NewPath):
        Children.append(North)
        
    East = [Node[0], Node[1] + 1]
    if(helper.look(maze, East) != 'X' and East not in NewPath):
        Children.append(East)
        
    South = [Node[0]+ 1, Node[1]]
    if(helper.look(maze, South) != 'X' and South not in NewPath):
        Children.append(South)
    
    return Children                             # Return a list of options that it can go
    

def UpdateMaze(maze, NodeonTree, vis):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if(maze[i][j] == 'P'):          
                maze[i][j] = '.'            # The original path becomes explored
                
    path = []
    while(NodeonTree.isRoot() == False):
        path.append(NodeonTree.data)
        NodeonTree = NodeonTree.getParent() # Get the new path
    
    for e in path:
        maze[e[0]][e[1]] = 'P'             # Put new path to red
    if(len(path) != 0):
        maze[path[0][0]][path[0][1]] = '.'  # The head is still under exploration
    if(vis == True):
        helper.show_maze(maze)
    return path

def A_Star_Search(maze, vis, Dtype):
    Start = helper.find_pos(maze, what = "S")            
    End = helper.find_pos(maze, what = "G")
    Result = []
    MaxFrontier = 1
    MaxDepth = 1
    counter = 0                     # a counter to identify paths with same distance
    if(Start == End):
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        return Result
    
    q = []                          # It's a sorted list with nodes (can be built as a path by tree) from shortest f(n) to largest f(n), like priority queue
    Root = Tree(Start)
    q.append([Find_F_Distance(maze,Start,Root,Root, End, Dtype), Root, counter])
    while (len(q) != 0):
        if(len(q) > MaxFrontier):
            MaxFrontier = len(q)
        tNode = q[0].copy()        # Pull out the node with smallest f(n)
        q.pop(0)

        NodeonTree = tNode[1]
        Node = NodeonTree.data
        
        depth = Find_Distance(NodeonTree, Root)
        if(MaxDepth < depth):                               # Find the depth of the node
            MaxDepth = depth

        UpdateMaze(maze, NodeonTree, vis)           # Update maze with each new path

        if(Node == End):
            newTreeNode = Tree(Node)
            NodeonTree.addChild(newTreeNode)
            tempNode = newTreeNode.getParent()
            while(tempNode != Root):
                maze[tempNode.data[0]][tempNode.data[1]] = 'P'
                tempNode = tempNode.getParent()
            maze[End[0]][End[1]] = 'G'              # Remark Path and Destination's colors

            Result = getResult(maze)
            Result.append(MaxFrontier)
            Result.append(MaxDepth)
            return Result
        
        children = Find_A_Star_Children(maze,Node,Root,NodeonTree,End, Dtype)               # Get the children of the current path
        
        for e in children:
            counter = counter + 1                       # Update counter to make diffferent identification for the node
            newchild = Tree(e)
            NodeonTree.addChild(newchild)
            newchildDistance = Find_Distance(NodeonTree, Root)
            UpdateMaze(maze, newchild, vis)
            
            newDistance = Find_F_Distance(maze,e,Root,newchild, End, Dtype)    # Find the f(n) for that node
            
            find = False                                        # insert the new node into the sorted list 
            index = -1
            has = False
            for a in range(len(q)):
                if(e == q[a][1].data):                         # Find where the node is already in the container
                    if(newDistance < q[a][0]):
                        q.pop(a)
                    else:
                        has = True
            if(has == False):                                   # Insert it into the container
                for b in range(len(q)):
                    if(newDistance < q[a][0]):
                        q.insert(a ,[newDistance, newchild, counter])
                        find = True
                        break
                    elif(newDistance == q[a][0]):
                        if(counter >= q[a][2]):
                            q.insert(a ,[newDistance, newchild, counter])
                            find = True
                            break;   
                if(find == False):
                    q.append([newDistance, newchild, counter])
                        
                
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    return Result


def Find_Weightd_F_Distance(maze, Node, Root, NodeonTree, End, Dtype, Weight):                 # A function for f(n)
    Total = 0
    while(NodeonTree != Root):
        NodeonTree = NodeonTree.getParent()
        Total = Total + 1

    if(Dtype == "MA"):
        Total = Total  + Weight * ( abs(Node[0] - End[0]) + abs(Node[1] - End[1]))
    elif(Dtype == "EU"):
        Total = Total  + Weight * ( math.sqrt((abs(Node[0] - End[0]))**2 + (abs(Node[1] - End[1]))**2) )
        
    return Total


def Weighted_A_Star_Search(maze, vis, Dtype, Weight):
    Start = helper.find_pos(maze, what = "S")            
    End = helper.find_pos(maze, what = "G")
    Result = []
    MaxFrontier = 1
    MaxDepth = 1
    counter = 0                     # a counter to identify paths with same distance
    if(Start == End):
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        Result.append("Start is End")
        return Result
    
    q = []                          # It's a sorted list with nodes (can be built as a path by tree) from shortest f(n) to largest f(n), like priority queue
    Root = Tree(Start)
    q.append([Find_Weightd_F_Distance(maze,Start,Root,Root, End, Dtype, Weight), Root, counter])
    while (len(q) != 0):
        if(len(q) > MaxFrontier):
            MaxFrontier = len(q)
        tNode = q[0].copy()        # Pull out the node with smallest f(n)
        q.pop(0)

        NodeonTree = tNode[1]
        Node = NodeonTree.data
        
        depth = Find_Distance(NodeonTree, Root)
        if(MaxDepth < depth):                               # Find the depth of the node
            MaxDepth = depth

        UpdateMaze(maze, NodeonTree, vis)           # Update maze with each new path

        if(Node == End):
            newTreeNode = Tree(Node)
            NodeonTree.addChild(newTreeNode)
            tempNode = newTreeNode.getParent()
            while(tempNode != Root):
                maze[tempNode.data[0]][tempNode.data[1]] = 'P'
                tempNode = tempNode.getParent()
            maze[End[0]][End[1]] = 'G'              # Remark Path and Destination's colors

            Result = getResult(maze)
            Result.append(MaxFrontier)
            Result.append(MaxDepth)
            return Result
        
        children = Find_A_Star_Children(maze,Node,Root,NodeonTree,End, Dtype)               # Get the children of the current path
        
        for e in children:
            counter = counter + 1                       # Update counter to make diffferent identification for the node
            newchild = Tree(e)
            NodeonTree.addChild(newchild)
            newchildDistance = Find_Distance(NodeonTree, Root)
            UpdateMaze(maze, newchild, vis)
            
            newDistance = Find_Weightd_F_Distance(maze,e,Root,newchild, End, Dtype, Weight)    # Find the f(n) for that node
            
            find = False                                        # insert the new node into the sorted list 
            index = -1
            has = False
            for a in range(len(q)):
                if(e == q[a][1].data):                         # Find where the node is already in the container
                    if(newDistance < q[a][0]):
                        q[a] = [newDistance, newchild, counter] 
                    has = True
            if(has == False):                                   # Insert it into the container
                for b in range(len(q)):
                    if(newDistance < q[a][0]):
                        q.insert(a ,[newDistance, newchild, counter])
                        find = True
                        break
                    elif(newDistance == q[a][0]):
                        if(counter >= q[a][2]):
                            q.insert(a ,[newDistance, newchild, counter])
                            find = True
                            break;   
                if(find == False):
                    q.append([newDistance, newchild, counter])
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    Result.append("Path not found")
    return Result






















def BFS_SearchRunner(maze,vis):
    mazes = []    
    mazes.append("small_maze.txt")
    mazes.append("medium_maze.txt")
    mazes.append("large_maze.txt")
    mazes.append("empty_maze.txt")
    mazes.append("wall_maze.txt")
    mazes.append("loops_maze.txt")
    mazes.append("open_maze.txt")

    for e in mazes:
        f = open(e, "r")
        maze_str = f.read()
        maze = helper.parse_maze(maze_str)
        result = []
        print("Running BFS with ", e)
        localResult = BFS_Search(maze,False)
        helper.show_maze(maze)
        print("Path cost: ", localResult[0])
        print("Explored squares: ", localResult[1])
        print("Maximum size of the frontier: ", localResult[2])
        print("Maximum tree depth: ", localResult[3])      


f = open("open_maze.txt", "r")
maze_str = f.read()
maze = helper.parse_maze(maze_str)
result = A_Star_Search(maze,False, "EU")
print("Path cost: ", result[0])
print("Explored squares: ", result[1])
print("Max Size: ", result[2])
print("Max Depth: ", result[3])
helper.show_maze(maze)

