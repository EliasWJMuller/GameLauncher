# first we need to import the required modules
import numpy as np
import random
import pygame
import sys
import math

#RGB value means we defin 0 for red, 0 for green and 255 for blue, which means we have a high level of blue in this variable
BLUE = (0,0,255)
#RGB value for black is defined as 0 for everything 
BLACK = (0,0,0)
#RGB value here is everything 0 apart form red 
RED = (255,0,0)
#RGB value here is red + green which gives the yellow colour
YELLOW = (255,255,0)

#rows an columns count
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

#define the structure to represent the matrix --> a matrix of all zeros with the dimension 6x7
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

#function to drop pieces 
def drop_piece(board, row, col, piece):
	board[row][col] = piece

#check if the location is valid by looking to whether the last row of the bord is free or if it's still occupied. 
# (if free means it is possible to locate the piece into that column, if not it is impossible to drop the piece into that column)
def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

#define in which row of the column will the piece be located
def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		#check board position --> if row is equal to 0 it means it's empty
		if board[r][col] == 0:
			return r
# since numpy counts rows from the top to the bottom, it is important to change this orientation because the connect four board
# has to be built from the bottom up
def print_board(board):
	#flip the board over the x axes
	print(np.flip(board, 0))

#let player knoe that he won
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

# this is going to evaluate windows in an arbitrary way
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

#assign the score to the board by looking at the entire board 
def score_position(board, piece):
	score = 0

	# Score center column
	# Add preference for center pieces, because this is going to create more opportunities with diagonals and horizontals 
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	
	score += center_count * 3

	# Score Horizontal by counting in windows of four how many empty squares and how many filled squares there are
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# Score Vertical by iterating through the rows windows 
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

# winning move is true if ando nly if it is a terminal node
def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# minimax function is used as the highest value that the player can be sure to get without knowing the actions of the other players; 
# equivalently, it is the lowest value the other players can force the player to receive when they know the player's action.
# minimax function retrieved from GeeksforGeeks 
def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			#
			# winning_move cases
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			# Game is over, no more valid moves
			else: 
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	
	if maximizingPlayer:
		# use -math.inf to get negtive infinity
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	# Minimizing player
	else: 
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

# get the list of columns in which AI can drop and evaluate based on this
def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

# pick best move for AI by simulating each move in a temporary board in a new memory location to not modify the original board
def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

#implement the graphics 
def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			#draw a blue rectangle with a black circle in the middle of it and leave the first row free by adding an additional 
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	#Add another loop to build background and fill the pieces afterwards
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False

#initializing pygame
pygame.init()

#break the board up into 100 pixels 
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

#define the radius smaller than the square 
RADIUS = int(SQUARESIZE/2 - 5)

#let pygame read the graphic
screen = pygame.display.set_mode(size)
#same as print but with pygame graphics
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

#randomly chose who starts
turn = random.randint(PLAYER, AI)

#creation of the main game loop
while not game_over:
	#allow pygame to read the movements players do with mouse and keyboard
	for event in pygame.event.get():

		#make sure to shut game down if player exits out the game 
		if event.type == pygame.QUIT:
			sys.exit()

		#let the game read the specific spot we click with our mouse to drop down the piece
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#See what color are the pieces and where the player is oging to drop it 
			posx = event.pos[0]
			#because AI doesn't need to see the color and everything, it directly does the move
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
				
				#if the location is valid, drop the piece
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					#Player 1 winning case
					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)


	# # Ask for Player 2 (AI) Input
	if turn == AI and not game_over:				

		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        #if the location is valid, drop the piece
		if is_valid_location(board, col):

			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			#Player 2 winning case
			if winning_move(board, AI_PIECE):
				label = myfont.render("Player 2 wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2
			
 #Add milliseconds to wait before the game shuts down 
	if game_over:
		pygame.time.wait(3000) 
