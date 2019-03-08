# -*- coding: utf-8 -*-
import copy 

# THIS CODE is copied from the faculty class
###################################################

# Obilazak grafa u dubinu
def dfs(board, piece, top_left_i, top_left_j, start, stop = '000000'):
    # Inicijalizacija skupa oznacenih cvorova
    # na prazan skup
    visited = set([])
    
    # Na stek path i u skup posecenih cvorova stavi samo polazni cvor;
    visited.add(start)
    path = [start]
    
    # Dok na steku path ima elemenata
    while len(path) > 0:
        
        # Uzmi cvor n sa vrha steka path;
        n = path[-1]
      
        # Ako je cvor n ciljni cvor
        if int(n) == int(stop):
        	#print("OVDE SAM!")
        	# izvesti o uspehu i vrati put konstruisan na osnovu sadrzaja steka path
        	# print('Pronadjen je put: {}'.format(path))
        	return path
        
        # Indikator da li cvor n ima neobidjenih suseda
        has_unvisited = False
        
        # Ako n IMA potomaka koji nisu poseceni
        # {'A': [('B', 1)], 'B': [('A', 1), ('C', 1)], 'C': [('A', 1)]}
        for (m, weight) in get_neighbors(board, piece, int(n[:3]), int(n[3:])):
            if m not in visited:
                # Izaberi prvog takvog potomka m 
                # i dodaj ga na vrh steka path i u skup posecenih cvorova
                path.append(m)
                visited.add(m)
                has_unvisited = True
                break

        # Inace izbaci n sa steka path
        if (not has_unvisited):
            path.pop()
        
    # ako je petlja zavrsena put nije pronadjen,
    # izvesti da trazeni put ne postoji.
    l = []
    return l

###################################################


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

	if(row >= 20 or column >= 10):
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

	if( i > 0):
		if(no_collisions(board, piece, i-1, j) and i > 0):
			ind = True

	return(ind)

def can_go_left(board, piece, i, j):
	ind = False

	if(j > 0):
		if(no_collisions(board, piece, i, j-1)):
			ind = True
	return(ind)		

def can_go_right(board, piece, i, j):
	ind = False

	if(j < (10 - len(piece[0]))):
		if(no_collisions(board, piece, i, j+1)):
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
							new_score = num_of_occupied_rows(new_board, H)
							if(new_score >= score):
								score = new_score	
								top_left_i = i
								top_left_j = j		
	
	# define path with DFS:
	# can I found path for (top_left_i, top_left_j) corner 
	# END is defined as (0, 0)
	start = get_string_rep(top_left_i, top_left_j)
	dfs(tetris_board, tetris_piece, top_left_i, top_left_j, start, stop = '000000')
	
	return(score, top_left_j, dfs(tetris_board, tetris_piece, top_left_i, top_left_j, start, stop = '000000'))

def get_string_rep(top_left_i, top_left_j):
	if(len(str(top_left_i)) > 1):
		start = str('0') + str(top_left_i) 
	if(len(str(top_left_i)) == 1):
		start = str('00') + str(top_left_i)
	if(len(str(top_left_j)) > 1):
		start = start + str('0') + str(top_left_j)
	if(len(str(top_left_j)) == 1):
		start = start + str('00') + str(top_left_j)

	return str(start)

def get_neighbors(tetris_board, piece, top_left_i, top_left_j):
	neighbors = {}
	tmp = get_string_rep(top_left_i, top_left_j)
	neighbors[tmp] = []
	#print(neighbors)

	if(can_go_up(tetris_board, piece, top_left_i, top_left_j)):
			neighbors[tmp].append((get_string_rep(top_left_i-1, top_left_j), 1))
	if(can_go_left(tetris_board, piece, top_left_i, top_left_j)):
		neighbors[tmp].append((get_string_rep(top_left_i, top_left_j-1), 1))
	if(can_go_right(tetris_board, piece, top_left_i, top_left_j)):
		neighbors[tmp].append((get_string_rep(top_left_i, top_left_j+1), 1))
	

	return neighbors[tmp]

#{'A': [('B', 1)], 'B': [('A', 1), ('C', 1)], 'C': [('A', 1)]}

def clean_list(l):
	best_l = l
	niz = []
	niz.append(0)

	left = 0
	right = 0
	k = 1
	while(k < len(best_l)):
		row = int(best_l[k][:3])
		col = int(best_l[k][3:])
		
		row_p = int(best_l[k-1][:3])
		col_p = int(best_l[k-1][3:])
		
		if(row_p == row and col == col_p + 1 and k < len(best_l)):
			if(k == 1):
				right = right + 1
			while(row_p == row and col == col_p + 1 and k < len(best_l)):
				right = right + 1
				k = k + 1
				if (k < len(best_l)):
					row_p = row
					row = int(best_l[k][:3])	
					col_p = col
					col = int(best_l[k][3:]) 		
			if(right > 0):
				if(k > 1 and len(niz) > 1):
					del niz[-1]
				niz.append(right)
				right = 0
		elif(col_p == col and k < len(best_l)):
			while(col_p == col and k < len(best_l)):
				niz.append(0)
				k = k + 1
				if (k < len(best_l)):
					col_p = col
					col = int(best_l[k][3:])
					row_p = row
					row = int(best_l[k][:3])
		elif(row_p == row and col == col_p - 1 and k < len(best_l)):
			while(row_p == row and col == col_p - 1 and k < len(best_l)):
				left = left - 1
				k = k + 1
				if(k < len(best_l)):
					row_p = row
					row = int(best_l[k][:3])	
					col_p = col
					col = int(best_l[k][3:]) 
			if(left < 0):
				if(k > 1 and len(niz) > 1):
					del niz[-1]
				niz.append(left)
				left = 0
	return niz

if __name__ == "__main__":
	H = 20 # board height
	W = 10 # board width

	file_path = input()
#	file_path = '/Users/mandja96/Downloads/public/set/0.txt'
	(tetris_board, tetris_pieces) = read_blocks(file_path, H, W)

	rotations = [0, 90, 180, 270]
	max_score = -1
	piece_number = -1
	piece_degrees = -1
	top_left = -1
	best_l = []

	for p in tetris_pieces:
		for r in rotations:
			if(r == 0):
				tmp = tetris_pieces[p]
				(score, top_left_j, l) = is_valid(tetris_board, tmp, H, W)
				if score > max_score and len(l) > 0:
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j
					best_l = l

			if(r == 90):
				tmp = tetris_pieces[p]
				tmp = rotate_matrix_90(tmp)
				(score, top_left_j, l) = is_valid(tetris_board, tmp, H, W)
				if score > max_score and len(l) > 0:
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j
					best_l = l

			if(r == 180):
				tmp = tetris_pieces[p]		
				tmp = rotate_matrix_180(tmp)
				(score, top_left_j, l) = is_valid(tetris_board, tmp, H, W)
				if score > max_score and len(l):
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j
					best_l = l

			if(r == 270):
				tmp = tetris_pieces[p]				
				tmp = rotate_matrix_270(tmp)
				(score, top_left_j, l) = is_valid(tetris_board, tmp, H, W)
				if score > max_score and len(l):
					max_score = score
					piece_number = p
					piece_degrees = r
					top_left = top_left_j
					best_l = l

	best_l.reverse()
	niz = clean_list(best_l)
	print(best_l)

	print("{0} {1} {2}".format(piece_number, piece_degrees, top_left))
	print("{0} {1}".format(piece_number, piece_degrees), end='')
	for i in niz:
		print(" {}".format(i), end='')
	print()

