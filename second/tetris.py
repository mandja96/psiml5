# -*- coding: utf-8 -*-

# matrix rotation counterclock wise
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

def after_deleting_empty_rows(tetris_board, tetris_piece, H, W):
	h = len(tetris_piece)
	w = len(tetris_piece[0])
	max_hw = max(h, w)

	# del l[0] is for removing first row
	# all(x == 0 for x in v) for checking if row is all 0
	# list.insert(index, elem) 
 
	for i in range(0, H):
		if(all(x == 0 for x in tetris_board[i]) == True):
			del tetris_board[0]

	for i in range(0, max_hw):
		tetris_board.insert(0, )




	return result

def check_collision(tetris_board, tetris_piece, row, column):
	piece_width = len(tetris_piece[0])
	piece_height = len(tetris_piece) 

	for w in range(0, piece_width-1):
		for h in range(0, piece_height-1):
			if(tetris_piece[w][h] == 1):
				if(tetris_board[row+w][column+h]) == 1:
					return True

	return False

if __name__ == "__main__":
	H = 20 # board height
	W = 10 # board width

	file_path = input()
	file_path = '/Users/mandja96/Downloads/public/set/1.txt'
	(tetris_board, tetris_pieces) = read_blocks(file_path, H, W)

	print("Tetris board:")
	display_matrix(tetris_board)
	print()
	print("Tetris pieces:")
	for k in tetris_pieces:
		display_matrix(tetris_pieces[k])
		print()


	print(check_collision(tetris_board, tetris_pieces[0], 12, 0))
