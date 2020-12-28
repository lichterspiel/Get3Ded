
def row_check(board):
	X_count = 0
	O_count = 0
	for row in board:
		for column in row:
			if column == 'X':
				X_count += 1
			elif column == 'O':
				O_count += 1
		if X_count == 3:
			raise Won
		elif O_count == 3:	
			raise Won
		else:
			X_count = 0
			O_count = 0
def column_check(board):
	X_count = 0
	O_count = 0
	for i in range(len(board[0])):
		for j in range(len(board)):
			if board[j][i] == 'X' :
				X_count += 1
			elif board[j][i] == 'O':
				O_count += 1
		if X_count == 3:
			raise Won
		elif O_count == 3:	
			raise Won
		else:
			X_count = 0
			O_count = 0
def diagonal_check(board):
	X_count = 0
	O_count = 0
	for i in range(3):
		if board[i][i] == 'X':
			X_count += 1
		elif board[i][i] == 'O':
			O_count += 1
	if X_count == 3:
		raise Won
	elif O_count == 3:
		raise Won

def diagonal2_check(board):
	X_count = 0
	O_count = 0
	for i in range(3):
		if i == 0:
			m = 2
		if i == 1:
			m = 0
		if i == 2:
			m = -2
		if board[i][i+m] == 'X':
			X_count += 1
		elif board[i][i+m] == 'O':
			O_count += 1
	if X_count == 3:
		raise Won
	elif O_count == 3:
		raise Won
