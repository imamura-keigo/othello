#/usr/bin/python3
from tkinter import *
import tkinter.messagebox as tkmsg
import rule 
import time

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
        
        self.kihu_bot = Button(self.bottom,text ="棋譜(w)")
        self.undo_bot = Button(self.bottom,text ="Undo(u)")
        self.restart_bot = Button(self.bottom,text ="Restart(r)")
        self.quit_bot = Button(self.bottom,text ="Quit(q)")
        
        self.screen = Canvas(self.root, width=500, height=500, background="#222",highlightthickness=0)
        self.score = Canvas(self.root, width=200, height=500, background="#220",highlightthickness=0)

        self.root.wm_title("Othello")
        self.screen.grid(column=0,row=0)
    #ゲームの起動
        self.runGame()
    #ボタン系の処理、ハンドラ処理
        self.screen.bind("<Button-1>", self.clickHandle)
        self.screen.bind("<Key>",self.keyHandle)
        self.screen.focus_set()
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
                                    self.sub_win_Update()	
                                while self.COM == self.othello.PL_turn:
                                    self.othello.com_search(self.othello.PL_turn)
                                    self.operate_othello()
                                    self.sub_win_Update()
                                self.sub_win_Update()	
                    
                            elif self.COM == 0:
                                if self.othello.put_stone(x,y,self.othello.PL_turn):
                                    self.operate_othello()
                                    self.sub_win_Update()
            if self.othello.finish:
                    self.show_result()

        else:
            if 300<= yMouse <=350:
                if 25<=xMouse<=155:
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
                        self.screen.create_rectangle(x1,y1,x2,y2,fill = '#222')
                else:
                        self.screen.create_rectangle(x1,y1,x2,y2,fill = 'green')
                        if self.othello.can_put[(c-1)+(r-1)*8] > 0:
                            self.screen.create_rectangle(x1,y1,x2,y2,fill = 'pale green')
                        if not len(self.othello.kihu) == 0:
                            if (c == k[1] + 1  and r == k[2] + 1 and self.running ):
                                self.screen.create_rectangle(x1,y1,x2,y2,fill = 'red')
                if c != 0 and r !=0:    
                    if self.othello.board[(c-1)+(r-1)*8]==1:
                        self.screen.create_oval(x1,y1,x2,y2,fill = 'black')
                    elif self.othello.board[(c-1)+(r-1)*8]==2:
                        self.screen.create_oval(x1,y1,x2,y2,fill = 'white')

        self.screen.grid(column=0,row=0)
        self.screen.update()

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
                    self.screen.create_rectangle(x1,y1,x2,y2,fill = '#222')
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
            elif "pass" !=  self.othello.kihu[self.listbox.curselection()[0]][1]:
                for i in range(len(self.othello.kihu) - self.listbox.curselection()[0]):
                    self.othello.PL_turn = int(self.othello.kihu.pop()[0])
                self.othello.board = self.othello.kihu[-1][3]	
        except IndexError:
            value = None
        self.sub_win_Update()
        self.screen.delete("stone")
        self.show_othello_board()
        self.operate_othello()


    def sub_win_Update(self):

        self.listbox.delete (first = 0, last=self.listbox.size())
        for kihu in self.othello.kihu:
            self.listbox.insert(END, str(kihu))
                
        self.listbox.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.listbox.yview)
        self.sub_win.update()

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
        elif symbol.lower()=="u" and self.running:
                print("undo")
                self.othello.Undo()
        
    def runGame(self):
        self.running = False
        
        self.screen.create_text(250,203,anchor="c",text="オセロにしたい\nしたくない？",font=("Consolas", 50),fill="#fff")
        for i in range(3):
            self.screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
        
        self.screen.create_text(90,330,anchor="c",text="PvP", font=("Consolas", 25),fill="#b29600")
        self.screen.create_text(245,330,anchor="c",text="PvC", font=("Consolas", 25),fill="#b29600")
        self.screen.create_text(400,330,anchor="c",text="CvP", font=("Consolas", 25),fill="#b29600")

        self.screen.update()


    def Pass(self,PL):
        ''' Passメッセージ呼び出し
        rule.py Pass()内から呼び出し '''
        self.tkmsg.showinfo('パス',PL + 'パスです')

    def show_result(self):
        ''' 
        結果表示画面
        '''
        if self.res_win is None or not self.res_win.winfo_exists():
            self.res_win = Toplevel()
            self.res_win.title("対戦結果")
            self.res_win.geometry("400x300")

            self.win_player = Label(self.res_win, text=othello.show_win, font=('Helvetica', '24', 'bold'))
            self.win_player.pack(pady = 20,anchor = N)

            self.display_score = Label(self.res_win, text=othello.res_score, font=('Helvetica', '18', 'bold'))
            self.display_score.pack(pady = 20)


    def playGame(self):
        
        self.running = True
        self.screen.delete(ALL)

        self.othello = rule.Board(self.COM)

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


