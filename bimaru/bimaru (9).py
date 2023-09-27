# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 98855 João Martinho
# 99441 Samuel Pearson


import sys
import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    #(vetor (a,b,c,d) especificando o numero de barcos de cada tipo ja postos no tabuleiro)
    """Representação interna de um tabuleiro de Bimaru."""
    
    
    def __init__(self, board, action): #action é (x,y,b,o) onde x,y são coord., b é tipo de barco e o é orientação vertical ou horizontal
        
    #Se board == None é porque __init__ foi chamada no parse_instance
        if board == None:
            
            self.grid = None
            
            self.row_counts = None
            self.col_counts = None
            
            self.boat_counts = None 
            
            self.present_row_counts = None
            self.present_col_counts = None
            
            self.hints = None
            
            self.good_squares = None
            
        else: 
            
            x = action[0]
            y = action[1]
            boat_type = action[2]
            
            self.grid = self.copiaGrelha(board.grid)
            
            self.row_counts = self.copia(board.row_counts)
            self.col_counts = self.copia(board.col_counts)
            
            self.boat_counts = self.copia(board.boat_counts)
            self.boat_counts[boat_type] += 1
            
            #Atualizar contagens:
            ncounts = board.new_counts(action)
            self.present_row_counts = ncounts[0]
            self.present_col_counts = ncounts[1]
            
            #obter grelha resultante da ação
                
            if boat_type == 0:
                    self.grid[x][y] = "c"
    
            elif boat_type == 1:
                if action[3]=="v":
                    if self.get_value(x, y) == '.': self.grid[x][y] = "t"
                    if self.get_value(x + 1, y) == '.': self.grid[x + 1][y] = "b"
                else:
                    if self.get_value(x, y) == '.': self.grid[x][y] = "l"
                    if self.get_value(x, y + 1) == '.': self.grid[x][y + 1] = "r"
    
            elif boat_type == 2:
                if action[3]=="v":
                    if self.get_value(x, y) == '.': self.grid[x][y] = "t"
                    if self.get_value(x + 1, y) == '.': self.grid[x + 1][y] = "m"
                    if self.get_value(x + 2, y) == '.': self.grid[x + 2][y] = "b"
                else:
                    if self.get_value(x, y) == '.': self.grid[x][y] = "l"
                    if self.get_value(x, y + 1) == '.': self.grid[x][y + 1] = "m"
                    if self.get_value(x, y + 2) == '.': self.grid[x][y + 2] = "r"
    
            else:
                if action[3]=="v":
                    if self.get_value(x, y) == '.': self.grid[x][y] = "t"
                    if self.get_value(x + 1, y) == '.': self.grid[x + 1][y] = "m"
                    if self.get_value(x + 2, y) == '.': self.grid[x + 2][y] = "m"
                    if self.get_value(x + 3, y) == '.': self.grid[x + 3][y] = "b"
                else:
                    if self.get_value(x, y) == '.': self.grid[x][y] = "l"
                    if self.get_value(x, y +1) == '.': self.grid[x][y + 1] = "m"
                    if self.get_value(x, y + 2) == '.': self.grid[x][y + 2] = "m"
                    if self.get_value(x, y + 3) == '.': self.grid[x][y + 3] = "r"
            
            
            #Obter lista de hints e good_squares (good_squares só se hints estiverem vazias)
            if len(board.hints) == 0:
                self.hints = []
            else:
                self.hints = self.copia(board.hints[1:])
                
            self.good_squares_upd(board, action)

    def good_squares_upd(self, board, action):
        
        if board == None or len(board.hints) > 0:
            
            if  len(self.hints) == 0:
                self.good_squares = []
                for i in range(10):
                    if self.present_row_counts[i] < self.row_counts[i]:
                        for j in range(10):
                            add = False
                            if self.present_col_counts[j] < self.col_counts[j]:
                                add = True
                                if self.get_value(i,j) != ".":
                                    add = False
                                else:
                                    for k in self.adjacent(i,j):
                                        if self.get_value(k[0],k[1]) != "." and self.get_value(k[0],k[1]) != "W":
                                            add = False
                                            break
                            if add:
                                self.good_squares += [(i,j)]
                            
            else:
                self.good_squares = None

        else:
            self.good_squares = []
            for sq in board.good_squares:
                if sq not in self.boat_adjacent(action) and self.present_row_counts[sq[0]] < self.row_counts[sq[0]] and self.present_col_counts[sq[1]] < self.col_counts[sq[1]]:
                    self.good_squares += [sq]

    #Se hints vazias, update dos good_squares. C.c, deixa como None
    def good_squares_upd2(self):
        
        if len(self.hints) == 0:
            self.good_squares = []
            for i in range(10):
                for j in range(10):
                    add = True
                    if self.get_value(i,j) != ".":
                        add = False
                    else:
                        for k in self.adjacent(i,j):
                            if self.get_value(k[0],k[1]) != "." and self.get_value(k[0],k[1]) != "W":
                                add = False
                                break
                        if self.present_row_counts[i] == self.row_counts[i]:
                            add = False
                            #break
                        if self.present_col_counts[j] == self.col_counts[j]:
                            add = False
                            #break
                    if add:
                        self.good_squares += [(i,j)]
        else:
            self.good_squares = None

    def copia(self, lista):
        return [element for element in lista]
    
    def copiaGrelha(self, grelha):
        res = np.full((10,10), '.')
        for i in range(10):
            for j in range(10):
                if res[i][j] != grelha[i][j]:
                    res[i][j] = grelha[i][j]
        return res

    def v_adjacent(self, x,y): #devolve verticais adjacentes incluindo o proprio (x,y)
        l=[]
        for j in range(max(x - 1, 0), min(x + 2, 10)):
            l += [(j, y)]
        return l
    
    def h_adjacent(self, x,y): #devolve horizontais adjacentes incluindo o proprio (x,y)
        l=[]
        for j in range(max(y - 1, 0), min(y + 2, 10)):
            l += [(x, j)]
        return l

    def adjacent(self, x,y): # devolve todos quadrados adjacentes a (x,y)

        if 0 < x < 9:
            if 0 < y < 9:
                
                return [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 1), (x , y - 1), (x - 1, y), (x - 1, y + 1), (x - 1, y - 1)]
            
            elif y == 0:
                return  [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y), (x - 1, y + 1)]
            
            elif y == 9:
                return  [(x + 1, y), (x + 1, y - 1), (x , y - 1), (x - 1, y),  (x - 1, y - 1)]
            
        elif x == 0:
            
            if 0 < y < 9:
                return  [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 1), (x , y - 1)]
            
            elif y == 0:
                return  [(x + 1, y), (x + 1, y + 1), (x, y + 1)]
            
            elif y == 9:
                return [(x + 1, y),  (x + 1, y - 1), (x , y - 1)]
            
        if x == 9:
            
            if 0 < y < 9:
                return [(x, y + 1), (x , y -  1), (x - 1, y), (x - 1, y + 1), (x - 1, y - 1)]
            
            elif y == 0:
                return [(x, y + 1),  (x - 1, y), (x - 1, y + 1)]
            
            elif y == 9:
                return [(x , y - 1), (x - 1, y),  (x - 1, y - 1)]
            
    def boat_adjacent(self, action): #quadrados do barco e adjacentes ao barco
        
        x = action[0]
        y = action[1]
        boat_type = action[2]
        
        if boat_type == 0:
            l = self.adjacent(x, y)
            l += [(x, y)]

        else:
            l=[]
            if action[3]=="v":
                for i in range(max(0, x - 1), min(10, x + boat_type + 2)):
                    for k in self.h_adjacent(i,y):
                        l += [k]
            else:
                for i in range(max(0, y - 1), min(10, y + boat_type + 2)):
                    for k in self.v_adjacent(x, i):
                        l += [k]
        return l
        
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col]


    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row!=0:
            if row!=9:
                return (self.get_value(row-1, col), self.get_value(row+1, col))
            else:
                return (self.get_value(row-1, col), '.')
        else:
            return ('.', self.get_value(row+1, col))


    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col!=0:
            if col!=9:
                return (self.get_value(row,col-1), self.get_value(row, col+1))
            else:
                return (self.get_value(row, col-1), '.')
        else:
            return ('.', self.get_value(row,col+1))
        
    def new_boat_squares(self, action): #devolve lista de todos os quadrados que mudam de '.' para uma peça de barco
        
        x = action[0]
        y = action[1]
        boat_type = action[2]
        res = []

        
        if action[3] == 'v':
            if y < 0 or y > 9:
                return False
            if x < 0 or x + boat_type > 9:
                return False
            for k in range(x, x + boat_type + 1):
                if self.get_value(k, y) == '.':
                    res += [(k,y)]
        else:
            if x < 0 or x > 9:
                return False
            if y < 0 or y + boat_type > 9:
                return False
            for k in range(y, y + boat_type + 1):
                if self.get_value(x, k) == '.':
                    res += [(x,k)]
        return res
    
    def total_boat_squares(self, action): #lista de todos os quadrados do barco
            
        x = action[0]
        y = action[1]
        boat_type = action[2]
        res = []
        
        if action[3] == 'v':
            if x < 0 or x + boat_type > 9:
                return False
            for k in range(x, x + boat_type + 1):
                res += [(k,y)]
        else:
            if y < 0 or y + boat_type > 9:
                return False
            for k in range(y, y + boat_type + 1):
                res += [(x,k)]
        return res
    
    def new_counts(self, action): #par de listas corresp. à contagem por linha e coluna atualizadas
        
        res = (self.copia(self.present_row_counts), self.copia(self.present_col_counts))
        
        for square in self.new_boat_squares(action):
            res[0][square[0]] += 1
            res[1][square[1]] += 1
            
        return res


    #Para ver se uma ação é válida quando o tabuleiro ainda tem dicas sem ser barcos completos
    def initial_action_check(self, action):
        
        #Nota: não consideramos barcos do tipo 0 pois estes são retirados das hints (já estão completos)
        
        x = action[0]
        y = action[1]
        boat_type = action[2]
        
        position = self.get_value(x, y)
        
        #já vemos se não excede nº de barcos desse tipo no valid_action
        
        
        # verificamos se o barco encaixa no tabuleiro

        if action[3] == 'v':

            if x + boat_type > 9: 
                return False
        else:
            if y + boat_type > 9: 
                return False
            
        #cria lista de quadrados adjacentes ao barco que queremos por
        only_adj = [x for x in self.boat_adjacent(action) if x not in self.total_boat_squares(action)]
        
        #ver se esses quadrados adjacentes não têm barcos
        for j in only_adj:
            if self.get_value(j[0],j[1]) != 'W' and self.get_value(j[0],j[1]) != '.':
                return False

        #se barco é na vertical...
        if action[3] == 'v':
            
            #verificar posição inicial e extremo
            if position != "." and position != "T":
                return False
            
            if self.get_value(x + boat_type, y) != "." and self.get_value(x + boat_type, y) != "B":
                return False
            
            #se barco c/ mais de 2 peças, so pode ter '.' ou 'M' pelo meio
            if boat_type > 1:
                for i in range(x + 1, x + boat_type):
                    if self.get_value(i, y) != "." and self.get_value(i, y) != "M":
                        return False
            
            
            #ver extra-adjacentes (nao pode haver um top 2 em cima por ex)
            
            for i in range(max(0, x - 1), min(x + boat_type + 2, 10)):
                if y > 1 and self.get_value(i, y - 2) == 'L':
                    return False
                if y < 8 and self.get_value(i, y + 2) == 'R':
                    return False
                
            if x > 1 and self.get_value(x - 2, y) == 'T':
                return False
            if x + boat_type < 8 and self.get_value(x + boat_type + 2, y) == 'B':
                return False
            


        else: #(horizontal)
            
            #verificar posição inicial e extremo
            if position != "." and position != "L":
                return False
            
            if self.get_value(x, y + boat_type) != "." and self.get_value(x, y + boat_type) != "R":
                return False
            
            #se barco c/ mais de 2 peças, so pode ter '.' ou 'M' pelo meio
            if boat_type > 1:
                for i in range(y + 1, y + boat_type):
                    if self.get_value(x, i) != "." and self.get_value(x, i) != "M":
                        return False
            
            
            #ver extra-adjacentes (nao pode haver um top 2 acima por ex)
            
            for i in range(max(0, y - 1), min(y + boat_type + 2, 10)):
                if x > 1 and self.get_value(x - 2, i) == 'T':
                    return False
                if x < 8 and self.get_value(x + 2, i) == 'B':
                    return False
                
            if y > 1 and self.get_value(x, y - 2) == 'L':
                return False
            if y + boat_type < 8 and self.get_value(x, y + boat_type + 2) == 'R':
                return False


        return True
    
    def valid_action(self, action):
        
        if self.boat_counts[action[2]] == 4 - action[2]:
            return False

        
        new_squares = self.new_boat_squares(action) #quadrados do barco que queremos por e ainda não estavam na grelha
        all_squares = self.total_boat_squares(action) #quadrados totais do barco
        
        if new_squares == False: #devolve falso se a posição do barco sair do limite da grelha
            return False
        

        #ver se não excedemos contagens
        if len(new_squares) > 0:
            first_coordinates, second_coordinates = zip(*new_squares)
            unique_first = list(set(first_coordinates)) #coord. de linhas em que queremos adicionar peças
            unique_second = list(set(second_coordinates)) #coord. de colunas " " "
            
            ncounts = self.new_counts(action) #contagem atualizada se a ação for realizada
            
            #verificar que não excede contagem
            for row in unique_first:
                if ncounts[0][row] > self.row_counts[row]:
                    return False
            for col in unique_second:
                if ncounts[1][col] > self.col_counts[col]:
                    return False
        

        if self.hints == []:
            
            #ver se não excedemos contagem do tipo de barco
            if self.boat_counts[action[2]] + 1 > 4 - action[2]:
                return False
            
            #verificar se todos quadrados que queremos estão nos good_squares
            for square in all_squares:
                if square not in self.good_squares:
                    return False
            return True
        
        else:
            
            #a ação tem de corresponder à 1ª dica
            if (self.hints[0][0], self.hints[0][1]) not in self.total_boat_squares(action):
                return False
            
            return self.initial_action_check(action)

    def print(self):
        
        res = ''
        for x in range(10):
            for y in range(10):
                res += self.get_value(x, y)
                if y == 9:
                    res += '\n'
        return res

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
            
        """
        
        values = [] # vai ser uma lista em q 10 primeiros são row counts, 10-20 são col counts e dos são triplos x,y,T onde T é top, bottom, middle, etc
        
        for line in sys.stdin:
            line = line.strip().split()
            if len(line)>1:
                values += [line[1:]]
        
        
        B = Board(None, None)
        
        B.row_counts = values[0]
        B.col_counts = values[1]
        
        #passar para inteiros
        for k in range(0,10):
            B.row_counts[k] = int(B.row_counts[k])
            B.col_counts[k] = int(B.col_counts[k])
            
        B.present_row_counts = np.full(10, 0)
        B.present_col_counts = np.full(10, 0)
        

        B.hints = values[2:]
        
        B.grid = np.full((10,10), '.')
        
        for i in range(len(B.hints)):
            B.grid[int(B.hints[i][0])][int(B.hints[i][1])] = B.hints[i][2]
            
        for hint in values[2:]:
            if hint[2] == 'W' or hint[2] == 'C':
                B.hints.remove(hint)
                
        for i in range(len(B.hints)):
            B.hints[i][0] = int(B.hints[i][0])
            B.hints[i][1] = int(B.hints[i][1])
        
        B.good_squares = None
        
        
            
        B.boat_counts = [0,0,0,0]
        for a in range(0,10):
            for b in range(0,10):
                
                if B.grid[a][b] != '.' and B.grid[a][b] != 'W':
                    B.present_row_counts[a] += 1
                    B.present_col_counts[b] += 1
                
                #ver se já há barcos completos nas dicas:
                if B.grid[a][b] == 'C':
                    B.boat_counts[0] += 1
                    
                elif B.grid[a][b] == 'T':
                    k = 1
                    found = False
                    while not found and k < 4 and a + k < 10:
                        if B.grid[a + k][b] == 'B':
                            B.boat_counts[k] += 1
                            found = True
                            for i in range(a, a + k + 1):
                                for hint in B.hints:
                                    if hint[0] == i and hint[1] == b:
                                        B.hints.remove(hint)
                        elif B.grid[a + k][b] != 'M':
                            found = True
                        k += 1
                        
                elif B.grid[a][b] == 'L':
                    k = 1
                    found = False
                    while not found and k < 4 and b + k < 10:
                        if B.grid[a][b + k] == 'R':
                            B.boat_counts[k] += 1
                            found = True
                            for i in range(b, b + k + 1):
                                for hint in B.hints:
                                    if hint[0] == a and hint[1] == i:
                                        B.hints.remove(hint)
                        elif B.grid[a][b + k] != 'M':
                            found = True
                        k += 1
                        
        B.good_squares_upd(None,None)
        return B
    
    
        
        
    # TODO: outros metodos da classe


class Bimaru(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        #????
        self.initial = BimaruState(board)
        pass

    def actions(self, state: BimaruState): #(coor, coor, tipo de barco, orientacao)
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        moves=[]
        
        #ver se para cada tipo de barco, se faltam n desse tipo, as acoes devolvem pelo menos n desse tipo
        bcounts = state.board.boat_counts
        remaining_boats = [4 - bcounts[0], 3 - bcounts[1], 2 - bcounts[2], 1 - bcounts[3]]
        boat_in_actions = [0, 0, 0, 0]
        
        #otimizar: se há hints, temos poucas ações possíveis
        if len(state.board.hints) > 0:
            
            x = state.board.hints[0][0]
            y = state.board.hints[0][1]
            letter = state.board.hints[0][2]
            
            
            for i in range(1,4):
                if letter == 'T':
                    action1 = (x, y, i, 'v')
                    if state.board.valid_action(action1):
                        moves += [action1]
                elif letter == 'B':
                    action1 = (x - i, y, i, 'v' )
                    if state.board.valid_action(action1):
                        moves += [action1]
                elif letter == 'L':
                    action1 = (x, y, i, 'h')
                    if state.board.valid_action(action1):
                        moves += [action1]
                elif letter == 'R':
                    action1 = (x, y - i, i, 'h' )
                    if state.board.valid_action(action1):
                        moves += [action1]
                elif letter == 'M':
                    if i == 2:
                        action1 = (x - 1, y, 2, 'v')
                        action2 = (x, y - 1, 2, 'h')
                        if state.board.valid_action(action1):
                            moves += [action1]
                        if state.board.valid_action(action2):
                            moves += [action2]
                    elif i == 3:
                        action1 = (x - 2, y, 3, 'v')
                        action2 = (x - 1, y, 3, 'v')
                        action3 = (x, y - 2, 3, 'h')
                        action4 = (x, y - 1, 3, 'h')
                        if state.board.valid_action(action1):
                            moves += [action1]
                        if state.board.valid_action(action2):
                            moves += [action2]
                        if state.board.valid_action(action3):
                            moves += [action3]
                        if state.board.valid_action(action4):
                            moves += [action4]

        #otimizar: se nao ha hints começar logo num good square
        
        else:
           
                        
            ############# as ações possíveis só correspondem a barcos do maior tipo possível
            i = 3
            j = 0 #guarda o valor do tipo de barco que vamos usar
            while i >= 0:
                if bcounts[i] < 4 - i:
                    j = i
                    for square in state.board.good_squares:
                        action1 = (square[0], square[1],i,"v")
                        if i != 0:
                            action2 = (square[0],square[1],i,"h")
                            if state.board.valid_action(action2):
                                moves += [action2]
                                boat_in_actions[i] += 1
                        if state.board.valid_action(action1):
                            moves += [action1]
                            boat_in_actions[i] += 1
                    i = -1
                else:
                    i -= 1
            
            
            
            #############
        
            #retorna lista vazia se ha um tipo de barco cuja contagem ja nao pode ser atingida
            #for i in range(4):
            if remaining_boats[j] > boat_in_actions[j]:
                moves = []
        
        return moves


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        B = Board(state.board, action)
        return BimaruState(B)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        return state.board.boat_counts == [4,3,2,1]

    def h1(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        return 20 - sum(node.state.board.present_row_counts)
        #return 10 - sum(node.state.board.boat_counts)
        
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        missing_row = np.amax(np.subtract(np.array(node.state.board.row_counts), np.array(node.state.board.present_row_counts)))
        missing_col = np.amax(np.subtract(np.array(node.state.board.col_counts), np.array(node.state.board.present_col_counts)))
        return missing_row + missing_col
        #return len(node.state.board.good_squares) if node.state.board.good_squares else 0

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    #print(board.grid)
    #print(board.row_counts)
    #print(board.col_counts)
    #print(board.hints)
    problem = Bimaru(board)
    """
    s0 = BimaruState(board)
    B = problem.result(s0, (0,0,3,'v'))
    print(B.board.grid)
    print(B.board.hints)
    print(problem.actions(B))
    print(B.board.good_squares)
    """
    #print((2,0) in board.total_boat_squares((0,0,2,'v')))
    #print(board.valid_action((0,0,2,'v')))
    #B = Board(board, (0,0,2,'v'))
    #print(B.grid)
    #print(B.hints)
    
    
    goal_node = astar_search(problem)
    #goal_node = iterative_deepening_search(problem)
    #print(problem.goal_test(goal_node.state))
    #print(goal_node.state.board.grid)
    print(goal_node.state.board.print(), file = sys.stdout, end = '')
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass



#exemplo: ROW\t2\t3\t2\t2\t3\t0\t1\t3\t2\t2\nCOLUMN\t6\t0\t1\t0\t2\t1\t3\t1\t2\t4\n 6\n HINT\t0\t0\tT\nHINT\t1\t6\tM\nHINT\t3\t2\tC\nHINT\t6\t0\tW\nHINT\t8\t8\tB\nHINT\t9\t5\tC\n


#tabuleiro = Board.parse_instance()


