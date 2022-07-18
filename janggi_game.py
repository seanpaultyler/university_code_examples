# Author: Sean Tyler
# Date: late
# Description:  A Janggi game (Korean chess).  Work in progress.

class Color:
    """A class of console colors, for printing purposes."""
    red_pieces = '\033[1;33;41m'
    blue_pieces = '\033[1;33;44m'
    board = '\033[1;37;48m'
    empty = '\033[5;35;48m'
    endc = '\033[m'


class JanggiGame:
    """A Janggi Game class."""

    def __init__(self):
        """Initializes the JanggiGame class."""
        self._board = []
        self._red_moves = []
        self._blue_moves = []
        self._generals = [None, None]
        self._player_turn = "BLUE"
        self._game_state = "UNFINISHED"
        for x in range(9):
            self._board.append([])
            for y in range(10):
                self._board[x].append(None)
        self.new_game()
        self.compile_all_moves()

    def set_general(self, general, player):
        """Sets the game's private general var.  For querying check conditions."""
        if player == "RED":
            self._generals[1] = general
        else:
            self._generals[0] = general

    def get_space(self, space):
        """Returns the piece at a spot on the board provided a [x,n] coordinate, or None if none."""
        return self._board[space[0]][space[1]]

    def get_in_palace(self, space):
        """Returns a string indicating which palace a provided [x,n] coordinate is in.  If none, returns None. """
        if 3 <= space[0] <= 5:
            if space[1] < 3:
                return "RED"
            if space[1] > 6:
                return "BLUE"

    def get_move_in_palace(self, start, end):
        """Returns True if a move begins and ends within a palace.  For pieces with certain move restrictions.

        Parameters
        ---------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """
        if self.get_in_palace(start) == self.get_in_palace(end) and self.get_in_palace(start) is not None:

            # Check diagonal lines according to rules.
            if start[0] in [3, 5] and start[1] == 8 and end[0] == 4 and end[1] in [0, 2, 7, 9]:
                return False
            if start[0] == 4 and start[1] in [0, 2, 7, 9] and end[0] in [3, 5] and end[1] in [1, 8]:
                return False
            return True
        return False

    def clear_space(self, space):
        """Sets a space to empty.  For after moving a piece, etc."""
        self._board[space[0]][space[1]] = None

    def assign_space(self, space, piece):
        """Sets a specified space as occupied by the specified piece, for initial board setup or moving a piece.

        Parameters
        ----------
        space : list
            The space to assign, as a list in the form [x,n]
        piece : Piece(subclass)
            The piece object subclass (soldier, General) that should occupy the space.
        """

        self._board[space[0]][space[1]] = piece

    def get_game_state(self):
        """Returns the state of the game.  "UNFINISHED if still playing, or RED WON or BLUE WON if respective
        player has won."""
        return self._game_state

    def make_move(self, alphanum_start, alphanum_end):
        """Makes the specified move.  Returns True if move is successful. Returns False if invalid move, wrong player's
        turn, or game over.

        Paramaters
        ----------
        alphanum_start : list
            Coordinates for a piece as a list, in alphanumeric form.  'a1', 'g5', etc.
        alphanum_end
            Coordinates for the specified piece to attempt to move to, as a list.
        """
        if alphanum_start == alphanum_end:
            self.switch_turn()
            return True

        # Convert board spaces from alphanumeric to corresponding list indices.
        start = self.map_to_board(alphanum_start)
        end = self.map_to_board(alphanum_end)
        piece = self.get_space(start)

        # Ensure game is ongoing.
        if self._game_state == "UNFINISHED":

            # Make sure a piece is being moved.
            if piece is not None:

                # Make sure the player is moving their own piece.
                # noinspection PyUnresolvedReferences
                if piece.get_player() == self._player_turn:

                    # Ask the piece if the move is valid.
                    piece.compile_valid_moves()
                    if piece.move(start, end):

                        if not self.move_in_check(start, end, piece):
                            self.clear_space(start)
                            self.assign_space(end, piece)
                            piece.set_position(end)
                            self.end_turn()
                            return True

        # If move fails for any reason, return invalid.
        return False

    def move_in_check(self, start, end, piece):
        """Finds out of a player made a move in check that didn't break check, or moved into check."""
        # Move the piece
        previous = self.get_space(end)
        self.clear_space(start)
        self.assign_space(end, piece)
        piece.set_position(end)

        # Store whether move was free of check.
        self.compile_all_moves()
        valid = self.is_in_check(self._player_turn)

        # Revert move
        self.assign_space(start, piece)
        piece.set_position(start)
        self.assign_space(end, previous)
        self.compile_all_moves()

        return valid

    def end_turn(self):
        """Ends a players turn."""
        self.switch_turn()
        if self.is_in_check(self._player_turn):
            self.determine_checkmate(self._player_turn)
        self.compile_all_moves()

    def determine_checkmate(self, player):
        """Runs through every piece that belongs to the player in check.  If no move returns as valid, game
        is over and opposing player wins."""

        # Goes through every space, if we find one of the checked player's pieces, find simulate every move it can
        # make.  If one of those moves breaks check, return False signalling no checkmate.  Otherwise, game over.
        for column in self._board:
            for piece in column:
                if piece is not None and piece.get_player() == player:
                    for move in piece.get_moves():
                        if not self.move_in_check(piece.get_position(), move, piece):
                            return False
        self._game_state = "RED_WON" if player == "BLUE" else "BLUE_WON"
        return True

    def switch_turn(self):
        """When called, switches the _player_turn var"""
        if self._player_turn == "RED":
            self._player_turn = "BLUE"
        else:
            self._player_turn = "RED"

    def compile_all_moves(self):
        """Compiles list of all moves each player can make."""
        self._blue_moves = list()
        self._red_moves = list()

        # Go through every space, if a piece is there, ask it what it can do, then add what is returns
        # to that player's potential moves.  For determining check/mate.
        for column in self._board:
            for piece in column:
                if piece is not None:
                    piece.compile_valid_moves()
                    for move in piece.get_moves():
                        if piece.get_player() == "BLUE":
                            if move not in self._blue_moves:
                                self._blue_moves.append(move)
                        else:
                            if move not in self._red_moves:
                                self._red_moves.append(move)

    def get_all_moves(self, player=None):
        """Returns the list of all moves a player's pieces can commit,
        or if provided a player, that player's moves only."""

        self.compile_all_moves()
        if player is None:
            moves = self._blue_moves
            for move in self._red_moves:
                if move not in self._blue_moves:
                    self._blue_moves.append(move)
            return moves
        else:
            if player == "RED":
                return self._red_moves
            else:
                return self._blue_moves

    def get_piece_moves(self, space):
        """Returns a list of a specific piece's moves.  For debugging."""
        return [self.board_to_map(i) for i in self.get_space(self.map_to_board(space)).get_moves()]

    def is_in_check(self, player):
        """Requests the check status of the specified player's General."""
        if player.upper() == "RED":
            return self._generals[1].in_check()
        else:
            return self._generals[0].in_check()

    def map_to_board(self, string):
        """Takes an alphanumeric board space (e.g. "a1") and converts it to numeric coordinates (e.g. 0,0)"""
        if len(string) == 3:
            return [self.alpha_to_numeric(string[0]), 9]
        return [self.alpha_to_numeric(string[0]), int(string[1])-1]

    def alpha_to_numeric(self, alpha):
        """Given a letter a-i, converts it to numeric equivalent, beginning at 0. e.g. a = 0, e = 5"""
        num = 0
        for letter in "abcdefghi":
            if letter is alpha:
                return num
            num += 1

    def board_to_map(self, space):
        """Takes an algebraic string and returns the associated list of list element."""
        string = "abcdefghi"
        return string[space[0]] + str(space[1]+1)

    def new_game(self):
        """Sets the board for a new game.  List of list for each piece, first list is all x coordinates,
        second list is all n coordinates.  For instance below, generals will be initialized at [4,1] and [4,8]"""
        pieces = [[[0, 2, 4, 6, 8], [3, 6]],  # 0 - soldier
                  [[1, 7], [2, 7]],           # 1 - cannon
                  [[3, 5], [0, 9]],           # 2 - guard
                  [[4], [1, 8]],              # 3 - general
                  [[2, 6], [0, 9]],           # 4 - elephant
                  [[1, 7], [0, 9]],           # 5 - horse
                  [[0, 8], [0, 9]]]           # 6 - chariot

        # Loop through each entry in the pieces list, calling the initialize_piece method for each coordinate pair.
        for piece in range(len(pieces)):
            for column in pieces[piece][0]:
                for row in pieces[piece][1]:
                    self.initialize_piece(piece, [column, row])

    def initialize_piece(self, piece, space):
        """Initializes pieces.

        Parameters
        -----------
        piece : int
            The type of piece to initialize.
        space : list
            The [x,n] coordinates at which to initialize the piece.
        """

        # Intialize piece's player var based on board position.  Blue is top.
        if space[1] < 4:
            color = "RED"
        else:
            color = "BLUE"

        # Change the class we initialize based on the piece specified.
        piece_class = Soldier
        if piece == 1:
            piece_class = Cannon
        if piece == 2:
            piece_class = Guard
        if piece == 3:
            piece_class = General
        if piece == 4:
            piece_class = Elephant
        if piece == 5:
            piece_class = Horse
        if piece == 6:
            piece_class = Chariot

        piece_class(space, color, self)

    def print_board(self):
        """Prints the board to console."""
        for n in range(len(self._board[0])-1, -1, -1):
            if n+1 < 10:
                line = str(n+1) + " "
            else:
                line = str(n + 1)
            for x in range(0, len(self._board)):

                piece = self.get_space([x, n])
                if piece is None:
                    line += Color.empty + "   " + Color.endc
                else:
                    if piece.get_player() == "RED":
                        line += Color.red_pieces + piece.get_marker() + Color.endc
                    else:
                        line += Color.blue_pieces + piece.get_marker() + Color.endc

                if x < len(self._board)-1:
                    line += Color.board + "--" + Color.endc
            print(line)
            if n > 0:
                board_line = Color.board
                if n < 3 or n > len(self._board[0])-3:
                    if n == 2 or n == 9:
                        board_line += r"   |    |    |    | \  |  / |    |    |    | "
                    else:
                        board_line += r"   |    |    |    | /  |  \ |    |    |    | "
                else:
                    board_line += "   |    |    |    |    |    |    |    |    | "
                print(board_line + Color.endc)
        print("   a    b    c    d    e    f    g    h    i")


class Piece:

    def __init__(self, space, player, game):
        """Initializes a board piece.  For extension into specific piece types."""
        self._game = game
        self._game.assign_space(space, self)
        self._position = space
        self._player = player
        self._marker = "X"
        self._moves = []
        if self._player == "RED":
            self._opponent = "BLUE"
        else:
            self._opponent = "RED"

    def get_player(self):
        """Returns the player the piece belongs to."""
        return self._player

    def get_position(self):
        """Returns the pieces position in [x,n] format"""
        return self._position

    def set_position(self, space):
        """Sets the piece's private coordinate tracker, a list in the form [x,n]"""
        self._position = space

    def move(self, start, end):
        """Checks multiple conditions ("vacant spot, or pieces that can be captured, no blocking pieces, etc.).  If
        pass, moves piece to new position, and removes captured piece if applicable."""
        if start == end:
            return True
        if end in self._moves:

            return True
        return False

    def get_moves(self):
        """Returns the set of valid moves each piece can make, to check win conditions."""
        return self._moves

    def compile_valid_moves(self):
        """Compiles a list of valid moves.  The JanggiGame class will retrieve this from each piece to check
        which players can move where, and for Generals, to determine check and game over conditions."""
        self._moves = list()
        for move in self.potential_moves():
            if self.check_on_board(move):
                if self.check_move_path(self._position, move):
                    piece = self._game.get_space(move)
                    if piece is None or piece is not None and self._player != piece.get_player():
                        self._moves.append(move)

    def potential_moves(self):
        """Returns a list of theoretical moves ignoring board position and other pieces.  Implemented in subclass"""
        pass

    def check_on_board(self, space):
        """Returns true if the space is within the borders of the game board.
        Parameter is a list as [column,row] coordinate."""
        if 0 <= space[0] <= 8 and 0 <= space[1] <= 9:
            return True
        return False

    def check_move_path(self, start, end):
        """Implemented in subclass."""
        pass

    def get_marker(self):
        """Returns the marker specific to the piece that is set in subclass.  For printing purposes."""
        return self._marker


class Soldier(Piece):
    """A class for the Soldier piece of Janggi.  Moves one space left, right of forward, and diagonally when within
    palace.  For use with the JanggiGame class.

    Parameters
    ----------
    space : list
        The initial coordinates for the piece, in the form [x,n], for [alphabetic column, numeric row]
    player : string
        The player the piece belongs to.  Either "RED" or "BLUE"
    game : JanggiGame
        The game instance the piece belongs to.

    """
    def __init__(self, space, player, game):
        """Initializes the Soldier class with the given parameters."""
        super(Soldier, self).__init__(space, player, game)
        self._type = "Soldier"
        self._marker = " S "

    def potential_moves(self):
        """Compiles a list of valid moves for the Soldier class."""
        moves = list()

        # Any adjacent square is added, with restrictions added in check_move_path below and move_in_palace
        # in game class.
        for x in range(3):
            for n in range(3):
                moves.append([self._position[0]+x-1, self._position[1]+n-1])
        return moves

    def check_move_path(self, start, end):
        """Checks the validity of a move given the Soldiers' move restrictions.

        Parameters
        ----------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """

        # Restrict to "forward" movement, which is based on player.
        if self._player == "RED":
            if start[1] > end[1]:
                return False
        else:
            if start[1] < end[1]:
                return False

        # Cannot move diagonally, unless in palace.
        distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
        if (distance == 1 or (distance == 2 and self._game.get_move_in_palace(start, end))) and distance > 0:
            return True
        return False


class General(Piece):
    """A class for the General piece of Janggi.  Moves one space in any direction, but only within the palace.  For use
    with the JanggiGame class.  If the General is placed in check and cannot move or be saved from check, the
    opponent wins.

    Parameters
    ----------
    space : list
        The initial coordinates for the piece, in the form [x,n], for [alphabetic column, numeric row]
    player : string
        The player the piece belongs to.  Either "RED" or "BLUE"
    game : JanggiGame
        The game instance the piece belongs to.

    """

    def __init__(self, space, player, game):
        """Initializes the General class."""
        super(General, self).__init__(space, player, game)
        self._type = "General"
        self._marker = " G "
        self._game.set_general(self, self._player)

    def potential_moves(self):
        moves = list()

        # Returns all adjacent spaces.  Restrictions are handled by the check_move_path function below and
        # get_move_in_palace of game class.
        for x in range(3):
            for n in range(3):
                moves.append([self._position[0] + x - 1, self._position[1] + n - 1])
        return moves

    def check_move_path(self, start, end):
        """Checks the validity of a move given the Generals' move restrictions.

        Parameters
        ----------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """

        if self._game.get_move_in_palace(start, end):
            return True
        return False

    def in_check(self):
        """Asks the game class if the Guard's position is in the opponent's list of valid moves.  If so, check."""
        if self._position in self._game.get_all_moves(self._opponent):
            return True
        return False


class Guard(Piece):
    """A class for the Guard piece of Janggi.  Moves one space in any direction, but only within the palace.  For use
    with the JanggiGame class.

    Parameters
    ----------
    space : list
        The initial coordinates for the piece, in the form [x,n], for [alphabetic column, numeric row]
    player : string
        The player the piece belongs to.  Either "RED" or "BLUE"
    game : JanggiGame
        The game instance the piece belongs to.

    """

    def __init__(self, space, player, game):
        """Initializes the Guard class"""
        super(Guard, self).__init__(space, player, game)
        self._type = "Guard"
        self._marker = "GRD"

    def potential_moves(self):
        """Adds all potential moves for the Guard class."""

        # Every adjacent square is added as a potential move.
        moves = list()
        for x in range(3):
            for n in range(3):
                moves.append([self._position[0] + x - 1, self._position[1] + n - 1])
        return moves

    def check_move_path(self, start, end):
        """Checks the validity of a move given the Generals' move restrictions.

        Parameters
        ----------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """
        # Palace movement and diagonals are only criteria.
        # General palace function checks this for all pieces in palace.
        if self._game.get_move_in_palace(start, end):
            return True
        return False


class Horse(Piece):
    """A class for the Horse piece of Janggi.  Moves one space orthogonally and one space diagonally.  For use
    with the JanggiGame class.

    Parameters
    ----------
    space : list
        The initial coordinates for the piece, in the form [x,n], for [alphabetic column, numeric row]
    player : string
        The player the piece belongs to.  Either "RED" or "BLUE"
    game : JanggiGame
        The game instance the piece belongs to.

    """

    def __init__(self, space, player, game):
        """Initializes the Horse class."""
        super(Horse, self).__init__(space, player, game)
        self._type = "Horse"
        self._marker = " H "

    def potential_moves(self):
        """Compiles a list of potential move spots for the Horse.  Disregards board position and move validity."""
        moves = list()

        # Horse moves orthogonally once and diagonally once, either 2 up/down 1 over or 2 over and 1 up/down.
        # Loop through, adding each 2/3 or 3/2 combo, both positive and negative.
        for x in range(-2, 3):
            if x == 0:
                continue
            for n in range(-2, 3):
                if n == 0:
                    continue
                if abs(x) != abs(n):
                    moves.append([self._position[0] + x, self._position[1] + n])
        return moves

    def check_move_path(self, start, end):
        """Checks the validity of a move given the Generals' move restrictions.

        Parameters
        ----------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """
        # Checks the orthogonal portion of the move.  Diagonal movement cannot be "blocked" except at end space,
        # which is already checked in the general move function.

        # If x movement is greater than n movement, check x direction orthogonal
        if abs(start[0] - end[0]) > abs(start[1] - end[1]):
            if self._game.get_space([start[0] + (1 if start[0] < end[0] else -1), start[1]]) is not None:
                return False
        # If n movement is greater, check n orthogonal
        else:
            if self._game.get_space([start[0], start[1] + (1 if start[1] < end[1] else -1)]) is not None:
                return False
        return True


class Cannon(Piece):
    """A class for the Cannon piece of Janggi.  Moves across the board as many spaces as desired, with the
    restriction that all spaces must be empty except for ONE ally between start and end.  For use
    with the JanggiGame class.

    Parameters
    ----------
    space : list
        The initial coordinates for the piece, in the form [x,n], for [alphabetic column, numeric row]
    player : string
        The player the piece belongs to.  Either "RED" or "BLUE"
    game : JanggiGame
        The game instance the piece belongs to.

    """

    def __init__(self, space, player, game):
        """Initializes the Cannon class."""
        super(Cannon, self).__init__(space, player, game)
        self._type = "Cannon"
        self._marker = " C "

    def potential_moves(self):
        """Compiles a list of valid moves.  The JanggiGame class will retrieve this from each piece to check
        which players can move where, and for the Generals, to determine check and game over conditions."""
        moves = []

        # Potential cannon moves in any orthogonal line, so as long as x or n coordinates match, its a potential
        # move spot.
        for x in range(0, 10):
            for n in range(0, 11):
                if x == self._position[0] or n == self._position[1]:
                    moves.append([x, n])
        return moves

    def check_move_path(self, start, end):
        """Checks the validity of a move given the Cannons' move restrictions.  End spot validity is checked in general
        move function.

        Parameters
        ----------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """
        # Cannon must have one ally "screen" between move spaces.
        ally = False
        x = start[0]
        n = start[1]

        # Loop through in between spaces, checking for MAX one ally and no other pieces blocking.
        while x != end[0] or n != end[1]:
            piece = self._game.get_space([x, n])

            # If we find a piece between self and end space, check if its ally.  If so, check if we've already
            # found an ally.  If so, return False.  If not, mark we have an ally. (Cannon move will fail if there is
            # not a ONE ally screen between start and end spots)
            if piece is not None:
                if piece is not self and piece.get_player() == self._player:
                    if ally is False:
                        ally = True
                    else:
                        return False

            # Increment towards end space and repeat loop
            if n > end[1]:
                n = n - 1
            elif n < end[1]:
                n = n + 1
            if x > end[0]:
                x = x - 1
            elif x < end[0]:
                x = x + 1

        # If we reach the end space and there wasn't an ally screen, return False.
        if ally is False:
            return False
        return True


class Chariot(Piece):
    """A class for the Chariot piece of Janggi.  Moves across the board as many spaces as desired so long as
      path is empty.  For use with the JanggiGame class.

    Parameters
    ----------
    space : list
        The initial coordinates for the piece, in the form [x,n], for [alphabetic column, numeric row]
    player : string
        The player the piece belongs to.  Either "RED" or "BLUE"
    game : JanggiGame
        The game instance the piece belongs to.

    """

    def __init__(self, space, player, game):
        """Initializes the Chariot class."""
        super(Chariot, self).__init__(space, player, game)
        self._type = "Chariot"
        self._marker = "CHT"

    def potential_moves(self):
        """Compiles a list of valid moves.  The JanggiGame class will retrieve this from each piece to check
        which players can move where, and for the Generals, to determine check and game over conditions."""
        moves = []

        # Chariot can move to any space orthogonally, so if x or n value matches, add to potential moves.
        for x in range(0, 10):
            for n in range(0, 11):
                if x == self._position[0] or n == self._position[1]:
                    moves.append([x, n])
        return moves

    def check_move_path(self, start, end):
        """Checks the validity of a move given the Chariots' move restrictions.

        Parameters
        ----------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """

        # Loop through from start to second-to-end space.
        x = start[0]
        n = start[1]
        while x != end[0] or n != end[1]:

            # Simple check for chariot, if any space is blocked by a piece that isn't the end space, return False.
            piece = self._game.get_space([x, n])
            if piece is not None:
                if piece is not self:
                    return False

            # Increment x or n towards end space
            if n > end[1]:
                n = n - 1
            elif n < end[1]:
                n = n + 1
            if x > end[0]:
                x = x - 1
            elif x < end[0]:
                x = x + 1

        return True


class Elephant(Piece):
    """A class for the Elephant piece of Janggi.  Moves one space orthogonally and two spaces diagonally.
    For use with the JanggiGame class.

    Parameters
    ----------
    space : list
        The initial coordinates for the piece, in the form [x,n], for [alphabetic column, numeric row]
    player : string
        The player the piece belongs to.  Either "RED" or "BLUE"
    game : JanggiGame
        The game instance the piece belongs to.

    """

    def __init__(self, space, player, game):
        """Initializes the Elephant class."""
        super(Elephant, self).__init__(space, player, game)
        self._type = "Elephant"
        self._marker = " E "

    def potential_moves(self):
        """Returns potential moves for the Elephant.  Does not screen invalid moves."""
        moves = list()

        #  Elephant can similar to horse, with one orthogonal move but two diagonal.  This means each combo of
        # 3,2 or 2,3, both positive and negative, is a potential spot.
        for x in range(-3, 4):
            if x == 0:
                continue
            for n in range(-3, 4):
                if n == 0:
                    continue
                if abs(x) == 3 and abs(n) == 2 or abs(n) == 3 and abs(x) == 2:
                    moves.append([self._position[0] + x, self._position[1] + n])
        return moves

    def check_move_path(self, start, end):
        """Checks the validity of a move given the Elephants' move restrictions.

        Parameters
        ----------
        start : list
            The space the piece is moving from, in the form [x,n], for [alphabetic column, numeric row]
        end : list
            The space the piece is moving to, in the form [x,n], for [alphabetic column, numeric row]
        """

        # Check orthogonal moves the same as horse.
        if abs(start[0] - end[0]) > abs(start[1] - end[1]):
            orthogonal = [start[0] + (1 if start[0] < end[0] else -1), start[1]]
        else:
            orthogonal = [start[0], start[1] + (1 if start[1] < end[1] else -1)]

        # Now check diagonal, which is a matter of selecting the diagonal one step both ways in the direction
        # from start to end.
        diagonal = [orthogonal[0] + (1 if start[0] < end[0] else -1),
                    orthogonal[1] + (1 if start[1] < end[1] else -1)]

        if self._game.get_space(orthogonal) is not None or self._game.get_space(diagonal) is not None:
            return False

        return True
