from enum import Enum
import copy
from pgm_reader import pgmToBoard

# --------------------------------
# CHANGE ME!
#     |
#     V

# use '16x16.pgm', '64x64.pgm'...'512x512.pgm'
PGM_FILE = '16x16.txt'
ITER = 1
OUTPUT_ALIVE = True

# --------------------------------

# for testing
BOARD_SIZE = 16
BOARD = [
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
"""
    UTIL
"""
class Dir(Enum):
    N_W = (-1,   1)
    N   = (0,   1)
    N_E = (1,   1)
    E   = (1,   0)
    S_E = (1,  -1)
    S   = (0,  -1)
    S_W = (-1,  -1)
    W   = (-1,  0)

def getDirX(dir: Dir) -> int:
    return dir.value[0]
    
def getDirY(dir: Dir) -> int:
    return dir.value[1]

def addZ(x: int, y: int, z: int) -> int:
    return (x + y) % z

def testAddZ():
    assert addZ(1, 1, 3) == 2
    assert addZ(1, 2, 3) == 0
    assert addZ(0, 2, 3) == 2
    assert addZ(-1, 2, 3) == 1
    assert addZ(-1, 0, 3) == 2
    assert addZ(-1, -2, 3) == 0
    assert addZ(1, BOARD_SIZE, BOARD_SIZE) == 1
  
  
"""
    BOARD
"""
def genBoard(size: int) -> [[int]]:
    board = []
    for y in range(0, size):
        row = []
        for x in range(0, size):
            row.append(0)
        board.append(row)
    return board

def placeInBoard(x: int, y: int, toPlace: [[int]], board: [[int]]) -> [[int]]:
    boardTemp = copy.deepcopy(board)
    tempX = 0
    tempY = 0
    for row in toPlace:
        for v in row:
            boardTemp[y + tempY][x + tempX] = v
            tempX += 1
        tempY += 1
        tempX = 0
    return boardTemp

"""
    GAME
"""
def neighbourVal(x: int, y: int, board: [[int]], dir: Dir) -> int:
    xx = addZ(x, getDirX(dir), BOARD_SIZE)
    yy = addZ(y, getDirY(dir), BOARD_SIZE)
    return board[yy][xx]

def neighbourVals(x: int, y: int, board: [[int]]) -> int:
    tot = 0
    for d in Dir:
        tot += neighbourVal(x, y, board, d)
    return tot

def isCellDead(x: int, y: int, board: [[int]]) -> bool:
    return board[y][x] == 0
    
def performCell(x: int, y: int, board: [[int]]) -> int:
    n = neighbourVals(x, y, board)
    ret = 0
    if isCellDead(x, y, board):
        return 1 if n == 3 else 0
    else:
        return 1 if (n == 2 or n == 3) else 0
    return ret
    
def performRound(board: [[int]]) -> [[int]]:
    boardNew = copy.deepcopy(board)
    for y in range(0, BOARD_SIZE):
        for x in range(0, BOARD_SIZE):
            boardNew[y][x] = performCell(x, y, board)
    return boardNew

def performRounds(board: [[int]], no_rounds: int):
    boardTemp = board.copy()
    for i in range(0, no_rounds):
        boardTemp = performRound(boardTemp)
        if OUTPUT_ALIVE:
            print('Round {}: {} alive'.format(i + 1, sumAlive(boardTemp)))
    return boardTemp

def sumAlive(board: [[int]]):
    alive = 0
    for y in range(0, BOARD_SIZE):
        for x in range(0, BOARD_SIZE):
            if board[y][x] == 1:
                alive += 1
    return alive
"""
    OUTPUT
"""
def printBoard(board: [[int]]):
    for y in range(0, BOARD_SIZE):
        for x in range(0, BOARD_SIZE):
            print("{},".format(board[y][x]), end='')
        print("\n")

        
testAddZ()

tp = [
    [0,1,0],
    [0,0,1],
    [1,1,1]
]

## NORMAL
#endBoard = placeInBoard(3, 5, tp, genBoard(16))
#endBoard = performRounds(BOARD, ITER)

#endBoard = placeInBoard(3, 5, tp, genBoard(BOARD_SIZE))
pgm = pgmToBoard(PGM_FILE)
BOARD_SIZE = pgm[0]
endBoard = pgm[1]
endBoard = performRounds(endBoard, ITER)

f = open('output.txt', 'w')
for y in range(0, BOARD_SIZE):
        for x in range(0, BOARD_SIZE):
            f.write("{},".format(endBoard[y][x]))
        f.write("\n")
f.close()

print('Output results in output.txt')