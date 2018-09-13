#/usr/bin/python3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import rule
import time
import numpy
import os
import csv

class Main: 
    #running = False

	def __init__(self):
		self.sub_win = None
		self.res_win = None
		self.pass_win = None
		self.COM = -1
		self.root = Tk()
		self.root.resizable(0,0)
		self.bottom = Frame(self.root)
        
		self.kihu_bot = Button(self.bottom,text ="棋譜(w)",command = self.create_new_screen)
		self.restart_bot = Button(self.bottom,text ="Restart(r)",command = self.restart)
		self.quit_bot = Button(self.bottom,text ="Quit(q)",command = self.root.destroy)
		self.screen = Canvas(self.root, width=500, height=500, background="#222",highlightthickness=0)
		self.score = Canvas(self.root, width=135, height=500, background="ivory3",highlightthickness=0)

		self.root.wm_title("Othello")
		self.screen.grid(column=0,row=0)
    #ゲームの起動
		self.runGame()
    #ボタン系の処理、ハンドラ処理
		self.screen.bind("<Button-1>", self.clickHandle)
		self.screen.bind("<Key>",self.keyHandle)
    #ループ    
		self.root.mainloop()

	def clickHandle(self,event):
		xMouse = event.x
		yMouse = event.y
		x = -1
		y = -1
		BOARD_SIZE = 8 + 1
		column_width = self.screen.winfo_width() / BOARD_SIZE
		row_height = self.screen.winfo_height() / BOARD_SIZE

		if self.running:
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
							if (self.COM == 1) or (self.COM == 2):
								if self.COM != self.othello.PL_turn:
									self.othello.put_stone(x,y,self.othello.PL_turn)
									self.operate_othello()
									if self.sub_win.winfo_exists():
										self.sub_win_Update()	
								
								while self.COM == self.othello.PL_turn:
									self.othello.com_search(self.othello.PL_turn)
									self.operate_othello()
									if self.sub_win.winfo_exists():
										self.sub_win_Update()
									if self.othello.finish or len(numpy.where(self.othello.board == 0)) == 0:
    										break
	                
							elif self.COM == 0:
								if self.othello.put_stone(x,y,self.othello.PL_turn):
									self.operate_othello()
									# print(self.sub_win)
									if self.sub_win.winfo_exists():
										self.sub_win_Update()

					if self.othello.finish or len(numpy.where(self.othello.board == 0)) == 0:
							self.othello.game_end()
							self.show_result()

		else:
			if 300<= yMouse <=350:
				if 25<= xMouse <=155:
					self.COM = 0
					self.playGame()
				elif 180<=xMouse<=310:
					self.COM = 2
					self.playGame()
				elif 335<=xMouse<=465:
					self.COM = 1
					self.playGame()



	def operate_othello(self):
		BOARD_SIZE = 8 + 1
		column_width = self.screen.winfo_width() / BOARD_SIZE
		row_height = self.screen.winfo_height() / BOARD_SIZE
        
		self.othello.put_checker(self.othello.PL_turn)
		if not len(self.othello.kihu) == 0:
			i = len(self.othello.kihu) - 1
			while True:
				if len(self.othello.kihu[i]) == 4:
					k = self.othello.kihu[i]
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
						self.screen.create_rectangle(x1,y1,x2,y2,fill = 'ivory3')
						if not c == r: 
							if c == 0:
								self.screen.create_text(x1+25,y1+25,anchor="c",text=str(r),font=("Consolas", 15),fill="black",tag = "board")
							else:
								column = "abcdefgh" [int(c)-1]
								self.screen.create_text(x1+25,y1+25,anchor="c",text=str(column),font=("Consolas", 15),fill="black",tag = "board")
				else:
						self.screen.create_rectangle(x1,y1,x2,y2,fill = 'dark green')
						if self.othello.can_put[(c-1)+(r-1)*8] > 0:
							self.screen.create_rectangle(x1,y1,x2,y2,fill = 'pale green')
						if not len(self.othello.kihu) == 0:
							if (c == k[1] + 1  and r == k[2] + 1 and self.running ):
								self.screen.create_rectangle(x1,y1,x2,y2,fill = 'red')
				if c != 0 and r !=0:    
					if self.othello.board[(c-1)+(r-1)*8]==1:
						self.screen.create_oval(x1,y1,x2,y2,fill = 'black', tag = "stone")
					elif self.othello.board[(c-1)+(r-1)*8]==2:
						self.screen.create_oval(x1,y1,x2,y2,fill = 'white', tag = "stone")	
		if((self.othello.PL1_pass == 1 and 3 - self.othello.PL_turn == 1) or (self.othello.PL2_pass == 1 and 3 - self.othello.PL_turn == 2)):
				if not len(numpy.where(self.othello.board == 0)) == 0:
					self.Pass_message()
					self.othello.put_checker(self.othello.PL_turn)
					# 2連パス判定
					for non_zero in numpy.nonzero(self.othello.can_put):
						if len(non_zero) == 0: #一個も取れない場合
							self.othello.Pass()
							self.Pass_message()

		self.screen.grid(column=0,row=0)
		self.screen.update()
		self.score_show()
	def restart(self):
                self.sub_win.destroy()
                self.runGame()
	def score_show(self):
		''' 
		現在の得点計算,score表示
 		'''
		self.othello.black_sum = 0
		self.othello.white_sum = 0
		for c in range(len(self.othello.board)):
				if self.othello.board[c] == 1:
					self.othello.black_sum = self.othello.black_sum + 1
				elif self.othello.board[c] == 2:
					self.othello.white_sum = self.othello.white_sum + 1
		
		self.score.delete("sum")
		self.score.create_text(70,150,anchor="c",text=self.othello.sente[self.COM],font=("Consolas", 20),fill="#000",tag = "sum")
		self.score.create_text(40,200,anchor="c",text="●",font=("Consolas", 40),fill="#000",tag = "sum")
		self.score.create_text(70,202,anchor="c",text= " :" + str(self.othello.black_sum),font=("Consolas", 20),fill="#000",tag = "sum")
		self.score.create_text(70,350,anchor="c",text=self.othello.gote[self.COM],font=("Consolas", 20),fill="#000",tag = "sum")
		self.score.create_text(40,400,anchor="c",text="○",font=("Consolas", 40),fill="#000",tag = "sum")
		self.score.create_text(70,402,anchor="c",text= " :" + str(self.othello.white_sum),font=("Consolas", 20),fill="#000",tag = "sum")

		

	def show_othello_board(self):
		BOARD_SIZE = 8 + 1
		column_width = self.screen.winfo_width() / BOARD_SIZE
		row_height = self.screen.winfo_height() / BOARD_SIZE
		for c in range(BOARD_SIZE):
			for r in range(BOARD_SIZE):
				x1 = c * (column_width)
				y1 = r * (row_height)
				x2 = x1 + (column_width)
				y2 = y1 + (row_height)
				if c == 0 or r == 0:
					xpos = x1+column_width
					ypos = y1+row_height + row_height/2
					self.screen.create_rectangle(x1,y1,x2,y2,fill = 'ivory3')
				else:
					self.screen.create_rectangle(x1,y1,x2,y2,fill = 'green')
        
		self.screen.grid(column=0,row=0)
		self.screen.update()

		self.bottom.grid(column=0,row=1)
		self.bottom.update()

		self.kihu_bot.grid(column=0,row=0)
		self.kihu_bot.update()
		self.restart_bot.grid(column=1,row=0)
		self.restart_bot.update()
		self.quit_bot.grid(column=2,row=0)
		self.quit_bot.update()

		self.score.grid(column=1,row=0)
		self.score.update()

	def choose(self):
                try:
                        if self.listbox.curselection()[0] == 0:
                                self.othello = rule.Board(self.COM)
                                #print("pass")
                        elif "pass" !=  self.othello.kihu[self.listbox.curselection()[0]][1]:
                                for i in range(len(self.othello.kihu) - self.listbox.curselection()[0]):
                                        self.othello.PL_turn = int(self.othello.kihu.pop()[0])
                                        if self.othello.PL_turn == 1:
                                                self.othello.PL2_pass = 0
                                        elif self.othello.PL_turn == 2:
                                                self.othello.PL1_pass = 0
                                self.othello.board = numpy.copy(self.othello.kihu[-1][3])	
                except IndexError:
                        value = None
                
                self.running = True
                if not self.res_win is None:
                        self.res_win.destroy()
                self.sub_win_Update()
                self.screen.delete("stone")
                self.show_othello_board()
                self.operate_othello()
                if self.sub_win.winfo_exists():
                        self.sub_win_Update()


	def sub_win_Update(self):
		ishi = str("")
		self.listbox.delete (first = 0, last=self.listbox.size())

#------------------棋譜の表示-------------------------------------------------
		for i,kihu in zip(range(len(self.othello.kihu)),self.othello.kihu):
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
				self.listbox.insert(END, str(i+1)+" :  "+ ishi + " " + str(zahyou))
#----------------------------------------------------------------------------	
		self.listbox.pack(side=LEFT, fill=BOTH)
		self.scrollbar.config(command=self.listbox.yview)
		self.sub_win.update()
		self.screen.grid(column=0,row=0)
		self.screen.update()

		self.bottom.grid(column=0,row=1)
		self.bottom.update()
		
		self.kihu_bot.grid(column=0,row=0)
		self.kihu_bot.update()
		self.restart_bot.grid(column=1,row=0)
		self.restart_bot.update()
		self.quit_bot.grid(column=2,row=0)
		self.quit_bot.update()

		self.score.grid(column=1,row=0)
		self.score.update()

	def create_new_screen(self):
		if self.sub_win is None or not self.sub_win.winfo_exists():
			self.sub_win=Toplevel()
			self.sub_win.title("棋譜")

			w = 150 # width for the Tk root
			h = 500 # height for the Tk root

			#親画面の情報
			ws = self.root.winfo_screenwidth() # width of the screen
			hs = self.root.winfo_screenheight() # height of the screen
			#親からの相対位置
			x = (ws/2) - (w/2)
			y = (hs/2) - (h/2)
			self.sub_win.geometry("%dx%d+%d+%d" % (w, h, x, y))
			self.msg = Message(self.sub_win, text="棋譜") #ここに棋譜を貼る
			self.msg.pack()
			self.scrollbar = Scrollbar(self.sub_win)
			self.scrollbar.pack(side=RIGHT, fill=Y)

			self.buttonFrame = Frame(self.sub_win)
			self.buttonFrame.pack(side=BOTTOM)

			self.chooseButton = Button(self.buttonFrame, text="Choose", command=self.choose)
			self.chooseButton.pack()

			self.listbox = Listbox(self.sub_win, yscrollcommand=self.scrollbar.set, selectmode  = SINGLE)

			self.sub_win_Update()
            
	def keyHandle(self,event):
		symbol = event.keysym
		if symbol.lower()=="r"  and self.running: #rでリスタート
			self.runGame()
		elif symbol.lower()=="q": #qでおわおわり
			self.root.destroy()
		elif symbol.lower()=="w" and self.running:
			self.create_new_screen()
		
        
	def runGame(self):
		self.running = False
		self.sub_win = None
		self.screen.create_text(250,203,anchor="c",text="オセロにしたい\nしたくない？",font=("Consolas", 50),fill="#fff")
		for i in range(3):
			self.screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
		#これいる?-----------------------------------------------------------------------------------------------
		# self.screen.create_text(125,400,anchor="c",text="Player1 names", font=("Consolas", 15),fill="#b29600")
		# self.name_P1 = ttk.Entry(self.screen,text = "")
		# self.name_P1.place(x = 50,y = 425,width = 150)

		# self.screen.create_text(375,400,anchor="c",text="Player2 names", font=("Consolas", 15),fill="#b29600")
		# self.name_P2 = ttk.Entry(self.screen,text = "")
		# self.name_P2.place(x = 300,y = 425,width = 150)
		#いらない------------------------------------------------------------------------------------------------

		self.screen.create_text(90,330,anchor="c",text="PvP", font=("Consolas", 25),fill="#b29600")
		self.screen.create_text(245,330,anchor="c",text="PvC", font=("Consolas", 25),fill="#b29600")
		self.screen.create_text(400,330,anchor="c",text="CvP", font=("Consolas", 25),fill="#b29600")

		self.screen.update()


	def Pass_message(self):
		''' Passメッセージ呼び出し'''
		if(self.othello.PL1_pass == self.othello.PL2_pass):
			messagebox.showinfo('ゲーム終了','ゲーム終了！')
		elif(self.othello.PL1_pass == 1):
			messagebox.showinfo('パス','先手側パス')
		else:
			messagebox.showinfo('パス','後手側パス')
    			

	def file_write(self):
			""" 棋譜の指定ファイルへの保存 """
			if not self.res_file.get() == "":
				name = self.res_file.get() + ".csv"
				dirlist = os.listdir('./')
				if not "history" in dirlist:
					os.mkdir("history")
				path = "./history/"
				for x in os.listdir(path):
					if x == name:
						messagebox.showinfo('保存失敗','同名のファイルまたはディレクトリが既に存在します (エラー E001)')
						self.res_file.delete(0,END)
						return
				#print(path)
				with open( path + name, 'w') as file:
                                        record = csv.writer(file, lineterminator='\n')
                                        header = ["ターン数","プレイヤー","手"]
                                        record.writerow(header)
                                        record.writerows(self.othello.csv_data)
			self.res_file.delete(0,END)
			self.res_win.destroy()
                        

	def show_result(self):
		''' 
		結果表示画面
		'''
		if self.res_win is None or not self.res_win.winfo_exists():
			if (self.othello.black_sum > self.othello.white_sum):
				show_win = self.othello.sente[self.COM] + " Win "
			elif (self.othello.white_sum > self.othello.black_sum):
				show_win = self.othello.gote[self.COM] + " Win "
			else:
				show_win = "draw"
			
			self.res_win = Toplevel()
			self.res_win.title("対戦結果")
			self.res_win.geometry("400x300")

			self.win_player = Label(self.res_win, text=show_win, font=('Helvetica', '24', 'bold'))
			self.win_player.pack(pady = 20,anchor = N)

			self.display_score = Label(self.res_win, text=self.othello.res_score, font=('Helvetica', '18', 'bold'))
			self.display_score.pack(pady = 20)

			self.res_file = ttk.Entry(self.res_win,text = "")
			self.res_file.pack()
			self.write_button = Button(self.res_win,text = "record!",width = 10, command = self.file_write)
			self.write_button.pack()
		
		self.othello.finish = False


	def playGame(self):
        
		self.running = True
		self.screen.delete(ALL)

		self.othello = rule.Board(self.COM)

		#これいる？？？？？？？？？？---------------------------
		# if not self.name_P1.get() == "":
		# 	self.othello.sente[self.COM] = self.name_P1.get()
		# if not self.name_P2.get() == "":
		# 	self.othello.gote[self.COM] =  self.name_P2.get()
		#self.name_P1.destroy()
		#self.name_P2.destroy()
		#----------------------------------------------------
		
		if not self.sub_win is None: 
                        if self.sub_win.winfo_exists():
                                self.sub_win.destroy()
		if not self.res_win is None:
                        if self.res_win.winfo_exists():
                                self.res_win.destroy()
    			
		self.create_new_screen() #棋譜用サブ画面表示 

		self.show_othello_board() #ゲームボードの表示
		#オセロの駒表示

		self.operate_othello()
		self.running = True
		if self.COM == 1: #COMが先手の場合。クリック前に先に打つ
			time.sleep(1)
			self.othello.com_search(1)
			self.sub_win_Update()
			self.operate_othello()

if __name__ == '__main__':
    main = Main()
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
