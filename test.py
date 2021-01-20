import time
import numpy
from copy import deepcopy
from heapq import * # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************


#                 YOUR CODE SHOULD GO HERE.

#                 WRITE YOUR CODE IN AN EASY TO READ MANNER.

#                 YOU MAY USE SEVERAL CLASSES AND FUNCTIONS


#                 MODIFY THE BODY OF THE FUNCTION FindMinimumPath()
def turnIntoTuple(state):
    return tuple([j for i in state for j in i])

def heuristic(state):
    linearConflict = 0
    cost=0
    for i in range(4):
        for j in range(4):
            num = int(state[i][j],16)
            row,col = divmod(num,4)
            if num != 0:
                cost+=abs(i - row) + abs(j - col)
                if (i, j) == (row, col):
                    continue
                elif i == row:
                    for tcol in range(j):
                        thisrow, thiscol = divmod(int(state[i][tcol],16),4)
                        if thisrow==i:
                            if  col<=thiscol:
                                linearConflict+=1

                elif j == col:
                    for trow in range(i):
                        thisrow, thiscol = divmod(int(state[trow][j],16),4)
                        if thiscol==j:
                            if  row<=thisrow:
                                linearConflict+=1

    return (2*linearConflict) + cost

def isAnswer(state, goalState):
    return state==goalState

def getMoves(state):
    possibleMoves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
    moves = []
    row = -1
    col = -1
    flag=0
    for i in range(4):
        for j in range(4):
            if state[i][j] == '0':
                row = i
                col = j
                for i, j, play in possibleMoves:
                    if 0 <= (row + i) < 4 and 0 <= (col + j) < 4:
# other

                        temp = deepcopy(state)  # creates a copy of the matrix so we dont change it in place
                        temp[row][col], temp[row+i][col+j] = temp[row+i][col+j], temp[row][col]
                        moves.append((temp, play))
                return moves

def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution

    pq = []
    visited = {}
    out = set()

    heappush(pq, ((0,heuristic(initialState), initialState, 0,"")))

    while len(pq)>0:
        cost, heurcost, state, level, ans = heappop(pq)

        if isAnswer(state,goalState):
            answer=ans
            break

        moves = getMoves(state)

        visited[turnIntoTuple(state)]=cost
        out.add(turnIntoTuple(state))
        for node, play in moves:
            nodeTuple = turnIntoTuple(node)
            heuristicCost=heuristic(node)
            if nodeTuple not in visited or (nodeTuple not in out and (heuristicCost+level+1 < visited[nodeTuple])):
                nodesGenerated+=1
                visited[nodeTuple]=heuristicCost+level+1
                heappush(pq, ((heuristicCost + level +1, heuristicCost, node, level +1,  ans +" "+play)))

    minPath=answer.split()
    return minPath, nodesGenerated

#**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state3.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
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