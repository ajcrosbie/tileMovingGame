import queue
import time

import pyautogui

"""
have board =[1,2,3,4..., 0] as final state, 0 reprisents the free peice
board takes form of a 4*4 with ints from 1 to 15 as well as 0
move order is the turn the move is made on, so turn 1 has order 1
pseudocode---
take board input
generate states availible from that input, add to priority queue with key being some heuristic + move order
begin loop
dequeue item, generate states from that,
check if any states are the final state
else add all to priority queue and repeate

"""


def find0(board):
    for i in range(len(board)):
        if board[i] == 0:
            return i


def generateStates(board):
    temp = board[::]
    states = []
    Zloc = find0(board)
    if Zloc > 3:
        t1 = temp[Zloc - 4]
        temp[Zloc - 4] = temp[Zloc]
        temp[Zloc] = t1
        states.append((temp, "down"))
    temp = board[::]
    if Zloc < 12:
        t1 = temp[Zloc + 4]
        temp[Zloc + 4] = temp[Zloc]
        temp[Zloc] = t1
        states.append((temp, "up"))
    temp = board[::]

    if Zloc % 4 > 0:
        t1 = temp[Zloc - 1]
        temp[Zloc - 1] = temp[Zloc]
        temp[Zloc] = t1
        states.append((temp, "right"))
    temp = board[::]

    if Zloc % 4 < 3:
        t1 = temp[Zloc + 1]
        temp[Zloc + 1] = temp[Zloc]
        temp[Zloc] = t1
        states.append((temp, "left"))
    return states


def heuristicFunc(board):
    sm = 0
    for i in range(len(board)):
        # how many up then how many accross
        # board[i] is ideal position + 1 so ideal position = board[i] - 1
        if board[i] != 0:
            sm = sm + ((board[i] - 1) // 4 - i // 4)**2
            sm = sm + ((board[i] - 1) % 4 - i % 4)**2
    return sm * 5


def hamming(board):
    sm = 0
    for i in range(len(board)):
        if board[i] != 0 and board[i] - 1 != i:
            sm = sm + 1
    return sm


def Astar(boardStart, heuristicFunc):
    q = queue.PriorityQueue()
    order = 0
    endNotFound = True
    q.put((0, (boardStart, "", 0)))
    visited = set()
    while endNotFound:
        board = q.get()[1]
        order = board[2] + 1
        visited.add(tuple(board[0]))
        if heuristicFunc(board[0]) == 0:
            return board[1]
        genStates = generateStates(board[0])
        for i in genStates:
            if tuple(i[0]) not in visited:
                q.put((heuristicFunc(i[0]) + order, (i[0], board[1] + " " + i[1], order)))


def doSteps(string):
    steps = string.split()
    print(len(steps))
    for i in steps:
        print(i)
        pyautogui.press(i)


def makeArray():
    board = []
    for i in range(16):
        board.append(int(input()))
    return board


c = makeArray()
v = Astar(c, heuristicFunc)
print("starting the running now")
time.sleep(2)
doSteps(v)
