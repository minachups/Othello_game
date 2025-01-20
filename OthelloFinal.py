import random
import time
import math
import copy
# Object used to create new boards


class Board:
    def __init__(self, size):
        self.size = size
        self.board = []

    def create_board(self):
        for y_pos in range(self.size):
            for x_pos in range(self.size):
                if x_pos != 0 and x_pos != 7 and y_pos != 0 and y_pos != 7:
                    self.board.append(Tile(x_pos, y_pos, "🟩", "🟩"))
                else:
                    self.board.append(Tile(x_pos, y_pos, "X", "🟩"))
        self.place_initial_pawns()

    def draw_board(self, data_type):
        display_board = []
        line_breaker = 0
        print([0, ' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7'])
        for board_index in self.board:
            if (board_index.x_pos == 0):
                display_board.append(board_index.y_pos)
            if data_type == "Coordinates":
                display_board.append([board_index.x_pos, board_index.y_pos])
            elif data_type == "Type":
                display_board.append(board_index.type)
            else:
                display_board.append(board_index.content)
            line_breaker += 1
            if line_breaker > 7:
                print(display_board)
                line_breaker = 0
                display_board = []
        print("\n")

    # Place the 4 initial pawns at the center of the board (2 white and 2 black)
    def place_initial_pawns(self):
        #  We pick the 4 central tiles
        #  And place 2 black pawns and 2 white pawns
        self.board[27].content = "⚪"
        self.board[28].content = "⚫"
        self.board[35].content = "⚫"
        self.board[36].content = "⚪"

    # Check if the position in inside the board
    # Return true or false depending if it is inside or not
    def is_on_board(self, x_pos, y_pos):
        if x_pos < 0 or x_pos > 7 or y_pos < 0 or y_pos > 7:
            return False
        else:
            return True

    # Check if the tile is an empty tile ("🟩")
    # Return true or false depending if it is empty or not
    def is_tile_empty(self, x_pos, y_pos):
        if self.board[(x_pos) + y_pos * 8].content == "🟩":
            return True
        else:
            return False

    
    def is_legal_move(self, x_pos, y_pos, color):

        directions = [
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
        ]

        # Opposite of the color of the placed pawn
        if color == "⚪":
            awaited_color = "⚫"
        else:
            awaited_color = "⚪"

        current_x_pos = x_pos
        current_y_pos = y_pos
        is_legal = False

        tiles_to_flip = []

        if (not self.is_tile_empty(current_x_pos, current_y_pos) or not self.is_on_board(current_x_pos, current_y_pos)):
            return False

        # Check for every direction
        for current_dir in directions:
            number_of_tiles_to_flip = 1
            # Get your original coordinates + the direction modifier
            current_x_pos = x_pos + current_dir[0]
            current_y_pos = y_pos + current_dir[1]
            # Check if the new position is on the board and empty
            if self.is_on_board(current_x_pos, current_y_pos):
                #  Get the tile informations
                current_index = self.board[current_x_pos + current_y_pos * 8]
                # If the tile contains a pawn of the opposite color, continue on the line
                while current_index.content == awaited_color:
                    current_x_pos += current_dir[0]
                    current_y_pos += current_dir[1]
                    if self.is_on_board(current_x_pos, current_y_pos):
                        current_index = self.board[current_x_pos +
                                                   current_y_pos * 8]
                        # If the line ends with a pawn of your color, then the move is legal
                        if current_index.content == color:
                            is_legal = True
                            tiles_to_flip.append(
                                [number_of_tiles_to_flip, current_dir])
                            break
                    else:
                        break
                    number_of_tiles_to_flip += 1

        if is_legal:
            return tiles_to_flip
        else:
            return False

    def flip_tiles(self, x_pos, y_pos, tiles_to_flip, color):
        # x_pos and y_pos = new pawn position
        # tiles_to_flip = list containing the number of pawn to flip and a direction
        # ex: [
        # [1, [1, 0]],
        # ] means we're changing 1 pawn to the right
        # color = the new color of the pawns to flip
        for current_dir in tiles_to_flip:
            current_x_pos = x_pos + current_dir[1][0]
            current_y_pos = y_pos + current_dir[1][1]
            for nb_tile in range(current_dir[0]):
                current_index = self.board[current_x_pos + current_y_pos * 8]
                current_index.content = color
                current_x_pos += current_dir[1][0]
                current_y_pos += current_dir[1][1]



class Tile:
    
    def __init__(self, x_pos, y_pos, type, content):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.content = content

class Game:
    def __init__(self):
        self.score_black = 2
        self.score_white = 2
        self.active_player = "⚫"
        self.is_game_over = False
        self.winner = "Noone"
        self.turn = 0

    def place_pawn(self, x_pos, y_pos, board_instance, color):
        if not board_instance.is_on_board(x_pos, y_pos):
            print("Coordinates outside the board")
        else:
            if board_instance.board[(x_pos) + y_pos * 8].content == "🟩":
                tiles_to_flip = board_instance.is_legal_move(
                    x_pos, y_pos, color)
                if not tiles_to_flip:
                    print("Invalid move for " + color)
                else:
                    board_instance.board[(x_pos) + y_pos * 8].content = color
                    board_instance.flip_tiles(
                        x_pos, y_pos, tiles_to_flip, color)
                    self.update_score(board_instance)
                    self.change_active_player()
                    self.check_for_valid_moves(board_instance)
            else:
                print("There is already a pawn here")

    # Change the active player color from black to white or white to black
    def change_active_player(self):
        # Prend self.active_player et change la couleur du joueur actif
        if self.active_player == "⚫":
            self.active_player = "⚪"
        else:
            self.active_player = "⚫"
            
        self.turn += 1

    # Update the players score after a successful move
    def update_score(self, board_instance):
        # Count all the black & white pawns, and update the scores
        w_score = 0
        b_score = 0
        for tile_index in board_instance.board:
            if tile_index.content == "⚪":
                w_score += 1
            elif tile_index.content == "⚫":
                b_score += 1
        self.score_black = b_score
        self.score_white = w_score

    # Check for a valid move, and end the game if there is none for the current player
    def check_for_valid_moves(self, board_instance):
        is_game_over = True
        first_player_can_play = False

        # Check if the current player can play
        for tile_index in board_instance.board:
            move_to_check = board_instance.is_legal_move(
                tile_index.x_pos, tile_index.y_pos, self.active_player)
            if move_to_check != False:
                first_player_can_play = True
                is_game_over = False

        # If not, check for the other player and skip the first player's turn
        if not first_player_can_play:
            self.change_active_player()
            for tile_index in board_instance.board:
                move_to_check = board_instance.is_legal_move(tile_index.x_pos, tile_index.y_pos, self.active_player)
                if move_to_check != False:
                  is_game_over = False  

        # If neither can play, end the game
        if is_game_over:
            self.check_for_winner()
            self.is_game_over = True

    # Compare the score, and print the winner's color
    def check_for_winner(self):
        if (self.score_black > self.score_white):
            self.winner = "⚫"
        elif (self.score_white > self.score_black):
            self.winner = "⚪"



class OthelloBotGroup7:
    def __init__(self):
        self.name = "OthelloBotGroup7"

    def evaluate_moves(self, game_board, current_game):
        matrix = [
            [1000, -50,  50,  30,  30,  50, -50, 1000],
            [-50, -100, -20, -10, -10, -20, -100, -50],
            [ 50,  -20,  15,   5,   5,  15,  -20,  50],
            [ 30,  -10,   5,   3,   3,   5,  -10,  30],
            [ 30,  -10,   5,   3,   3,   5,  -10,  30],
            [ 50,  -20,  15,   5,   5,  15,  -20,  50],
            [-50, -100, -20, -10, -10, -20, -100, -50],
            [1000, -50,  50,  30,  30,  50, -50, 1000]
        ]
        
        best_moves = []
        highest_score = float('-inf')
        compteur = 0

        for tile in game_board.board:
            x, y = tile.x_pos, tile.y_pos
            legal_move = game_board.is_legal_move(x, y, current_game.active_player)
        
            if legal_move:
                move_value = matrix[x][y]
                move_value += self.additional_score(x, y)
                move_value += compteur

                if move_value > highest_score:
                    highest_score = move_value
                    best_moves = [[x, y]]
                elif move_value == highest_score:
                    best_moves = best_moves + [[x, y]]

            compteur += 1

        if best_moves:
            if random.random() < 0.1:
                return random.choice(best_moves)
            else:
                return best_moves[0]
        else:
            return None

    def additional_score(self, x, y):
        score = 0
        if (x == 0 or x == 7) and (y == 0 or y == 7):
            score += 30
        elif (x == 1 or x == 6) and (y == 1 or y == 6):
            score += 15
        elif x == 3 or x == 4 or y == 3 or y == 4:
            score += 10
        return score



    
class CrotoBotEz:
    def __init__(self):
        self.coners = [[0, 0], [7, 0], [0, 7], [7, 7]]
        self.avoided_tiles = [[1, 0], [0, 1],  [1, 1], [1, 7], [0, 6], [1, 6], [6, 0], [7, 1], [6, 1], [6, 7], [7, 6], [6, 6]]

    # BOT FUNCTIONS

    def check_valid_moves(self, board, game):
        max_points = -999
        best_moves = []
        current_move = []

        for current_tile in board.board:
            points = 0

            if(board.is_tile_empty):
                current_move = board.is_legal_move(current_tile.x_pos, current_tile.y_pos, game.active_player)
                
                if (current_move != False):
                    for tiles_to_flip in current_move:
                        points += tiles_to_flip[0]
                    
                    points += self.get_tile_weight(current_tile.x_pos, current_tile.y_pos)
                    if(points > max_points):
                        best_moves = [[current_tile.x_pos, current_tile.y_pos]]
                        max_points = points
                    elif(points == max_points):
                        best_moves.append([current_tile.x_pos, current_tile.y_pos])

        return random.choice(best_moves)
                
    def get_tile_weight(self, x, y):
        total_points = 0

        for current_coord in self.coners:
            if x == current_coord[0] and y == current_coord[1]:
                total_points += 100
                break
            
        for current_coord in self.avoided_tiles:
            if x == current_coord[0] and y == current_coord[1]:
                total_points -= 30
                break
        
        return total_points

othello_board = Board(8)
othello_game = Game()

# Fill the board with tiles
othello_board.create_board()

# Draw the board
othello_board.draw_board("Content")

# Create 2 bots
myBot = OthelloBotGroup7()
# otherBot = Bot()
croto_bot = CrotoBotEz()

def play_games(number_of_games, timeout_value):
    white_victories = 0
    black_victories = 0
    white_win_icons = ""
    black_win_icons = ""
    
    for current_game in range(number_of_games):

        timeout = time.time() + timeout_value

        # Create a new board & a new game instances
        othello_board = Board(8)
        othello_game = Game()

        # Fill the board with tiles
        othello_board.create_board()


        while not othello_game.is_game_over:

            if(time.time() > timeout):
                othello_game.check_for_winner()
                othello_game.is_game_over = True
                print("Player " + othello_game.active_player + " caused a Timeout")
                break

            # First player / bot logic goes here
            if(othello_game.active_player == "⚫"):
                move_coordinates = [0, 0]
                move_coordinates = myBot.evaluate_moves(othello_board, othello_game)
                othello_game.place_pawn(
                move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)


            # Second player / bot logic goes here
            else:
                move_coordinates = [0, 0]
                move_coordinates = croto_bot.check_valid_moves(othello_board, othello_game)
                othello_game.place_pawn(
                move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)
        
        if(othello_game.winner == "⚫"):
            black_win_icons += "⚫"
            black_victories += 1
        elif(othello_game.winner == "⚪"):
            white_win_icons += "⚪"
            white_victories += 1
        
        print(black_win_icons)
        print(white_win_icons)
    
    print("End of the games, showing scores: ")
    print("Black player won " + str(black_victories) + " times")
    print("White player won " + str(white_victories) + " times")
        
play_games(100, 0.8)