import random
import sys

gamemode = ["A", "a", "P", "p"]
answers = ["Yes", "yes", "No", "no"]
gamemode_variant = 0
win = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7),
       (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]


def draw_board(board):
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


def input_game_mode():
    global gamemode_variant
    gamemode_variant = 0
    chosen_gamemode = 0
    while chosen_gamemode not in gamemode:
        chosen_gamemode = input(
            "\nPress A to play against AI \nor P to play against another player: \n")
    if chosen_gamemode == "A" or chosen_gamemode == "a":
        print("\nYou are playing against: AI\n")
        gamemode_variant = gamemode_variant + 1
    else:
        print("\nYou are playing against: Player2\n")
        gamemode_variant = gamemode_variant + 2
    return gamemode_variant


def enemy_ai():
    global board_setup
    board_setup = [" "] * 10
    player_marker, computer_marker = input_player_marker()
    turn = who_goes_first()
    print("\nThe " + turn + " will go first.\n")
    game_is_playing = True
    while game_is_playing:
        if turn == "player":
            draw_board(board_setup)
            move = get_player_move(board_setup)
            make_move(board_setup, player_marker, move)
            if check_for_winner(board_setup, player_marker):
                draw_board(board_setup)
                print("You have won the game!\nCongratulation!\n")
                game_is_playing = False
            else:
                if is_board_full(board_setup):
                    draw_board(board_setup)
                    print("The game is a tie!\n")
                    break
                else:
                    turn = "computer"
        else:
            move = get_computer_move(board_setup, computer_marker)
            make_move(board_setup, computer_marker, move)
            if check_for_winner(board_setup, computer_marker):
                draw_board(board_setup)
                print("The computer has beaten you!\n You lose.\n")
                game_is_playing = False
            else:
                if is_board_full(board_setup):
                    draw_board(board_setup)
                    print("The game is a tie!\n")
                    break
                else:
                    turn = "player"


def input_player_marker():
    marker = ""
    while not (marker == "X" or marker == "O"):
        print("Do you want to be X or O?")
        marker = input().upper()
    if marker == "X":
        return ["X", "O"]
    else:
        return ["O", "X"]


def who_goes_first():
    if random.randint(0, 1) == 0:
        return "computer"
    else:
        return "player"


def get_player_move(board):
    move = ' '
    while move not in "1 2 3 4 5 6 7 8 9".split() or not is_space_free(board, int(move)):
        print("\nWhat is your next move? (1-9)")
        move = input()
    return int(move)


def make_move(board, marker, move):
    board[move] = marker


def check_for_winner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[9] == le and bo[5] == le and bo[1] == le))


def space_taken(board):
    while True:
        try:
            x = int(input())
            if x in board:
                return x
            else:
                print("\nSpace already taken. Please try again.")
        except ValueError:
            print("\nPlease enter a number between 1 and 9.")


def get_computer_move(board, computer_marker):
    global move
    if computer_marker == "X":
        player_marker = "O"
    else:
        player_marker = "X"
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, computer_marker, i)
            if check_for_winner(copy, computer_marker):
                return i
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, player_marker, i)
            if check_for_winner(copy, player_marker):
                return i
    move = choose_random_move_from_list(board, [1, 3, 7, 9])
    if move is not None:
        return move
    if is_space_free(board, 5):
        return 5
    return choose_random_move_from_list(board, [2, 4, 6, 8])


def is_space_free(board, move):
    return board[move] == " "


def get_board_copy(board):
    copy_board = []
    for i in board:
        copy_board.append(i)
    return copy_board


def choose_random_move_from_list(board, moves_list):
    possible_moves = []
    for i in moves_list:
        if is_space_free(board, i):
            possible_moves.append(i)
    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None


def is_board_full(board):
    for i in range(1, 10):
        if is_space_free(board, i):
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


def enemy_player():
    for player in "XO" * 9:
        draw_board(board)
        if end(win, board):
            break
        print("\nPlayer {0}".format(player))
        board[space_taken(board)] = player
        print()


def play_again():
    escape_input = None
    while escape_input not in answers:
        escape_input = input("Do you want to play again? (yes or no)\n")
    if escape_input == "No" or escape_input == "no":
        exit()
    return escape_input


def exit():
    sys.exit("\nGood Bye!")


print("\n /  Welcome to  \ \n \ TIC TAC TOE !/ \n ")

while True:
    input_game_mode()
    board = [None] + list(range(1, 10))
    if gamemode_variant == 1:
        enemy_ai()
    if gamemode_variant == 2:
        enemy_player()
    play_again()
