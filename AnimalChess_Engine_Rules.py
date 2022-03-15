"""
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
"""


class GameState:
    def __init__(self):
        """
        Board is an 9x7 2d list, each element in list has 2 characters.
        The first character represents the color of the piece: 'b' or 'r'.
        The second character represents the type of the piece: 'M', 'L', 'T', 'E', 'O', 'D','T','L.
        "--" represents an empty space with no piece.
        """
        self.board = [
            ["bL", "--", "--", "--", "--", "--", "bT"],
            ["--", "bD", "--", "--", "--", "bC", "--"],
            ["bM", "--", "bO", "--", "bW", "bL", "bE"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["rE", "rT", "rW", "--", "rO", "--", "rM"],
            ["--", "rC", "--", "--", "--", "rD", "--"],
            ["rT", "--", "--", "--", "--", "--", "rL"]]

        self.moveFunctions = {"M": self.getRatMoves, "L": self.getJumpMoves,"T": self.getJumpMoves,
                              "E": self.getNormalMoves, "O": self.getNormalMoves,"D": self.getNormalMoves,
                              "W": self.getNormalMoves, "C": self.getNormalMoves}

        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.den_invaded = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        # self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
        # self.enpassant_possible_log = [self.enpassant_possible]


    def makeMove(self, move):
        """
        Takes a Move as a parameter and executes it.
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players

        # # update king's location if moved
        # if move.piece_moved == "wK":
        #     self.white_king_location = (move.end_row, move.end_col)
        # elif move.piece_moved == "bK":
        #     self.black_king_location = (move.end_row, move.end_col)


    def undoMove(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # swap players

            # update the king's position if needed
            # if move.piece_moved == "wK":
            #     self.white_king_location = (move.start_row, move.start_col)
            # elif move.piece_moved == "bK":
            #     self.black_king_location = (move.start_row, move.start_col)

            self.checkmate = False
            self.stalemate = False



    def getValidMoves(self):
        """
        All moves considering checks.
        """
        # advanced algorithm
        moves = []
        #self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

        # if self.white_to_move:
        #     king_row = self.white_king_location[0]
        #     king_col = self.white_king_location[1]
        # else:
        #     king_row = self.black_king_location[0]
        #     king_col = self.black_king_location[1]
        # if self.in_check:
        #     if len(self.checks) == 1:  # only 1 check, block the check or move the king
        #         moves = self.getAllPossibleMoves()
        #         # to block the check you must put a piece into one of the squares between the enemy piece and your king
        #         check = self.checks[0]  # check information
        #         check_row = check[0]
        #         check_col = check[1]
        #         piece_checking = self.board[check_row][check_col]
        #         valid_squares = []  # squares that pieces can move to
        #         # if knight, must capture the knight or move your king, other pieces can be blocked
        #         if piece_checking[1] == "N":
        #             valid_squares = [(check_row, check_col)]
        #         else:
        #             for i in range(1, 8):
        #                 valid_square = (king_row + check[2] * i,
        #                                 king_col + check[3] * i)  # check[2] and check[3] are the check directions
        #                 valid_squares.append(valid_square)
        #                 if valid_square[0] == check_row and valid_square[
        #                     1] == check_col:  # once you get to piece and check
        #                     break
        #         # get rid of any moves that don't block check or move king
        #         for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
        #             if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
        #                 if not (moves[i].end_row,
        #                         moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
        #                     moves.remove(moves[i])
        #     else:  # double check, king has to move
        #         self.getKingMoves(king_row, king_col, moves)
        # else:  # not in check - all moves are fine
        moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            self.den_invaded = True
            # if self.inCheck():
            #     self.checkmate = True
            # else:
            #     # TODO stalemate on repeated moves
            #     print('Empate?')
            #     #self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        if self.enemyConquerDen():
            self.den_invaded=True
        else:
            self.den_invaded=False

        return moves

    def inCheck(self):  ###inTrapp inWater
        """
        Determine if a current player is in check
        """
        if self.white_to_move:
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])

    def inWater(self,row,col):
        if row in [3, 4, 5]:
            if col in [1, 2, 4, 5]:
                return True
        return False

    def jumpConditions(self,end_row,end_col,jump_row,jump_col,enemy_color):

        if jump_row != 0 and self.board[end_row + (3 * jump_row)][end_col][0] in ['-',enemy_color]:
            if  self.board[end_row + (2 * jump_row)][end_col][1] not in ['M'] and self.board[end_row + (1 * jump_row)][end_col][1] not in ['M'] :
                return True

        elif jump_col != 0 and self.board[end_row][end_col + (2 * jump_col)][0] in ['-',enemy_color]:
            if self.board[end_row][end_col++ (1 * jump_col)][1] not in ['M']:
                return True

        else:
            return False

    def moveNotOwnDen(self,rol_end,col_end,enemy_color):
        if enemy_color == 'b' and rol_end == 8 and col_end == 3:
            return False
        elif enemy_color == 'r' and rol_end == 0 and col_end == 3:
            return False
        else:
            return True

    def enemyConquerDen(self):
        if self.board[0][3][0] == "r" or self.board[8][3][0] == "b":
            return True
        else:
            return False

    def AnimalProtectedOwnTrap(self,rol_end,col_end,enemy_color):
        if enemy_color == 'r' and rol_end == 8 and col_end in [2,4]:
            return True
        elif enemy_color == 'r' and rol_end == 7 and col_end == 3:
            return True
        elif enemy_color == 'b' and rol_end == 0 and col_end in [2,4]:
            return True
        elif enemy_color == 'b' and rol_end == 1 and col_end == 3:
            return True
        else:
            return False


    def squareUnderAttack(self, row, col):
        """
        Determine if enemy can attack the square row col
        """
        self.white_to_move = not self.white_to_move  # switch to opponent's point of view
        opponents_moves = self.getAllPossibleMoves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:  # square is under attack
                return True
        return False

    def getAllPossibleMoves(self):
        """
        All moves without considering checks.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "r" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)  # calls appropriate move function based on piece type
        return moves


    def getRatMoves(self, row, col, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.white_to_move else "r"
        for direction in directions:
            for i in range(1, 2):
                end_row = row + direction[0] * 1
                end_col = col + direction[1] * 1
                if 0 <= end_row <= 8 and 0 <= end_col <= 6:  # check for possible moves only in boundaries of the board
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--" and self.moveNotOwnDen(end_row,end_col,enemy_color):  # empty space is valid and not own DEN
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    elif end_piece[0] == enemy_color and not self.inWater(row,col) and end_piece[1] == 'E':  # capture enemy piece, if the rat is not in the water
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    elif end_piece[0] == enemy_color and end_piece[1] == 'M' and not self.AnimalProtectedOwnTrap(end_row,end_col,enemy_color):  # capture Rat enemy, if the rat is not in the water
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off board
                    break

    def getNormalMoves(self, row, col, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.white_to_move else "r"
        for direction in directions:
            for i in range(1, 2):
                end_row = row + direction[0] * 1
                end_col = col + direction[1] * 1
                if 0 <= end_row <= 8 and 0 <= end_col <= 6:  # check for possible moves only in boundaries of the board
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--" and not self.inWater(end_row,end_col) and self.moveNotOwnDen(end_row,end_col,enemy_color):  # empty space is valid and Not in Water
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    elif end_piece[0] == enemy_color and not self.inWater(end_row,end_col) and not self.AnimalProtectedOwnTrap(end_row,end_col,enemy_color):  # capture enemy piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off board
                    break

    def getJumpMoves(self, row, col, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.white_to_move else "r"
        for direction in directions:
            for i in range(1, 2):
                end_row = row + direction[0] * 1
                end_col = col + direction[1] * 1
                if 0 <= end_row <= 8 and 0 <= end_col <= 6:  # check for possible moves only in boundaries of the board
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--" and not self.inWater(end_row,end_col) and self.moveNotOwnDen(end_row,end_col,enemy_color):  # empty space is valid and Not in Water
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    elif end_piece == "--" and self.inWater(end_row,end_col):
                        jump_row = end_row - row  #Vertical jump
                        jump_col = end_col - col  #Horizontal jump

                        if jump_row != 0 and self.jumpConditions(end_row,end_col,jump_row,jump_col,enemy_color):
                            moves.append(Move((row, col), (end_row+(3*jump_row), end_col), self.board))

                        elif jump_col != 0 and self.jumpConditions(end_row,end_col,jump_row,jump_col,enemy_color):
                            moves.append(Move((row, col), (end_row, end_col+(2*jump_col)), self.board))

                    elif end_piece[0] == enemy_color and not self.inWater(end_row,end_col) and not self.AnimalProtectedOwnTrap(end_row,end_col,enemy_color):  # capture enemy piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off board
                    break



class Move:
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is corresponding to rows)
    # and the second one being a letter between a-f (corresponding to columns), in order to use this notation we need to map our [row][col] coordinates
    # to match the ones used in the original chess game
    ranks_to_rows = {"9":8, "8": 7, "7": 6, "6": 5, "5": 4,
                     "4": 3, "3": 2, "2": 1, "1": 0}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        self.is_capture = self.piece_captured != "--"
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):

        if self.piece_captured != "--":
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                    self.end_col)
            else:
                return self.piece_moved[1] + "x" + self.getRankFile(self.end_row, self.end_col)
        else:
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.end_row, self.end_col)
            else:
                return self.piece_moved[1] + self.getRankFile(self.end_row, self.end_col)


    def getRankFile(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __str__(self):
        # if self.is_castle_move:
        #     return "0-0" if self.end_col == 6 else "0-0-0"

        end_square = self.getRankFile(self.end_row, self.end_col)

        if self.piece_moved[1] == "p":
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square

        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square