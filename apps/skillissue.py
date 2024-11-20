import numpy as np
import random
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
import time

# Inicjalizacja wyświetlacza SSD1306

device = sh1106(spi(device=0, port=0, ),rotate=2)

# Inicjalizacja przycisków
up_button = Button(6)
down_button = Button(19)
left_button = Button(5)
right_button = Button(26)

# Parametry gry
grid_size = 4
score = 0

# Inicjalizacja tablicy gry 4x4
grid = np.zeros((grid_size, grid_size), dtype=int)

# Funkcje gry 2048

def add_random_tile():
    """Dodaj losowy kafelek 2 lub 4 w pustym miejscu."""
    empty_cells = [(r, c) for r in range(grid_size) for c in range(grid_size) if grid[r, c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r, c] = 2 if random.random() < 0.9 else 4

def compress(grid):
    """Przesuwa wszystkie kafelki na lewo."""
    new_grid = np.zeros_like(grid)
    for r in range(grid_size):
        position = 0
        for c in range(grid_size):
            if grid[r, c] != 0:
                new_grid[r, position] = grid[r, c]
                position += 1
    return new_grid

def merge(grid):
    """Łączy sąsiednie kafelki o tej samej wartości."""
    global score
    for r in range(grid_size):
        for c in range(grid_size - 1):
            if grid[r, c] == grid[r, c + 1] and grid[r, c] != 0:
                grid[r, c] *= 2
                grid[r, c + 1] = 0
                score += grid[r, c]
    return grid

def reverse(grid):
    """Odwraca tablicę."""
    new_grid = np.zeros_like(grid)
    for r in range(grid_size):
        new_grid[r] = grid[r][::-1]
    return new_grid

def transpose(grid):
    """Transponuje tablicę (zmienia wiersze na kolumny)."""
    return np.transpose(grid)

def move_left(grid):
    """Ruch w lewo."""
    compressed_grid = compress(grid)
    merged_grid = merge(compressed_grid)
    final_grid = compress(merged_grid)
    return final_grid

def move_right(grid):
    """Ruch w prawo."""
    reversed_grid = reverse(grid)
    moved_grid = move_left(reversed_grid)
    return reverse(moved_grid)

def move_up(grid):
    """Ruch w górę."""
    transposed_grid = transpose(grid)
    moved_grid = move_left(transposed_grid)
    return transpose(moved_grid)

def move_down(grid):
    """Ruch w dół."""
    transposed_grid = transpose(grid)
    moved_grid = move_right(transposed_grid)
    return transpose(moved_grid)

def is_game_over():
    """Sprawdza, czy nie można wykonać więcej ruchów."""
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r, c] == 0:
                return False
            if r < grid_size - 1 and grid[r, c] == grid[r + 1, c]:
                return False
            if c < grid_size - 1 and grid[r, c] == grid[r, c + 1]:
                return False
    return True

def draw_grid(grid, score):
    """Rysowanie planszy gry i wyniku na wyświetlaczu."""
    with Image.new("1", (device.width, device.height)) as image:
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Rysowanie kafelków
        tile_size = device.height // grid_size
        for r in range(grid_size):
            for c in range(grid_size):
                value = grid[r, c]
                if value != 0:
                    draw.text((64+c * tile_size + 5, r * tile_size + 5), str(value), font=font, fill=255)
        
        # Wyświetlanie wyniku
        draw.text((0, device.height - 10), f"Score: {score}", font=font, fill=255)
        
        # Aktualizacja ekranu
        device.display(image)

# Inicjalizacja gry
add_random_tile()
add_random_tile()
draw_grid(grid, score)

# Główna pętla gry
while True:
    # Ruchy na podstawie przycisków
    moved = False
    if up_button.is_pressed:
        new_grid = move_up(grid)
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            moved = True
    elif down_button.is_pressed:
        new_grid = move_down(grid)
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            moved = True
    elif left_button.is_pressed:
        new_grid = move_left(grid)
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            moved = True
    elif right_button.is_pressed:
        new_grid = move_right(grid)
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            moved = True

    # Dodanie nowego kafelka po ruchu
    if moved:
        add_random_tile()
        draw_grid(grid, score)
    
    # Sprawdzenie końca gry
    if is_game_over():
        break
    
    time.sleep(0.1)  # Zmniejszenie szybkości reakcji na przyciski

# Wyświetlanie komunikatu końca gry
with Image.new("1", (device.width, device.height)) as image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((20, 20), "Game Over!", font=font, fill=255)
    draw.text((20, 40), f"Score: {score}", font=font, fill=255)
    device.display(image)
