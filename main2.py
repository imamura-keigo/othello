#/usr/bin/python3
from tkinter import *
import rule
import time

#running = False
sub_win = None
COM = -1
once = 0
x = 0
y = 0

def clickHandle(event):
        global x,y,COM,othello #PL has option 0 : Human Player 1 : Computer
        xMouse = event.x
        yMouse = event.y
        x = -1
        y = -1
        BOARD_SIZE = 8 + 1
        column_width = screen.winfo_width() / BOARD_SIZE
        row_height = screen.winfo_height() / BOARD_SIZE
        global running
        
        if running:
                for c in range(BOARD_SIZE):
                        for r in range(BOARD_SIZE):
                                x1 = c * (column_width)
                                y1 = r * (row_height)
                                x2 = x1 + (column_width)
                                y2 = y1 + (row_height)
                                if y1 <= yMouse <= y2:
                                        if x1 <= xMouse <= x2:
                                                x = c - 1
                                                y = r - 1
                                                #print(x,y)
                                                if (COM == 1) or (COM == 2):
                                                        if COM != othello.PL_turn:
                                                                othello.put_stone(x,y,othello.PL_turn)
                                                                operate_othello()
                                                                #-------棋譜の表示--------------
                                                                #othello.show_record()
                                                                #---------------------
                                                                sub_win_Update()
                                                                time.sleep(1)
                                                        
                                                        if COM == othello.PL_turn:
                                                                othello.com_search(othello.PL_turn)
                                                                x = othello.x_before
                                                                y = othello.y_before
                                                                operate_othello()
                                                        #--------棋譜の表示-------------
                                                        #othello.show_record()
                                                        #----------------------
                                                        sub_win_Update()


                                                elif(COM == 0):
                                                        if othello.put_stone(x,y,othello.PL_turn):
                                                                operate_othello()
                                                                #----------------
                                                                #othello.show_record()
                                                                #----------------
                                                                sub_win_Update()

        else:
                if 300<= yMouse <=350:
                        if 25<=xMouse<=155:
                                COM = 0
                                playGame()
                        elif 180<=xMouse<=310:
                                COM = 2
                                playGame()
                        elif 335<=xMouse<=465:
                                COM = 1
                                playGame()


def operate_othello():
        global x,y,running,PL_turn
        BOARD_SIZE = 8 + 1
        column_width = screen.winfo_width() / BOARD_SIZE
        row_height = screen.winfo_height() / BOARD_SIZE

        for c in range(BOARD_SIZE):
                for r in range(BOARD_SIZE):
                        x1 = c * (column_width)
                        y1 = r * (row_height)
                        x2 = x1 + (column_width)
                        y2 = y1 + (row_height)
                        if (c == x + 1  and r == y + 1 and running ):
                                screen.create_rectangle(x1,y1,x2,y2,fill = 'red')
                        elif (c == 0 or r == 0):
                                screen.create_rectangle(x1,y1,x2,y2,fill = '#222')
                        else:
                                screen.create_rectangle(x1,y1,x2,y2,fill = 'green')
                                # if othello.can_put[(c-1)+(r-1)*8] > 0:
                                #         othello.put_checker(3-PL_turn)
                                #         screen.create_rectangle(x1,y1,x2,y2,fill = 'blue')

                        if c != 0 and r !=0:
                                #othello.put_checker(PL_turn)
                                #if othello.can_put[(c-1)+(r-1)*8] > 0:
                                #        screen.create_rectangle(x2,y1,x2,y2,fill="blue")      
                                if othello.board[(c-1)+(r-1)*8]==1:
                                        screen.create_oval(x1,y1,x2,y2,fill = 'black')
                                elif othello.board[(c-1)+(r-1)*8]==2:
                                        screen.create_oval(x1,y1,x2,y2,fill = 'white')
        screen.pack()
        screen.update()

def show_othello_board():
        global x,y
        BOARD_SIZE = 8 + 1
        column_width = screen.winfo_width() / BOARD_SIZE
        row_height = screen.winfo_height() / BOARD_SIZE
        for c in range(BOARD_SIZE):
                for r in range(BOARD_SIZE):
                        x1 = c * (column_width)
                        y1 = r * (row_height)
                        x2 = x1 + (column_width)
                        y2 = y1 + (row_height)
                        if (c == 0 or r == 0):
                                xpos = x1+column_width
                                ypos = y1+row_height + row_height/2
                                screen.create_rectangle(x1,y1,x2,y2,fill = '#222')
                        else:
                                screen.create_rectangle(x1,y1,x2,y2,fill = 'green')
	
        screen.pack()
        screen.update()
        undo.pack()
        undo.update()


def sub_win_Update():
        global sub_win
        global othello
        global scrollbar
        global listbox
        ishi = str("")
        listbox.delete (first = 0, last=listbox.size())

#------------------棋譜の表示-------------------------------------------------
        for i,kihu in zip(range(len(othello.kihu)),othello.kihu):
                if len(kihu)!=0:
                        #パスだった場合
                        if  kihu[1] == -1:
                                zahyou = "Pass"

                        #それ以外
                        else:
                                zahyou = "abcdefgh" [kihu[1]]+str(kihu[2]+1)
                if kihu[0]==1:
                        ishi = '●'
                elif kihu[0]==2:
                        ishi = '○'
                listbox.insert(END, str(i+1)+" :  "+ ishi + " " + str(zahyou) )
#----------------------------------------------------------------------------
        listbox.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=listbox.yview)
        sub_win.update()

def create_new_screen():
	global sub_win
	global othello
	global scrollbar
	global listbox
	if sub_win is None or not sub_win.winfo_exists():
		sub_win=Toplevel()
		sub_win.title("棋譜")

		w = 150 # width for the Tk root
		h = 500 # height for the Tk root
		
		#親画面の情報
		ws = root.winfo_screenwidth() # width of the screen
		hs = root.winfo_screenheight() # height of the screen
		#親からの相対位置
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		sub_win.geometry("%dx%d+%d+%d" % (w, h, x, y))
		# msg = Message(sub_win, text="棋譜出してくれ~") #ここに棋譜を貼る
		# msg.pack()
		scrollbar = Scrollbar(sub_win)
		scrollbar.pack(side=RIGHT, fill=Y)
		
		listbox = Listbox(sub_win, yscrollcommand=scrollbar.set)
		
		sub_win_Update()

def keyHandle(event):
	global ruuning
	symbol = event.keysym
	if symbol.lower()=="r": #rでリスタート
		runGame()
	elif symbol.lower()=="q": #qでおわおわり
		root.destroy()
	elif symbol.lower()=="w" and running:
                #--------csvから棋譜を読み込む-----------
		create_new_screen()
	elif symbol.lower()=="u" and running:
                print("undo")
                othello.Undo(COM)
                sub_win_Update()

def runGame():
	global running
	running = False
	
	screen.create_text(250,203,anchor="c",text="オセロにしたい\nしたくない？",font=("Consolas", 50),fill="#fff")
	for i in range(3):
		screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
    
	screen.create_text(90,330,anchor="c",text="PvP", font=("Consolas", 25),fill="#b29600")
	screen.create_text(245,330,anchor="c",text="PvC", font=("Consolas", 25),fill="#b29600")
	screen.create_text(400,330,anchor="c",text="CvP", font=("Consolas", 25),fill="#b29600")

	screen.update()

def playGame():
        global board, running,x,y
        global othello
        global PL2
        global COM

        screen.delete(ALL)
        othello = rule.Board(COM)
        create_new_screen() #棋譜用サブ画面表示 
	
        
        show_othello_board() #ゲームボードの表示
	#オセロの駒表示
        operate_othello()
        running = True
        if COM == 1: #COMが先手の場合。クリック前に先に打つ
                time.sleep(1)
                othello.com_search(1)
                x = othello.x_before
                y = othello.y_before
                operate_othello()
                #-----------------------
                #othello.show_record()
                #-----------------------
                sub_win_Update()
	#ゲーム結果


if __name__ == '__main__':
#親画面の初期化処理
	root = Tk()
	root.resizable(0,0)
	Fboard = Frame(root)
	bottom = Frame(Fboard)
	undo = Button(Fboard,text ="Undo")
	screen = Canvas(Fboard, width=500, height=500, background="#222",highlightthickness=0)
	#score = Canvas(Fboard, width=500, height=500, background="#222",highlightthickness=0)
#	screen.create_rectangle(0, 0, 500, 500, fill = 'green')
	Fboard.pack()
	screen.pack(anchor = W)
	#score.pack(anchor = E)
	root.wm_title("Othello")
#ゲームの起動
	runGame()
#ボタン系の処理、ハンドラ処理
	screen.bind("<Button-1>", clickHandle)
	screen.bind("<Key>",keyHandle)
	screen.focus_set()
#ループ    
	root.mainloop()
""" 
root ---*--- Fboard ---*--- screen
        |              |
		|              *--- bottom
		|              |
		|              *--- score
        |
		*--- sub_win
"""
