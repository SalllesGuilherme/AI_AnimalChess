"""
FEUP - Faculty of Engineering of Porto
MASTER OF DATA SCIENCE AND ENGINEERING
Course: Artificial Inteligence
Professor: Luis Reis
Students: Danilo Brandão / Guilherme Salles
"""

"""
Storing all the information about the current state of chess game.
Determining valid moves at current state.
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
        self.animal_strengths = {"M": 1, "L": 7, "T": 6, "E": 8, "O": 5,"D": 3, "W": 4, "C": 2}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.red_trap_locations = [(7,3), (8,2), (8, 4)]
        self.black_trap_locations = [(1,3), (0,2), (0, 4)]
        self.checkmate = False
        self.den_invaded = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []


    def makeMove(self, move):

        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players


    def undoMove(self):

        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # swap players
            self.checkmate = False
            self.stalemate = False



    def getValidMoves(self):
        """
        All valid moves.
        """
        moves = []

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

    def moveNotOwnDen(self,row_end,col_end,enemy_color):
        if enemy_color == 'b' and row_end == 8 and col_end == 3:
            return False
        elif enemy_color == 'r' and row_end == 0 and col_end == 3:
            return False
        else:
            return True

    def enemyConquerDen(self):
        if self.board[0][3][0] == "r" or self.board[8][3][0] == "b":
            return True
        else:
            return False

#delete
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
                    elif end_piece[0] == enemy_color and self.canAttack(row, col, end_row, end_col):  # capture enemy piece, if the enemy is weaker or trapped
                        moves.append(Move((row, col), (end_row, end_col), self.board))
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
                    elif end_piece[0] == enemy_color and self.canAttack(row, col, end_row, end_col):  # capture enemy piece, if the enemy is weaker or trapped
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

                    elif end_piece[0] == enemy_color and not self.inWater(end_row,end_col) and self.canAttack(row, col, end_row, end_col):  # capture enemy piece
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


        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square