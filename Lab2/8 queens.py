import copy
import random

import time


class Board:
    AMOUNT_OF_QUEENS = 8

    def __init__(self):
        self.board = [[] for _ in range(self.AMOUNT_OF_QUEENS)]
        self.queens_positions_lst = []
        self.moving_history = []
        self.amount_of_collisions = float('inf')
        self.path_cost = 0

    def add_board(self, board):
        self.board = board
        self.queens_positions_lst = self.queens_positions()
        self.amount_of_collisions = self.number_of_collisions()

    def generate_board(self):
        for col in range(self.AMOUNT_OF_QUEENS):
            queen_index = random.randint(0, self.AMOUNT_OF_QUEENS - 1)
            for row in range(self.AMOUNT_OF_QUEENS):
                if row == queen_index:
                    self.board[row].append("Q")
                else:
                    self.board[row].append("0")
        self.queens_positions_lst = self.queens_positions()
        self.amount_of_collisions = self.number_of_collisions()

    def queens_positions(self):
        """return sorted by column index positions of the queens """
        position = []
        for row, value in enumerate(self.board):
            for column, item in enumerate(value):
                if self.board[int(row)][int(column)] == "Q":
                    position.append((row + 1, column + 1))
        return sorted(position, key=lambda k: k[1])

    def number_of_collisions(self):
        """counts the number of pairs of queens that "beat" each other"""
        collisions = 0
        for count_1, attack_queen in enumerate(self.queens_positions_lst):
            conflict_row = []
            conflict_diagonal = []
            for count_2 in range(count_1 + 1, Board.AMOUNT_OF_QUEENS):
                attacked_queen = self.queens_positions_lst[count_2]
                (atk_row, atk_column) = attack_queen
                (attacked_row, attacked_column) = attacked_queen
                if atk_row == attacked_row and attacked_row not in conflict_row:  # check rows
                    collisions += 1
                    conflict_row.append(attacked_row)
                elif abs(int(atk_row) - int(attacked_row)) == abs(
                        int(atk_column) - int(attacked_column)):  # check diagonals
                    if atk_row + atk_column == attacked_column + attacked_row and "up" + str(
                            atk_row + atk_column) not in conflict_diagonal:
                        conflict_diagonal.append("up" + str(attacked_column + attacked_row))
                        collisions += 1
                    elif attacked_column - attacked_row == atk_column - atk_row and "down" + str(
                            attacked_column - attacked_row) not in conflict_diagonal:
                        conflict_diagonal.append("down" + str(attacked_column - attacked_row))
                        collisions += 1
        return collisions

    def print_board(self):
        for row in range(self.AMOUNT_OF_QUEENS):
            for col in range(self.AMOUNT_OF_QUEENS):
                if (row + 1, col + 1) in self.queens_positions_lst:
                    print("1", end=" ")
                else:
                    print("-", end=" ")
            print()
        print()

    def move_queen(self, start_pos, finish_pos):
        new_matrix = copy.deepcopy(self.board)
        start_row, start_col = start_pos
        finish_row, finish_col = finish_pos
        new_matrix[int(start_row - 1)][int(start_col - 1)] = 0
        new_matrix[int(finish_row - 1)][int(finish_col - 1)] = "Q"
        return new_matrix

    def A_star(self):
        """searching for solutions among the nodes added to the stack
         until the heuristic function of the best solution becomes less
         than the length of the element from the stack with the smallest
         value of this function"""
        print("Algorithm: A* search")
        print("\nInitial arrangement")
        self.print_board()
        number_of_iterations = 0
        number_of_states = 0
        open_ = []
        closed = []
        solutions = []
        curr_board = Board()
        curr_board.add_board(self.board)
        curr_board.path_cost = 0
        open_.append(curr_board)
        while open_:
            curr_board = open_.pop(0)
            if solutions and solutions[0].path_cost <= open_[0].path_cost + open_[0].amount_of_collisions + 1:
                break
            for board in closed:
                number_of_iterations += 1
                if curr_board.board == board.board:
                    continue
            closed.append(curr_board)
            for queen_position in curr_board.queens_positions_lst:
                new_col = queen_position[1]
                for row_index in range(1, curr_board.AMOUNT_OF_QUEENS + 1):
                    number_of_iterations += 1
                    if row_index != queen_position[0]:
                        flag = True
                        new_row = row_index
                        new_position = (new_row, new_col)
                        new_board = Board()
                        number_of_states += 1
                        new_board.add_board(curr_board.move_queen(queen_position, new_position))
                        new_board.moving_history = curr_board.moving_history.copy()
                        new_board.moving_history.append(str(queen_position) + " => " + str(new_position))
                        new_board.path_cost = curr_board.path_cost + 1
                        new_cost = new_board.amount_of_collisions + new_board.path_cost + 1
                        if new_board.amount_of_collisions == 0:
                            if solutions and len(solutions[0].moving_history) > len(new_board.moving_history):
                                solutions.insert(0, new_board)
                                print(new_board.moving_history)
                            elif not solutions:
                                solutions.append(new_board)
                            continue
                        for board in open_:
                            number_of_iterations += 1
                            if new_board.board == board.board and board.path_cost + new_board.amount_of_collisions < new_cost:
                                flag = False
                        if flag:
                            open_.append(new_board)
                            open_.sort(key=lambda x: x.amount_of_collisions + x.path_cost)
        print("\nFinal arrangement")
        solutions[0].print_board()
        print("Total permutations done:", len(solutions[0].moving_history))
        print(solutions[0].moving_history)
        print("Amount of iterations:", number_of_iterations)
        print("Total generated states:", number_of_states)
        print("Total states in memory:", len(open_) + len(closed))

    def ldfs(self, limit=8):
        """search in depth; new nodes obtained by moving one
        queen are added to the stack, 56 new states are generated
        for each new arrangement of pieces, the search is carried out
        until an arrangement without collisions is found"""
        print("Algorithm: LDFS")
        print("\nInitial arrangement")
        self.print_board()
        stack = []
        number_of_iterations = 0
        number_of_states = 0
        solution = None
        curr_board = Board()
        curr_board.add_board(self.board)
        stack.append(curr_board)
        while len(stack):
            curr_board = stack.pop()
            if len(curr_board.moving_history) > limit:
                number_of_iterations += 1
                continue
            if curr_board.amount_of_collisions == 0:
                solution = curr_board
                break
            for queen_position in curr_board.queens_positions_lst:
                new_col = queen_position[1]
                for row_index in range(1, curr_board.AMOUNT_OF_QUEENS + 1):
                    number_of_iterations += 1
                    if row_index != queen_position[0]:
                        new_row = row_index
                        new_position = (new_row, new_col)
                        new_board = Board()
                        number_of_states += 1
                        new_board.add_board(curr_board.move_queen(queen_position, new_position))
                        new_board.moving_history = curr_board.moving_history.copy()
                        new_board.moving_history.append(str(queen_position) + " => " + str(new_position))
                        stack.append(new_board)
        print("\nFinal arrangement")
        solution.print_board()
        print("Total permutations done:", len(solution.moving_history))
        print(solution.moving_history)
        print("Amount of iterations:", number_of_iterations)
        print("Total generated states:", number_of_states)
        print("Total states in memory:", len(stack))


start = time.time()
board_ = Board()

# matrix = []
# with open("../MainVersion/input.txt", "r") as f:
#     for i_ in f:
#         j_ = [it for it in i_.strip().split(' ')]
#         matrix.append(j_)
# board_.add_board(matrix)

board_.generate_board()
board_.ldfs()
# board_.A_star()
end = time.time()
print("Time taken: ", str(end - start), "seconds / ", str((end - start) / 60), "minutes")
