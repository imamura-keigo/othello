import numpy
import sys
import random


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
        self.board[28] = self.board[35] = 1 #1:黒
        self.board[27] = self.board[36] = 2 #2:白
        self.PL_turn = 1
        self.running = True
        self.com = x #0: PvP 1:CvP 2:PvC CUI起動とかUndoに必要
        self.kihu = []
        self.finish = False
        # 特定計算、勝利判定用
        self.black_sum = 0
        self.white_sum = 0
        self.sente = ["Player1" , "COM", "Player1"]
        self.gote = ["Player2" , "Player1", "COM"]
        self.res_score = ""

    def game_end(self):
        """ ゲーム終了なんよなぁ """ #片方が盤面に打てなくなると終了してしまうので何とかしようね
        # self.running = False
        # print(self.board.argmin())
        # print(self.board)
        self.finish = True
        self.black_sum = 0
        self.white_sum = 0
        ''' 石集計 '''
        for c in range(len(self.board)):
                if self.board[c] == 1:
                    self.black_sum = self.black_sum + 1
                elif self.board[c] == 2:
                    self.white_sum = self.white_sum + 1

        # スコア計算、勝敗判定
        self.res_score = '●' + str(self.black_sum) + ' - ' + str(self.white_sum) + '○'
        ''' from main2 import show_result
        show_result(self.show_win,self.res_score) '''

         
    def Pass(self):
        """ 
        パスなんだよなぁ...　
        """
        if self.PL_turn == 1:
            # Main.Pass("先手側",(self.PL1_pass == 1 and self.PL2_pass))
            print("pass_PL1")
            self.PL1_pass = 1
        elif self.PL_turn == 2:
            # print("pass_PL2")
            # Main.Pass("後手側"(self.PL1_pass == 1 and self.PL2_pass))
            self.PL2_pass = 1

        if self.PL1_pass == 1 and self.PL2_pass == 1:
            print("game_end")
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
            elif len(non_zero) == 0: #一個も取れない場合
                self.Pass()
            else:
                self.put_decision(x,y,stone,True)
                self.kihu.append([stone,x,y,numpy.copy(self.board)])
        
        #次の手番で打てるか判定
        self.put_checker(self.PL_turn)
        for non_zero in numpy.nonzero(self.can_put): 
            if self.board.min() != 0: #盤面埋まり申した
                #print("盤面埋まり_COM")
                self.game_end()
            elif len(non_zero) == 0: #一個も取れない場合
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
#        print(self.kihu)
        print()
#        for i in range(8):
#            for j in self.can_put[i*8:][:8]:
#                print(' ',j,end ="")
#            print()

    def com_search(self,stone): #AI様やぞ
        """ 
        AI様。一番多くとれる場所にランダムに置くだけ。うんち
        """
        self.put_checker(stone)
        for non_zero in numpy.nonzero(self.can_put):
            if len(non_zero) == 0: #一個も取れない場合
                self.Pass(stone)
            if len(non_zero) != 0:
                maxIndex = [i for i, x in enumerate(self.can_put) if x == max(self.can_put)]
                random_pos = random.choice(maxIndex)
                x = random_pos%8
                y = random_pos//8
                self.put_decision(x,y,stone,True)
                self.kihu.append([stone,x,y,numpy.copy(self.board)])
        
        #次の手番で打てるか判定
        self.put_checker(self.PL_turn) 
        for non_zero in numpy.nonzero(self.can_put): 
            if (self.board.min()) != 0: #盤面埋まり申した
                # print("盤面埋まり_COM")
                self.game_end()
            elif len(non_zero) == 0: #一個も取れない場合
                self.Pass()
        if len(numpy.where(self.board == 0)) == 0:
            self.game_end()




    def Undo(self):
        if len(self.kihu) == 1 or len(self.kihu) == 0:
            self.board = numpy.zeros(64,dtype=int) #0:空白
            self.cp_board = numpy.zeros(64,dtype=int)
            self.board[27] = self.board[36] = 1 #1:黒
            self.board[28] = self.board[35] = 2 #2:白
            self.PL_turn = 1
        elif len(self.kihu) != 0:
            pop = self.kihu.pop()
            last = self.kihu[-2]
            PL_turn = last[0]
            #print("pop  ", pop)
            #print("pop  ", pop[0])
            if self.com == pop[0]:
                self.Undo()
            else:
                self.board = last[3]

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
            if x == 10:
                self.Undo()
            print("y >> ", end ="")
            y = int(input())
            self.put_stone(x,y,self.PL_turn) 
            
            if self.com == 2 and self.PL_turn == 2 and self.running == True:
                self.printer()    
                self.com_search(self.PL_turn)
            
            self.printer()


if __name__ == '__main__':
    board = Board(1) #0: PVP 1: CvP 2:PvC
    board.play_game_CUI()

