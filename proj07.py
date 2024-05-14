import sys
import NMM  # This is necessary for the project

BANNER = """
    __      _(_)_ __  _ __   ___ _ __| | |
    \ \ /\ / / | '_ \| '_ \ / _ \ '__| | |
     \ V  V /| | | | | | | |  __/ |  |_|_|
      \_/\_/ |_|_| |_|_| |_|\___|_|  (_|_)
"""

RULES = """                                                                                       
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    The game is ends when a player (the loser) has less than three 
    pieces on the board.
"""

MENU = """
    Game commands (first character is a letter, second is a digit):
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game

"""


## Uncomment the following lines when you are ready to do input/output tests!
## Make sure to uncomment when submitting to Codio.
# def input( prompt=None ):
#    if prompt != None:
#        print( prompt, end="" )
#    aaa_str = sys.stdin.readline()
#    aaa_str = aaa_str.rstrip( "\n" )
#    print( aaa_str )
#    return aaa_str


def count_mills(board, player):
    """
        add your function header here.
    """
    count = 0

    for item in board.MILLS:
        L1 = []
        for location in item:
            if board.points[location] == player:
                L1.append(location)
        if L1 in board.MILLS:
            count += 1
            break
    return count


def place_piece_and_remove_opponents(board, player, destination):
    """
        add your function header here.
    """
    if board.points[destination] == " ":
        x = count_mills(board, player)
        board.assign_piece(player, destination)
        y = count_mills(board, player)
        if y > x:
            print("A mill was formed!")
            print(board)
            remove_piece(board, player)
    else:
        x = count_mills(board, player)
        if x >= 1:
            remove_piece(board, player)
        else:
            raise RuntimeError


def move_piece(board, player, origin=0, destination=0):
    """
        add your function header here.
    """
    if origin == 0 or destination == 0:
        raise RuntimeError("Invalid number of points")
    if destination in board.ADJACENCY[origin]:
        if board.points[origin] == player:
            if board.points[destination] == " ":
                board.clear_place(origin)
                place_piece_and_remove_opponents(board, player, destination)
            else:
                raise RuntimeError("Invalid command: Destination point already taken")
        else:
            raise RuntimeError("Invalid command: Origin point does not belong to player")

    else:
        raise RuntimeError("Invalid command: Destination is not adjacent")


def points_not_in_mills(board, player):
    """
        add your function header here.
    """
    mill = []
    not_in_mill = []
    for item in board.MILLS:
        L1 = []
        for location in item:
            if board.points[location] == player:
                L1.append(location)
        if L1 in board.MILLS:
            mill.extend(L1)
        else:
            not_in_mill.extend(L1)
    S1 = set(mill)
    S2 = set(not_in_mill)
    S_final = S2-S1
    return S_final

def placed(board, player):
    """
        add your function header here.
    """
    S1 = set()
    for key, value in board.points.items():
        if value == player:
            S1.add(key)
    return S1

def remove_piece(board, player):
    """
        add your function header here.
    """
    x = True
    while x:
        removed_p = input("Remove a piece at :> ")
        player = get_other_player(player)
        piece_placed = placed(board, player)
        not_mill = points_not_in_mills(board, player)

        if removed_p in piece_placed and removed_p in not_mill:
            board.clear_place(removed_p)
            x = False

        elif board.points[removed_p] != player:
            raise RuntimeError("Invalid command: Point does not belong to player")

        elif removed_p not in not_mill:
            raise RuntimeError("Invalid command: Point is in a mill")


def is_winner(board, player):
    """
        add your function header here.
    """
    player1_counter = 0
    player2_counter = 0
    for key,value in board.points.items():
        if value == " ":
            pass
        elif value == player:
            player1_counter += 1
        else:
            player2_counter += 1
    if player2_counter <= 2:
        return True
    else:
        return False


def get_other_player(player):
    """
    Get the other player.
    """
    return "X" if player == "O" else "O"


def main():
    # Loop so that we can start over on reset
    while True:
        # Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        player = "X"
        placed_count = 0  # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent

        # PHASE 1
        print(player + "'s turn!")
        # placed = 0
        command = input("Place a piece at :> ").strip().lower()
        print()

        # Until someone quits or we place all 18 pieces...
        while command != 'q' and command != 'r' and placed_count != 18:
            x = True
            while x:
                try:
                    place_piece_and_remove_opponents(board, player, command)
                    placed_count += 1
                    x = False

                # Any RuntimeError you raise inside this try lands here
                except RuntimeError as error_message:
                    print(("{:s}\nTry again.").format("Invalid number of points"))

            # Prompt again
            print(board)

            player = get_other_player(player)
            # if placed_count % 2 == 0:
            #     player = "X"
            # else:
            #     player = "O"

            print(player + "'s turn!")

            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()

            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        # Go back to top if reset
        if command == 'r':
            continue
        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            command = command.replace(",", " ").split()
            y = True
            while y:

                try:
                    if len(command) == 2:
                        move_piece(board, player, command[0], command[1])
                        S1 = placed(board, player)
                        if len(S1) <= 2:
                            x = is_winner(board, player)
                            if x == True:
                                print(BANNER)
                        player = get_other_player(player)
                        y = False
                    else:
                        raise RuntimeError

                # Any RuntimeError you raise inside this try lands here
                except RuntimeError as error_message:
                    print("{:s}\nTry again.".format(str(error_message)))

            # Display and reprompt
            print(board)
            # display_board(board)
            print(player + "'s turn!")
            command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        # If we ever quit we need to return
        if command == 'q':
            return


if __name__ == "__main__":
    main()
