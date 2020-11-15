import os, random
path = os.getcwd()

BOARD_WIDTH = 200
BOARD_HEIGHT = 400

NUM_ROWS = 20
NUM_COLS = 10

CELL_WIDTH = BOARD_WIDTH / NUM_COLS
CELL_HEIGHT = BOARD_HEIGHT / NUM_ROWS

COLORS = [[255,51,52],[12, 150, 228],[30, 183, 66],[246, 187, 0],[76, 0, 153],[255, 255, 255],[0, 0, 0]]

class Block:
    def __init__(self,row,col,clr):
        self.row = row
        self.col = col
        self.clr = clr
        self.key_handler = {LEFT:False, RIGHT:False}
        

    def display(self):
        self.update()
        stroke(180)
        strokeWeight(1)
        fill(self.clr)
        rect(self.col * CELL_WIDTH, self.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
    
    def update(self):
        if self.key_handler[LEFT] == True:
            if self.canMove("LEFT"):
                self.col -= 1
        elif self.key_handler[RIGHT] == True:
            if self.canMove("RIGHT"):
                self.col += 1
    
# This is used to check whether the block can be moved.
    def canMove(self, direction):
        if direction == "LEFT":
            if self.col > 0 and game[self.row][self.col-1] == None:
                return True
            else:
                return False
        elif direction == "RIGHT":
            if self.col < NUM_COLS - 1 and game[self.row][self.col+1] == None: 
                return True
            else:
                return False
            
            
class Game(list):
    def __init__(self):
        for r in range(NUM_ROWS):
            row_list = []
            for c in range(NUM_COLS):
                row_list.append(None)
            self.append(row_list)
        
        tmp_color = random.choice(COLORS)
        self.new_block = Block(0,random.randint(0,NUM_COLS-1),color(tmp_color[0],tmp_color[1],tmp_color[2]))
        self.speed = 0
        self.score = 0
        self.game_over = False
    
    def score_display(self):
        textSize(15)
        fill(0,0,0)
        text("Score: "+str(self.score), 10, 30)       
          
    def display(self):
        self.update()
        
        for r in self:
            for c in r:
                if c != None:
                    c.display()
                
        self.new_block.display()
        self.score_display()

    def update(self):
        if self.new_block.row < NUM_ROWS - 1:
            if self[self.new_block.row + 1][self.new_block.col] == None:
                self.new_block.row += 1
            else:
                self.new_block.key_handler = {LEFT:False, RIGHT:False}
                self[self.new_block.row][self.new_block.col] = self.new_block
                self.new_block_generator()
        elif self.new_block.row == NUM_ROWS - 1:
            self.new_block.key_handler = {LEFT:False, RIGHT:False}
            self[self.new_block.row][self.new_block.col] = self.new_block
   
            self.new_block_generator()
        
        self.check()

    def new_block_generator(self):
        tmp_color = random.choice(COLORS)
        self.new_block = Block(0,random.randint(0,NUM_COLS-1),color(tmp_color[0],tmp_color[1],tmp_color[2]))
        self.speed += 0.25
    
    #This is used to check offset four blocks with same colors    
    def check(self):
        tmp_counter = 0
        for c in range(NUM_COLS):
            for r in range(NUM_ROWS - 1):
                if self[r][c] != None and self[r+1][c] != None and self[r][c].clr == self[r+1][c].clr:
                    tmp_counter += 1
                else:
                    tmp_counter = 0
                
                if tmp_counter == 3:
                    tmp_counter = 0
                    self.speed = 0
                    self.score += 1
                    self[r][c] = None
                    self[r+1][c] = None
                    self[r-1][c] = None
                    self[r-2][c] = None
                    
    def check_game_over(self):
        #if you empty the board in this function, the next time draw is called, the board will be empty and game_over will be false again
        self.game_over = not(any(None in sublist for sublist in self))


                    
    def game_over_display(self):
        textSize(15)
        fill(0,0,0)
        text("Game over!"+"\n"+"Your score is "+str(self.score), 50, 200)
        
    def reset(self):
        if self.game_over == True:
            for r in range(NUM_ROWS):
                row_list = []
                for c in range(NUM_COLS):
                    row_list.append(None)
                self[r] = row_list
        
        tmp_color = random.choice(COLORS)
        self.new_block = Block(0,random.randint(0,NUM_COLS-1),color(tmp_color[0],tmp_color[1],tmp_color[2]))
        self.speed = 0
        self.score = 0
        self.game_over = False
        
game = Game()        
def setup():
    size(BOARD_WIDTH,BOARD_HEIGHT)
    background(210)

def draw():
    if frameCount % (max(1, int(8 - game.speed)))==0 or frameCount==1: 
        background(210)
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                stroke(180)
                strokeWeight(1)
                fill(210)
                rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        
        game.check_game_over()
        #this calls the display method of the game class 
        if game.game_over == False:
            game.display()
        elif game.game_over == True:
            game.game_over_display()
def keyPressed():
    if keyCode == LEFT:
        game.new_block.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.new_block.key_handler[RIGHT] = True

        
def keyReleased():
    if keyCode == LEFT:
        game.new_block.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.new_block.key_handler[RIGHT] = False

def mouseClicked():
    game.reset()
