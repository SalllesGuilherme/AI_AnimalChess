"""
Handling the AI moves.
"""
import random

piece_score = {"E": 20, "M": 10, "L": 8, "T": 6, "O": 3, "W": 3,"D": 1,"C": 1}

DEN_CONQUESTED=1000
DRAW=0

def findRandomMove(valid_moves):
    #return random.choice(valid_moves)
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

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'r':
                score = score + piece_score[square[1]]
            elif square[0] == 'b':
                score = score - piece_score[square[1]]

    return score
# def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
#     global next_move
#     if depth == 0:
#         return turn_multiplier * scoreBoard(game_state)
#     # move ordering - implement later //TODO Alpha-Beta Cuts
#     max_score = -CHECKMATE
#     for move in valid_moves:
#         game_state.makeMove(move)
#         next_moves = game_state.getValidMoves()
#         score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
#         if score > max_score:
#             max_score = score
#             if depth == DEPTH:
#                 next_move = move
#         game_state.undoMove()
#         if max_score > alpha:
#             alpha = max_score
#         if alpha >= beta:
#             break
#     return max_score
#
#
# def scoreBoard(game_state):
#     """
#     Score the board. A positive score is good for white, a negative score is good for black.
#     """
#     if game_state.checkmate:
#         if game_state.white_to_move:
#             return -CHECKMATE  # black wins
#         else:
#             return CHECKMATE  # white wins
#     elif game_state.stalemate:
#         return STALEMATE
#     score = 0
#     for row in range(len(game_state.board)):
#         for col in range(len(game_state.board[row])):
#             piece = game_state.board[row][col]
#             if piece != "--":
#                 piece_position_score = 0
#                 if piece[1] != "K":
#                     piece_position_score = piece_position_scores[piece][row][col]
#                 if piece[0] == "w":
#                     score += piece_score[piece[1]] + piece_position_score
#                 if piece[0] == "b":
#                     score -= piece_score[piece[1]] + piece_position_score
#
#     return score


