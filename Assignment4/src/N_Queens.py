import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import math
import copy 
import random
from queue import PriorityQueue
import time
import matplotlib.pyplot as plt
from math import e

def random_board(n):
    """Creates a random board of size n x n. Note that only a single queen is placed in each column!"""
    
    return(np.random.randint(0,n-1, size = n))


def conflicts(board):
    """Caclulate the number of conflicts, i.e., the objective function."""
    
    board = np.array(board)
    
    n = len(board)
    conflicts = 0

    # check horizontal (we do not check vertical since the state space is restricted to one queen per col)
    for i in range(n): conflicts += math.comb(np.sum(board == i), 2)
    #print(f"Horizontal conflicts: {conflicts}")
    
    # check for each queen diagonally up and down (only to the right side of the queen)
    for j in range(n):
        q_up = board[j]
        q_down = board[j]
     
        for jj in range(j+1, n):
            q_up -= 1
            q_down += 1
            if board[jj] == q_up: conflicts += 1
            if board[jj] == q_down: conflicts += 1
        #print(f"Conflicts after queen {j}: {conflicts}")
       
    return(conflicts)
        

def show_board(board, cols = ['white', 'gray']):  
    """display the board"""
    
    n = len(board)
    
    # create chess board display
    display = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            if (((i+j) % 2) != 0): 
                display[i,j] = 1
    
    cmap = colors.ListedColormap(cols)
    fig, ax = plt.subplots()
    ax.imshow(display, cmap = cmap, 
              norm = colors.BoundaryNorm(range(len(cols)+1), cmap.N))
    ax.set_xticks([])
    ax.set_yticks([])
    
    # place queens. Note: 1 and j are switched. Unicode u265B is a black queen
    for j in range(n):
        plt.text(j, board[j], u"\u265B", fontsize = 48, 
                 horizontalalignment = 'center',
                 verticalalignment = 'center')
    
    print(f"Board with {conflicts(board)} conflicts.")
    plt.show()
    
    
#####################################################################################################################################

    
def FindBest(board):                            # Find the best neighbour nearby
    bestLayout = board
    bestConflict = conflicts(bestLayout)
    
    for i in range(len(bestLayout)):
        for j in range(len(bestLayout)):                # Loop through all its neighbours
            currentLayout = copy.deepcopy(board)
            currentLayout[i] = j
            newconflict = conflicts(currentLayout)
            if(newconflict <= bestConflict):            # Here is equal so that it allows movement on the flat local maxima.
                bestLayout = currentLayout
                bestConflict = newconflict
    return bestLayout
                
    
def SAHC_Search(board, maxStep, vis):                   # Max is the maximum number of repeated steps it allowed
    current = board
    currentConflict = conflicts(current)
    UnchangedTimes = 0
    step = 0
    if(vis is True):
        print(f"Step: {step}")
        print(f"Queens (left to right) are at rows: {current}") 
        show_board(current)
        
    while(currentConflict != 0):
        step = step + 1
        newboard = FindBest(current)
        newConflicts = conflicts(newboard)
        
        if(newConflicts < currentConflict):
            if(vis is True):
                print(f"\nStep: {step}")
                print(f"Queens (left to right) are at rows: {newboard}") 
                show_board(newboard)
            UnchangedTimes = 0
        else:
            UnchangedTimes = UnchangedTimes + 1
        
        current = newboard
        currentConflict = newConflicts
        
        if(UnchangedTimes >= maxStep):                                      # If it gets stuck in the local maxima, stop the code.
            if(vis is True):
                print("Reach maximum repeat bound, but still cannot find global best")
                show_board(current)
            return (step,current)
    return (step,current)


#####################################################################################################################################


def SAHC_Search_Restart(board, maxStep, maxRestart, vis):
    current = board
    currentConflict = conflicts(current)
    UnchangedTimes = 0
    step = 0
    RestartTime = 0
    
    if(vis is True):
        print(f"Step: {step}")
        print(f"Queens (left to right) are at rows: {current}") 
        print(f"Number of conflicts: {currentConflict}")
    if(vis is True):
        show_board(current)
        
    while(currentConflict != 0):
        step = step + 1
        newboard = FindBest(current)
        newConflicts = conflicts(newboard)
        
        if(newConflicts < currentConflict):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Find smaller conflict")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = 0
        elif((newboard == current).all() == False):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Find same conflict but different layout")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = UnchangedTimes + 1
        else:
            UnchangedTimes = UnchangedTimes + 1
        
        current = newboard
        currentConflict = newConflicts
        
        if(UnchangedTimes >= maxStep):                      # If the function gets stuck in the local maxima within the 100 steps, do the restart
            RestartTime = RestartTime + 1
            if(RestartTime <= maxRestart):                
                current = random_board(len(current))                   # Reset the board
                currentConflict = conflicts(current)
                UnchangedTimes = 0
                if(vis is True):
                    print(f"\nStep: {step}")
                    print("Reach maximum repeat bound, start doing restart. Restart Time: ", RestartTime)
                    print(f"Queens (left to right) are at rows: {current}") 
            else:    
                if(vis is True):                                       # If it is still stucked in the local maxima even reach the maximum number of restart times, end the function
                    print(f"\nStep: {step}")
                    print("Reach maximum restart bound, but still cannot find global best")
                    show_board(current)
                return (step,current)
    return (step,current)


#####################################################################################################################################


def FindRandom(board):
    Total = []
    TotalFlate = []
    oldconflict = conflicts(board)
    for i in range(len(board)):
        for j in range(len(board)):
            if(j != board[i]):
                currentLayout = copy.deepcopy(board)
                currentLayout[i] = j
                if(conflicts(currentLayout) < oldconflict):
                    Total.append(currentLayout)
                elif(conflicts(currentLayout) == oldconflict):
                    TotalFlate.append(currentLayout)
    if(len(Total) != 0):
        return random.choice(Total)
    elif(len(TotalFlate) != 0):
        return random.choice(TotalFlate)
    else:
        return board


def SHC_Search(board, maxStep, maxRestart, vis):
    current = board
    currentConflict = conflicts(current)
    UnchangedTimes = 0
    step = 0
    RestartTime = 0
    
    if(vis is True):
        print(f"Step: {step}")
        print(f"Queens (left to right) are at rows: {current}") 
        print(f"Number of conflicts: {currentConflict}")
    if(vis is True):
        show_board(current)
        
    while(currentConflict != 0):
        step = step + 1
        newboard = FindRandom(current)
        newConflicts = conflicts(newboard)
        
        if(newConflicts < currentConflict):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Find smaller conflict")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = 0
        elif((newboard == current).all() == False):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Find same conflict but different layout")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = UnchangedTimes + 1
        else:
            UnchangedTimes = UnchangedTimes + 1
        
        current = newboard
        currentConflict = newConflicts
        
        if(UnchangedTimes >= maxStep):
            RestartTime = RestartTime + 1
            if(RestartTime <= maxRestart):
                current = random_board(len(current))
                currentConflict = conflicts(current)
                UnchangedTimes = 0
                if(vis is True):
                    print(f"\nStep: {step}")
                    print("Reach maximum repeat bound, start doing restart. Restart Time: ", RestartTime)
                    print(f"Queens (left to right) are at rows: {current}") 
            else:
                if(vis is True):
                    print(f"\nStep: {step}")
                    print("Reach maximum restart bound, but still cannot find global best")
                    show_board(current)
                return (step,current)
    return (step,current)


#####################################################################################################################################

def FindFirst(board):                   # Find the first better neighbour it met.
    FirstFlate = board
    oldconflict = conflicts(board)
    for i in range(len(board)):
        for j in range(len(board)):
            if(j != board[i]):
                currentLayout = copy.deepcopy(board)
                currentLayout[i] = j
                if(conflicts(currentLayout) < oldconflict):
                    return currentLayout                        # Return that best neighbour 
                elif(conflicts(currentLayout) == oldconflict and (FirstFlate == board).all() == True ):
                    FirstFlate = currentLayout                  # Record the first neighbour with same conflicts but different layout
    return FirstFlate                                           # If there is no better neighbour, it will return that


def FCHC_Search(board, maxStep, maxRestart, vis):
    current = board
    currentConflict = conflicts(current)
    UnchangedTimes = 0
    step = 0
    RestartTime = 0
    
    if(vis is True):
        print(f"Step: {step}")
        print(f"Queens (left to right) are at rows: {current}") 
        print(f"Number of conflicts: {currentConflict}")
        show_board(current)
        
    while(currentConflict != 0):
        step = step + 1
        newboard = FindFirst(current)
        newConflicts = conflicts(newboard)
        
        if(newConflicts < currentConflict):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Find smaller conflict")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = 0
        elif((newboard == current).all() == False):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Find same conflict but different layout")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = UnchangedTimes + 1
        else:
            UnchangedTimes = UnchangedTimes + 1
        
        current = newboard
        currentConflict = newConflicts
        
        if(UnchangedTimes >= maxStep):
            RestartTime = RestartTime + 1
            if(RestartTime <= maxRestart):
                current = random_board(len(current))
                currentConflict = conflicts(current)
                UnchangedTimes = 0
                if(vis is True):
                    print(f"\nStep: {step}")
                    print("Reach maximum repeat bound, start doing restart. Restart Time: ", RestartTime)
                    print(f"Queens (left to right) are at rows: {current}") 
            else:
                if(vis is True):
                    print(f"\nStep: {step}")
                    print("Reach maximum restart bound, but still cannot find global best")
                    show_board(current)
                return (step,current)
    return (step,current)


#####################################################################################################################################


def Find_Option(board, TBList):
    oldconflict = conflicts(board) 
    q = PriorityQueue(maxsize=(len(board)*len(board)))   # Use a PriorityQueue to store all the neighbours, sorted based on the conflicts    
    count = 0

    for i in range(len(board)):
        for j in range(len(board)):
            if(j != board[i]):
                newItem = [i, j]
                newLayout = copy.deepcopy(board)
                newLayout[i] = j
                newConflict = conflicts(newLayout) - oldconflict
                q.put((newConflict, count, newItem))        # Put all the neighbours into the queue
                count = count + 1
    FirstItem = q.get()[2]                                 
    while(FirstItem in TBList):                             # It will get the best neighbour nearby even it has more conflicts, as long as it is not in the Tabu List
        FirstItem = q.get()[2]
    return FirstItem
    

def TB_Search(board, maxStep, TabuSize, vis):                  # It is a modified Tabu Search algorithm 
    TabuList = []                               # Initialize the tabu list, The first item is the location(row), the second item is the column number 
    step = 0                                    # For example, [1,2] is moving the second queen to the third column. 
    
    while(step <= maxStep):
    
        if(conflicts(board) == 0):
            return (step - 1,board)
    
        NewItem = Find_Option(board, TabuList)          # Find a new layout
        TabuList.append(NewItem)                        # Add that layout into the tabu list to avoid circuit search
    
        if(len(TabuList) >= TabuSize):                  # If it reaches the maximum size of tabu list, pop the first item (FIFO)                        
            TabuList.pop(0)
        
        oldconflict = conflicts(board)
        board[NewItem[0]] = NewItem[1]                  # Set the new layout
        if(vis == True):
            print(f"\nStep: {step}")
            newconflict = conflicts(board)
            if(newconflict < oldconflict):
                print("Find smaller conflict")
                print(f"Queens (left to right) are at rows: {board}") 
                print(f"Number of conflicts: {newconflict}")
            elif(newconflict > oldconflict):
                print("Doing Annealing")
                print(f"Queens (left to right) are at rows: {board}") 
                print(f"Number of conflicts: {newconflict}")
            else:
                print("Moving on the flat space")
                print(f"Queens (left to right) are at rows: {board}") 
                print(f"Number of conflicts: {newconflict}")
            show_board(board)
        
        step = step + 1
    
    print("Reach maximum repeat bound, but still cannot find global best")
    return (step - 1,board)
    

#####################################################################################################################################

def Insert_List(Geneticlist, board, max):               # Insert an item into the genetic list
    for j in range(len(Geneticlist)):
        if((Geneticlist[j] == board).all()):            # If exist
            return
        
    newconflict = conflicts(board)
    for k in range(len(Geneticlist)):                   # Insert based on the conflicts, make sure the list is always sorted
        if(newconflict <= conflicts(Geneticlist[k])):
            Geneticlist.insert(k, board)
            if(len(Geneticlist) > max):                # Make sure the list does not exceed the maximum size
                Geneticlist.pop()
            return
    Geneticlist.append(board)
    if(len(Geneticlist) > max):
        Geneticlist.pop()
    return 
    
        
def CrossOver(Parent1, Parent2):
    Child1 = copy.deepcopy(Parent1)
    Child2 = copy.deepcopy(Parent2)
    SinglePoint = random.randint(1,len(Child1)-2)           # Randomly choose the single crossover point
    for i in range(SinglePoint):
        temp = Child1[i]
        Child1[i] = Child2[i]                               # Make two children based on the rotation around the single point
        Child2[i] = temp
    return [Child1, Child2]
    
    
def Mutation(Children, p):
    for Child in Children:
        result = random.randint(1,100)
        if(result <= p*100):                                # Evoke muatation based on the possibility, if mutations happens, a random queen will move to a random column
            loc = random.randint(0,len(Child)-1)
            newnumber = random.randint(0,len(Child)-1)
            Child[loc] = newnumber

def GA_Search(boardSize, ListSize, maxStep, p, vis):
    Geneticlist = []
    while(len(Geneticlist) < ListSize):
        Insert_List(Geneticlist, random_board(boardSize), ListSize)     # Initialize the genetic list
    
    step = 0
    bestConflict = conflicts(Geneticlist[0])
    
    if(vis == True):
        print(f"\nStep: {step}")
        print("Find Initial configuration")
        print(f"Queens (left to right) are at rows: {Geneticlist[0]}") 
        print(f"Number of conflicts: {bestConflict}")
        show_board(Geneticlist[0])
    
    
    while(step < maxStep):
        Parent1 = copy.deepcopy(Geneticlist[0])             # Choose two parents from the top of the list. (better parents may bring better children)
        Parent2 = copy.deepcopy(Geneticlist[1])
        
        if(conflicts(Parent1) == 0):                        # If parents are global maxima
            if(vis == True):
                print(f"\nStep: {step}")
                print("Find 0 conflict configuration")
                print(f"Queens (left to right) are at rows: {Parent1}") 
                print(f"Number of conflicts: {conflicts(Parent1)}")
                show_board(Parent1)
            return (step,Parent1)
        
        if(conflicts(Parent2) == 0):
            if(vis == True):
                print(f"\nStep: {step}")
                print("Find 0 conflict configuration")
                print(f"Queens (left to right) are at rows: {Parent2}") 
                print(f"Number of conflicts: {conflicts(Parent2)}")
                show_board(Parent2)
            return (step,Parent2)
        
        
        Children = CrossOver(Parent1, Parent2)                  # Doing crossover to create two children
        
        if(conflicts(Children[0]) == 0):                        # If children are global maxima
            if(vis == True):
                print(f"\nStep: {step}")
                print("Find 0 conflict configuration")
                print(f"Queens (left to right) are at rows: {Children[0]}") 
                print(f"Number of conflicts: {conflicts(Children[0])}")
                show_board(Children[0])
            return (step,Children[0])
        elif(conflicts(Children[0]) < bestConflict and vis == True):
            print(f"\nStep: {step}")
            print("Find smaller conflict configuration")
            print(f"Queens (left to right) are at rows: {Children[0]}") 
            print(f"Number of conflicts: {conflicts(Children[0])}")
            show_board(Children[0])
            bestConflict = conflicts(Children[0])               # Update the smallest conflict it found
            
        if(conflicts(Children[1]) == 0):
            if(vis == True):
                print(f"\nStep: {step}")
                print("Find 0 conflict configuration")
                print(f"Queens (left to right) are at rows: {Children[1]}") 
                print(f"Number of conflicts: {conflicts(Children[1])}")
                show_board(Children[1])
            return (step, Children[1])
        elif(conflicts(Children[1]) < bestConflict and vis == True):
            print(f"\nStep: {step}")
            print("Find smaller conflict configuration")
            print(f"Queens (left to right) are at rows: {Children[1]}") 
            print(f"Number of conflicts: {conflicts(Children[1])}")
            show_board(Children[1])
            bestConflict = conflicts(Children[1])
        

        Mutation(Children, p)                            # Doing mutation based on possibility p       
        
        if(conflicts(Children[0]) == 0):                # Check if new children are global maxima
            if(vis == True):
                print(f"\nStep: {step}")
                print("Find 0 conflict configuration")
                print(f"Queens (left to right) are at rows: {Children[0]}") 
                print(f"Number of conflicts: {conflicts(Children[0])}")
                show_board(Children[0])
            return (step,Children[0])
        elif(conflicts(Children[0]) < bestConflict and vis == True):
            print(f"\nStep: {step}")
            print("Find smaller conflict configuration")
            print(f"Queens (left to right) are at rows: {Children[0]}") 
            print(f"Number of conflicts: {conflicts(Children[0])}")
            show_board(Children[0])
            bestConflict = conflicts(Children[0])
        
        if(conflicts(Children[1]) == 0):
            if(vis == True):
                print(f"\nStep: {step}")
                print("Find 0 conflict configuration")
                print(f"Queens (left to right) are at rows: {Children[1]}") 
                print(f"Number of conflicts: {conflicts(Children[1])}")
                show_board(Children[1])
            return ( step, Children[1])
        elif(conflicts(Children[1]) < bestConflict and vis == True):
            print(f"\nStep: {step}")
            print("Find smaller conflict configuration")
            print(f"Queens (left to right) are at rows: {Children[1]}") 
            print(f"Number of conflicts: {conflicts(Children[1])}")
            show_board(Children[1])
            bestConflict = conflicts(Children[1])
        
        for Child in Children:                          # Put those two children into the list
            Insert_List(Geneticlist,Child, ListSize)
        
        step = step + 1
    
    print("Reach maximum repeat bound, but still cannot find global best")
    return (step, Geneticlist[0])                            # If cannot find global maxima, use the cloest one 
    
    
#####################################################################################################################################


def Find_Child(board, T):
    Total = []                      
    oldconflict = conflicts(board)          
    for i in range(len(board)):                     # Find all the options
        for j in range(len(board)):
            if(j != board[i]):
                currentLayout = copy.deepcopy(board)
                currentLayout[i] = j
                Total.append(currentLayout)
    
    newlayout = random.choice(Total)
    if(conflicts(newlayout) <= oldconflict):       # If the new layout has fewer conflicts
        return newlayout
    else:
        p = e**( -(conflicts(newlayout) - oldconflict) / T)    # It is the Simulated Annealing formula
        select = random.randint(0,100000)         # Here is 100000 to make accuracy millionths decimal place 
        if(select < p*100000 and p >= (1 * e**-6)):   # At some of the possibility, accept bad moves
            return newlayout
        else:
            return board
    

def SA_Search(board, maxStep, maxRestart, vis):
    current = board
    currentConflict = conflicts(current)
    UnchangedTimes = 0
    step = 0
    RestartTime = 0
    
    if(vis is True):
        print(f"Step: {step}")
        print(f"Queens (left to right) are at rows: {current}") 
        print(f"Number of conflicts: {currentConflict}")
        show_board(current)
        
    while(currentConflict != 0):
        step = step + 1             
        newboard = Find_Child(current, 50 * (0.9 ** step)) # The Cooling Schedule formula
        newConflicts = conflicts(newboard) # Alpha is 0.9, T0 is 50 so that the initial probability is around 0.9    
        
        if(newConflicts < currentConflict):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Find smaller conflict")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = 0
        elif(newConflicts > currentConflict):
            if(vis is True):
                print(f"\nStep: {step}")
                print("Try to accept worse case")
                print(f"Queens (left to right) are at rows: {newboard}") 
                print(f"Number of conflicts: {newConflicts}")
                show_board(newboard)
            UnchangedTimes = UnchangedTimes + 1
        else:
            UnchangedTimes = UnchangedTimes + 1
        
        current = newboard
        currentConflict = newConflicts
        
        if(UnchangedTimes >= maxStep):
            RestartTime = RestartTime + 1
            if(RestartTime <= maxRestart):
                current = random_board(len(current))
                currentConflict = conflicts(current)
                UnchangedTimes = 0
                if(vis is True):
                    print(f"\nStep: {step}")
                    print("Reach maximum repeat bound, start doing restart. Restart Time: ", RestartTime)
                    print(f"Queens (left to right) are at rows: {current}") 
            else:
                if(vis is True):
                    print(f"\nStep: {step}")
                    print("Reach maximum restart bound, but still cannot find global best")
                    show_board(current)
                return (step,current)
    return (step,current)


#####################################################################################################################################


def Analysis():
    SAHC_Step = []
    SAHC_Time = []
    SAHCR_Step = []
    SAHCR_Time = []
    SHC_Step = []
    SHC_Time = []
    FCHC_Step = []
    FCHC_Time = []
    SA_Step = []
    SA_Time = []
    X_axis = [4,5,6,7,8]
    
    for i in range(5):
        SAHC_totalTime = 0
        SAHC_totalStep = 0
        SAHCR_totalStep = 0
        SAHCR_totalTime = 0
        SHC_totalStep = 0
        SHC_totalTime = 0
        FCHC_totalStep = 0
        FCHC_totalTime = 0
        SA_totalStep = 0
        SA_totalTime = 0
        
        for j in range(50):
            
            t0 = time.time()
            board = random_board(i+4)
            Result1 = SAHC_Search(board, 1000, False)
            t1 = time.time()
            SAHC_totalTime = SAHC_totalTime + ((t1-t0) * 1e3)
            SAHC_totalStep = SAHC_totalStep + Result1[0]
            
            t0 = time.time()
            board = random_board(i+4)
            Result2 = SAHC_Search_Restart(board, 50, 20, False)
            t1 = time.time()
            SAHCR_totalTime = SAHCR_totalTime + ((t1-t0) * 1e3)
            SAHCR_totalStep = SAHCR_totalStep + Result2[0]
            
            t0 = time.time()
            board = random_board(i+4)
            Result3 = SHC_Search(board, 50, 20, False)
            t1 = time.time()
            SHC_totalTime = SHC_totalTime + ((t1-t0) * 1e3)
            SHC_totalStep = SHC_totalStep + Result3[0]
            
            t0 = time.time()
            board = random_board(i+4)
            Result4 = FCHC_Search(board, 50, 20, False)
            t1 = time.time()
            FCHC_totalTime = FCHC_totalTime + ((t1-t0) * 1e3)
            FCHC_totalStep = FCHC_totalStep + Result4[0]
        
            t0 = time.time()
            board = random_board(i+4)
            Result5 = SA_Search(board, 50, 20, False)
            t1 = time.time()
            SA_totalTime = SA_totalTime + ((t1-t0) * 1e3)
            SA_totalStep = SA_totalStep + Result5[0]
     
        SAHC_totalTime = SAHC_totalTime / 50
        SAHC_totalStep = SAHC_totalStep / 50
        SAHCR_totalTime = SAHCR_totalTime / 50
        SAHCR_totalStep = SAHCR_totalStep / 50
        SHC_totalTime = SHC_totalTime / 50
        SHC_totalStep = SHC_totalStep / 50
        FCHC_totalTime = FCHC_totalTime / 50
        FCHC_totalStep = FCHC_totalStep / 50
        SA_totalTime = SA_totalTime / 50
        SA_totalStep = SA_totalStep / 50
        
        SAHC_Step.append(SAHC_totalStep)
        SAHC_Time.append(SAHC_totalTime)
        SAHCR_Step.append(SAHCR_totalStep)
        SAHCR_Time.append(SAHCR_totalTime)
        SHC_Step.append(SHC_totalStep)
        SHC_Time.append(SHC_totalTime)
        FCHC_Step.append(FCHC_totalStep)
        FCHC_Time.append(FCHC_totalTime)
        SA_Step.append(SA_totalStep)
        SA_Time.append(SA_totalTime)
        
        
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(X_axis, SAHC_Step, 'r-' , label = 'SAHC_Step')
    ax.plot(X_axis, SAHCR_Step, 'b-' , label = 'SAHCR_Step')
    ax.plot(X_axis, SHC_Step, 'g-' , label = 'SHC_Step')
    ax.plot(X_axis, FCHC_Step, 'y-' , label = 'FCHC_Step')
    ax.plot(X_axis, SA_Step, 'c-' , label = 'SA_Step')
    leg = ax.legend()
    plt.title("Average steps for each algorithm with different size")
    plt.xlabel("Board Length")
    plt.ylabel("Average Steps")
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1,1,1)
    ax1.plot(X_axis, SAHC_Time, 'r-' , label = 'SAHC_Time')
    ax1.plot(X_axis, SAHCR_Time, 'b-' , label = 'SAHCR_Time')
    ax1.plot(X_axis, SHC_Time, 'g-' , label = 'SHC_Time')
    ax1.plot(X_axis, FCHC_Time, 'y-' , label = 'FCHC_Time')
    ax1.plot(X_axis, SA_Time, 'c-' , label = 'SA_Time')
    leg = ax1.legend()
    plt.title("Average time for each algorithm with different size")
    plt.xlabel("Board Length")
    plt.ylabel("Average Time (milliseconds)")
    
    plt.show()


Analysis()