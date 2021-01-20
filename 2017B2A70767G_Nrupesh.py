#!/home/flamealchemist/Prog_Assignment_1/ai/bin/env/ python3
import time
import copy
from heapq import * # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************


#                 YOUR CODE SHOULD GO HERE.

#                 WRITE YOUR CODE IN AN EASY TO READ MANNER.

#                 YOU MAY USE SEVERAL CLASSES AND FUNCTIONS 


#                 MODIFY THE BODY OF THE FUNCTION FindMinimumPath()



traversal = [[1,0,"Down"],[0,1,"Right"],[-1,0,"Up"],[0,-1,"Left"]]



class Puzzle:
    def __init__(self, arr, parent, cost, row, col,move):
        self.arr = arr                               #storing the grid (current state)
        self.parent = parent                         #store the parent to this configuration
        self.cost = cost                             #store the path cost
        self.hcost = self.manhattanDistance()        #store the heurestic value
        self.zeror = row                             #store the row index of zero    
        self.zeroc = col                             #store the col index of zero 
        self.move = move                             #store the move which took it to this configuration

    def isGoal(self):
        return self.hcost==0                         #check if the configuration is the goal state
    
    def manhattanHelper(self, num):                  #return the index of value in goal state
        row = num//4
        col = num%4
        return row,col

    def linearConflict(self):                     #implementation of linearconflict
        linearconflict=0
        maxval = 0
        for i in range(4):
            maxval = 0
            for j in range(4):
                num=self.arr[i][j]
                if num!=0 and num//4 == i:
                    if num>maxval:
                        maxval=num
                    else: 
                        linearconflict +=2
        # maxval=0
        for j in range(4):
            maxval = 0
            for i in range(4):
                num=self.arr[i][j]
                if num!=0 and num%4 == j:
                    if num>maxval:
                        maxval=num
                    else:   
                        linearconflict +=2
        return linearconflict

    def manhattanDistance(self):                        #implementation of manhattan distance 
        ans = 0
        for i in range(4):
            for j in range(4):
                if(self.arr[i][j]==0):
                    continue
                (r,c) = self.manhattanHelper(self.arr[i][j])
                ans+=abs(r-i)+abs(c-j)
        return ans+self.linearConflict()

    def swapHelper(self, trav):                                 #helper function to help swap the array of current config to neighbouring configs
        if trav[0]+self.zeror<0 or trav[0]+self.zeror>3 or trav[1]+self.zeroc<0 or trav[1]+self.zeroc>3:
            return False,[],[],""
        arr2 = copy.deepcopy(self.arr)
        arr2[self.zeror][self.zeroc],arr2[self.zeror+trav[0]][self.zeroc+trav[1]]=arr2[self.zeror+trav[0]][self.zeroc+trav[1]],arr2[self.zeror][self.zeroc]
        return True,arr2,[self.zeror+trav[0],self.zeroc+trav[1]],trav[2]

    def swapping(self):                                         #function to help create objects which are neighbours
        ans = list()
        for i in range(4):
            possible,arr1,zc,move = self.swapHelper(traversal[i])
            if possible==True:
                neighbour = Puzzle(arr1,self,self.cost+1,zc[0],zc[1],move)
                ans.append(neighbour)
        return ans

    def __eq__(self, other):                                    #function to help check if objects are equal (needed since i passed objects to pq)
        return self.arr == other.arr

    def __lt__(self, other):                                    #function to help compare objects, less than in this case because of priority queue (needed since i passed objects to pq)
        return self.cost < other.cost

    def __hash__(self):                                         #making the object hashable since am storing the visited set as a dictionary. used the grid to hash since its unique for each object
        return hash(tuple([tuple(i) for i in self.arr]))

def dataFormatting(state):                                      #function to format the data to list of ints and also store the coordinates of zero
    for i in range(len(state)):
        for j in range(len(state[i])):
            if ord(state[i][j])<60:
                state[i][j] = ord(state[i][j])-48
                if(state[i][j]==0):
                    row = i
                    col = j
            else:
                state[i][j] = ord(state[i][j])-55
    return state,row,col

def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    
    ### Your Code for FindMinimumPath function
    ### Write your program in an easy to read manner. You may use several classes and functions.
    ### Your function names should indicate what they are doing
    
    
    ### Your Code ends here. minPath is a list that contains actions.
    ### For example, minPath = ['Up','Right','Down','Down','Left']
    initialState,row,col = dataFormatting(initialState)                         
    Node = Puzzle(initialState,None,0,row,col,"end")                        #create the first node

    pq=[]
    vis = {}
    vis[Node]=0                                                             #mark node as visited
    heappush(pq,(Node.hcost+Node.cost,Node.hcost,Node))                     #push it to the frontier queue
    top = None

    while len(pq):
        top = heappop(pq)[2]                                                #pop the node 
        if top.isGoal()==True:                                              #check if the node is visited 
            break
        neighbours = top.swapping()                                         #generate the neighbours which are possible to generate
        for n in neighbours:
            if n not in vis or n.cost+n.hcost<vis[n]:                       #check if neighbour has not been visited or if its been visited with a higher cost before 
                nodesGenerated+=1                                           #increment the nodes generated 
                vis[n]=n.cost+n.hcost                                       #mark the node as visited 
                heappush(pq,(n.cost+n.hcost,n.hcost,n))                     #push the node to the frontier queue

    while(top.move!="end"):                                                 #backtrack to trace the path from final state to initial state 
        minPath.append(top.move)
        top = top.parent

    minPath.reverse()

    return minPath, nodesGenerated



#**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state4.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
                                                        #               evaluators test your program. You will lose 2 marks.
        initialState = [[x for x in line.split()] for i,line in enumerate(file) if i<4]
    return initialState

def ShowState(state,heading=''):
    print(heading)
    for row in state:
        print(*row, sep = " ")

def main():
    initialState = ReadInitialState()
    ShowState(initialState,'Initial state:')
    goalState = [['0','1','2','3'],['4','5','6','7'],['8','9','A','B'],['C','D','E','F']]
    ShowState(goalState,'Goal state:')
    
    start = time.time()
    minimumPath, nodesGenerated = FindMinimumPath(initialState,goalState)
    timeTaken = time.time() - start
    
    if len(minimumPath)==0:
        minimumPath = ['Up','Right','Down','Down','Left']
        print('Example output:')
    else:
        print('Output:')

    print('   Minimum path cost : {0}'.format(len(minimumPath)))
    print('   Actions in minimum path : {0}'.format(minimumPath))
    print('   Nodes generated : {0}'.format(nodesGenerated))
    print('   Time taken : {0} s'.format(round(timeTaken,4)))

if __name__=='__main__':
    main()
