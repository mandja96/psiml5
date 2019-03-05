# -*- coding: utf-8 -*-
import copy 

# matrix rotations counterclock wise
def rotate_matrix_90(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]
def rotate_matrix_180(m):
	return (rotate_matrix_90(rotate_matrix_90(m)))
def rotate_matrix_270(m):
	return (rotate_matrix_180(rotate_matrix_90(m)))	

def display_matrix(m):
	N = len(m) # rows
	M = len(m[0]) # columns
	for i in range(0, N):  
		for j in range(0, M):  
			print(m[i][j], end = '') 
		print("") 

def read_blocks(file_path, H, W):
	with open(file_path, encoding = "utf-8") as f:
		lines = f.read().splitlines()

	tetris_board = []
	tetris_pieces = {}

	i = 0
	count = 0
	for l in lines:
		if(i < H):
			row = []
			for s in l:
				if s == '#':
					row.append(1)
				else:
					row.append(0)
			tetris_board.append(row)

		elif( i >= H and (len(l.strip()) == 0) ):
			# pieces
			tetris_pieces[count] = []
			count = count + 1

		elif( i > H and (len(l.strip()) > 0) ):
			#new piece is coming
			row = []
			for s in l:
				if s == '#':
					row.append(1)
				else:
					row.append(0)	
			tetris_pieces[count-1].append(row)					
		i = i + 1

	return(tetris_board, tetris_pieces)

def detecting_empty_rows(tetris_board, H, W):
	num_of_empty = 0 
	for i in range(0, H):
		if(all(x == 0 for x in tetris_board[i]) == True):
			num_of_empty = num_of_empty + 1
		else:
			return num_of_empty	

def no_collisions(tetris_board, tetris_piece, row, column):
	piece_height = len(tetris_piece)
	piece_width = len(tetris_piece[0]) 

	if(row == 20 or column == 10):
		return False

	ind = True

	for h in range(0, piece_height):
		for w in range(0, piece_width):	
			if((tetris_piece[h][w] == 1 and tetris_board[row+h][column+w] == 1)):
				ind = False
	return ind

def can_go_down(board, piece, i, j):
	ind = False

	if(i >= 20 - len(piece)):
		ind = False

	elif(no_collisions(board, piece, i+1, j) and i < 20):
		ind = True

	return(ind)

def can_go_up(board, piece, i, j):
	ind = False

	if(no_collisions(board, piece, i-1, j) and i > 0):
		ind = True

	return(ind)

def top(board, piece, i, j):
	br = i
	while(br > 0):
		if(can_go_up(board, piece, br, j)):
			br = br - 1
		else:
			return False

	return True

def num_of_occupied_rows(tetris_board, H):
	r = 0
	for i in range(0, H):
		if(all(x == 1 for x in tetris_board[i]) == True):
			r = r + 1			
	return(r)

def is_valid(tetris_board, tetris_piece, H, W):
	piece_height = len(tetris_piece)
	piece_width = len(tetris_piece[0])

	score = 0
	top_left_i = 0
	top_left_j = 0

	for i in range(0, H):
		if (i <= (H - piece_height)):
			for j in range(0, W):
				if (j <= (W - piece_width)):
					if(no_collisions(tetris_board, tetris_piece, i, j)):
						new_board = copy.deepcopy(tetris_board)
						for k in range(i, i + piece_height):
							for l in range(j, j + piece_width):
								if(new_board[k][l] == 0):
									new_board[k][l] = tetris_piece[k-i][l-j]			
						if (can_go_down(tetris_board, tetris_piece, i, j) == False):
							if(top(tetris_board, tetris_piece, i, j) == True): 
								new_score = num_of_occupied_rows(new_board, H)
								if(new_score >= score):
									score = new_score	
									top_left_i = i
									top_left_j = j			
						
	#display_matrix(tetris_piece)				
	return(score, top_left_j)

if __name__ == "__main__":
	H = 20 # board height
	W = 10 # board width

	file_path = input()
	#file_path = '/Users/mandja96/Downloads/public/set/10.txt'
	(tetris_board, tetris_pieces) = read_blocks(file_path, H, W)

	# print(tetris_pieces)
	# print("Tetris board:")
	# display_matrix(tetris_board)
	# print()

	# print("Tetris pieces:")
	# for k in tetris_pieces:
	# 	display_matrix(tetris_pieces[k])
	# 	print()
	

	rotations = [0, 90, 180, 270]
	max_score = -1
	piece_number = -1
	piece_degrees = -1
	top_left = -1

	for p in tetris_pieces:
		for r in rotations:
			if(r == 0):
				tmp = tetris_pieces[p]
				(score, top_left_j) = is_valid(tetris_board, tmp, H, W)
				if score > max_score:
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j
			if(r == 90):
				tmp = tetris_pieces[p]
				tmp = rotate_matrix_90(tmp)
				(score, top_left_j) = is_valid(tetris_board, tmp, H, W)
				if score > max_score:
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j

			if(r == 180):
				tmp = tetris_pieces[p]		
				tmp = rotate_matrix_180(tmp)
				(score, top_left_j) = is_valid(tetris_board, tmp, H, W)
				if score > max_score:
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j

			if(r == 270):
				tmp = tetris_pieces[p]				
				tmp = rotate_matrix_270(tmp)
				(score, top_left_j) = is_valid(tetris_board, tmp, H, W)
				if score > max_score:
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j

print("{0} {1} {2}".format(piece_number, piece_degrees, top_left))