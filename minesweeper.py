import random, math

DIFFICULTY = 2

class Board:
    board = []
    def __init__(self, height, width, numMines):
        self.height = height;
        self.width = width;
        self.numMines = numMines;
        self.mines = {};
        self.revealed = {};

        #Initialize empty board
        for i in range(0,height):
            self.board.append([])
            for j in range(0, width):
                self.board[i].append(0);

        #Initialize mine locations
        minecount = 0
        while minecount < self.numMines:
            y = int(random.random()*height)
            x = int(random.random()*width)
            if (y,x) not in self.mines.keys():
                self.mines[(y,x)] = True
                minecount += 1

        #Initialize warning numbers
        for (y,x) in self.mines.keys():
            self.board[y][x] = 9
        for (y,x) in self.mines.keys():
            for i in range(y-1, y+2):
                for j in range(x-1, x+2):
                    if i in range(height) and j in range(width) and (i,j) not in self.mines.keys():
                        self.board[i][j] += 1

    def __getitem__(self, x):
        # Allow easier access to board elements as an array
        return self.board[x]

    def display(self):
        # Print Board state
        for i in range(self.height):
            print ''.join([str(self.board[i][j]) if (i,j) in self.revealed.keys() else '-' for j in range(self.width)])

    def reveal(self, y, x, visited):
        # Recursively reveal all adjacent 0 values
        if (y,x) in visited.keys():
            return;
        else:
            self.revealed[(y,x)] = True
            visited[(y,x)] = True
            if(self.board[y][x] == 0):
                for i in range(y-1, y+2):
                    if i not in range(self.height):
                        continue
                    for j in range(x-1, x+2):
                        if j not in range(self.width):
                            continue
                        elif (i,j) == (y,x):
                            continue
                        if self.board[i][j] not in self.revealed.keys():
                            self.reveal(i, j, visited)

if DIFFICULTY == 0:
    gameboard = Board(9,9,10)
elif DIFFICULTY == 1:
    gameboard = Board(16,16,40)
else:
    gameboard = Board(16,30,99)

gameover = False

#Game Loop
while not gameover:
    gameboard.display()
    checkX = -1
    checkY = -1

    # Get X
    while True:
        print("Enter x coordinate to check: (0-{})".format(gameboard.width-1))
        try:
            checkX = int(raw_input())
        except ValueError:
            print("Please enter a number! (0-{})".format(gameboard.width-1))
        if not (checkX < 0 or checkX > gameboard.width-1):
            break;

    # Get Y
    while True:
        print("Enter y coordinate to check: (0-{})".format(gameboard.height-1))
        try:
            checkY = int(raw_input())
        except ValueError:
            print("Please enter a number! (0-{})".format(gameboard.height-1))
        if not (checkY < 0 or checkY > gameboard.height-1):
            break;

    # Death Check
    try:
        gameboard.reveal(checkY, checkX, {})
        if(gameboard[checkY][checkX] == 9):
            gameboard.display()
            print("You are dead!")
            gameover = True
    # Out of bounds check
    except IndexError as e:
        print e
        print("Please enter a number within the boundary!")

    # Win Check
    if len(gameboard.revealed.keys()) == (gameboard.width*gameboard.height - gameboard.numMines):
        gameover = True
        gameboard.display()
        print("You win!")
