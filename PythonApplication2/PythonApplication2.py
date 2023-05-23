import random

class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0

    def is_sunk(self):
        return self.hits == self.size

    def __str__(self):
        return 'S'

class Board:
    def __init__(self, size):
        self.size = size
        self.ships = []
        self.board = [['O'] * size for _ in range(size)]
        self.shots = set()

    def place_ship(self, ship):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            orientation = random.choice(['horizontal', 'vertical'])
            if self.is_valid_placement(x, y, orientation, ship.size):
                self.add_ship(x, y, orientation, ship)
                break

    def is_valid_placement(self, x, y, orientation, ship_size):
        if orientation == 'horizontal':
            return y + ship_size <= self.size and all(self.board[x][y+i] == 'O' for i in range(ship_size))
        elif orientation == 'vertical':
            return x + ship_size <= self.size and all(self.board[x+i][y] == 'O' for i in range(ship_size))
        return False

    def add_ship(self, x, y, orientation, ship):
        if orientation == 'horizontal':
            for i in range(ship.size):
                self.board[x][y+i] = ship
        elif orientation == 'vertical':
            for i in range(ship.size):
                self.board[x+i][y] = ship
        self.ships.append(ship)

    def receive_shot(self, x, y):
        if (x, y) in self.shots:
            print("Already shot there!")
            return

        target = self.board[x-1][y-1]
        if target == 'O':
            self.board[x-1][y-1] = 'Z'
            print("Missed!")
        elif isinstance(target, Ship):
            target.hits += 1
            self.board[x-1][y-1] = 'X'
            if target.is_sunk():
                print("Hit, ship sunk!")
            else:
                print("Hit!")

        self.shots.add((x, y))

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def display(self):
        for row in self.board:
            print(' '.join(str(cell) if str(cell) != 'S' else 'O' for cell in row))

class Game:
    def __init__(self, board_size, ship_sizes):
        self.board_size = board_size
        self.ship_sizes = ship_sizes
        self.board = Board(board_size)

    def setup_ships(self):
        for size in self.ship_sizes:
            ship = Ship(size)
            self.board.place_ship(ship)

    def play(self):
        print("Let's play Battleship!")
        self.setup_ships()

        while not self.board.all_ships_sunk():
            print("Opponent's board:")
            self.board.display()

            x = int(input("Enter X coordinate (1-8): "))
            y = int(input("Enter Y coordinate (1-8): "))

            self.board.receive_shot(x, y)

        print("All opponent's ships have been sunk!")
        print("Game over.")

# Example usage:
game = Game(8, [5, 4, 3, 3, 2])
game.play()

