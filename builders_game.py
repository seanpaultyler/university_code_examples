# Author: Sean Tyler
# Date: 12/01/2020
# Description:  A class for a "builder game".

class BuildersGame:
    """A class for a builder's game, where each player takes turns moving one of two of their builders around a 5x5
    board.  Each player must move a builder into an adjacent square that is within 1 level of their current square,
    and then add a level to an adjacent surrounding square up to a max of 4.  The game ends when one player places
    a builder upon a 3 or higher square, or the opposing player cannot make any valid moves.

    Attributes
    ----------
    _board (list of list of int):
        5x5 list of lists to represent the game board.  Columns and rows range from 0 to 4

    _current_state (string):
        Can be one of three - UNFINISHED, X_WON, O_WON

    _turn (bool):
        True for player 1, false for player 2.

    _player_1_xy
    _player_2_xy (list[[int, int], [int, int]]):
        x,y coordinate of both builders [xy, xy]

    Methods
    -------
    get_current_state (string):
        Returns one of three strings representing the state of the game: UNFINISHED, X_WON, O_WON

    initial_placement (int, int, int, int, string):
        Places each player's builders on the board.

            int: x coordinate of builder 1
            int: y coordinate of builder 1
            int: x coordinate of builder 2
            int: y coordinate of builder 2
            string: player that is placing builders, either 'x' or 'o'

    make_move (int, int, int, int, int, int):
        Commits the player's move on the board.

            int: x coordinate of builder to be moved
            int: y coordinate of builder to be moved
            int: x coordinate of where builder should be moved to
            int: y coordinate of where builder should be moved to
            int: x coordinate of square that should be added to by builder
            int: y coordinate of square that should be added to by builder

    get_cell (list[int, int]):
        Returns the value of a cell, representing the height of the "tower" built there.

            list[int, int]: x,y coordinate of cell to return value of.

    get_row (int):
        Returns the values of the cells in an entire row.

            int: row number to return values for.

    get_col (int):
        Returns the values of the cells in an entire column.

            int: column number to return values for.

    build_pos (list[int, int]):
        Returns a string indicating which builder occupies the provided square.

            list[int, int]: x,y coordinates of cell to check for builders.  Returns which builder occupies the square.
    """
    def __init__(self):
        """Constructs the BuildersGame class."""
        self._board = [None] * 5
        # A 5 length list of lists length 5, to create a 5x5 board.
        for column in range(5):
            self._board[column] = [0] * 5
        self._current_state = "UNFINISHED"
        self._turn = True
        # Initial builder coordinates are set out of bounds so that we can check for initial placement later.
        self._player_1_xy = [[-1, -1], [-1, -1]]
        self._player_2_xy = [[-1, -1], [-1, -1]]

    def get_current_state(self):
        """Returns the current game state"""
        return self._current_state

    def initial_placement(self, builder_1_x, builder_1_y, builder_2_x, builder_2_y, player):
        """Commits the initial builder placement for both players."""

        # Make sure placement is on the board.
        if 0 <= builder_1_x <= 4 and 0 <= builder_1_y <= 4 and 0 <= builder_2_x <= 4 and 0 <= builder_2_y <= 4:

            # Make sure builders aren't placed on the same spot
            if builder_1_x != builder_2_x or builder_1_y != builder_2_y:

                # Make sure each player is placing their own builders.
                if self._turn and player == 'x' or not self._turn and player == 'o':

                    # Make sure the chosen spots are vacant.
                    if self.__check_vacant([builder_1_x, builder_1_y]) and self.__check_vacant([builder_2_x, builder_2_y]):

                        # Make sure the player hasn't already placed their own builders.
                        if self._turn and self._player_1_xy == [[-1, -1], [-1, -1]]:

                            # Commit the placements and switch turns.
                            self._player_1_xy = [[builder_1_x, builder_1_y], [builder_2_x, builder_2_y]]
                            self._turn = not self._turn
                            return True

                        elif not self._turn and self._player_2_xy == [[-1, -1], [-1, -1]]:

                            # Commit the placements and switch turns.
                            self._player_2_xy = [[builder_1_x, builder_1_y], [builder_2_x, builder_2_y]]
                            self._turn = not self._turn
                            return True
        return False

    def make_move(self, col_init, row_init, col_destination, row_destination, col_build, row_build):
        """Makes the move for the player.  Returns false if a valid move is not made.  If no valid moves can
        be made, ends the game in the other player's favor.
        """
        # Make sure the current player can even make a valid move

        # Set pertinent variables for relevant function calls.
        xy_init = [col_init, row_init]
        xy_destination = [col_destination, row_destination]
        xy_build = [col_build, row_build]

        # Check that the game hasn't ended, that players have made initial builder placements, and that the
        # correct player is moving according to whose turn it is.
        if self._current_state == "UNFINISHED" and self.__check_initial_placement() and self.__check_turn(xy_init):

            # Check that the destination square is vacant and that it's a valid movement.
            if self.__check_vacant(xy_destination) and self.__check_valid_move(xy_init, xy_destination, xy_build):

                # Commit the valid moves.
                self.__move_builder(xy_init, xy_destination)
                self.__build_cell(xy_build)

                # Check for winning conditions. (Builder on 3 or higher tower or other player has no moves.)
                if self.__check_height(xy_destination):

                    if self._turn:
                        self._current_state = "X_WON"
                    else:
                        self._current_state = "O_WON"

                else:

                    if self._turn:
                        if not self.__check_for_valid_moves(1):
                            self._current_state = "X_WON"
                    else:
                        if not self.__check_for_valid_moves(0):
                            self._current_state = "O_WON"

                # Switch which player's turn it is.
                self._turn = not self._turn
                return True

        # Invalid move returns false without switching turns.
        return False

    def __check_turn(self, builder):
        """Returns false if a player is not moving their own builder or no builder at all"""
        if self._turn:

            if builder == self._player_1_xy[0] or builder == self._player_1_xy[1]:
                return True

        else:

            if builder == self._player_2_xy[0] or builder == self._player_2_xy[1]:
                return True

        return False

    def __move_builder(self, xy_init, xy_destination):
        """Moves the selected builder to the destination spot"""
        # Match the given coordinates to the builder, then move that builder.
        for builder in range(2):

            if (self._player_1_xy[builder]) == xy_init:
                self._player_1_xy[builder] = xy_destination

            if (self._player_2_xy[builder]) == xy_init:
                self._player_2_xy[builder] = xy_destination

    def __check_initial_placement(self):
        """Makes sure initial placement has happened."""
        # Check that each player's builders have diff coordinates than initial -1, -1
        if self._player_1_xy[0] == [-1, -1] or self._player_1_xy[1] == [-1, -1]:
            return False

        if self._player_2_xy[0] == [-1, -1] or self._player_2_xy[1] == [-1, -1]:
            return False

        return True

    def __build_cell(self, xy_coord):
        """ "Builds" a tower at the selected cell (adds 1 to the cell's value)"""
        self._board[xy_coord[1]][xy_coord[0]] += 1

    def __check_build(self, xy_coord_init, xy_coord_builder, xy_coord):
        """Checks to see if a tower can be constructed and is within builder range."""

        # Make sure tower isn't at max height and that the square is vacant (exception: If the builder
        # that is about to move occupies the build square, that's valid.)
        if self.get_cell(xy_coord) < 4 and (self.__check_vacant(xy_coord) or xy_coord_init == xy_coord):

            if abs(xy_coord[0] - xy_coord_builder[0]) <= 1 and abs(xy_coord[1] - xy_coord_builder[1]) <= 1:

                # Can't build on own square
                if xy_coord_builder != xy_coord:

                    return True

        return False

    def __check_vacant(self, xy_coord):
        """Checks that a cell a player is moving a builder to is vacant.  Returns True if
        vacant, False if occupied."""
        # If either of the players' builders is a cell, return False (not vacant)
        for i in range(2):
            if xy_coord == self._player_1_xy[i] or xy_coord == self._player_2_xy[i]:
                return False
        return True

    def __check_for_valid_moves(self, player):
        """Checks adjacent spaces for valid moves.  If none, the other player wins."""
        # Iterate over all 8 spaces around a builder for a spot to move to, then all 8 spaces around the destination for
        # a build spot. Then plug all of that into the check_valid_moves func to see if a player can make a move.
        # If no spaces return valid, they lose.
        
        # Check moves around first builder, then second builder.
        for build in range(2):

            for x_offset in range(-1, 2):

                for y_offset in range(-1, 2):

                    # The cell we're already in isn't a valid space to move to, so skip.
                    if x_offset == 0 and y_offset == 0:
                        continue

                    if player == 0:
                        destination = [self._player_1_xy[build][0] + x_offset, self._player_1_xy[build][1] + y_offset]
                    else:
                        destination = [self._player_2_xy[build][0] + x_offset, self._player_2_xy[build][1] + y_offset]

                    # If out of bounds, ignore checking for moves.
                    if not 0 <= destination[0] <= 4 or not 0 <= destination[1] <= 4:
                        continue

                    # Now check valid build spaces
                    for destination_x_offset in range(-1, 2):

                        for destination_y_offset in range(-1, 2):

                            # OUr destination space isn't a valid build space, so skip.
                            if destination_x_offset == 0 and destination_y_offset == 0:
                                continue

                            build_cell = [destination[0] + destination_x_offset, destination[1] + destination_y_offset]

                            # Can't build out of bounds.
                            if not 0 <= build_cell[0] <= 4 or not 0 <= build_cell[1] <= 4:
                                continue

                            # Plug into the valid move func and see if the cell works.
                            if player == 0:
                                if self.__check_valid_move(self._player_1_xy[build], destination, build_cell):
                                    return True
                            else:
                                if self.__check_valid_move(self._player_2_xy[build], destination, build_cell):
                                    return True
        # No valid moves found
        return False

    def __check_valid_move(self, xy_coord_init, xy_coord_destination, xy_build):
        """Returns true if a builder can be moved from its spot to another spot.  False
        if any of the prohibiting rules blocks the movement.
        """

        # Make sure all move values are on the board.
        for i in range(2):

            if xy_coord_init[i] > 4 or xy_coord_init[i] < 0:
                return False
            if xy_coord_destination[i] > 4 or xy_coord_destination[i] < 0:
                return False
            if xy_build[i] > 4 or xy_build[i] < 0:
                return False

        # Check if the height difference permits the move.  Can't move onto towers 2 or more units in height diff.
        if abs(self.get_cell(xy_coord_init) - self.get_cell(xy_coord_destination)) < 2:

            # Check if the move is within one unit x and y in any direction.
            if abs(xy_coord_init[0] - xy_coord_destination[0]) <= 1:

                if abs(xy_coord_init[1] - xy_coord_destination[1]) <= 1:

                    # Check that a tower can be constructed.
                    if self.__check_build(xy_coord_init, xy_coord_destination, xy_build):
                        return True

        return False

    def __check_height(self, xy_coord):
        """Checks the height of the tower the builder moved to.  If >2, that player wins."""
        if self.get_cell(xy_coord) > 2:
            return True

        return False

    def get_cell(self, xy_coord):
        """Returns the "height" of the cell (int)"""
        return self._board[xy_coord[1]][xy_coord[0]]

    def get_row(self, row_num):
        """Returns the "height" of and entire row's cells.  For printing purposes."""
        lst = list()
        for i in range(len(self._board)):
            lst.append(self._board[i][row_num])
        return lst

    def get_column(self, col_num):
        """Returns the "height" of an entire column's cells.  For printing purposes."""
        lst = list()
        for i in range(len(self._board)):
            lst.append(self._board[col_num][i])
        return lst

    def build_pos(self, cell):
        """If a builder is in a cell, returns a string specifying which builder. For printing purposes."""
        for i in range(2):
            if self._player_1_xy[i] == cell:
                return "X" + str(i)
            if self._player_2_xy[i] == cell:
                return "O" + str(i)
        return "  "
