"""
FEUP - Faculty of Engineering of Porto
MASTER OF DATA SCIENCE AND ENGINEERING
Course: Artificial Inteligence
Professor: Luis Reis
Students: Danilo Brandão / Guilherme Salles
"""


"""
Library for generate the AI moves
"""

import random

piece_score = {"E": 100, "M": 80, "L": 100, "T": 80, "O": 50, "W": 40,"D": 30,"C": 20}

mouse_score = [[11, 13, 50, 10000, 50, 13, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 11, 13, 13, 13],
                [8, 9, 9, 11,12, 12, 13],
                [8, 8, 8, 9, 12, 12, 12],
                [8, 8, 8, 9, 10, 12, 11],
                [8, 8, 8, 9, 10, 10, 10],
                [8, 8, 8, 9, 9, 9, 9],
                [8, 8, 8, 0, 8, 8, 8]]

cat_score = [[11, 15, 50, 10000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

wolf_score = [[11, 15, 50, 10000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

dog_score = [[11, 15, 50, 10000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

leopard_score = [[11, 15, 50, 10000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

tiger_score = [[25, 30, 150, 10000, 150, 30, 25],
                [25, 25, 30, 150, 30, 25, 25],
                [18, 20, 20, 30, 20, 20, 18],
                [8, 0, 0, 15,0, 0, 15],
                [8, 0, 0, 15, 0, 0, 12],
                [8, 0, 0, 15, 0, 0, 11],
                [8, 8, 8, 9, 16, 16, 14],
                [14, 12, 12, 12, 12, 12, 12],
                [5, 12, 12, 0, 12, 12, 5]]

lion_score = [[25, 30, 150, 10000, 150, 30, 25],
                [25, 25, 30, 150, 30, 25, 25],
                [18, 20, 20, 30, 20, 20, 18],
                [8, 0, 0, 15,0, 0, 15],
                [8, 0, 0, 15, 0, 0, 12],
                [8, 0, 0, 15, 0, 0, 11],
                [8, 8, 8, 9, 16, 16, 14],
                [12, 12, 12, 12, 12, 12, 14],
                [5, 12, 12, 0, 12, 12, 5]]

elephant_score = [[25, 30, 100, 10000, 100, 30, 25],
                [25, 25, 30, 100, 30, 25, 25],
                [18, 20, 20, 30, 20, 20, 18],
                [16, 0, 0, 15,0, 0, 16],
                [14, 0, 0, 15, 0, 0, 14],
                [12, 0, 0, 15, 0, 0, 12],
                [10, 15, 14, 14, 14, 14, 12],
                [11, 11, 11, 11, 11, 11, 11],
                [11, 11, 11, 0, 11, 11, 11]]

pieces = ['bT','bE','bC','bW','bO','bD','bM','bL','rT','rE','rC','rW','rO','rD','rM','rL','trap','den','grass','water']

piece_position_scores = {"rM": mouse_score,
                         "bM": mouse_score[::-1],
                         "rC": cat_score,
                         "bC": cat_score[::-1],
                         "rW": wolf_score,
                         "bW": wolf_score[::-1],
                         "rD": dog_score,
                         "bD": dog_score[::-1],
                         "rO": leopard_score,
                         "bO": leopard_score[::-1],
                         "rT": tiger_score,
                         "bT": tiger_score[::-1],
                         "rL": lion_score,
                         "bL": lion_score[::-1],
                         "rE": elephant_score,
                         "bE": elephant_score[::-1]
                         }



DEN_CONQUESTED=10000
DRAW=0
DEPTH=4

def findRandomMove(valid_moves):
    return valid_moves[random.randint(0,len(valid_moves)-1)]


def findBestMove(game_state, valid_moves):
    turnMultiplier = 1 if game_state.white_to_move else -1
    maxScore = -DEN_CONQUESTED
    bestMove = None

    for playerMove in valid_moves:
        game_state.makeMove(playerMove)
        score = turnMultiplier * scoreMaterial(game_state.board)

        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        game_state.undoMove()

    return bestMove


def scoreMaterial(game_state):
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "r":
                    score += piece_score[piece[1]] + piece_position_score
                elif piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

            # if square[0] == 'r':
            #     score = score + piece_score[square[1]] + piece_position_score
            # elif square[0] == 'b':
            #     score = score - piece_score[square[1]] + piece_position_score

    return score

def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreMaterial(game_state)
    # move ordering - implement later
    max_score = -DEN_CONQUESTED
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

def findBestMove_AlphaBeta(game_state, valid_moves):
    global next_move
    next_move = None

    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -DEN_CONQUESTED, DEN_CONQUESTED,1 if game_state.white_to_move else -1)

    return next_move



