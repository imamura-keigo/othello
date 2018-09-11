import numpy
import sys
import random
import csv

global file



class Board:    
    def __init__(self,x):
        """ 
        盤面初期化
         """
        self.board = numpy.zeros(64,dtype=int) #0:空白
        self.cp_board = numpy.zeros(64,dtype=int)
        self.can_put = numpy.zeros(64,dtype=int) #0:置けない 1:置ける
        self.PL1_pass = 0
        self.PL2_pass = 0
        self.board[27] = self.board[36] = 1 #1:黒
        self.board[28] = self.board[35] = 2 #2:白
        self.PL_turn = 1
        self.running = True
        self.x_before = 0
        self.y_before = 0
        self.com = x #0: PvP 1:CvP 2:PvC
        self.kihu = []
        self.csv_data = []


    def game_end(self):
        """ ゲーム終了なんよなぁ """
        self.running = False
        print(self.board.argmin())
        print(self.board)
        print("finish")

    def Pass(self):
        """ 
        パスなんだよなぁ...　
        """
        #print("ぱぁすPL_turn", self.PL_turn)

        self.show_record()

        if self.PL_turn == 1:
            self.PL1_pass = 1
            print("Pass1")
        elif self.PL_turn == 2:
            self.PL2_pass = 1
            print("Pass2")

        if self.PL1_pass == 1 and self.PL2_pass == 1:
            print("pass")
            self.game_end()

        self.PL_turn = 3 - self.PL_turn

    def put_decision(self,x,y,stone,put): #置ける場所の判定
        """ 
        必要な情報は八方の情報を取得⇒[-9,-8,-7,-1,1,7,8,9にずれたものを見る]
        x,yは座標を示し、stoneは黒または白を指す。putは実際に置くか否か。(盤面の探索に必要)
         """
        t = 0
        p = x + (y * 8)
        for di, fi in zip([-1, 0, 1], [x, 7, 7-x]):
            for dj, fj in zip([-8, 0, 8], [y, 7, 7-y]):
                if not di == dj == 0:
                    b = self.board[p+di+dj::di+dj][:min(fi, fj)]
                    n = (b==3-stone).cumprod().sum()
                    if b.size <=n or b[n] != stone:
                         n = 0
                    t += n
                    if put:
                        b[:n] = stone
        if (self.board[p]==0 and t > 0):
            if put:
                self.PL_turn = 3 - self.PL_turn
                self.board[p] = stone
                if stone == 1:
                    self.PL1_pass = 0
                elif stone == 2:
                    self.PL2_pass = 0
            else:
                self.can_put[p] = t
        
    def put_checker(self,stone):
        """ 
        盤面を全探索する
         """
        self.can_put = numpy.zeros(64,dtype=int) #0:置けない 1以上:置ける
        for x in range(8):
            for y in range(8):
                self.put_decision(x,y,stone,False)
            

    def put_stone(self,x,y,stone): #石を置く
        """ 
        石を置くついでにパスの判定
        """
        self.put_checker(stone)
        for non_zero in numpy.nonzero(self.can_put): 
#            elif numpy.argmin(self.board) != 0: #盤面埋まり申した
#                self.game_end()
            if len(numpy.where(non_zero == (x + y*8))[0]) == 0: #置けやん場所指定したやつ 入力しなおさねば
                print("そこ置けやん")
                return False
            else:
                self.put_decision(x,y,stone,True)
                self.kihu.append([stone,x,y,numpy.copy(self.board)])
                self.show_record()
        #print("PL_turn_put_stone", self.PL_turn)
        #次の手番で打てるか判定
        self.put_checker(stone)
        for non_zero in numpy.nonzero(self.can_put): 
            if self.board.min() != 0: #盤面埋まり申した
                print("盤面埋まり_COM")
                self.game_end()
            elif len(non_zero) == 0: #一個も取れない場合
                self.kihu.append([stone,-1,-1,numpy.copy(self.board)])
                print("put_stone_pass")
                self.Pass()
        return True
        
    def printer(self): #CUI盤面表示
        """ 
        CUIの盤面表示
        """
        j = 0
        print ('  ',end = "")
        for i in range(8):
            print (i,'',end = "")
        print("x")
        for i in range(8):
            print(j,' '.join('.BW'[j] for j in self.board[i*8:][:8]))
            j = j + 1
        print("y")
        print(self.kihu)
        print()
#        for i in range(8):
#            for j in self.can_put[i*8:][:8]:
#                print(' ',j,end ="")
#            print()

    def com_search(self,stone): #AI様やぞ
        """ 
        AI様。一番多くとれる場所にランダムに置くだけ。うんち
        """
        global GUI 
        self.put_checker(stone)
        for non_zero in numpy.nonzero(self.can_put):
            if len(non_zero) == 0: #一個も取れない場合
                return False
            if len(non_zero) != 0:
                maxIndex = [i for i, x in enumerate(self.can_put) if x == max(self.can_put)]
                random_pos = random.choice(maxIndex)
                x = random_pos%8
                y = random_pos//8
                self.x_before = x
                self.y_before = y
                self.put_decision(x,y,stone,True)
                self.kihu.append([stone,x,y,numpy.copy(self.board)])
                self.show_record()
        #print("PL__turn_com_search", self.PL_turn)
        #次の手番で打てるか判定
        self.put_checker(self.PL_turn) 
        for non_zero in numpy.nonzero(self.can_put): 
            if (self.board.min()) != 0: #盤面埋まり申した
                print("盤面埋まり_COM")
                self.game_end()
            elif len(non_zero) == 0: #一個も取れない場合
                self.kihu.append([stone,-1,-1,numpy.copy(self.board)])
                print("com_search_pass")
                print("non_zero",non_zero)
                self.Pass()

        return True

    #---------今度こそ棋譜表示させたいンゴォｗｗｗｗ------------
    def show_record(self):
        global file
        ishi = str('')
        x = str('')
        p = ''
        
        k = self.kihu[-1] #棋譜の最新情報(リストの一番後ろ)
        i = 0
        self.csv_data = []
        if len(self.kihu)!=0: 
            if k[0] == 1:
                ishi = '●'
            elif k[0] == 2:
                ishi = '○'
            else:
                print("石がおかしい")

            if k[1] == -1:
                x = "Pass"
                print (str(len(self.kihu))+ ishi + " :  "+str(x))
            else:
                x = "abcdefgh" [k[1]] + str(k[2]+1)
                print (str(len(self.kihu)) + ishi + " :  "+str(x))
            
        for k in self.kihu:
            if self.com == 0:
                if k[0] == 1:
                    p = "Player1"
                elif k[0] == 2:
                    p = "Player2"
                else:
                    print("error_show_record")
                
            elif self.com == 1:
                if k[0] == 1:
                    p = "COM"
                elif k[0] == 2:
                    p = "Player1"
            
            elif self.com == 2:
                if k[0] == 1:
                    p = "Player1"
                elif k[1] == 2:
                    p = "COM"

            else:
                print("error_show_record2")
            
            if k[1] == -1:
                x = "Pass"
                # print (str(i+1)+ ishi + " :  "+str(x))
            else:
                x = "abcdefgh" [k[1]] + str(k[2]+1)
                # print (str(i+1) + ishi + " :  "+str(x))
            self.csv_data.append([i+1,p,x,numpy.copy(k[3])])
            i = i + 1


        with open('data.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(self.csv_data)
    #-----------------------------------------------------

    def Undo(self,com_player):
        i = 1
        if not len(self.kihu) == 0:
            while True:
                if com_player == 0:
                    if len(self.kihu[0-i]) == 4:
                        for nyaan in range(i):
                            self.kihu.pop()
                        break
                    else:
                        i = i + 1 
                else:
                    if len(self.kihu[0-i]) == 4 and com_player != self.PL_turn:
                        for nyaan in range(i-1):
                            self.kihu.pop()
                        break
                    else:
                        i = i + 1 
                    
    def play_game_CUI(self):
        """ CUI上の入力 """
        self.printer()
        while(self.running):

            self.put_checker(self.PL_turn)

            if self.com == 1 and self.PL_turn == 1 and self.running == True:
                self.com_search(self.PL_turn)
                self.printer()    

            print("x >> ", end ="")
            x = int(input())
            print("y >> ", end ="")
            y = int(input())
            self.put_stone(x,y,self.PL_turn) 
            
            if self.com == 2 and self.PL_turn == 2 and self.running == True:
                self.printer()    
                self.com_search(self.PL_turn)
            
            self.printer()


if __name__ == '__main__':
    board = Board(1)
    with open('data.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows("手数 " + "ターンプレイヤー "+"1行目" )
    board.play_game_CUI()
