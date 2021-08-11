import game
DEPTH=2
def go(gm):
    if game.isHumTurn(gm): # human is min, if its human's turn, start the tree with min
        obj= abmin(gm, DEPTH, game.LOSS-1, game.VICTORY+1)[1]
        return obj
    else: # computer is max, if its computer's turn, start the tree with max
        obj= abmax(gm, DEPTH, game.LOSS-1, game.VICTORY+1)[1]
        return obj

'''
Minmax algorithm:
    Creates a tree of next possible moves with a given depth.
    Each level of the tree is called "min" or "max" which represents
    the two players.
    Each node of the tree has heuristic value of its move. 
    If a node in the tree is in a "min" level, then it will choose
    from its children the one with the minimum heuristic value.
    If the node is in a "max" level, then it will choose
    from its children the one with the maximum heuristic value.
    The value of the tree's leaves, is calculated by a heuristic function.
    At the end, the most optimal move is selected (according to the depth)
    for the player that started the tree (min or max).

Alpha beta pruning algorithm:
    This algorithm is an extension to the Minmax algorithm.
    The algorithm is trying to shorten the Minmax algorithm by
    "pruning" the branches which are obviously won't give any
    better result.
    Each node of the Minmax tree has alpha and betha values.
    This values representing the minimum score for the maximum player
    and the maximum score for the minimum player.
    At the start, this values contains the "wrost" value
    (infinity and negative infinity).
'''

#s = the state (max's turn)
#d = max. depth of search
#a,b = alpha and beta
#returns [v, ns]: v = state s's value. ns = the state after recomended move.
#        if s is a terminal state ns=0.
def abmax(gm, d, a, b):
    # if the depth is 0 or is game over, got to the end of the tree's branch
    if d==0 or game.isFinished(gm):
        return [game.value(gm),gm] # calculate the heuristic value

    v=float("-inf")
    ns=game.getNext(gm) # list of next-state boards
    bestMove=0

    # for each state, calculate the min of the next depth and take the best move (with alpha beta pruning).
    for st in ns:
        tmp=abmin(st,d-1,a,b)
        if tmp[0]>v:
            v=tmp[0]
            bestMove=st
        if v>=b: # pruning
            return [v,st]
        if v>a: # set the minimum assured value for max
            a=v
    return [v,bestMove]

#s = the state (min's turn)
#d = max. depth of search
#a,b = alpha and beta
#returns [v, ns]: v = state s's value. ns = the state after recomended move.
#        if s is a terminal state ns=0.
def abmin(gm, d, a, b):
    # if the depth is 0 or is game over, got to the end of the tree's branch
    if d==0 or game.isFinished(gm):
        return [game.value(gm),0] # calculate the heuristic value

    v=float("inf")
    ns=game.getNext(gm) # list of next-state boards
    bestMove=0

    for st in ns:
        tmp = abmax(st, d - 1, a, b)
        if tmp[0]<v:
            v = tmp[0]
            bestMove = st
        if v <= a: # pruning
            return [v,st]
        if v < b: # set the maximum assured value for min
            b = v
    return [v, bestMove]
