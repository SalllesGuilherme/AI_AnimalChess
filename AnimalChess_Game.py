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

from json import load
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
Total_time_p1 = 0
Total_time_p2 = 0
Total_move_p1 = 0
Total_move_p2 = 0



def loadImages():
    pieces = ['bT','bE','bC','bW','bO','bD','bM','bL','rT','rE','rC','rW','rO','rD','rM','rL','trap','den','grass','water']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main(player1,player2,depth_p1,depth_p2):

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
    player_won = 0

    while running:
        human_turn = (game_state.red_to_move and player_one) or (not game_state.red_to_move and player_two)
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
                    move_undone = True

                if e.key == p.K_h:
                    print("JucAI recomends move:")
                    ai_move = AnimalChess_AI.find_BestMove(game_state, valid_moves,depth_p1)
                    print(ai_move)

                if e.key == p.K_m:
                        print("JucAI MCTS recomends move:")
                        ai_move = AnimalChess_AI.find_BestMove_mcst(game_state, valid_moves)
                        print(ai_move)

                if e.key == p.K_q:
                    print("\nEND GAME statistics:")
                    log_perfomance(process_time(), process_time(), 0,0 , 1,depth_p1,depth_p2,player_won)
                    exit()


                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = AnimalChess_Engine_Rules.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:

            if not player_one and game_state.red_to_move: #RED
                t1_start = process_time()
                ai_move=[]
                ai_move = AnimalChess_AI.find_BestMove(game_state,valid_moves,depth_p1)
                if ai_move is not None:
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                else:
                    print("Out of moves? Go gready")
                    ai_move = AnimalChess_AI.find_GreadyMove(game_state,valid_moves)
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                t1_stop = process_time()
                log_perfomance(t1_start,t1_stop,1,ai_move,0,player1,player2)

            elif not player_two and not game_state.red_to_move: #Black
                t2_start = process_time()
                ai_move = []
                ai_move = AnimalChess_AI.find_BestMove(game_state, valid_moves,depth_p2)
                #ai_move = AnimalChess_AI.find_BestMove_mcst(game_state, valid_moves)
                if ai_move is not None:
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                else:
                    print("Out of moves... Go gready")
                    ai_move = AnimalChess_AI.find_GreadyMove(game_state, valid_moves)
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                t2_stop=process_time()
                log_perfomance(t2_start,t2_stop,2,ai_move,0,player1,player2)


        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(screen, game_state, move_log_font)

        if game_state.enemyConquerDen():
            game_over = True
            if game_state.red_to_move:
                drawEndGameText(screen, "Black wins")
                player_won=2
            else:
                drawEndGameText(screen, "Red wins")
                player_won=1
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
            p.draw.rect(screen, p.Color(90,150,75), p.Rect((column * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3, SQUARE_SIZE - 3, SQUARE_SIZE - 3))

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
        if game_state.board[row][col][0] == ('r' if game_state.red_to_move else 'b'):  # square_selected is a piece that can be moved
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

def log_perfomance(t_start,t_stop,player,move,gameover,depth_p1=4,depth_p2=4,player_won=0):
    global Total_time_p1
    global Total_time_p2
    global Total_move_p1
    global Total_move_p2

    delta_t = 0
    delta_t = t_stop - t_start

    if gameover == 1:
        if player_won == 2:
            print("BLACK WINS")
        elif player_won == 1:
            print("RED WINS")
        else:
            print("DRAW!")

        if Total_time_p1 > 0:
            print(f"Red AI1 with depth:{depth_p1}    | Total time:{Total_time_p1:.3f} | Avg thinking time:{Total_time_p1/Total_move_p1:.3f} ")
        if Total_time_p2 > 0:
            print(f"Black AI2 with depth:{depth_p2}  | Total time:{Total_time_p2:.3f} | Avg thinking time:{Total_time_p2/Total_move_p2:.3f}")

    elif player == 1:
        Total_time_p1 += delta_t
        Total_move_p1 += 1
        print(f"Red AI1: {move}, Thinking Time:{delta_t} , Total time:{Total_time_p1}, Move:{Total_move_p1}")
    elif player == 2:
        Total_time_p2 += delta_t
        Total_move_p2 += 1
        print(f"Black AI2: {move}, Thinking Time:{delta_t} , Total time:{Total_time_p2}, Move:{Total_move_p2}")


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

    return p1,p2,mode

def levelgame(mode):
    depth_p1=4
    depth_p2=4
    not_select = True
    p1, p2 = False, False
    msg_select = 'Please type 1-9 for the level of the AI:\n'
    msg_lvl=   "Easy....Medium....Hard....SuperAI\n"
    msg_lvl2 = "1...2...3...4...5...6...7...8...9"
    messagevalue = "If cann't type a number between 1-9, you have no change against our AI"

    while not_select:
        try:
            if mode == 1:
                print("Player vs Player selected")
                break
            elif mode == 2:
                print(msg_select, msg_lvl, msg_lvl2)
                depth_p2 = int(input())
                break
            elif mode == 3:
                print(msg_select,msg_lvl,msg_lvl2)
                depth_p1 = int(input())
                break
            elif mode == 4:
                print(msg_select, msg_lvl, msg_lvl2)
                depth_p1 = int(input())
                print(msg_select, msg_lvl, msg_lvl2)
                depth_p2 = int(input())
                break
            else:
                print(messagevalue)
        except ValueError:
            print(messagevalue)

    return depth_p1,depth_p2


class Button:
    def __init__(self, image, position, callback=None):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.callback = callback

    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self)
    

class DropDown():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = p.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        p.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                p.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event_list):
        mpos = p.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1    
       

def main_menu():
    p.init()
    mainClock = p.time.Clock()

    # create display window
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # load main screen
    screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    p.display.set_caption("Jungle Chess by Danilo Brandao and Guilherme Salles")
    bg_img = p.image.load("images/main_menu.gif")
    

    # load button images
    hvh_img = p.image.load('images/button_hvh.png').convert_alpha()
    hva_img = p.image.load('images/button_hva.png').convert_alpha()
    avh_img = p.image.load('images/button_avh.png').convert_alpha()
    ava_img = p.image.load('images/button_ava.png').convert_alpha()
    sel_1 = p.image.load('images/select_lvl_1.png').convert_alpha()
    sel_2 = p.image.load('images/select_lvl_2.png').convert_alpha()
    

    # #create button instances
    button_1 = Button(hvh_img, (250, 350))
    button_2 = Button(hva_img, (250, 400))
    button_3 = Button(avh_img, (250, 450))
    button_4 = Button(ava_img, (250, 500))
    
    difficulty_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # list1 = OptionBox(
    # 75, 350, 100, 30, (150, 150, 150), (100, 200, 255), p.font.SysFont(None, 30), difficulty_levels)
    
    COLOR_INACTIVE = (255, 128, 0)
    COLOR_ACTIVE = (255, 208, 0)
    COLOR_LIST_INACTIVE = (0, 143, 90)
    COLOR_LIST_ACTIVE = (3, 252, 140)

    list1 = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                     [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                     75, 350, 100, 20,
                     p.font.SysFont("Courier", 20),
                     "Click",
                     difficulty_levels)
    
    list2 = DropDown([COLOR_INACTIVE, COLOR_ACTIVE],
                     [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                     650, 350, 100, 20,
                     p.font.SysFont("Courier", 20),
                     "Click",
                     difficulty_levels)
    

    # game music
    # p.mixer.init()
    # music = p.mixer.Sound('assets/theme_song.mp3')
    # music.set_volume(0.65)
    # music.play()

    # p.display.flip()

    p1, p2 = False, False

    run = True
    while run:
        mainClock.tick(60)
               
        # screen.blit(bg_img, (0, 0))
        
        mode=0
        event_list = p.event.get()
        
        selected_option_1 = list1.update(event_list)
        if selected_option_1 >= 0:
            list1.main = list1.options[selected_option_1]
            print(list1.main)
            
        selected_option_2 = list2.update(event_list)
        if selected_option_2 >= 0:
            list2.main = list2.options[selected_option_2]
            print(list2.main)
        
        for event in event_list:
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    p.quit()
                    sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_1.rect.collidepoint(p.mouse.get_pos()):
                        # print("Over button 1!")
                        p1, p2 = True, True
                        depth1, depth2 = None, None
                        run = False
                        mode=1
                    if button_2.rect.collidepoint(p.mouse.get_pos()):
                        # print("Over button 2!")
                        p1, p2 = True, False
                        if list2.main == "Click":
                            print("Please select a difficulty level for AI 2!")
                        else:
                            depth1, depth2 = None, int(list2.main)
                            mode = 2
                            run = False
                            
                        # run = False
                        # mode=2
                    if button_3.rect.collidepoint(p.mouse.get_pos()):
                        # print("Over button 3!")
                        p1, p2 = False, True
                        if list1.main == "Click":
                            print("Please select a difficulty level for AI 1!")
                        else:
                            depth1, depth2 = int(list1.main), None
                            mode = 3
                            run = False
                        # run = False
                        # mode=3
                    if button_4.rect.collidepoint(p.mouse.get_pos()):
                        # print("Over button 4!")
                        p1, p2 = False, False
                        if "Click" in (list1.main, list2.main):
                            print("Please make sure you selected the difficulty level for both AI players!")
                        else:
                            depth1, depth2 = int(list1.main), int(list2.main)
                            mode = 4
                            run = False
                            
                        
        
            
        # if mode == 2 and selected_option_2 == 0:
        #     run = True
        #     print("Please select a difficulty level for AI 2!")
        # elif mode == 3 and selected_option_1 == 0:
        #     run = True
        #     print("Please select a difficulty level for AI 1!")
        # elif mode == 4 and selected_option_1 == 0 or mode == 4 and selected_option_2 == 0:
        #     run = True
        #     print("Please make sure you selected the difficulty level for both AI players!")
        # else:
        #     run = False

        screen.blit(bg_img, (0, 0))  # Loads background image
        screen.blit(sel_1, (50, 300))
        screen.blit(sel_2, (625, 300))
        screen.blit(button_1.image, button_1.rect)  # Loads button 1 on screen
        screen.blit(button_2.image, button_2.rect)  # Loads button 2 on screen
        screen.blit(button_3.image, button_3.rect)  # Loads button 3 on screen
        screen.blit(button_4.image, button_4.rect)  # Loads button 4 on screen
        list1.draw(screen)
        list2.draw(screen)
               
        p.display.flip()           

        #p.display.update()

    #music.stop()
    mainClock.tick(60)
    # return p1, p2,mode
    return p1, p2, depth1, depth2

if __name__ == "__main__":

    #Old Interface
    #player1,player2,mode = start_page()

    click = False  # Resets click event
    # player1, player2,mode = main_menu()  # Loads main menu
    player1, player2, depth_1, depth_2 = main_menu()  # Loads main menu

    print("Loading... ")
    # depth_p1,depth_p2 = levelgame(mode)

    print("Initialing game...")
    # main(player1,player2,depth_p1,depth_p2)
    main(player1, player2, depth_1, depth_2)