class Playfield:
    field = [[0,0,0],[0,0,0],[0,0,0]]

    def printField(self):
        for y in range(0,3):
            for x in range(0,3):
                #print("("+str(x)+","+str(y)+")="+str(self.field[x][y]), end = ' ')
                print(self.field[x][y], end=' ');
            print()

    def set(self, move):
        x,y,v = move
        self.field[x][y] = v

    def cells(self):
        ret = []
        for y in range(0,3):
            for x in range (0,3):
                ret.append((x, y, self.field[x][y]))
        return ret

    def free_cells(self):
        return list(filter( lambda x: x[2] == 0, self.cells()))

    def has_won_row_or_column(self, symbol, row):
        return len(list(filter(lambda x: x != symbol, row))) == 0

    def has_won(self, symbol):
        for r in range (0,3):
            if self.has_won_row_or_column(symbol, self.row(r)):
                print(f"Row {r} complete.")
                print(self.row(r))
                return True

        for c in range (0,3):
            if self.has_won_row_or_column(symbol, self.column(c)):
                print(f"Column {c} complete.")
                print(self.column(c))
                return True

        dl = []
        dr = []
        for r in range(0,3):
            dr.append(self.field[r][r])
            dl.append(self.field[2-r][r])
        if self.has_won_row_or_column(symbol, dl):
            print("Left diagonal complete.")
            print(dl)
            return True
        if self.has_won_row_or_column(symbol, dr):
            print("Right diagonal complete")
            print(dr)
            return True

        return False

    def gameover(self):
        return self.has_won('X') or self.has_won('O') or self.all_fields_set()

    def all_fields_set(self):
        return len(self.free_cells())==0

    def can_place(self, amove):
        x,y = amove
        return self.field[x][y] == 0

    def column(self, number):
        return [row[number] for row in self.field]

    def row(self, number):
        return self.field[number]

class HumanPlayer:
    def next_move(self, playfield, symbol):
        move = None
        move_valid = False
        print("Playfield for "+symbol+" is:")
        playfield.printField()
        while not move_valid:
            move = input("Enter move x,y (where x and y are between 0 and 2):")
            move_valid=True
            if len(move) != 3:
                move_valid = False
            elif move[1] != ',':
                move_valid = False

            m = (int(move[0]), int(move[2]))
            if not playfield.can_place(m):
                print(f"Square is already taken {m}")
                move_valid = False

        return (m[0], m[1], symbol)


#this is simplest possible player, he always takes first free position.
class SimplestComputerPlayer:
    def next_move(self, playfield, symbol):
        x,y,zero = playfield.free_cells()[0]
        return (x,y,symbol)


class Player:
    def __init__(self, name, symbol, player):
        self.name = name
        self.symbol = symbol
        self.player = player

    def __str__(self):
        s = "Player name: "+self.name
        s += ", Symbol: "+self.symbol
        s += ", Alg: " +str(self.player)
        return s

class Game:
    playfield = Playfield()
    player1 = HumanPlayer
    player2 = SimplestComputerPlayer

    current_player = 0
    players = [Player("Player1", "X", player1), Player("Computer", "O", player2)]

    def is_move_legal(move):
        print(len(move))
        if len(move) != 3:
            return False
        if move[1] != ':':
            return False
        return True

    def play(self):
        print("Starting game between "+str(self.players[0]) + " and "+str(self.players[1]))
        while not self.playfield.gameover():
            my_player = self.players[self.current_player]
            print("Now playing "+my_player.name+" with "+my_player.symbol)
            print("----")
            move = my_player.player.next_move(my_player.player, self.playfield, my_player.symbol)
            print("Move "+str(move))
            self.playfield.set(move)

            self.current_player+= 1
            if self.current_player>1:
                self.current_player = 0

        print("Game over.")
        self.playfield.printField()

        if self.playfield.has_won(self.players[0].symbol):
            print("Player '"+self.players[0].name+"' won.")
        elif self.playfield.has_won(self.players[1].symbol):
            print("Player '"+self.players[1].name+"' won.")
        else:
            print("Draw")

game = Game()
game.play()


