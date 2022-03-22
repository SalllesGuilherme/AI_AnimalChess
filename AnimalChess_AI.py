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
from math import inf
import collections

piece_score = {"E": 120, "M": 100, "L": 120, "T": 100, "O": 80, "W": 60,"D": 70,"C": 50}

mouse_score = [[11, 25, 50, 100000, 50, 25, 13],
                [11, 20, 25, 50, 25, 20, 13],
                [10, 15, 20, 20, 20, 15, 13],
                [8, 9, 9, 11,12, 13, 13],
                [8, 8, 8, 9, 11, 12, 12],
                [8, 8, 8, 9, 11, 12, 11],
                [8, 8, 8, 9, 10, 10, 10],
                [8, 8, 8, 9, 9, 9, 9],
                [8, 8, 8, 0, 8, 8, 8]]

cat_score = [[11, 15, 50, 100000, 50, 15, 11],
                [12, 12, 20, 50, 20, 15, 12],
                [14, 15, 20, 20, 20, 14, 14],
                [13, 14, 14, 13,0, 14, 13],
                [12, 0, 0, 12, 0, 0, 12],
                [11, 0, 0, 11, 0, 0, 11],
                [10, 0, 0, 10, 0, 0, 10],
                [8, 8, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

wolf_score = [[11, 15, 50, 100000, 50, 15, 11],
                [12, 12, 20, 50, 20, 15, 12],
                [14, 15, 20, 20, 20, 14, 14],
                [13, 0, 0, 13,0, 0, 13],
                [12, 0, 0, 12, 0, 0, 12],
                [11, 0, 0, 11, 0, 0, 11],
                [10, 10, 10, 11, 10, 10, 10],
                [8, 8, 9, 10, 9, 8, 8],
                [8, 8, 10, 0, 10, 8, 8]]

dog_score = [[11, 15, 50, 100000, 50, 15, 11],
                [12, 12, 20, 50, 20, 15, 12],
                [14, 15, 20, 20, 20, 14, 14],
                [13, 0, 0, 13,0, 0, 13],
                [12, 0, 0, 12, 0, 0, 12],
                [11, 0, 0, 11, 0, 0, 11],
                [10, 10, 10, 11, 10, 10, 10],
                [8, 8, 9, 10, 9, 8, 8],
                [8, 8, 10, 0, 10, 8, 8]]

leopard_score = [[11, 15, 50, 100000, 50, 15, 11],
                [12, 12, 20, 50, 20, 15, 12],
                [14, 15, 20, 20, 20, 14, 14],
                [13, 0, 0, 13,0, 0, 13],
                [12, 0, 0, 12, 0, 0, 12],
                [11, 0, 0, 11, 0, 0, 11],
                [10, 10, 10, 11, 10, 10, 10],
                [8, 8, 9, 10, 9, 8, 8],
                [8, 8, 10, 0, 10, 8, 8]]

tiger_score = [[20, 40, 150, 100000, 150, 40, 20],
                [20, 25, 40, 150, 40, 25, 20],
                [18, 30, 30, 20, 30, 30, 18],
                [15, 0, 0, 15,0, 0, 15],
                [12, 0, 0, 15, 0, 0, 12],
                [11, 0, 0, 15, 0, 0, 11],
                [14, 16, 16, 9, 16, 16, 14],
                [12, 12, 12, 12, 12, 12, 12],
                [5, 12, 12, 0, 12, 12, 5]]

lion_score = [[20, 40, 150, 100000, 150, 40, 20],
                [20, 25, 40, 150, 40, 25, 20],
                [18, 30, 30, 20, 30, 30, 18],
                [15, 0, 0, 15,0, 0, 15],
                [12, 0, 0, 15, 0, 0, 12],
                [11, 0, 0, 15, 0, 0, 11],
                [14, 16, 16, 9, 16, 16, 14],
                [12, 12, 12, 12, 12, 12, 12],
                [5, 12, 12, 0, 12, 12, 5]]

elephant_score = [[20, 40, 150, 100000, 150, 40, 20],
                [20, 25, 40, 150, 40, 25, 20],
                [18, 30, 30, 20, 30, 30, 18],
                [15, 0, 0, 15,0, 0, 15],
                [12, 0, 0, 15, 0, 0, 12],
                [11, 0, 0, 15, 0, 0, 11],
                [14, 16, 16, 9, 16, 16, 14],
                [12, 12, 12, 12, 12, 12, 12],
                [5, 12, 12, 0, 12, 12, 5]]

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
global DEPTH #=4

def findRandomMove(valid_moves):
    return valid_moves[random.randint(0,len(valid_moves)-1)]


def find_GreadyMove(game_state, valid_moves):
    turnMultiplier = 1 if game_state.white_to_move else -1
    maxScore = -DEN_CONQUESTED
    bestMove = None

    for playerMove in valid_moves:
        game_state.makeMove(playerMove)
        score = turnMultiplier * scoreMaterial(game_state)
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        game_state.undoMove()

    return bestMove


def scoreMaterial(game_state):
    score = 0
    penalty_for_rep = 0

    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                piece_position_score = piece_position_scores[piece][row][col]
                if piece_position_scores[piece][row][col] in last_moves:
                    penalty_for_rep = 50
                if piece[0] == 'r':
                    score +=  piece_position_score + piece_score[piece[1]] - penalty_for_rep

                elif piece[0] == 'b':
                     score -=  piece_position_score + piece_score[piece[1]] - penalty_for_rep

    return score

def findMove_NegaMaxAlphaBeta(game_state, valid_moves, depth,DEPTH, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        #print(f"{turn_multiplier} move:{next_move}, depth:{depth},score:{turn_multiplier * scoreMaterial(game_state)},A B:{alpha,beta}")
        return turn_multiplier * scoreMaterial(game_state)

    max_score = -inf
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMove_NegaMaxAlphaBeta(game_state, next_moves, depth - 1,DEPTH, -beta, -alpha, -turn_multiplier)

        if score > max_score:   # > or >= ??
            max_score = score
            if depth == DEPTH:
                next_move = move
                #print("Move found")
        game_state.undoMove()
        if max_score > alpha:
             alpha = max_score
        if alpha >= beta:
            break
    return max_score


def findMove_MiniMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move

    def max_value(game_state,next_moves, alpha, beta,depth):
        if depth == 0:
            return turn_multiplier * scoreMaterial(game_state)
        v = -inf
        for move in valid_moves:
            next_moves = game_state.getValidMoves()
            v = max(v, min_value(game_state,next_moves, alpha, beta,depth - 1))
            game_state.undoMove()
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(game_state,next_moves, alpha, beta,depth):
        if depth == 0:
            return turn_multiplier * scoreMaterial(game_state)
        v = -inf
        for move in valid_moves:
            next_moves = game_state.getValidMoves()
            v = min(v, max_value(game_state,next_moves, alpha, beta,depth - 1))
            game_state.undoMove()
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -inf
    beta = inf
    best_action = None
    for move in valid_moves:
        v = min_value(game_state,valid_moves, best_score, beta,depth)
        if v > best_score:
            best_score = v
            best_action = move
    return best_action

def find_BestMove(game_state, valid_moves,depth_p):
    global next_move
    DEPTH= depth_p
    next_move = None
    global last_moves
    last_moves = collections.deque(maxlen=8)

    random.shuffle(valid_moves)
    ordered_valid_moves=orderby_GreadyMove(game_state, valid_moves)

    # for i in valid_moves:
    #     print(f"Possible: {i}")
    # for i in ordered_valid_moves:
    #     print(f"New possible: {i}")
    findMove_NegaMaxAlphaBeta(game_state, ordered_valid_moves,depth_p,DEPTH, -DEN_CONQUESTED, DEN_CONQUESTED,1 if game_state.red_to_move else -1)
    last_moves.append(next_move)

    return next_move


def orderby_GreadyMove(game_state, valid_moves):
    turnMultiplier = 1 if game_state.red_to_move else -1
    maxScore = -DEN_CONQUESTED
    de = collections.deque([])

    for playerMove in valid_moves:
        game_state.makeMove(playerMove)
        score = turnMultiplier * scoreMaterial(game_state)

        if score > maxScore:
            maxScore = score
            de.appendleft(playerMove)
        else:
            de.append(playerMove)

        game_state.undoMove()
    return de

'''
Monte Carlo algorithm
'''
import AnimalChess_AI_mcst

def find_BestMove_mcst(game_state, valid_moves):
    global mcst_move
    mcst_move = None

    searcher = AnimalChess_AI_mcst.mcts(timeLimit=1000000)
    action = searcher.search(initialState=game_state)
    mcst_move=action
    print(f"mcts: {mcst_move}")
    return mcst_move