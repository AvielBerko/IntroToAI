import alphaBetaPruning
import game
# import game1 as game

SMART = 1
SIMPLE = 0
num = 0

def play(first):
    board = game.game()
    game.create(board)
    board.playTurn = game.COMPUTER if first == SMART else game.HUMAN
    comp_count = 0
    for _ in range(0,100):#This loops takes about 15 seconds on my computer 
        while not game.isFinished(board):
            if game.isHumTurn(board):
                game.inputRandom(board)
            else:
                board=alphaBetaPruning.go(board)
        if game.value(board)==game.VICTORY: #the computer (or smart agent) won
            comp_count+=1
        game.create(board)
    result = max(comp_count-90,0)*2

    global num
    print("SMART" if first == SMART else "SIMPLE", num)
    num += 1

    return result

def avg(times):
    global num
    num = 0

    from multiprocessing.pool import ThreadPool
    sum_result_smart = 0
    sum_result_simple = 0
    with ThreadPool(8) as pool:
        data = []
        for i in range(times):
            data.append((SMART, i))
        for i in range(times):
            data.append((SIMPLE, i))
        results = pool.map(play, data)

        for i in range(times):
            sum_result_smart += results[i]
        for i in range(times):
            sum_result_simple += results[20 + i]
        avg_result_smart = sum_result_smart / times
        avg_result_simple = sum_result_simple / times
        print("avg result smart started", avg_result_smart)
        print("avg result simple started", avg_result_simple)

# if __name__ == "__main__":
#     avg(40)
#     exit()

board=game.game()
game.create(board)
print("Initial Game")
game.printState(board)
game.decideWhoIsFirst(board)
comp_count = 0
i = 0
for i in range(0,100):#This loops takes about 15 seconds on my computer 
#for i in range(0,50): 
    while not game.isFinished(board):
        if game.isHumTurn(board):
            game.inputRandom(board)
            #game.inputMove(board)
        else:
            board=alphaBetaPruning.go(board)
        game.printState(board)
        # input("Continue? ")
    if game.value(board)==10**20: #the computer (or smart agent) won
        comp_count+=1
    print("Start another game")
    game.create(board)
print("The agent beat you:", comp_count, " out of ", i+1)
print("Your grade in this section would be ", max(comp_count-90,0)*2, " out of 20 ")
#print("Your grade in this section would be ", max(comp_count-40,0)*4, " out of 20 ")

