import pygame
import random
 
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 540, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
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
selected = None
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

# Solve the Sudoku using backtracking algorithm
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

# Find an empty cell in the board
def find_empty_cell():
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                return (i, j)
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
    pygame.draw.rect(screen, GRAY, generate_rect)
    pygame.draw.rect(screen, GRAY, solve_rect)
    pygame.draw.rect(screen, GRAY, clear_rect)
    screen.blit(generate_text, generate_rect)
    screen.blit(solve_text, solve_rect)
    screen.blit(clear_text, clear_rect)

# Main loop
running = True
selected = None  # Initialize selected here
generate_board()
clock = pygame.time.Clock()
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
                elif WIDTH // 2 - 50 < x < WIDTH // 2 + 50:
                    solve_sudoku()
                elif WIDTH * 3 // 4 - 50 < x < WIDTH * 3 // 4 + 50:
                    board[selected[0]][selected[1]] = 0
        
        elif event.type == pygame.KEYDOWN:
             if selected and board[selected[0]][selected[1]] == 0:  # Check if the selected cell is empty
                if event.unicode.isdigit() and int(event.unicode) in valid_moves and is_valid_move(selected[0], selected[1], int(event.unicode)):
                 board[selected[0]][selected[1]] = int(event.unicode)
        

    draw_board()
    draw_numbers()
    draw_buttons()

    if selected:
        pygame.draw.rect(screen, (0, 0, 255), (selected[1] * cell_size, selected[0] * cell_size, cell_size, cell_size), 3)

    pygame.display.flip()
    

pygame.quit()