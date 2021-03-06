import numpy
import sys
import random
import csv

class Board:
    """
    オセロゲームのルールを記述するクラス
    """
    evaluate_Board = numpy.array([40, -12, 0, -1, -1, 0, -12, 40,
                                -12, -15, -3, -3, -3, -3, -15, -12,
                                0, -3, 0, -1, -1, 0, -3, 0,
                                -1, -3, -1, -1, -1, -1, -3, -1,
                                -1, -3, -1, -1, -1, -1, -3, -1,
                                0, -3, 0, -1, -1, 0, -3, 0,
                                -12, -15, -3, -3, -3, -3, -15, -12,
                                40, -12, 0, -1, -1, 0,-12, 40])
    ''' 評価ボード '''
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
        """
        ゲーム終了時の処理
        終了フラグを立てる
        スコアの計算
        結果のCUI上への表示
        """
        #片方が盤面に打てなくなると終了してしまうので何とかしようね
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
        パス判定時のターン遷移及び連続パスの終了判定　
        """
        self.show_record()

        if self.PL_turn == 1:
            # Main.Pass("先手側",(self.PL1_pass == 1 and self.PL2_pass))
            #print("pass_PL1")
            self.PL1_pass = 1
        elif self.PL_turn == 2:
            # print("pass_PL2")
            # Main.Pass("後手側"(self.PL1_pass == 1 and self.PL2_pass))
            self.PL2_pass = 1

        if self.PL1_pass == 1 and self.PL2_pass == 1:
            #print("game_end")
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
                    copy = numpy.copy(self.board)
                    n = (b==3-stone).cumprod().sum()
                    if b.size <=n or b[n] != stone:
                         n = 0
                    t += n
                    if put:
                        b[:n] = stone
                    else:
                        copy[:n] = stone
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
                copy[p] = stone
                return copy
        
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
        プレイヤー動作
        石を置く
        パスの判定
        盤面埋まりによる終了の判定
         """
        self.put_checker(stone)
        for non_zero in numpy.nonzero(self.can_put): 
#            elif numpy.argmin(self.board) != 0: #盤面埋まり申した
#                self.game_end()
            if len(numpy.where(non_zero == (x + y*8))[0]) == 0: #置けやん場所指定したやつ 入力しなおさねば
                #print("そこ置けやん")
                return False
            elif len(non_zero) == 0: #一個も取れない場合
                self.Pass()
            else:
                self.put_decision(x,y,stone,True)
                self.kihu.append([stone,x,y,numpy.copy(self.board)])
                self.show_record()
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


    def evaluate(self,stone,put):
        """ 現在の盤面を渡された石で評価して最大のインデックスを返す """
        black = 0
        white = 0
        MAX = -500
        MAX_Index = list(put)
        
        for i in put:
            x = i%8
            y = i//8
            next_board = self.put_decision(x,y,stone,False)
            for j in range(8):
                for k in range(8):
                    if next_board[k + j*8] == 1:
                        black = black + Board.evaluate_Board[k + j*8]
                    elif next_board[k + j*8] == 2:
                        white = white + Board.evaluate_Board[k + j*8]

            if stone == 1: #COM先手
                if MAX < (black - white):
                    MAX = black - white
                    MAX_Index = list([])
                    MAX_Index.append(i)
                elif (MAX == (black - white)):
                    MAX_Index.append(i)

            elif stone == 2: #COM後手 
                if MAX < (white - black):
                    MAX = white - black
                    MAX_Index = list([])
                    MAX_Index.append(i)
                elif(MAX == (white - black)):
                    MAX_Index.append(i)
            black = 0
            white = 0
        return MAX_Index



    def com_search(self,stone): #AI様やぞ
        """ 
        コンピュータ動作
        静的評価値を持つ各マスから各石の評価値を出し、差が一番大きくなる手を選択
        残り10手は一番多く取れるものから選択
        パスの判定
        盤面埋まりによる終了の判定
        """
        self.put_checker(stone)
        for non_zero in numpy.nonzero(self.can_put):
            if len(non_zero) == 0: #一個も取れない場合
                self.Pass()
            if len(non_zero) != 0:
#                maxIndex = [i for i, x in enumerate(self.can_put) if x == max(self.can_put)]
#                random_pos = random.choice(maxIndex)
#                x = random_pos%8
#                y = random_pos//8
                for non_zero_b in numpy.nonzero(self.board):
                    if len(non_zero_b) >= 54:
                        #print("AI_rand")
                        maxIndex = [i for i, x in enumerate(self.can_put) if x == max(self.can_put)]
                        random_pos = random.choice(maxIndex)
                    else:
                        #print("AI_board")
                        random_pos = random.choice(self.evaluate(stone,non_zero))
                x = random_pos%8
                y = random_pos//8

                self.put_decision(x,y,stone,True)
                self.kihu.append([stone,x,y,numpy.copy(self.board)])
                self.show_record()
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


        #---------今度こそ棋譜表示させたいンゴォｗｗｗｗ------------
    def show_record(self):
        ''' 
        CUI上での棋譜表示の操作
        CSVへの棋譜の出力
        '''
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
                #print (str(len(self.kihu))+ ishi + " :  "+str(x))
            else:
                x = "abcdefgh" [k[1]] + str(k[2]+1)
                #print (str(len(self.kihu)) + ishi + " :  "+str(x))
            
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
            # 盤面情報もコピー
            # self.csv_data.append([i+1,p,x,numpy.copy(k[3])])

            self.csv_data.append([i+1,p,x])
            i = i + 1


        with open('data.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            header =  ["ターン数","プレイヤー","手"]
            writer.writerow(header)
            writer.writerows(self.csv_data)
    #-----------------------------------------------------

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
    board = Board(1) #0: PVP 1: CvP 2:PvC
    board.play_game_CUI()

