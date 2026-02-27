from stockfish import Stockfish
import mss
from PIL import Image
from pynput.mouse import Button,Controller
import time
import keyboard
import random
import chess_engine_gui

def run(website,highlight,bongcloud,fen):

    #REQUIRED CHESS.COM THEME
    '''
    PIECES:ALPHA
    BOARD:GREEN
    COORDINATES:INSIDE
    '''

    #REQUIRED LICHESS THEME
    '''
    BACKGROUND:DARK BOARD
    ZOOM:80%
    PIECES:ALPHA (1st row, 3rd column)
    BOARD:BLUE (1st row, 1st column)
    '''

    # Get path relative to the script
    base_dir = os.path.dirname(__file__)
    stockfish_path = os.path.join(base_dir, "stockfish_15_win_x64_avx2", "stockfish_15_x64_avx2.exe")
    stockfish.update_engine_parameters({"Threads":10,"Hash":2048})

    position=fen
    stockfish.set_fen_position(position)

    def eval_bar():
        eval=stockfish.get_evaluation()
        if eval['type']=='mate':
            if eval['value']>0:
                return "Mate in "+str(eval['value'])+" for White"
            return "Mate in "+str(abs(eval['value']))+" for Black"
        if eval['value']>0:
            if len(str(eval['value']/100))==3:
                return '+'+str(eval['value']/100)+"0"
            return '+'+str(eval['value']/100)
        elif eval['value']<0:
            if len(str(eval['value']/100))==4:
                return str(eval['value']/100)+"0"
            return str(eval['value']/100)
        else:
            return '0.00'

    '''
    mouse=Controller()
    while True:
        print(mouse.position)
    '''

    '''
    import pyautogui
    mouse=Controller()
    while True:
        print(pyautogui.pixel(pyautogui.position()[0],pyautogui.position()[1]),mouse.position)
    '''

    if website=="Chess.com":
        bounding=(197,141,1021,965)
        light_square=(233,237,204)
        dark_square=(119,153,84)
        '''moved_square1=(186,203,43)
        moved_square2=(247,247,106)
        moved_square3=(187,202,43)
        moved_square4=(246,246,104)'''
        squareWidth=103
    else:
        bounding=(465,131,1225,891)
        light_square=(133,136,138)
        dark_square=(84,97,104)
        '''moved_square1=(138,152,104)
        moved_square2=(101,122,78)
        moved_square3=(138,152,104)
        moved_square4=(101,122,78)'''
        squareWidth=95

    #LiChess
    #bounding=(465,131,1225,891)

    #Chess.com
    #bounding=(197,141,1021,965)

    def screenshot():
        with mss.mss() as sct:
            sct_img=sct.grab(bounding)
            frame=Image.frombytes("RGB",sct_img.size,sct_img.bgra,"raw","BGRX")
        #frame.show()
        return frame

    while not keyboard.is_pressed('s'):pass

    #mouse=Controller()
    #while True:print(mouse.position[0]-197,mouse.position[1]-141,screenshot().getpixel((mouse.position[0]-197,mouse.position[1]-141)))
    
    if website=="Chess.com":
        if screenshot().getpixel((364,64))==(0,0,0):side_of_board="WHITE"
        else:side_of_board="BLACK"
    else:
        if screenshot().getpixel((237,703))==(12,12,12):side_of_board="WHITE"
        else:side_of_board="BLACK"


    #LiChess

    '''light_square=(133,136,138)
    dark_square=(84,97,104)
    moved_square1=(138,152,104)
    moved_square2=(101,122,78)
    squareWidth=95'''

    #Chess.com

    '''light_square=(243,243,244)
    dark_square=(106,155,65)
    moved_square1=(186,203,43)
    moved_square2=(247,247,106)
    squareWidth=103'''

    #LiChess
    '''if screenshot().getpixel((237,703))==(12,12,12):side_of_board="WHITE"
    else:side_of_board="BLACK"'''



    #Chess.com

    '''if screenshot().getpixel((256,41))==(255,255,255):side_of_board="WHITE"
    else:side_of_board="BLACK"'''


    print("SIDE OF BOARD: ",side_of_board)

    turn="WHITE"
    upcoming_turn="BLACK"

    def coord_to_move(x,y):
        if side_of_board=="WHITE":
            alpha="abcdefgh"
            nums=[8,7,6,5,4,3,2,1]
        else:
            alpha="hgfedcba"
            nums=[1,2,3,4,5,6,7,8]
        
        if nums[y%8] in {1,8}:
            if stockfish.get_what_is_on_square(alpha[x//8]+str(nums[x%8])) in {Stockfish.Piece.WHITE_PAWN,Stockfish.Piece.BLACK_PAWN}:
                return alpha[x//8]+str(nums[x%8])+alpha[y//8]+str(nums[y%8])+"q"

        return alpha[x//8]+str(nums[x%8])+alpha[y//8]+str(nums[y%8])

    def make_best_move(best_move,click):
        if side_of_board=="WHITE":
            alpha="abcdefgh"
            nums=[8,7,6,5,4,3,2,1]
        else:
            alpha="hgfedcba"
            nums=[1,2,3,4,5,6,7,8]
        mouse.position=(bounding[0],bounding[1])
        mouse.move(alpha.find(best_move[0])*squareWidth+squareWidth//2,nums.index(int(best_move[1]))*squareWidth+squareWidth//2)
        if click:mouse.press(Button.left)
        else:mouse.press(Button.right)
        mouse.position=(bounding[0],bounding[1])
        mouse.move(alpha.find(best_move[2])*squareWidth+squareWidth//2,nums.index(int(best_move[3]))*squareWidth+squareWidth//2)
        if click:mouse.release(Button.left)
        else:
            time.sleep(0.1)
            mouse.release(Button.right)
            mouse.click(Button.right)
            mouse.release(Button.right)


    game_moves=set()
    game_move_order=[]

    mouse=Controller()

    #messages=["Nice Try","Decent Move!","Good Try!","OOF!","UH OH","YOU GOT ME!"]
    messages=["Resign trash can","KYS","Actually terrible"]

    while True:

        color_squares=[]

        board=screenshot()

        #USER INPUT TO END EARLY
        if keyboard.is_pressed('0') or board.getpixel((600,350)) in {(102,100,99),(129,182,76)}:
            return

        try:

            for i in range(0,squareWidth*8,squareWidth):
                for j in range(0,squareWidth*8,squareWidth):
                    color_squares.append(board.getpixel((i+5,j+30)))

            move=[]

            '''print(color_squares)
            exit()'''

            for i in range(len(color_squares)):
                '''if abs(sum(color_squares[i])-sum(moved_square1))<=5 or abs(sum(color_squares[i])-sum(moved_square2))<=5:
                    move.append(i)'''
                if color_squares[i] not in {light_square,dark_square}:
                    move.append(i)

            if len(move)!=2:continue

            if board.getpixel((move[0]//8*squareWidth+squareWidth//2,move[0]%8*squareWidth+squareWidth//2))!=board.getpixel((move[0]//8*squareWidth+5,move[0]%8*squareWidth+30)):
                move=coord_to_move(move[1],move[0])
            elif board.getpixel((move[1]//8*squareWidth+squareWidth//2,move[1]%8*squareWidth+squareWidth//2))!=board.getpixel((move[1]//8*squareWidth+5,move[1]%8*squareWidth+30)):
                move=coord_to_move(move[0],move[1])
            else:
                #Castled
                if side_of_board=="WHITE":
                    if move==[39,63]:move="e1g1"
                    if move==[7,39]:move="e1c1"
                    if move==[32,56]:move="e8g8"
                    if move==[0,32]:move="e8c8"
                if side_of_board=="BLACK":
                    if move==[15,31]:move="e8g8"
                    if move==[31,63]:move="e8c8"
                    if move==[0,24]:move="e1g1"
                    if move==[24,56]:move="e1a1"

            cur_len=len(game_moves)
            game_moves.add(move)

            if len(game_moves)!=cur_len:
                
                stockfish.make_moves_from_current_position([move])
                best_move=stockfish.get_best_move(1)
                print(turn,"played",move+';',upcoming_turn,"should respond with",best_move+".      EVALUATION BAR:",eval_bar(),'\n')
                game_move_order.append(move)
                if len(game_move_order)>=2:game_moves.remove(game_move_order[-2])

                turn,upcoming_turn=upcoming_turn,turn

                time.sleep(0.1)

                if turn==side_of_board:
                    #BONGCLOUD
                    if bongcloud:
                        if side_of_board=="WHITE":
                            if len(game_move_order)==2:make_best_move("e1e2",True)
                            else:make_best_move(best_move,True)
                        else:
                            if len(game_move_order)==1:make_best_move("e7e6",True)
                            elif len(game_move_order)==3:make_best_move("e8e7",True)
                            else:make_best_move(best_move,True)

                    else:
                        make_best_move(best_move,True)

                    #Check if checkmated
                    if eval_bar()[:13]=="Mate in 1 for":return

                    #Troll feature
                    '''
                    mouse.position=(0,0)
                    mouse.move(1070,1007)
                    mouse.click(Button.left)
                    keyboard.write(random.choice(messages))
                    keyboard.press_and_release('enter')
                    '''
                
                #Draw Arrow for opponent
                elif highlight:
                    make_best_move(best_move,False)

        except Exception as e:pass
