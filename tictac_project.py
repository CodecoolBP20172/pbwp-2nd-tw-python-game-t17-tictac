import random
import sys

Modes = ["A", "a", "P", "p"]
Answers = ["Yes", "yes", "No", "no"]
gamemode = 0
win = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7),
       (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]


def drawBoard(board):
    print("     |     |")
    print("  " + str(board[7]) + "  |  " +
          str(board[8]) + "  |  " + str(board[9]))
    print("     |     |")
    print("-----------------")
    print("     |     |")
    print("  " + str(board[4]) + "  |  " +
          str(board[5]) + "  |  " + str(board[6]))
    print("     |     |")
    print("-----------------")
    print("     |     |")
    print("  " + str(board[1]) + "  |  " +
          str(board[2]) + "  |  " + str(board[3]))
    print("     |     |")


def inputGameMode():
    global gamemode
    gamemode = 0
    moveletter = 0
    while moveletter not in Modes:
        moveletter = input(
            "\nPress A to play against AI \nor P to play against another player: \n")
    if moveletter == "A" or moveletter == "a":
        print("\nYou are playing against: AI\n")
        gamemode = gamemode + 1
    else:
        print("\nYou are playing against: Player2\n")
        gamemode = gamemode + 2
    return gamemode


def enemyAI():
    global theBoard
    theBoard = [" "] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print("\nThe " + turn + " will go first.\n")
    gameIsPlaying = True
    while gameIsPlaying:
        if turn == "player":
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print("You have won the game!\nCongratulation!\n")
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print("The game is a tie!\n")
                    break
                else:
                    turn = "computer"
        else:
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print("The computer has beaten you!\n You lose.\n")
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print("The game is a tie!\n")
                    break
                else:
                    turn = "player"


def inputPlayerLetter():
    letter = ""
    while not (letter == "X" or letter == "O"):
        print("Do you want to be X or O?")
        letter = input().upper()
    if letter == "X":
        return ["X", "O"]
    else:
        return ["O", "X"]


def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return "computer"
    else:
        return "player"


def getPlayerMove(board):
    move = ' '
    while move not in "1 2 3 4 5 6 7 8 9".split() or not isSpaceFree(board, int(move)):
        print("\nWhat is your next move? (1-9)")
        move = input()
    return int(move)


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[9] == le and bo[5] == le and bo[1] == le))


def taken(board):
    while True:
        try:
            x = int(input())
            if x in board:
                return x
            else:
                print("\nSpace already taken. Please try again.")
        except ValueError:
            print("\nPlease enter a number between 1 and 9.")


def getComputerMove(board, computerLetter):
    global move
    if computerLetter == "X":
        playerLetter = "O"
    else:
        playerLetter = "X"
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move is not None:
        return move
    if isSpaceFree(board, 5):
        return 5
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isSpaceFree(board, move):
    return board[move] == " "


def getBoardCopy(board):
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard


def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


def end(win, board):
    for x, o, b in win:
        if board[x] == board[o] == board[b]:
            print("\nPlayer {0} wins!".format(board[x]))
            print("Congratulations!\n")
            return True
    if 9 == sum((pos == "X" or pos == "O") for pos in board):
        print("The game ends in a tie.\n")
        return True


def enemyPlayer():
    for player in "XO" * 9:
        drawBoard(board)
        if end(win, board):
            break
        print("\nPlayer {0}".format(player))
        board[taken(board)] = player
        print()


def playAgain():
    escInput = None
    while escInput not in Answers:
        escInput = input("Do you want to play again? (yes or no)\n")
    if escInput == "No" or escInput == "no":
        exit()
    return escInput


def exit():
    sys.exit("\nGood Bye!")


print("\n /  Welcome to  \ \n \ TIC TAC TOE !/ \n ")

while True:
    inputGameMode()
    board = [None] + list(range(1, 10))
    if gamemode == 1:
        enemyAI()
    if gamemode == 2:
        enemyPlayer()
    playAgain()
