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

from AnimalChess_Engine_Rules import GameState

piece_score = {"E": 100, "M": 80, "L": 100, "T": 80, "O": 50, "W": 40,"D": 30,"C": 20}

mouse_score = [[11, 13, 50, 100000, 50, 13, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 11, 13, 13, 13],
                [8, 9, 9, 11,12, 12, 13],
                [8, 8, 8, 9, 12, 12, 12],
                [8, 8, 8, 9, 10, 12, 11],
                [8, 8, 8, 9, 10, 10, 10],
                [8, 8, 8, 9, 9, 9, 9],
                [8, 8, 8, 0, 8, 8, 8]]

cat_score = [[11, 15, 50, 100000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

wolf_score = [[11, 15, 50, 100000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

dog_score = [[11, 15, 50, 100000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

leopard_score = [[11, 15, 50, 100000, 50, 15, 13],
                [11, 12, 13, 50, 13, 13, 13],
                [10, 11, 11, 15, 11, 11, 10],
                [10, 0, 0, 11,0, 0, 13],
                [10, 0, 0, 9, 0, 0, 12],
                [10, 0, 0, 9, 0, 0, 11],
                [10, 0, 0, 9, 0, 0, 10],
                [13, 10, 8, 8, 8,8, 8],
                [8, 8, 8, 0, 8, 8, 8]]

tiger_score = [[25, 30, 150, 100000, 150, 30, 25],
                [25, 25, 30, 150, 30, 25, 25],
                [18, 20, 20, 30, 20, 20, 18],
                [8, 0, 0, 15,0, 0, 15],
                [8, 0, 0, 15, 0, 0, 12],
                [8, 0, 0, 15, 0, 0, 11],
                [8, 8, 8, 9, 16, 16, 14],
                [14, 12, 12, 12, 12, 12, 12],
                [5, 12, 12, 0, 12, 12, 5]]

lion_score = [[25, 30, 150, 100000, 150, 30, 25],
                [25, 25, 30, 150, 30, 25, 25],
                [18, 20, 20, 30, 20, 20, 18],
                [8, 0, 0, 15,0, 0, 15],
                [8, 0, 0, 15, 0, 0, 12],
                [8, 0, 0, 15, 0, 0, 11],
                [8, 8, 8, 9, 16, 16, 14],
                [12, 12, 12, 12, 12, 12, 14],
                [5, 12, 12, 0, 12, 12, 5]]

elephant_score = [[25, 30, 100, 100000, 100, 30, 25],
                [25, 25, 30, 100, 30, 25, 25],
                [18, 20, 20, 30, 20, 20, 18],
                [16, 0, 0, 15,0, 0, 16],
                [14, 0, 0, 15, 0, 0, 14],
                [12, 0, 0, 15, 0, 0, 12],
                [10, 15, 14, 14, 14, 14, 12],
                [11, 11, 11, 11, 11, 11, 11],
                [11, 11, 11, 0, 11, 11, 11]]

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
    #enemy_color = "b" if game_state.white_to_move else "r"

    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                piece_position_score = piece_position_scores[piece][row][col]

                if piece[0] == 'r':
                    score += piece_score[piece[1]] + piece_position_score

                elif piece[0] == 'b':
                     score -= piece_score[piece[1]] + piece_position_score

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

import numpy as np
from collections import defaultdict

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.get_legal_actions()
        return self._untried_actions

    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):	
        action = self._untried_actions.pop()
        next_state = self.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 
    
    def is_terminal_node(self):
        return self.is_game_over()

    
    def rollout(self):
        current_rollout_state = self.state
        
        while not current_rollout_state.is_game_over():
            
            possible_moves = current_rollout_state.get_legal_actions()
            
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()


    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):    
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)
    
    def get_legal_actions(self): 
        '''
        Constructs a list of all possible actions from current state.
        Returns a list.
        '''
        return self.state.getAllPossibleMoves()

    def is_game_over(self):
        '''
        Checks if the game is over. 
        Returns True or False
        '''
        return self.state.den_invaded

    def game_result(self):
        '''
        Returns 1 or 0 or -1 depending on current state corresponding to win, tie or a loss.
        '''
        if self.state.white_to_move:
            if self.board[0][3][0] == "r":
                return 1
            elif self.board.den_invaded:
                return -1
            else:
                return 0
        if not self.state.white_to_move:
            if self.board[8][3][0] == "b":
                return 1
            elif self.board.den_invaded:
                return -1
            else:
                return 0
            

    def move(self,action):
        '''
        Modify according to your game or 
        needs. Changes the state of your 
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board 
        position is empty. If you place x in
        row 2 column 3, then it would be some 
        thing like board[2][3] = 1, where 1f
        represents that x is placed. Returns 
        the new state after making a move.
        '''
        return self.state.makeMove(action)

def main(initial_state):
    root = MonteCarloTreeSearchNode(state = initial_state)
    selected_node = root.best_action()
    return selected_node



"""
class MCTS:
    
    def __init__(self, gamestate):
        self.state = gamestate
        self.board = gamestate.board
        
    
    def getAvailablePieces(self):
        player = "r" if self.state.white_to_move else "b"
        available_pieces = []
        for row in self.board:
            for piece in row:
                if piece[0] == player:
                    available_pieces.append(piece)
        return available_pieces
"""