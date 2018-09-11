#/usr/bin/python3
from tkinter import *
import tkinter.messagebox as tkmsg
import rule
import time
import numpy

#running = False
sub_win = None
COM = -1
once = 0
x = 0
y = 0

def clickHandle(event):
	global COM #PL has option 0 : Human Player 1 : Computer
	global othello
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
						if (COM == 1) or (COM == 2):
							if COM != othello.PL_turn:
								othello.put_stone(x,y,othello.PL_turn)
								operate_othello()
								sub_win_Update()	
							while COM == othello.PL_turn:
								othello.com_search(othello.PL_turn)
								operate_othello()
								sub_win_Update()
							sub_win_Update()	
				
						elif COM == 0:
							if othello.put_stone(x,y,othello.PL_turn):
								operate_othello()
								sub_win_Update()

		if othello.finish or len(numpy.where(othello.board == 0)) ==0:
				othello.game_end()
				show_result()

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
	BOARD_SIZE = 8 + 1
	column_width = screen.winfo_width() / BOARD_SIZE
	row_height = screen.winfo_height() / BOARD_SIZE
	
	othello.put_checker(othello.PL_turn)
	if not len(othello.kihu) == 0:
		i = len(othello.kihu) - 1
		while True:
			if len(othello.kihu[i]) == 4:
				k = othello.kihu[i]
				break
			else:
				i = i-1


	for c in range(BOARD_SIZE):
		for r in range(BOARD_SIZE):
			x1 = c * (column_width)
			y1 = r * (row_height)
			x2 = x1 + (column_width)
			y2 = y1 + (row_height)
			
			if (c == 0 or r == 0):
					screen.create_rectangle(x1,y1,x2,y2,fill = '#222')
			else:
					screen.create_rectangle(x1,y1,x2,y2,fill = 'green')
					if othello.can_put[(c-1)+(r-1)*8] > 0:
						screen.create_rectangle(x1,y1,x2,y2,fill = 'pale green')
					if not len(othello.kihu) == 0:
						if (c == k[1] + 1  and r == k[2] + 1 and running ):
							screen.create_rectangle(x1,y1,x2,y2,fill = 'red')
			if c != 0 and r !=0:    
				if othello.board[(c-1)+(r-1)*8]==1:
					screen.create_oval(x1,y1,x2,y2,fill = 'black')
				elif othello.board[(c-1)+(r-1)*8]==2:
					screen.create_oval(x1,y1,x2,y2,fill = 'white')

	screen.grid(column=0,row=0)
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
	
        screen.grid(column=0,row=0)
        screen.update()


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
				if kihu[0] == 1:
						ishi = '●'
				elif kihu[0] == 2:
						ishi = '○'
				listbox.insert(END, str(i+1)+" :  "+ ishi + " " + str(zahyou))
#----------------------------------------------------------------------------	
		listbox.pack(side=LEFT, fill=BOTH)
		scrollbar.config(command=listbox.yview)
		sub_win.update()
		screen.grid(column=0,row=0)
		screen.update()

		bottom.grid(column=0,row=1)
		bottom.update()
		
		kihu_bot.grid(column=0,row=0)
		kihu_bot.update()
		restart_bot.grid(column=1,row=0)
		restart_bot.update()
		quit_bot.grid(column=2,row=0)
		quit_bot.update()

		score.grid(column=1,row=0)
		score.update()

def choose():
	global listbox
	global othello
	global screen
	global COM
	try:
		if listbox.curselection()[0] == 0:
			othello = rule.Board(COM)
		elif "pass" !=  othello.kihu[listbox.curselection()[0]][1]:
			for i in range(len(othello.kihu) - listbox.curselection()[0]):
				othello.PL_turn = int(othello.kihu.pop()[0])
			othello.board = othello.kihu[-1][3]	
	except IndexError:
		value = None
	self.finish = False
	sub_win_Update()
	screen.delete("stone")
	show_othello_board()
	operate_othello()


def sub_win_Update():
	global sub_win
	global othello
	global scrollbar
	global listbox
	zahyou = ''
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
		if kihu[0] == 1:
			ishi = '●'
		elif kihu[0] == 2:
			ishi = '○'
		listbox.insert(END, str(i+1)+" :  "+ ishi + " " + str(zahyou))
#----------------------------------------------------------------------------	
	listbox.pack(side=LEFT, fill=BOTH)
	scrollbar.config(command=listbox.yview)
	sub_win.update()
	screen.grid(column=0,row=0)
	screen.update()

	bottom.grid(column=0,row=1)
	bottom.update()
	
	kihu_bot.grid(column=0,row=0)
	kihu_bot.update()
	restart_bot.grid(column=1,row=0)
	restart_bot.update()
	quit_bot.grid(column=2,row=0)
	quit_bot.update()

	score.grid(column=1,row=0)
	score.update()

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
		msg = Message(sub_win, text="棋譜") #ここに棋譜を貼る
		msg.pack()
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


def Pass(PL,end_flag):
	global othello
	if end_flag:
		tkmsg.showinfo("ゲーム終了")
	else:
		tkmsg.showinfo('パス',PL + 'パスです')

def show_result():
	global res_win,othello
	''' 
	結果表示画面
	'''
	if res_win is None or not res_win.winfo_exists():
		res_win = Toplevel()
		res_win.title("対戦結果")
		res_win.geometry("400x300")

		win_player = Label(res_win, text=othello.show_win, font=('Helvetica', '24', 'bold'))
		win_player.pack(pady = 20,anchor = N)

		display_score = Label(res_win, text=othello.res_score, font=('Helvetica', '18', 'bold'))
		display_score.pack(pady = 20)


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
#	Fboard = Frame(root)
	bottom = Frame(root)
	
	kihu_bot = Button(bottom,text ="棋譜(w)")
	undo_bot = Button(bottom,text ="Undo(u)")
	restart_bot = Button(bottom,text ="Restart(r)")
	quit_bot = Button(bottom,text ="Quit(q)")
	
	screen = Canvas(root, width=500, height=500, background="#222",highlightthickness=0)
	score = Canvas(root, width=200, height=500, background="#220",highlightthickness=0)

#	Fboard.pack()
	root.wm_title("Othello")
	screen.grid(column=0,row=0)
#ゲームの起動
	runGame()
#ボタン系の処理、ハンドラ処理
	screen.bind("<Button-1>", clickHandle)
	screen.bind("<Key>",keyHandle)
	screen.focus_set()
#ループ    
	root.mainloop()
""" 
root ---*---------------*--- screen
        |				|
		|               *--- bottom
        |               |
        |               *---score
        |
		*--- sub_win
		|
		|
		*---res_win
"""
