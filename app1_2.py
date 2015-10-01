from tkinter import *
import random
import time
import sys



#window, canvas
tk = Tk()
tk.title("Python3  AI Othello")
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, bg = 'beige', width = 500, height = 700,bd = 0, highlightthickness = 0)
score_text_id = canvas.create_text(150, 350,text = ('COMPUTER:      HUMAN:'),
                           font = ('Helvetica', 20), fill = 'black', state = 'normal')
score_text_id1 = canvas.create_text(170, 350, text = ('2'),
                                    font = ('Helvetica', 20), fill = 'black', state = 'normal')
score_text_id2 = canvas.create_text(290, 350, text = ('2'),
                                    font = ('Helvetica', 20), fill = 'black', state = 'normal')


#menubar
menubar = Menu(tk)
tk.configure(menu = menubar)
games = Menu(menubar, tearoff = True)
color = Menu(menubar, tearoff = True)
Pass = Menu(menubar, tearoff = True)
menubar.add_cascade(label="Games", underline = 0, menu=games)
menubar.add_cascade(label="Color", underline = 0, menu=color)
menubar.add_cascade(label="Pass", underline = 0, menu=Pass)

#Pass variable
globalpass = 0



#grid
class Grid:
    def __init__(self, canvas):
        self.canvas = canvas
        self.grid_id = self.canvas.create_rectangle(0, 0, 300, 300, fill = 'green')
        for x in range(0,10):
            self.canvas.create_line(x*30+30, 0, x*30+30, 300)
        for y in range(0,10):
            self.canvas.create_line(0, y*30+30, 300, y*30+30)

        
        
                    
                    
                    
                    
                
        
        
        
        
#cell
class Cell:
    def __init__(self,canvas):
        self.canvas = canvas
        
        self.cell_state = [0]*100
        self.cell_id = [0]*100
        #This id is for cell_state and cell_id
        self.id = 0
        #click point x and y    
        self.pointX = 0
        self.pointy = 0
        self.click_cell = 0
        self.humanTrun = False
        self.click_ok = False
        #global label_board
        self.canvas.bind_all('<Button-1>',self.checkClick)
        for y in range(0,10):
            for x in range(0,10):
                self.cell_id[self.id] = self.canvas.create_rectangle(x*30, y*30, x*30+30, y*30+30, fill = 'green')
                self.id += 1
            
        for x in range(0,10):       
            self.canvas.itemconfig(self.cell_id[x], fill = 'navy', outline = 'navy')
            self.cell_state[x] = 9
        for x in range(0,10):
            self.canvas.itemconfig(self.cell_id[x*10], fill = 'navy',outline = 'navy')
            self.cell_state[x*10] = 9
        for x in range(0,10):
            self.canvas.itemconfig(self.cell_id[x*10+9], fill = 'navy',outline = 'navy')
            self.cell_state[x*10+9] = 9
        for x in range(0,10):
            self.canvas.itemconfig(self.cell_id[90+x], fill = 'navy',outline = 'navy')
            self.cell_state[90+x] = 9

        for x in range(8):
            self.canvas.create_text(30*x+45, 15,text=(label_board[x]), font = ('Helvetica', 20), fill = 'white')
        for x in range(8):
            self.canvas.create_text(285, 30*x+45,text=('%d' %(x+1)), font = ('Helvetica', 20), fill = 'white')
            
        self.canvas.itemconfig(self.cell_id[44], state = 'hidden')
        self.drawStone(44, 'white',2)
        
        self.canvas.itemconfig(self.cell_id[55], state = 'hidden')
        self.drawStone(55, 'white',2)
        
        
        self.canvas.itemconfig(self.cell_id[45], state = 'hidden')
        self.drawStone(45, 'black',1)
        
        
        self.canvas.itemconfig(self.cell_id[54], state = 'hidden')
        self.drawStone(54, 'black', 1)
        

        

    def drawStone(self,number,color,state):
        self.cell_id[number] = self.canvas.create_oval(self.canvas.coords(self.cell_id[number])[0], self.canvas.coords(self.cell_id[number])[1],
                                self.canvas.coords(self.cell_id[number])[2], self.canvas.coords(self.cell_id[number])[3],
                                fill = color)
        tk.update()
        self.cell_state[number] = state

    

    def checkClick(self,evt):
        self.pointX = evt.x
        self.pointY = evt.y
        
        global start_up_all
        if self.humanTrun == True and start_up_all  == True:
            if self.pointX >=30 and self.pointX <= 270:
                if self.pointY >= 30 and self.pointY <= 270:
                    self.click_cell = ((int)((self.pointY)/30))*10 + ((int)((self.pointX) / 30))
                    self.click_ok = True
                    
                    
    

    def debug(self):
        #print(self.cell_id)
        self.debugX = 0
        self.debugY = 10
        self.debugY_label = (' ','1','2','3','4','5','6','7','8',' ')
        for i in range(10):
            print(self.debugY_label[i],self.cell_state[self.debugX:self.debugY],self.debugY_label[i])
            self.debugX += 10
            self.debugY += 10
        print('+' * 35)




#check move class
class MoveChecker:
    def __init__(self, canvas, cell):
        self.move_ok = 0
        self.canvas = canvas
        self.cell = cell
        self.canreverse = 0
        self.passflag = 0
        self.playerstones = 0
        self.computerstones = 0
        self.state = 0
        

    def buttonRelease(self, evt):
        if self.cell.click_ok == True:
            self.check_move(self.cell.click_cell ,player_color, player_state)
            
    def check_move(self, move, color, state):
        self.move = move
        self.color = color
        self.state = state
        
        self.canreverse = 0
        self.opposit_state = 0
        self.check = 1
        self.i = 0
        self.dir = (-11, -10, -9, -1, 1, 9, 10, 11)
        self.dir_ok = [0,0,0,0,0,0,0,0]
        if self.state == 1:
            self.opposit_state = 2
        elif self.state == 2:
            self.opposit_state = 1
        else:
            print('board_state error')

        self.move_ok = 0
        if self.cell.cell_state[self.move] == 0:
            for x in range(8):
                
                self.i = (move + (self.dir[x]))
                
                while True:
                    if self.cell.cell_state[self.i] == self.opposit_state:
                        self.dir_ok[x] += 1
                        self.i += (self.dir[x])
                    elif self.cell.cell_state[self.i] == 9 or self.cell.cell_state[self.i] == 0:
                        self.dir_ok[x] = 0
                        break
                    elif self.cell.cell_state[self.i] == state:
                        break
                       
            for x in self.dir_ok:
                self.canreverse += x
            #print('%d stones can be fliped' % self.canreverse)

            if self.canreverse > 0:
                self.move_ok = 1
                if self.state == 2:
                    self.cell.humanTrun = False
                    self.draw_move()
                    
                
    def pass_check(self):
        global globalpass
        global start_up_all
        global tesuu
        global indent
        if self.cell.humanTrun == True:
            
            self.canvas.create_text(355,30+indent, text = ('(%d) human pass' %tesuu), fill = 'black',
                                                     font = ('Helvetica', 10), state = 'normal')
            tesuu += 1
            indent += 10
            
            tk.update()
            
            globalpass += 1
            self.cell.humanTrun = False
            print('human pass')
            if globalpass == 2 and start_up_all == True:
                self.check_finish()
            elif globalpass < 2:
                open_AI()
        elif self.cell.humanTrun == False:
            if self.state == 1:
                self.canvas.create_text(355,30+indent, text = ('(%d) computer pass' %tesuu), fill = 'black',
                                                     font = ('Helvetica', 10), state = 'normal')
            elif self.state == 2:
                self.canvas.create_text(355,30+indent, text = ('(%d) human pass' %tesuu), fill = 'black',
                                                     font = ('Helvetica', 10), state = 'normal')
            tesuu += 1
            indent += 10
            
            tk.update()
            
            print('computer pass')
            globalpass += 1
            if globalpass == 2:
                self.cell.humanTrun = False
                self.check_finish()
            self.cell.humanTrun = True
                
        


    def check_finish(self):
        global score_text_id1
        global score_text_id2
        self.computerstones = 0
        self.playerstones = 0
        for x in self.cell.cell_state:
            if x == 1:
                self.computerstones +=1
            elif x == 2:
                self.playerstones += 1

        if self.playerstones > self.computerstones:
            self.canvas.create_text(150, 320, text = 'HUMAN WIN', font = ('Helvetica', 20), fill = 'red', state = 'normal')

        elif self.playerstones < self.computerstones:
            self.canvas.create_text(150, 320, text = 'COMPUTER WIN', font = ('Helvetica', 20), fill = 'red', state = 'normal')

        elif self.playerstones == self.computerstones:
            self.canvas.create_text(150, 320, text = 'COMPUTER Draw HUMAN', font = ('Helvetica', 20), fill = 'red', state = 'normal')

        self.canvas.itemconfig(score_text_id1, state = 'hidden')
        self.canvas.itemconfig(score_text_id2, state = 'hidden')
        score_text_id1 = self.canvas.create_text(170, 350, text = (' %d' %self.computerstones),
                                                 font = ('Helvetica', 20), fill = 'black', state = 'normal')
        score_text_id2 = self.canvas.create_text(290, 350, text = (' %d' %self.playerstones),
                                                 font = ('Helvetica', 20), fill = 'black', state = 'normal')

 
 
    def draw_move(self):
        global globalpass
        global label_board
        global score_text_id1
        global score_text_id2
        global tesuu
        global indent
        
        if self.move_ok > 0:
            self.canvas.itemconfig(self.cell.cell_id[self.move], state = 'hidden')
            tk.update()
            self.cell.drawStone(self.move, self.color, self.state)
            tk.update()
            for x in range(8):
                if self.dir_ok[x] == 0:
                    continue
                for y in range(self.dir_ok[x]):
                    self.canvas.itemconfig(self.cell.cell_id[(self.move) + ((y+1) * (self.dir[x]))], state = 'hidden')
                    tk.update()
                    self.cell.drawStone((self.move) + ((y+1) * (self.dir[x])), self.color, self.state)
                    tk.update()
            else:
                globalpass = 0
            print(label_board[self.move%10-1],'%d' %(self.move/10))
            print(self.state)
            self.cal_stone()
            self.canvas.itemconfig(score_text_id1, state = 'hidden')
            self.canvas.itemconfig(score_text_id2, state = 'hidden')
            score_text_id1 = self.canvas.create_text(170, 350, text = ('%d' %self.computerstones), font = ('Helvetica', 20), fill = 'black', state = 'normal')
            score_text_id2 = self.canvas.create_text(290, 350, text = ('%d' %self.playerstones), font = ('Helvetica', 20), fill = 'black', state = 'normal')
            if self.state == 1:
                self.canvas.create_text(355,30+indent, text = ('(%d) computer %s%d' %(tesuu, label_board[self.move%10-1], self.move/10)), fill = 'black',
                                                     font = ('Helvetica', 10), state = 'normal')
            elif self.state == 2:
                self.canvas.create_text(355,30+indent, text = ('(%d) human %s%d' %(tesuu, label_board[self.move%10-1], self.move/10)), fill = 'black',
                                                     font = ('Helvetica', 10), state = 'normal')
                
            tesuu += 1
            indent += 10
            
            tk.update()
            if self.state == 2:
                open_AI()

    def cal_stone(self):
        self.computerstones = 0
        self.playerstones = 0                                               
        for x in self.cell.cell_state:
            if x == 1:
                self.computerstones +=1
            elif x == 2:
                self.playerstones += 1
        
        
                                                
                                                
            
            
            

            
             
#STARTCHECKER
class GameMaster:
    def __init__(self,cell,canvas,AIengine):
        self.canvas = canvas
        self.cell = cell
        self.AIengine = AIengine
        self.start_up_color = False
        self.start_up_teban = True
        global start_up_all

    def start_check(self):
        global start_up_all
        global player_color
        if start_up_all == False and self.start_up_color == True and self.start_up_teban == True:
            start_up_all = True
            if player_color == 'black':
                self.cell.humanTrun = True
                self.canvas.create_text(355, 10, text = ('COMPUTER : WHITE'), font = ('Helvetica', 10), fill = 'black', state = 'normal')
                self.canvas.create_text(450, 10, text = ('HUMAN : BLACK'), font = ('Helvetica', 10), fill = 'black',state = 'normal')
                tk.update()
            elif player_color == 'white':
                self.cell.humanTrun = False
                self.canvas.create_text(355, 10, text = ('COMPUTER : BLACK'), font = ('Helvetica', 10), fill = 'black', state = 'normal')
                self.canvas.create_text(450, 10, text = ('HUMAN : WHITE'), font = ('Helvetica', 10), fill = 'black',state = 'normal')
                tk.update()
                self.AIengine.thinking()

    def ini_set_cell(self):
        global player_color
        if player_color == 'black':
            self.cell.cell_state[44] = 1
            self.cell.cell_state[45] = 2
            self.cell.cell_state[54] = 2
            self.cell.cell_state[55] = 1
            print('OK')
        if player_color == 'white':
            self.cell.cell_state[44] = 2
            self.cell.cell_state[45] = 1
            self.cell.cell_state[54] = 1
            self.cell.cell_state[55] = 2
            print('OK')
    



    def start_color_black(self):
        global player_color
        global computer_color
        global start_up_all
        if start_up_all == False:
            self.start_up_color = True
            player_color = 'black'
            computer_color = 'white'
            self.ini_set_cell()
            
    def start_color_white(self):
        global player_color
        global computer_color
        global start_up_all
        if start_up_all == False:
            self.start_up_color = True
            player_color = 'white'
            computer_color = 'black'
            self.ini_set_cell()

    
    
        
#AI engine
class AI:
    def __init__(self, canvas, cell, moveChecker):
        self.canvas = canvas
        self.cell = cell
        self.moveChecker = moveChecker
        self.AIboard = (11, 12, 13, 14, 15, 16, 17, 18,
                        21, 22, 23, 24, 25, 26, 27, 28,
                        31, 32, 33, 34, 35, 36, 37, 38,
                        41, 42, 43, 46, 47, 48,
                        51, 52, 53, 56, 57, 58,
                        61, 62, 63, 64, 65, 66, 67, 68,
                        71, 72, 73, 74, 75, 76, 77, 78,
                        81, 82, 83, 84, 85, 86, 87, 88)

        self.AIboardReverseStoneNumber = [0] * (len(self.AIboard))
        self.vlaueCell = (120, -20, 20, 5, 5, 20, -20, 120,
                          -20, -40, -5, -5, -5, -5, -40, -20,
                          20, -5, 15, 3, 3, 15, -5, 20,
                          5, -5, 3, 3, -5, 5,
                          5, -5, 3, 3, -5, 5,
                          20, -5, 15, 3, 3, 15, -5, 20,
                          -20, -40, -5, -5, -5, -5, -40, -20,
                          120, -20, 20, 5, 5, 20, -20, 120)
        self.canPutPlace = []
        self.corner = [11, 18, 81, 88]
        self.cancorner = []
        self.random_number = 0
        

    def thinking(self):
        global computer_state
        global computer_color
        global tesuu
        self.AIboardReverseStoneNumber = []
        self.canPutPlace = []
        self.cancorner = []
        
        time.sleep(1)
        for x in range(len(self.AIboard)):
            self.moveChecker.check_move(self.AIboard[x], computer_color, computer_state)
            
            if self.moveChecker.move_ok != 0:
                self.canPutPlace.append(self.AIboard[x])
        print(self.canPutPlace)
        if len(self.canPutPlace) == 0:
            self.moveChecker.pass_check()
            
            
        else:
            
            print(len(self.canPutPlace))
            

            
            for x in range(len(self.canPutPlace)):
                self.moveChecker.check_move(self.canPutPlace[x], computer_color, computer_state)
                self.AIboardReverseStoneNumber.append(self.moveChecker.canreverse)
                if self.canPutPlace[x] == 11 or self.canPutPlace[x] == 18 or self.canPutPlace[x] == 81 or self.canPutPlace[x] == 88:
                    self.cancorner.append(self.canPutPlace[x])
                                          
            
            if (len(self.cancorner)) != 0:
                self.moveChecker.check_move(self.cancorner[0], computer_color, computer_state)
                                          
            else:                              
                self.minreverse = min(self.AIboardReverseStoneNumber)
                self.maxreverse = max(self.AIboardReverseStoneNumber)
                if tesuu < 35:
                    self.moveChecker.check_move(self.canPutPlace[(self.AIboardReverseStoneNumber.index(self.minreverse))],
                                            computer_color, computer_state)
                else:
                    self.moveChecker.check_move(self.canPutPlace[(self.AIboardReverseStoneNumber.index(self.maxreverse))],
                                            computer_color, computer_state)
                
            self.moveChecker.draw_move()
            self.cell.humanTrun = True
            print(self.cell.humanTrun)

            
    
#window setup
canvas.pack()   
tk.update()

#line of board display
label_board = ('a', 'b', 'c' , 'd', 'e', 'f', 'g', 'h')

#information of color and state
player_state = 2
computer_state = 1
player_color = 'black'
computer_color = 'white'

#all ok
start_up_all = False

#tesuu
tesuu = 1
indent = 0
                             
#create object
grid = Grid(canvas)
cell = Cell(canvas) 
moveChecker = MoveChecker(canvas, cell)
AIengine = AI(canvas, cell, moveChecker)
gamemaster = GameMaster(cell, canvas, AIengine)


#menubar option
games.add_command(label = "start", under = 0, command = gamemaster.start_check)
games.add_command(label = "exit", under = 0, command = exit)
color.add_command(label = "Black", under = 0, command = gamemaster.start_color_black)
color.add_command(label = "White", under = 0, command = gamemaster.start_color_white)
Pass.add_command(label = "pass", under = 0, command = moveChecker.pass_check)


#open AI
def open_AI():
    AIengine.thinking()
    

#START
canvas.bind_all('<ButtonRelease>',moveChecker.buttonRelease)


#mainloop
tk.mainloop()

