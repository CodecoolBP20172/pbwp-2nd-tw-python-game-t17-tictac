import random
import sys
import time
import pygame

name_of_players = {"X": "", "O": ""}
gamemode = ["A", "a", "P", "p"]
answers = ["Yes", "yes", "No", "no"]
# -------------------------------------Used by both Modes-------------------------------------------------


def intro():
    print("\n\t|  Welcome to    | ")
    print("\t|  TIC TAC TOE ! | \n ")
    pygame.init()
    pygame.mixer.init()
    play_sound("welcome_message.wav")


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


def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()


def input_game_mode():
    global gamemode_variant
    gamemode_variant = 0
    chosen_gamemode = 0
    while chosen_gamemode not in gamemode:
        chosen_gamemode = input(
            "\nPress A to play against AI \nor P to play against another player: \n")
    if chosen_gamemode == "A" or chosen_gamemode == "a":
        play_sound("ai_mode_start.ogg")
        gamemode_variant = gamemode_variant + 1
    else:
        play_sound("player_mode_start.wav")
        gamemode_variant = gamemode_variant + 2
    return gamemode_variant


def quit_game(board, message=None):
    draw_board(board)
    print(message)


def get_player_move(board):
    move = " "
    while move not in "1 2 3 4 5 6 7 8 9".split() or not is_space_free(board, int(move)):
        play_sound("fire.wav")
        print("\nWhat is your next move? (1-9)")
        move = input()
    return int(move)


def make_move(board, marker, move):
    board[move] = marker


def is_board_full(board):
    for space in range(1, 10):
        if is_space_free(board, space):
            return False
    return True


def space_taken(board):
    while True:
        try:
            move = int(input())
            if move in board:
                return move
            else:
                play_sound("ping.wav")
                print("\nSpace already taken. Please try again.")
        except ValueError:
            print("\nPlease enter a number between 1 and 9.")


def play_again():
    escape_input = None
    while escape_input not in answers:
        escape_input = input("\nDo you want to play again? (yes or no)\n")
    if escape_input == "No" or escape_input == "no":
        exit()
    return escape_input


def exit():
    play_sound("exit_message.ogg")
    time.sleep(1)
    good_bye()
    sys.exit()


def congrats():
    play_sound("good_shot.wav")
    print("\n CCCC    OOOO   N    N   GGGG   RRRR    AAAA   TTTTT   SSSS   !!")
    print("C       O    O  NN   N  G       R   R  A    A    T    S       !!")
    print("C       O    O  N N  N  G  GGG  RRRRR  AAAAAA    T     SSSS   !!")
    print("C       O    O  N   NN  G    G  R  R   A    A    T         S")
    print(" CCCC    OOOO   N    N   GGGG   R   R  A    A    T     SSSS   !!\n")
    return


def good_bye():
    print("\n GGGG    OOOO    OOOO   DDDD       BBBB  Y   Y  EEEE  !!")
    print("G       O    O  O    O  D   D      B  B   Y Y   E     !!")
    print("G  GGG  O    O  O    O  D    D     B B     Y    EEE   !!")
    print("G    G  O    O  O    O  D   D      B  B    Y    E")
    print(" GGGG    OOOO    OOOO   DDDD       BBBB    Y    EEEE  !!\n")
    return
# -------------------------------------------Used by AI-----------------------------------------------------


def game_against_ai():
    global board_setup
    global game_is_playing
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
                quit_game(board_setup, "\nYou have won the game!\n")
                congrats()
                game_is_playing = False
            else:
                if is_board_full(board_setup):
                    play_sound("ai_mode_player_tie.ogg")
                    quit_game(board_setup, "\nThe game is a tie!\n")
                    break
                else:
                    turn = "computer"
        else:
            move = get_computer_move(board_setup, computer_marker)
            make_move(board_setup, computer_marker, move)
            if check_for_winner(board_setup, computer_marker):
                play_sound("ai_win.ogg")
                quit_game(board_setup, "\nThe computer has beaten you!\n You lose.\n")
                break
            else:
                if is_board_full(board_setup):
                    play_sound("no_happy_ending_for_a_turret.ogg")
                    quit_game(board_setup, "\nThe game is a tie!\n")
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


def get_computer_move(board, computer_marker):
    global move
    if computer_marker == "X":
        player_marker = "O"
    else:
        player_marker = "X"
    for space in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, space):
            make_move(copy, computer_marker, space)
            if check_for_winner(copy, computer_marker):
                return space
    for space in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, space):
            make_move(copy, player_marker, space)
            if check_for_winner(copy, player_marker):
                return space
    move = choose_random_move_from_list(board, [1, 3, 7, 9])
    if move is not None:
        return move
    if is_space_free(board, 5):
        return 5
    return choose_random_move_from_list(board, [2, 4, 6, 8])


def choose_random_move_from_list(board, moves_list):
    possible_moves = []
    for space in moves_list:
        if is_space_free(board, space):
            possible_moves.append(space)
    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None


def check_for_winner(board, marker):
    return ((board[7] == marker and board[8] == marker and board[9] == marker) or
            (board[4] == marker and board[5] == marker and board[6] == marker) or
            (board[1] == marker and board[2] == marker and board[3] == marker) or
            (board[7] == marker and board[4] == marker and board[1] == marker) or
            (board[8] == marker and board[5] == marker and board[2] == marker) or
            (board[9] == marker and board[6] == marker and board[3] == marker) or
            (board[7] == marker and board[5] == marker and board[3] == marker) or
            (board[9] == marker and board[5] == marker and board[1] == marker))


def is_space_free(board, move):
    return board[move] == " "


def get_board_copy(board):
    copy_board = []
    for space in board:
        copy_board.append(space)
    return copy_board
# ---------------------------------------------Used by PvP------------------------------------------------


def game_against_player(players):
    #play_sound("player_mode_start2.wav")
    board_setup = [" "] * 10
    for marker in players:
        players[marker] = ("")
    assigning_names(players)
    print("First come, first served!\n")
    game_is_playing = True
    while game_is_playing:
        for marker in players:
            if not game_is_playing:
                break
            draw_board(board_setup)
            move = get_player_move(board_setup)
            make_move(board_setup, marker, move)
            for marker, name in players.items():
                if check_for_winner(board_setup, marker):
                    draw_board(board_setup)
                    print("\n{0}".format(name), "wins.")
                    congrats()
                    game_is_playing = False
                    break
                else:
                    if is_board_full(board_setup):
                        draw_board(board_setup)
                        print("The game ends in a tie.\n")
                        game_is_playing = False
                        break


def get_name_input():
    name = input("\nPlease, enter a name!\n").title()
    return str(name)


def assigning_names(dictionary):
    global name
    for key in dictionary:
        if dictionary[key] == (""):
            name = get_name_input()
            dictionary[key] = name
        print(name, "will play with", key, "\n")
    return dictionary
# ----------------------------------------------The Game------------------------------------------------


intro()

while True:
    input_game_mode()
    if gamemode_variant == 1:
        game_against_ai()
    if gamemode_variant == 2:
        game_against_player(name_of_players)
    play_again()
