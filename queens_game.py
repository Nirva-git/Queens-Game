import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Game constants
BOARD_SIZE = 8
CELL_SIZE = 70
MARGIN = 50
WINDOW_SIZE = (BOARD_SIZE * CELL_SIZE + MARGIN * 2, BOARD_SIZE * CELL_SIZE + MARGIN * 2 + 100)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Region colors (lighter versions)
REGION_COLORS = [
    (150, 255, 255),  # Cyan: #00FFFF (lighter)
    (245, 245, 220),  # Beige (lighter)
    (255, 255, 150),  # Yellow (lighter)
    (230, 230, 250),  # Lavender (lighter)
    (255, 200, 220),  # Pink (lighter)
    (200, 255, 200),  # Light green (lighter)
    (255, 210, 150),  # Orange (lighter)
    (210, 210, 150),  # Olive (lighter)
]

# Game state
# 0: empty, 1: X, 2: Queen
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Define multiple region layouts for variety
region_layouts = [
    # Layout 1
    [
        [1, 1, 1, 2, 2, 3, 3, 3],
        [1, 1, 2, 2, 2, 3, 3, 3],
        [1, 1, 2, 2, 4, 4, 4, 3],
        [5, 5, 5, 4, 4, 4, 6, 6],
        [5, 5, 5, 4, 7, 6, 6, 6],
        [5, 8, 8, 7, 7, 7, 6, 6],
        [8, 8, 8, 8, 7, 7, 7, 6],
        [8, 8, 8, 8, 8, 7, 7, 7]
    ],
    # Layout 2
    [
        [1, 1, 1, 1, 2, 2, 2, 2],
        [1, 3, 3, 3, 3, 2, 2, 2],
        [1, 3, 4, 4, 4, 4, 2, 2],
        [1, 3, 4, 5, 5, 4, 6, 6],
        [7, 7, 4, 5, 5, 4, 6, 6],
        [7, 7, 8, 8, 8, 8, 6, 6],
        [7, 7, 7, 8, 8, 8, 6, 6],
        [7, 7, 7, 7, 8, 8, 8, 8]
    ],
    # Layout 3
    [
        [1, 1, 2, 2, 3, 3, 4, 4],
        [1, 1, 2, 2, 3, 3, 4, 4],
        [5, 5, 2, 2, 3, 3, 4, 4],
        [5, 5, 6, 6, 3, 3, 4, 4],
        [5, 5, 6, 6, 7, 7, 4, 4],
        [5, 5, 6, 6, 7, 7, 8, 8],
        [5, 5, 6, 6, 7, 7, 8, 8],
        [5, 5, 6, 6, 7, 7, 8, 8]
    ],
    # Layout 4
    [
        [1, 1, 1, 2, 2, 2, 3, 3],
        [1, 4, 4, 2, 2, 3, 3, 3],
        [4, 4, 4, 5, 5, 5, 3, 3],
        [4, 4, 5, 5, 5, 6, 6, 6],
        [7, 7, 5, 5, 6, 6, 6, 6],
        [7, 7, 7, 8, 8, 6, 6, 6],
        [7, 7, 8, 8, 8, 8, 8, 8],
        [7, 7, 8, 8, 8, 8, 8, 8]
    ]
]

# Start with the first layout
current_layout = 0
regions = region_layouts[current_layout]

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Queens Game")

# Load fonts
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 36)
symbol_font = pygame.font.SysFont('Arial', 36)

# Game status message
status_message = "Place queens (♛) in each row, column, and region"

def generate_random_layout():
    """Generate a random layout with 8 distinct regions that are connected"""
    # Start with all cells as region 0
    new_layout = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # For each region 1-8
    for region in range(1, 9):
        # Start with a random cell that's not assigned yet
        available_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if new_layout[r][c] == 0]
        if not available_cells:
            break
            
        start_r, start_c = random.choice(available_cells)
        new_layout[start_r][start_c] = region
        
        # Grow the region to approximately 8 cells (each region should have 8 cells in an 8x8 board)
        cells_to_add = 7  # Already added 1
        cells_added = [(start_r, start_c)]
        
        while cells_to_add > 0 and available_cells:
            # Find cells adjacent to the current region
            adjacent_cells = []
            for r, c in cells_added:
                # Check all 4 directions (up, down, left, right)
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and 
                        new_layout[nr][nc] == 0 and (nr, nc) not in adjacent_cells):
                        adjacent_cells.append((nr, nc))
            
            if not adjacent_cells:
                # No adjacent cells available, we can't grow this region anymore
                break
            else:
                # Pick a random adjacent cell
                r, c = random.choice(adjacent_cells)
                new_layout[r][c] = region
                cells_added.append((r, c))
                cells_to_add -= 1
                available_cells.remove((r, c))
    
    # After creating connected regions, we need to ensure all cells are assigned
    # We'll use a flood fill approach to expand existing regions to fill empty spaces
    while True:
        empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if new_layout[r][c] == 0]
        if not empty_cells:
            break
            
        # For each empty cell, find an adjacent region to expand into it
        changes_made = False
        for r, c in empty_cells:
            adjacent_regions = set()
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and new_layout[nr][nc] != 0):
                    adjacent_regions.add(new_layout[nr][nc])
            
            if adjacent_regions:
                # Expand a random adjacent region into this cell
                new_layout[r][c] = random.choice(list(adjacent_regions))
                changes_made = True
        
        # If we couldn't expand any regions, assign remaining cells to random regions
        if not changes_made:
            for r, c in empty_cells:
                # Find the nearest non-empty cell and use its region
                min_dist = float('inf')
                nearest_region = 1
                
                for r2 in range(BOARD_SIZE):
                    for c2 in range(BOARD_SIZE):
                        if new_layout[r2][c2] != 0:
                            dist = abs(r - r2) + abs(c - c2)
                            if dist < min_dist:
                                min_dist = dist
                                nearest_region = new_layout[r2][c2]
                
                new_layout[r][c] = nearest_region
            break
    
    # Verify that each region is connected
    for region in range(1, 9):
        # Find all cells of this region
        region_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if new_layout[r][c] == region]
        if not region_cells:
            continue
            
        # Use BFS to check connectivity
        visited = set()
        queue = [region_cells[0]]
        visited.add(region_cells[0])
        
        while queue:
            r, c = queue.pop(0)
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and 
                    new_layout[nr][nc] == region and (nr, nc) not in visited):
                    queue.append((nr, nc))
                    visited.add((nr, nc))
        
        # If not all cells of this region are connected, merge disconnected parts with adjacent regions
        if len(visited) < len(region_cells):
            for r, c in region_cells:
                if (r, c) not in visited:
                    # Find an adjacent region to merge with
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and 
                            new_layout[nr][nc] != region):
                            new_layout[r][c] = new_layout[nr][nc]
                            break
    
    return new_layout

def draw_board():
    """Draw the game board with regions and pieces"""
    # Draw title
    layout_text = f"Layout #{current_layout + 1}" if current_layout >= 0 else "Random Layout"
    title = title_font.render(f"Queens Game (♛) - {layout_text}", True, BLACK)
    screen.blit(title, (WINDOW_SIZE[0] // 2 - title.get_width() // 2, 10))
    
    # Draw board background
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE + MARGIN
            y = row * CELL_SIZE + MARGIN
            
            # Get region and color
            region_idx = regions[row][col] - 1  # Convert 1-8 to 0-7 for array indexing
            color = REGION_COLORS[region_idx]
            
            # Draw cell with region color
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            # Draw cell content (X or Queen)
            if board[row][col] == 1:  # X
                x_text = symbol_font.render("❌", True, BLACK)
                screen.blit(x_text, (x + CELL_SIZE // 2 - x_text.get_width() // 2, 
                                    y + CELL_SIZE // 2 - x_text.get_height() // 2))
            elif board[row][col] == 2:  # Queen
                queen_text = symbol_font.render("♛", True, BLACK)
                screen.blit(queen_text, (x + CELL_SIZE // 2 - queen_text.get_width() // 2, 
                                        y + CELL_SIZE // 2 - queen_text.get_height() // 2))
    
    # Draw status message
    status_text = font.render(status_message, True, BLACK)
    screen.blit(status_text, (WINDOW_SIZE[0] // 2 - status_text.get_width() // 2, 
                             BOARD_SIZE * CELL_SIZE + MARGIN + 30))
    
    # Draw buttons
    pygame.draw.rect(screen, GRAY, (MARGIN, WINDOW_SIZE[1] - 60, 120, 40))
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(reset_text, (MARGIN + 60 - reset_text.get_width() // 2, 
                            WINDOW_SIZE[1] - 60 + 20 - reset_text.get_height() // 2))
    
    pygame.draw.rect(screen, GRAY, (WINDOW_SIZE[0] - MARGIN - 120, WINDOW_SIZE[1] - 60, 120, 40))
    check_text = font.render("Check", True, BLACK)
    screen.blit(check_text, (WINDOW_SIZE[0] - MARGIN - 60 - check_text.get_width() // 2, 
                            WINDOW_SIZE[1] - 60 + 20 - check_text.get_height() // 2))

def handle_click(pos):
    """Handle mouse click on the board"""
    global board, status_message
    
    x, y = pos
    
    # Check if click is on the board
    if (MARGIN <= x < MARGIN + BOARD_SIZE * CELL_SIZE and 
        MARGIN <= y < MARGIN + BOARD_SIZE * CELL_SIZE):
        
        # Convert pixel coordinates to board coordinates
        col = (x - MARGIN) // CELL_SIZE
        row = (y - MARGIN) // CELL_SIZE
        
        # Cycle through: empty -> X -> Queen -> empty
        board[row][col] = (board[row][col] + 1) % 3
        status_message = "Place queens (♛) in each row, column, and region"
    
    # Check if Reset button was clicked
    elif (MARGIN <= x < MARGIN + 120 and 
          WINDOW_SIZE[1] - 60 <= y < WINDOW_SIZE[1] - 20):
        reset_game()
        print("Reset button clicked")
    
    # Check if Check button was clicked
    elif (WINDOW_SIZE[0] - MARGIN - 120 <= x < WINDOW_SIZE[0] - MARGIN and 
          WINDOW_SIZE[1] - 60 <= y < WINDOW_SIZE[1] - 20):
        print("Check button clicked")
        check_solution()

def reset_game():
    """Reset the game board and change the region layout"""
    global board, status_message, regions, current_layout
    
    # Clear the board
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # Change to the next layout or generate a random one
    if random.random() < 0.3:  # 30% chance to generate a random layout
        regions = generate_random_layout()
        current_layout = -1  # Indicate random layout
        status_message = "Game reset with random layout. Each color region is connected."
        print("Changed to a random layout")
    else:
        # Use predefined layouts
        current_layout = (current_layout + 1) % len(region_layouts)
        regions = region_layouts[current_layout]
        status_message = f"Game reset with layout #{current_layout + 1}. Place queens (♛) in each row, column, and region"
        print(f"Changed to layout #{current_layout + 1}")

def check_solution():
    """Check if the current board state is a valid solution"""
    global status_message
    
    # Check rows
    for row in range(BOARD_SIZE):
        queens_in_row = board[row].count(2)
        if queens_in_row != 1:
            status_message = f"Invalid: Row {row+1} must have exactly one queen"
            return
    
    # Check columns
    for col in range(BOARD_SIZE):
        queens_in_col = sum(1 for row in range(BOARD_SIZE) if board[row][col] == 2)
        if queens_in_col != 1:
            status_message = f"Invalid: Column {col+1} must have exactly one queen"
            return
    
    # Check regions
    queens_in_region = [0] * 9  # 1-indexed regions
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 2:
                queens_in_region[regions[row][col]] += 1
    
    for region in range(1, 9):
        if queens_in_region[region] != 1:
            status_message = f"Invalid: Region {region} must have exactly one queen"
            return
    
    # Check if queens attack each other
    for row1 in range(BOARD_SIZE):
        for col1 in range(BOARD_SIZE):
            if board[row1][col1] == 2:  # If there's a queen
                for row2 in range(BOARD_SIZE):
                    for col2 in range(BOARD_SIZE):
                        if board[row2][col2] == 2 and (row1 != row2 or col1 != col2):
                            # Check if queens are adjacent (including diagonally)
                            if abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1:
                                status_message = "Invalid: Queens (♛) cannot touch each other, even diagonally"
                                return
    
    # If all checks pass
    status_message = "Congratulations! You solved the puzzle!"

def main():
    """Main game loop"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)
        
        # Draw everything
        screen.fill(WHITE)
        draw_board()
        pygame.display.flip()

if __name__ == "__main__":
    main()
