"""
FEUP - Faculty of Engineering of Porto
MASTER OF DATA SCIENCE AND ENGINEERING
Course: Artificial Inteligence
Professor: Luis Reis
Students: Danilo Brandão / Guilherme Salles
"""

"""
JUNGLE CHESS
Main code for run the game, it handle user input and GUI
"""

import pygame as p
import AnimalChess_Engine_Rules,AnimalChess_AI
import sys
from time import process_time

WIDTH = 512 #448
HEIGHT = 512 #572
BOARD_WIDTH = 448
BOARD_HEIGHT = 576
MOVE_LOG_PANEL_WIDTH = 0
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
DIMENSION_ROW = 9
DIMENSION_COL = 7
SQUARE_SIZE = 64 #BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['bT','bE','bC','bW','bO','bD','bM','bL','rT','rE','rC','rW','rO','rD','rM','rL','trap','den','grass','water']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main(player1,player2):

    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = AnimalChess_Engine_Rules.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = player1   # True for Human, False for AI
    player_two = player2  # True for Human, False for AI
    Total_time_p1 = 0
    Total_time_p2 = 0
    Total_move_p1 = 0
    Total_move_p2 = 0

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = AnimalChess_Engine_Rules.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

                if e.key == p.K_h:
                    print("JucAI recomends this move:")
                    ai_move = AnimalChess_AI.findBestMove_AlphaBeta(game_state, valid_moves)
                    print(ai_move)

                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = AnimalChess_Engine_Rules.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

    # AI move finder for player 1
        if not game_over and not human_turn and not move_undone and not player_one:
            t1_start = process_time()
            ai_move = AnimalChess_AI.findBestMove_AlphaBeta(game_state , valid_moves)
            print(f"ai_move = {ai_move}")

            if ai_move is not None:
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                t1_stop = process_time()
            else:
                game_state.den_invaded=True   #\\Improve the condition for not move

            #Log performance AI1
            delta_t1=t1_stop-t1_start
            Total_time_p1 += delta_t1
            Total_move_p1 += 1
            print(f"AI 1: {ai_move}, Thinking Time:{delta_t1} , Total time:{Total_time_p1}, Move:{Total_move_p1}")

        if move_made and not player_one:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

    # AI move finder for player 2
        if not game_over and not human_turn and not move_undone and not player_two:
            t2_start = process_time()
            #ai_move = AnimalChess_AI.findBestMove_AlphaBeta(game_state, valid_moves)
            ai_move = AnimalChess_AI.main(game_state)
            print(f"This is the MCTS best move: {ai_move}")
                         
            if ai_move is not None:
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                t2_stop = process_time()
            else:
                game_state.den_invaded = True  # \\Improve the condition for not move

            # Log performance AI2
            delta_t2 = t2_stop - t2_start
            Total_time_p2 += delta_t2
            Total_move_p2 += 1
            print(f"AI 2: {ai_move}, Thinking Time:{delta_t2}, Total time:{Total_time_p2}")

        if move_made and not player_two:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(screen, game_state, move_log_font)

        if game_state.den_invaded:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins")
            else:
                drawEndGameText(screen, "Red wins")

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, game_state, valid_moves, square_selected):

    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):

    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION_ROW):
        for column in range(DIMENSION_COL):
            p.draw.rect(screen, p.Color(25,65,25), p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            #screen.blit(IMAGES['grass'], p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE -3, SQUARE_SIZE - 3))  # grass image
            p.draw.rect(screen, p.Color(200,225,200), p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE - 3, SQUARE_SIZE - 3))

            if row in [3,4,5]:  #WATER
                if column in [1,2,4,5]:
                    p.draw.rect(screen, p.Color(5,120,230),p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE - 3,SQUARE_SIZE - 3))
                    #screen.blit(IMAGES['water'], p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE -3, SQUARE_SIZE - 3))
            if row in [0,8]:    #TRAP
                if column in [2,4]:
                    #p.draw.rect(screen, p.Color(255,105,60),p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE - 3,SQUARE_SIZE - 3))
                    screen.blit(IMAGES['trap'], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if row in [1,7]:   #TRAP
                if column in [3]:
                    #p.draw.rect(screen, p.Color(255,105,60),p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE - 3,SQUARE_SIZE - 3))
                    screen.blit(IMAGES['trap'], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if row in [0,8]:   #DEN
                if column in [3]:
                    #p.draw.rect(screen, p.Color(50,180,50),p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE - 3,SQUARE_SIZE - 3))
                    screen.blit(IMAGES['den'], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ('r' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):

    for row in range(DIMENSION_ROW):
        for column in range(DIMENSION_COL):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(screen, game_state, font):

    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def animateMove(move, screen, board, clock):

    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)

        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)

        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

def start_page():

    junglechess ='''


    
WELCOME TO

   ___                   _      _____ _                   
  |_  |                 | |    /  __ \ |                  
    | |_   _ _ __   __ _| | ___| /  \/ |__   ___  ___ ___ 
    | | | | | '_ \ / _` | |/ _ \ |   | '_ \ / _ \/ __/ __|
/\__/ / |_| | | | | (_| | |  __/ \__/\ | | |  __/\__ \__ |
\____/ \__,_|_| |_|\__, |_|\___|\____/_| |_|\___||___/___/
                    __/ |                                 
                   |___/    
                                            
################################################################                   

Please type one of the numbers below for choose a mode for play:
   ( 1 ) - Human vs Human
   ( 2 ) - Human vs AI
   ( 3 ) - AI vs Human
   ( 4 ) - AI vs AI
   
################################################################    
'''
    print(junglechess)
    not_select=True
    p1 , p2 = False, False
    messagevalue = "If cann't type a number between 1-4, you have no change against our AI"

    while not_select:
        try:
            mode=int(input())
            if mode in [1,2,3,4]:
                if mode == 1:
                    p1, p2 = True, True
                elif mode == 2:
                    p1,p2 = True,False
                elif mode == 3:
                    p1,p2 = False,True
                elif mode == 4:
                    p1,p2 = False,False
                not_select=False
            else:
                print(messagevalue)
        except ValueError:
            print(messagevalue)

    return p1,p2

if __name__ == "__main__":
    player1,player2 = start_page()
    print("Loading... ")
    main(player1,player2)