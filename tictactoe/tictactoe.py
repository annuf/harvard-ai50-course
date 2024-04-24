"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    xs,os=0,0
    for i in range(3):
        xs+=board[i].count(X)
        os+=board[i].count(O)
    if xs==1+os:
        return O
    elif xs == os:
        return X
    else:
        raise Exception("something doesn't seem right")
    """
    Returns player who has the next turn on a board.  #X gets the first move
    """
    #raise NotImplementedError

#print(player([[X, EMPTY, O],[X, O, O],[X,X,O]]))



def actions(board):
    acts=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                acts.add((i,j))
    return(acts)
    #raise NotImplementedError

#print(actions([[X, EMPTY, O],[X, EMPTY, O],[X,X,O]]))

def result(board, action):
    i,j=action[0],action[1]
    
    if i<0 or i>2 or j<0 or j>2:
        raise Exception("action not allowed")
    
    if board[i][j]!=EMPTY:
        raise Exception("not an empty field")
    
    turn = player(board)
    newboard = copy.deepcopy(board)
    newboard[i][j]=turn

    return newboard
    #raise NotImplementedError

#print(result([[X, EMPTY, O],[X, O, O],[X,X,O]], (0,1)))

def winner(board):  
    for i in range(3):
        hor_xs=board[i].count(X)
        hor_os=board[i].count(O)
        if hor_xs==3:
            return X
        elif hor_os==3:
            return O
        ver = [board[k][i] for k in range(3)]
        ver_xs= ver.count(X)
        ver_os = ver.count(O)
        if ver_xs == 3:
            return X
        elif ver_os == 3:
            return O
    diag1 = [board[i][i] for i in range(3)]
    if diag1.count(X)==3:
        return X
    elif diag1.count(O)==3:
        return O
    diag2 = [board[i][2-i] for i in range(3)]
    if diag2.count(X)==3:
        return X
    elif diag2.count(O)==3:
        return O
    return None
    """
    Returns the winner of the game, if there is one.
    """
    #raise NotImplementedError
    
#print(winner([[X, EMPTY, O],[O, O, X],[O,X,X]]))
    



def terminal(board):
    
    if winner(board) in [X,O]:
        return True
    flat_board = sum(board,[])
    if flat_board.count(EMPTY)==0:
        return True
    return False
    """
    Returns True if game is over, False otherwise.
    """
    #raise NotImplementedError
#print(terminal([[X, X, O],[O, X, X],[X,X,O]]))
    


def utility(board):
    won = winner(board)
    if won==X:
        return 1
    elif won==O:
        return -1
    else: 
        return 0
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #raise NotImplementedError

#print(utility([[X, O, O],[O, X, X],[X,X,O]]))


def minValue(board):
    if terminal(board):
        return utility(board)
    acts = actions(board)
    v = float('inf')
    for action in acts:
        v = min(v, maxValue(result(board, action)))
    return v

def maxValue(board):
    if terminal(board):
        return utility(board)
    acts = actions(board)
    v = float('-inf')
    for action in acts:
        v = max(v, minValue(result(board, action)))
    return v

def minimax(board):
    if terminal(board):
        return None
    turn = player(board)
    acts = actions(board)
    bestAct = None
    save = list()
    for action in acts:
        if turn == X:
            save.append((action, minValue(result(board,action))))
        if turn == O:
            save.append((action, maxValue(result(board,action))))
    if turn == X:
        maxi = max(save, key=lambda x:x[1])
        return maxi[0]
    if turn == O:
        mini = min(save, key=lambda x:x[1])
        return mini[0]


    """
    Returns the optimal action for the current player on the board.
    """
    #raise NotImplementedError

#print(minimax([[EMPTY, O, X],[O, X, X],[EMPTY,X,O]]))
