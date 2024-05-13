import pygame
import sys
import copy
import heapq

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define the grid size
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Example Sudoku board
EXAMPLE_BOARD = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Function to draw the grid and numbers
def draw_board(board):
    screen.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 4)
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 4)
        else:
            pygame.draw.line(screen, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
            pygame.draw.line(screen, GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)

    font = pygame.font.SysFont('comicsans', 40)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                text_surface = font.render(str(board[i][j]), True, BLACK)
                screen.blit(text_surface, (j * CELL_SIZE + 20, i * CELL_SIZE + 15))

# Function to check if a number can be placed in a cell
def is_safe(board, row, col, num):
    # Check row
    for i in range(GRID_SIZE):
        if board[row][i] == num:
            return False

    # Check column
    for i in range(GRID_SIZE):
        if board[i][col] == num:
            return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

# DFS (Depth-First Search)
def solve_dfs(board):
    stack = [(board, 0, 0)]  # (board, row, col)
    while stack:
        board, row, col = stack.pop()
        if row == GRID_SIZE:
            return board
        if board[row][col] != 0:
            next_row = row + 1 if col == GRID_SIZE - 1 else row
            next_col = (col + 1) % GRID_SIZE
            stack.append((board, next_row, next_col))
            continue
        for num in range(1, GRID_SIZE + 1):
            if is_safe(board, row, col, num):
                board[row][col] = num
                next_row = row + 1 if col == GRID_SIZE - 1 else row
                next_col = (col + 1) % GRID_SIZE
                stack.append((copy.deepcopy(board), next_row, next_col))
                board[row][col] = 0
    return None

# A* (A Star)
def heuristic(board):
    # Very simple heuristic: count the number of empty cells
    return sum(board[i].count(0) for i in range(GRID_SIZE))

def solve_a_star(board):
    pq = [(heuristic(board), board)]
    while pq:
        _, board = heapq.heappop(pq)
        if heuristic(board) == 0:
            return board
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
        row, col = min(empty_cells, key=lambda x: len(possible_values(board, *x)))
        for num in possible_values(board, row, col):
            new_board = copy.deepcopy(board)
            new_board[row][col] = num
            heapq.heappush(pq, (heuristic(new_board), new_board))
    return None

def possible_values(board, row, col):
    values = set(range(1, GRID_SIZE + 1))
    values -= set(board[row])  # Remove values in row
    values -= {board[i][col] for i in range(GRID_SIZE)}  # Remove values in column
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    values -= {board[i][j] for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)}  # Remove values in 3x3 box
    return values

# Main function
def main():
    board = EXAMPLE_BOARD.copy()

    draw_board(board)
    pygame.display.update()

    # Solve using DFS
    # solved_board = solve_dfs(board)

    # Solve using A*
    solved_board = solve_a_star(board)

    if solved_board:
        draw_board(solved_board)
        pygame.display.update()
    else:
        print("No solution found.")

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
