# Algorithms used to solve the problem

def is_solved(board):
   count = 0
   for i in range(len(board)): 
      if board[i] == 'X':
         count = count + 1
   if count == 1:
      return True
   else:
      return False

# ----- RETURNS LIST OF MOVES Eg-(3, 'R')-----
def find_moves(board):
   moves = []
   for i in range(len(board)):
      if board[i] == 'X':
         if (i < len(board)-2 and board[i+1] == 'X'):
            if board[i+2] == 'o':
               moves.append((i, 'R'))
         if i > 1 and board[i-1] == 'X':
            if board[i-2] == 'o':
               moves.append((i, 'L'))
   return moves

# ------ Takes input (3,'R') format and outputs 'Xoxox' transform -----               
def make_move(board, move):
   new_move = list(board)
   position = move[0]
   if 'L' in move:
      new_move[position] = 'o'
      new_move[position-1] = 'o'
      new_move[position-2] = 'X'
   if 'R' in move:
      new_move[position] = 'o'
      new_move[position+1] = 'o'
      new_move[position+2] = 'X'
   return ''.join(new_move)


def spanningTree2(u, gameBoard):
   parents = { u : ( None, None ) }
   D = { u }
   while(D):
      Dnew = set()
      for v in D:
         possible_moves = find_moves(v)
         for move in possible_moves :
            w = make_move(v, move)
            if w == None or w in parents or w in D:
               continue
            parents[w] = (v, move)
            if w == is_solved(v): return parents
            Dnew.add(w)
      D = Dnew
   return parents


def possible_final_paths(gameboard):
   paths = []
   alter = []
   saveString = []
   for i in range(len(gameboard)):
      alter.append('o')
      
   for m in range(len(gameboard)):
      saveString = alter
      for i in range(len(gameboard)):
         if m!= i:
            saveString[i] = 'o'
         saveString[m] = 'X'
      paths.append(''.join(saveString))
   return paths


def get_path(parents, finish_condition):
   boardshape, u = parents[finish_condition]
   if u == None: return[]
   return get_path(parents, boardshape)+[boardshape]      
                  

def pegsSolution(gameBoard):
   V = []
   V.append(gameBoard)
   tree = (spanningTree2(gameBoard, gameBoard))

   Solution = None
   final_p = []
   for i in possible_final_paths(gameBoard):
      li = []
      if i in tree.keys():
         li.append(i)

      for v in li:
         Solution = v
   if Solution == None:
      pass
   else:
      final_p.append(get_path(tree, Solution))
      final_p[0].append(Solution)

   return_list = []
   for v in final_p:
      for c in v:
         if c == gameBoard:
            pass
         else:
            a,b =tree[c]
            return_list.append(b)
   
   return return_list

