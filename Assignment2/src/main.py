import random
import numpy as np 
import copy

actions_simple_randomized = ["north", "east", "west", "south", "suck"]          # Types of action for task 1
actions_simple_reflex = ["north", "east", "west", "south", "suck"]             # Types of action for task 2

def checkClear(Matrix):                  # Check is there any dirty point left
    for i in Matrix:
        for j in i:
            if(j != False):
                return False
    return True

                
def Analysis_Bumper(row, column, lengthoftable):       # Return the bumpers that indicate walls
    newbound = {}
    if(row == 0):
        newbound["north"] = "True"
    if(row == lengthoftable - 1):
        newbound["south"] = "True"
    if(column == 0):
        newbound["west"] = "True"
    if(column == lengthoftable - 1):
        newbound["east"] = "True"
    return newbound


def simple_randomized_agent(lengthoftable, maxstep,p, printed):
    Matrix = np.random.choice(a=[False,True], size=(lengthoftable,lengthoftable), p = [p, 1-p])  # Create the environment
    CurrentRow = random.randint(0,lengthoftable - 1)           # Randomly set start point
    CurrentColumn = random.randint(0,lengthoftable - 1)
    
    if(printed == True) : print("Room:\n", Matrix) 
    
    for i in range(maxstep):
        Ndirty = np.sum(Matrix)             # The number of dirty points 
        newBound = Analysis_Bumper(CurrentRow, CurrentColumn, lengthoftable)    # Analyze bounds
        
        if(printed == True) :
            print("===========================")
            print("Step: ", i)
            print("Dirty parts left: ", Ndirty)
            print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
            print("Bumper: ", newBound)
            print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
            
        Newaction = random.choice(actions_simple_randomized)             # The simple_randomized_agent will choose the action randomly
        
        if(printed == True) : print("Action: ", Newaction)          # Processing Actions 
        if(Newaction == "north" and CurrentRow != 0) : CurrentRow = CurrentRow - 1 
        if(Newaction == "south" and CurrentRow != lengthoftable - 1) : CurrentRow = CurrentRow + 1
        if(Newaction == "east" and CurrentColumn != lengthoftable - 1) : CurrentColumn = CurrentColumn + 1
        if(Newaction == "west" and CurrentColumn != 0) : CurrentColumn = CurrentColumn - 1
        if(Newaction == "suck") :  Matrix[CurrentRow, CurrentColumn] = False
        
        if(checkClear(Matrix)) :
            if(printed == True):
                print("All the dirty points have been cleared")
            return i
        if(i == maxstep - 1) :
            if(printed == True):
                print("Reach the max number of steps")
            return i


def simple_reflex_agent(lengthoftable, maxstep,p,printed):
    Matrix = np.random.choice(a=[False,True], size=(lengthoftable,lengthoftable), p = [p, 1-p])
    CurrentRow = random.randint(0,lengthoftable - 1)
    CurrentColumn = random.randint(0,lengthoftable - 1)
    
    if(printed == True) : print("Room:\n", Matrix)
    
    for i in range(maxstep):
        Ndirty = np.sum(Matrix)
        newBound = Analysis_Bumper(CurrentRow, CurrentColumn, lengthoftable)
        
        if(printed == True) :
            print("===========================")
            print("Step: ", i)
            print("Dirty parts left: ", Ndirty)
            print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
            print("Bumper: ", newBound)
            print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
            
        NewChoice = copy.deepcopy(actions_simple_reflex)        # Use Deep Copy to create a list of action choices so that I can do remove
        
        for j in newBound:
            NewChoice.remove(j)                                 # Remove the impossible actions
            
        if(Matrix[CurrentRow, CurrentColumn] == True):      # If the current place is dirty, the only action will be suck
            Matrix[CurrentRow, CurrentColumn] = False
            if(printed == True):
                print("Action: suck")
        else:
            Newaction = random.choice(NewChoice)
            if(printed == True) :
                print("Action: ", Newaction)
            if(Newaction == "north") : CurrentRow = CurrentRow - 1 
            if(Newaction == "south") : CurrentRow = CurrentRow + 1
            if(Newaction == "east") : CurrentColumn = CurrentColumn + 1
            if(Newaction == "west") : CurrentColumn = CurrentColumn - 1
        
        if(checkClear(Matrix)) :
            if(printed == True):
                print("All the dirty points have been cleared")
            return i
        if(i == maxstep - 1) :
            if(printed == True):
                print("Reach the max number of steps")
            return i      
        

def model_reflex_agent(lengthoftable,p,printed):
    step = 0
    Matrix = np.random.choice(a=[False,True], size=(lengthoftable,lengthoftable), p = [p, 1-p])
    CurrentRow = random.randint(0,lengthoftable - 1)
    CurrentColumn = random.randint(0,lengthoftable - 1)
    print(np.sum(Matrix))
    if(printed == True) : print("Room:\n", Matrix, "\nStarts at: [" ,CurrentRow, "," ,CurrentColumn , "]" )
    
    while(CurrentRow != 0):             # Since the start location is random, the agent will firstly go to the top-left
        CurrentRow = CurrentRow - 1
        step = step + 1                 
    while(CurrentColumn != 0):
        CurrentColumn = CurrentColumn - 1
        step = step + 1
    print("Steps to return to the top-left point", step)
    
    
    for i in range(lengthoftable):                  # The idea is cleaning the room with a s shape path
        if(CurrentColumn == 0):
            while(CurrentColumn < lengthoftable - 1):
                if(Matrix[i][CurrentColumn] == True):           # If the current position is dirty
                    step = step + 1
                    if(printed == True):
                        print("===========================")
                        print("Step: ", step)
                        print("Dirty parts left: ", np.sum(Matrix))
                        print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
                        print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
                        print("Action: suck")                     
                    Matrix[i][CurrentColumn] = False
                else:
                    step = step + 1                     # If it's clean, go to the east
                    if(printed == True):
                        print("===========================")
                        print("Step: ", step)
                        print("Dirty parts left: ", np.sum(Matrix))
                        print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
                        print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
                        print("Action: east")  
                    CurrentColumn = CurrentColumn + 1
            if(Matrix[i][CurrentColumn] == True):                  # Clean the last one in the column
                step = step + 1
                if(printed == True):
                    print("===========================")
                    print("Step: ", step)
                    print("Dirty parts left: ", np.sum(Matrix))
                    print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
                    print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
                    print("Action: suck")        
                Matrix[i][CurrentColumn] = False
        else:                                           # If the column is started from the east to west
            while(CurrentColumn > 0):
                if(Matrix[i][CurrentColumn] == True):
                    step = step + 1
                    if(printed == True):
                        print("===========================")
                        print("Step: ", step)
                        print("Dirty parts left: ", np.sum(Matrix))
                        print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
                        print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
                        print("Action: suck")        
                    Matrix[i][CurrentColumn] = False
                else:
                    step = step + 1
                    if(printed == True):
                        print("===========================")
                        print("Step: ", step)
                        print("Dirty parts left: ", np.sum(Matrix))
                        print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
                        print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
                        print("Action: west") 
                    CurrentColumn = CurrentColumn - 1
            if(Matrix[i][CurrentColumn] == True):
                step = step + 1
                if(printed == True):
                    print("===========================")
                    print("Step: ", step)
                    print("Dirty parts left: ", np.sum(Matrix))
                    print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
                    print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
                    print("Action: suck")        
                Matrix[i][CurrentColumn] = False
        if(printed == True and CurrentRow != lengthoftable - 1):            #If one column is finished, go down the the next one
            print("===========================")
            print("Step: ", step)
            print("Dirty parts left: ", np.sum(Matrix))
            print("Current Position: [", CurrentRow, "," , CurrentColumn , "]")
            print("Dirty: ", Matrix[CurrentRow, CurrentColumn])
            print("Action: south")  
        CurrentRow = CurrentRow + 1
        step = step + 1
    return step - 1                                     # The final step will leads to out of bound, so we don't need that step
               

def Check_remaining(Matrix):                                    # Count how many dirty points left
    total = 0
    for i in Matrix:
        for j in i:
            if(j == "True"):
                total = total + 1
    return total


def Analyze_Neighbour(currentpair, Visited, lengthoftable, printed):
    choice = []
    if(currentpair[0] != 0):                                            # Check if the north is not a wall or an obstacle
        if(Visited[currentpair[0] - 1][currentpair[1]] != 1):
            choice.append((currentpair[0] - 1, currentpair[1]))
            
    if(currentpair[1] != 0):                                            # Check if the south is not a wall or an obstacle
        if(Visited[currentpair[0]][currentpair[1] - 1] != 1):
            choice.append((currentpair[0], currentpair[1] -1))
            
    if(currentpair[0] != lengthoftable - 1):                            # Check if the west is not a wall or an obstacle
        if(Visited[currentpair[0] + 1][currentpair[1]] != 1):
           choice.append((currentpair[0] + 1, currentpair[1]))  
           
    if(currentpair[1] != lengthoftable - 1):                           # Check if the east is not a wall or an obstacle
        if(Visited[currentpair[0]][currentpair[1] + 1] != 1):
            choice.append((currentpair[0], currentpair[1] + 1))
    if(len(choice) == 0):
        if(printed == True) : print("No Available place to go")
        return (-1,-1)                                                  # If it has no new place to go, return -1,-1
    else:
        if(printed == True) : print("Can go: ", choice, "\nAction: ", choice[0])
        return choice[0]                                                # Else go to the first option


def obstacle_agent(lengthoftable,p,printed):
    step = 0
    Matrix = np.random.choice(a=["False","True"], size=(lengthoftable,lengthoftable), p = [p, 1-p])
    Matrix[1][2] = "None"                                       # Manually set the obstacles
    Matrix[2][3] = "None"
    
    Visited = [[0 for x in range(5)] for y in range(5)]        # Create a table to store visited location
    Visited[1][2] = 1                                          # Two obstacles is set to be visited 
    Visited[2][3] = 1
    path = []                                                   # Create a vector to store the pass Like DFS 
    path.append((0,0))                                          # We always set the top-left as our start position
    Visited[0][0] = 1
    if(printed == True) : print("Room:\n", Matrix)
    while(len(path) != 0):                                      # While it's not back to the top left
        
        oldpair = path[len(path) - 1]                           # Old pair is the current location
        if(printed == True) : print("===========================\nstep: ", step)
        if(printed == True) : print("Current Position: ", oldpair)
        
        if(Matrix[oldpair[0]][oldpair[1]] == "True"):           # If the current location is dirty, clean it
            Matrix[oldpair[0]][oldpair[1]] = "False"
            step = step + 1
            if(printed == True) : print("Action: suck")
        else:                                                   
            newpair = Analyze_Neighbour(oldpair, Visited, lengthoftable, printed)
        
            if(newpair != (-1,-1)):                             # If there is an unvisited point nearby
                Visited[newpair[0]][newpair[1]] = 1
                path.append((newpair[0],newpair[1]))
                step = step + 1
            else:                                               # If all the place around are visited, go back to the last point
                path.pop()
                step = step + 1
        if(printed == True) : print("Dirty parts left: ", Check_remaining(Matrix)) 
    return step


print( "step is ", model_reflex_agent(5,0.8,False))
    