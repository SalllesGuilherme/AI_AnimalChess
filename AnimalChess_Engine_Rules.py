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
from copy import deepcopy

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
            ["bM", "--", "bO", "--", "bW", "--", "bE"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["rE", "--", "rW", "--", "rO", "--", "rM"],
            ["--", "rC", "--", "--", "--", "rD", "--"],
            ["rT", "--", "--", "--", "--", "--", "rL"]]

        # self.board = [
        #      ["--", "--", "--", "--", "--", "--", "--"],
        #      ["--", "--", "--", "--", "--", "rL", "--"],
        #      ["--", "--", "--", "--", "--", "--", "--"],
        #      ["--", "--", "--", "--", "--", "--", "--"],
        #      ["--", "--", "--", "--", "--", "--", "--"],
        #      ["--", "--", "--", "--", "--", "--", "--"],
        #      ["--", "--", "--", "bT", "--", "--", "--"],
        #      ["--", "--", "--", "--", "--", "--", "--"],
        #      ["--", "--", "--", "--", "--", "--", "--"]]

        # self.board = [
        #     ["bD", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "rC", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--"]]

        self.moveFunctions = {"M": self.getRatMoves, "L": self.getJumpMoves,"T": self.getJumpMoves,
                              "E": self.getNormalMoves, "O": self.getNormalMoves,"D": self.getNormalMoves,
                              "W": self.getNormalMoves, "C": self.getNormalMoves}

        self.animal_strengths = {"M": 1, "L": 7, "T": 6, "E": 8, "O": 5,"D": 4, "W": 3, "C": 2}
        self.red_to_move = True
        self.move_log = []
        self.red_trap_locations = [(7,3), (8,2), (8, 4)]
        self.black_trap_locations = [(1,3), (0,2), (0, 4)]
        self.den_invaded = False
        self.draw = False
        #self.isTerminal = False


    def makeMove(self, move):

        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.red_to_move = not self.red_to_move  # switch players


    def undoMove(self):

        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.red_to_move = not self.red_to_move  # swap players
            self.den_invaded = False
            self.draw = False

    ### Simulate move on MTSC
    def takeAction(self, move):
        newState = deepcopy(self)
        newState.board[move.start_row][move.start_col] = "--"
        newState.board[move.end_row][move.end_col] = move.piece_moved
        newState.red_to_move = not self.red_to_move  # switch players
        return newState

    def getReward(self):
        if self.board[0][3][0] == "r" or self.board[8][3][0] == "b":
            return True
        else:
            return False

    def isTerminal(self):
        moves = []
        moves = self.getAllPossibleMoves()
        if self.board[0][3][0] == "r" or self.board[8][3][0] == "b":
            return True
        elif len(moves) == 0:
            return True
        else:
            return False

    def getCurrentPlayer(self):
        return (2 -self.red_to_move)
    ###

    def getValidMoves(self):
        """
        All valid moves.
        """
        #moves = []
        moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            print("No moves?")
        else:
            self.den_invaded = False
            self.draw = False

        return moves

    def getAllPossibleMoves(self):

        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "r" and self.red_to_move) or (turn == "b" and not self.red_to_move):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)  # calls appropriate move function based on piece type
        return moves


    def inWater(self,row,col):
        if row in [3, 4, 5]:
            if col in [1, 2, 4, 5]:
                return True
        return False

    def jumpConditions(self,row,col,end_row,end_col,jump_row,jump_col,enemy_color):

        if jump_row != 0 and self.board[end_row + (3 * jump_row)][end_col][0] in ['-',enemy_color]:
            if  self.board[end_row + (2 * jump_row)][end_col][1] not in ['M'] and self.board[end_row + (1 * jump_row)][end_col][1] not in ['M']: #No Mouse on the way
                if self.board[end_row + (3 * jump_row)][end_col][0] in ['-']: #Available space
                    return True
                elif self.canAttack(row,col,end_row + (3 * jump_row) ,end_col): #Enemy check on end square jump
                    return True

        elif jump_col != 0 and self.board[end_row][end_col + (2 * jump_col)][0] in ['-',enemy_color]:
            if self.board[end_row][end_col++ (1 * jump_col)][1] not in ['M']:    #No Mouse on the way
                if self.board[end_row][end_col + (2 * jump_col)][0] in ['-']:    #Available space
                    return True
                elif self.canAttack(row, col, end_row , end_col+ (2 * jump_col)): #Enemy check on end square jump
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
            self.den_invaded = True
            #self.isTerminal = True
            return True
        else:
            return False




    def canAttack(self, own_row, own_col, row_end, col_end):
        """
        Determines if player can attack opponent's piece

        Args:
            own_row (int): Player's piece row
            own_col (int): Player's piece column
            row_end (int): Opponent's piece row
            col_end (int): Opponent's piece column

        Returns:
            boolean: Returns 'True' if it's possible to attack the opponent's piece or 'False' if it's an invalid move.
        """
        own_piece = self.board[own_row][own_col]
        target_piece = self.board[row_end][col_end]
        # Traps attacks and protection
        if target_piece[0] == 'r' and (row_end,col_end) in self.red_trap_locations:  # red player protected by own traps
            return False
        if target_piece[0] == 'b' and (row_end,col_end) in self.black_trap_locations:  # black player protected by own traps
            return False
        if target_piece[0] == 'b' and (row_end,col_end) in self.red_trap_locations:  # black player vulnerable by enemy traps
            return True
        if target_piece[0] == 'r' and (row_end,col_end) in self.black_trap_locations:  # red player vulnerable by enemy traps
            return True
        # Elephant cannot attack rat
        if own_piece[1] == 'E' and target_piece[1] == 'M':
            return False
        # Rat attacks
        if own_piece[1] == 'M':
            if self.inWater(own_row, own_col) and self.inWater(row_end, col_end):  # Rat can attack another rat in the water
                return True
            elif self.inWater(own_row, own_col) and not self.inWater(row_end, col_end):  # Rat cannot attack from inside the water
                return False
            elif not self.inWater(own_row, own_col) and self.inWater(row_end, col_end):  # Rat cannot attack target inside the water from land
                return False
            elif target_piece[1] == 'E':  # Regular rat attack against elephant
                return True
            elif self.animal_strengths[target_piece[1]] <= self.animal_strengths[own_piece[1]]:
                return True
        # Regular animal battle
        elif self.animal_strengths[target_piece[1]] <= self.animal_strengths[own_piece[1]]:
            return True


    def getRatMoves(self, row, col, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.red_to_move else "r"
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
        enemy_color = "b" if self.red_to_move else "r"
        for direction in directions:
            for i in range(1, 2):
                end_row = row + direction[0] * 1
                end_col = col + direction[1] * 1
                if 0 <= end_row <= 8 and 0 <= end_col <= 6:  # check for possible moves only in boundaries of the board
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--" and not self.inWater(end_row,end_col) and self.moveNotOwnDen(end_row,end_col,enemy_color):  # empty space is valid and Not in Water
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    elif end_piece[0] == enemy_color  and not self.inWater(end_row,end_col) and self.canAttack(row, col, end_row, end_col):  # capture enemy piece, if the enemy is weaker or trapped
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off board
                    break

    def getJumpMoves(self, row, col, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.red_to_move else "r"
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

                        if jump_row != 0 and self.jumpConditions(row,col,end_row,end_col,jump_row,jump_col,enemy_color):
                            moves.append(Move((row, col), (end_row+(3*jump_row), end_col), self.board))

                        elif jump_col != 0 and self.jumpConditions(row,col,end_row,end_col,jump_row,jump_col,enemy_color):
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

    def __init__(self, start_square, end_square, board):
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

    ##HASH for moves on mcst
    def __hash__(self):
        return hash((self.getChessNotation()))

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

        end_square = self.getRankFile(self.end_row, self.end_col)
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square