import random
from asyncio import PriorityQueue

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 540, 600
WHITE = (0, 102, 102)
BLACK = (218, 165, 32)
GRAY = (245, 222, 179)
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Fonts
font = pygame.font.SysFont("comicsansms", 40)
small_font = pygame.font.SysFont("comicsansms", 20)

# Board settings
board_size = 9
cell_size = 60
grid_size = board_size * cell_size
board = [[0 for _ in range(board_size)] for _ in range(board_size)]
selected: None = None
valid_moves = set(range(1, board_size + 1))


# Helper function to generate a random Sudoku board
def generate_board():
    global board
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    for _ in range(20):  # Adjust the number of iterations for difficulty
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        num = random.randint(1, board_size)
        if is_valid_move(row, col, num):
            board[row][col] = num


# Check if a move is valid
def is_valid_move(row, col, num):
    for i in range(board_size):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True


# Solve the Sudoku using Depth-first search algorithm
def solve_sudoku():
    empty_cell = find_empty_cell()
    if not empty_cell:
        return True
    row, col = empty_cell
    for num in range(1, board_size + 1):
        if is_valid_move(row, col, num):
            board[row][col] = num
            if solve_sudoku():
                return True
            board[row][col] = 0
    return False

# Solve the Sudoku using Depth-Limited Search algorithm
def solve_sudoku_dls(depth_limit):
    def dls(board, depth):
        empty_cell = find_empty_cell()
        if not empty_cell:
            return True
        if depth == depth_limit:  # يتم التحقق من الحد الأقصى للعمق
            return False
        row, col = empty_cell
        for num in range(1, board_size + 1):
            if is_valid_move(row, col, num):
                board[row][col] = num
                if dls(board, depth + 1):  # زيادة العمق بشكل تدريجي
                    return True
                board[row][col] = 0
        return False

    return dls(board, 0)  # بدء البحث من العمق 0


    # Solve the Sudoku using Breadth-First Search algorithm
from collections import deque

def solve_sudoku_bfs():
    queue = deque()  # استخدام deque كطابور
    queue.append(board)  # إضافة اللوحة الأساسية إلى الطابور
    while queue:
        current_board = queue.popleft()  # استخراج أول لوحة من الطابور
        empty_cell = find_empty_cell(current_board)  # البحث عن الخلية الفارغة في اللوحة
        if not empty_cell:
            return True  # تم حل السودوكو
        row, col = empty_cell
        for num in range(1, board_size + 1):
            if is_valid_move(current_board, row, col, num):
                new_board = [row[:] for row in current_board]  # إنشاء نسخة جديدة من اللوحة
                new_board[row][col] = num  # وضع الرقم في الخلية الفارغة
                queue.append(new_board)  # إضافة اللوحة الجديدة إلى الطابور
    return False  # لم يتم العثور على حل

# Solve the Sudoku using Greedy Best-First Search algorithm
def is_solved(current_board):
    pass


def heuristic(new_board):
    pass


def solve_sudoku_greedy_best_first(board):
    priority_queue = PriorityQueue()  # Initialize the priority queue
    priority_queue.put((0, board))  # Put the initial board configuration with priority 0
    while not priority_queue.empty():
        _, current_board = priority_queue.get()  # Get the board configuration with the highest priority
        if is_solved(current_board):  # Check if the board is solved
            return current_board
        empty_cell = find_empty_cell(current_board)  # Find the first empty cell in the board
        row, col = empty_cell
        for num in range(1, 10):  # Try all possible numbers for the empty cell
            if is_valid_move(current_board, row, col, num):
                new_board = current_board.copy()  # Create a copy of the board
                new_board[row][col] = num  # Place the number in the empty cell
                priority =heuristic(new_board)  # Calculate the priority using a heuristic function
                priority_queue.put((priority, new_board))  # Put the new board configuration with its priority into the queue
    return None

    board[row][col] = 0
    return False
import heapq

# A* Search Algorithm for Sudoku
def solve_sudoku_a_star(board):
    def heuristic(board):
        # يُحسب التقدير المتوقع لتكلفة الانتقال إلى الهدف
        # يُمكن تحسين هذه الدالة بشكل أفضل للتقدير المتوقع
        return 0

    # دالة للتحقق من تكرار القيم
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num or board[(row//3)*3 + i//3][(col//3)*3 + i%3] == num:
                return False
        return True

    # تحديد الخلية التالية للملء
    def find_next_empty(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    # بدء البحث
    heap = []
    heapq.heappush(heap, (0, board))
    while heap:
        _, current_board = heapq.heappop(heap)
        next_empty = find_next_empty(current_board)
        if not next_empty:
            return current_board
        row, col = next_empty
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                heapq.heappush(heap, (heuristic(new_board), new_board))
    return None

# قم بتعريف اللوحة هنا واستدعاء الدالة لحلها

from collections import deque



# Find an empty cell in the given board configuration
def find_empty_cell(board):
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                return (i, j)
    return None




# Add an AI function to solve the Sudoku automatically
def ai_solve_sudoku():
    solve_sudoku()
    solve_sudoku_a_star(board)
    solve_sudoku_greedy_best_first(board)
    solve_sudoku_dls()
    solve_sudoku_bfs()

    # Heuristic function: count empty cells
def heuristic_count_empty_cells(board):
        count = 0
        for row in board:
            count += row.count(0)  # Count the number of empty cells in each row
        return count

    # You can add additional AI logic here if needed


# Find an empty cell in the board
def find_empty_cell():
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                return i, j
    return None


# Draw the Sudoku board
def draw_board():
    screen.fill(WHITE)
    for i in range(board_size + 1):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (cell_size * i, 0), (cell_size * i, grid_size), 4)
            pygame.draw.line(screen, BLACK, (0, cell_size * i), (grid_size, cell_size * i), 4)
        else:
            pygame.draw.line(screen, GRAY, (cell_size * i, 0), (cell_size * i, grid_size), 2)
            pygame.draw.line(screen, GRAY, (0, cell_size * i), (grid_size, cell_size * i), 2)


# Draw numbers on the board
def draw_numbers():
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] != 0:
                num_text = font.render(str(board[i][j]), True, BLACK)
                num_rect = num_text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
                screen.blit(num_text, num_rect)


# Draw buttons for control
def draw_buttons():
    generate_text = small_font.render("Generate", True, BLACK)
    solve_text = small_font.render("Solve", True, BLACK)
    clear_text = small_font.render("Clear", True, BLACK)
    generate_rect = generate_text.get_rect(center=(WIDTH // 4, grid_size + 30))
    solve_rect = solve_text.get_rect(center=(WIDTH // 2, grid_size + 30))
    clear_rect = clear_text.get_rect(center=(WIDTH * 3 // 4, grid_size + 30))
    pygame.draw.rect(screen, WHITE, generate_rect)
    pygame.draw.rect(screen, WHITE, solve_rect)
    pygame.draw.rect(screen, WHITE, clear_rect)
    screen.blit(generate_text, generate_rect)
    screen.blit(solve_text, solve_rect)
    screen.blit(clear_text, clear_rect)


# Show message upon solving Sudoku
def show_message(message):
    message_text = small_font.render(message, True, BLACK)
    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(message_text, message_rect)


# Main loop
running = True
selected = None  # Initialize selected here
generate_board()
clock = pygame.time.Clock()
solved = False  # Flag to track if Sudoku is solved
ai_enabled = False  # Flag to track if AI solving is enabled

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < grid_size:
                selected = (y // cell_size, x // cell_size)
            else:
                if WIDTH // 4 < x < WIDTH // 4 + 100:
                    generate_board()
                    solved = False
                    ai_enabled = False  # Disable AI when generating a new board
                elif WIDTH // 2 - 50 < x < WIDTH // 2 + 50:
                    if ai_enabled:
                        ai_solve_sudoku()  # Use AI to solve Sudoku
                        solved = True
                    else:
                        if solve_sudoku():
                            solved = True
                elif WIDTH * 3 // 4 - 50 < x < WIDTH * 3 // 4 + 50:
                    board[selected[0]][selected[1]] = 0

        elif event.type == pygame.KEYDOWN:
            if selected and board[selected[0]][selected[1]] == 0:  # Check if the selected cell is empty
                if event.unicode.isdigit() and int(event.unicode) in valid_moves and is_valid_move(selected[0],
                                                                                                   selected[1],
                                                                                                   int(event.unicode)):
                    board[selected[0]][selected[1]] = int(event.unicode)

    draw_board()
    draw_numbers()
    draw_buttons()

    if selected:
        pygame.draw.rect(screen, (0, 0, 255), (selected[1] * cell_size, selected[0] * cell_size, cell_size, cell_size),
                         3)

    if solved:
        show_message("Sudoku Solved!")

    pygame.display.flip()

pygame.quit()