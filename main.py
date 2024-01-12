import random
import json


def is_mine(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid) and grid[x][y] == "M"


def count_adjacent_mines(grid, x, y):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            if is_mine(grid, x + dx, y + dy):
                count += 1
    return count


def all_diagonal_mines(grid, x, y):
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if not (0 <= x + dx < len(grid) and 0 <= y + dy < len(grid)) or not is_mine(
                grid, x + dx, y + dy
            ):
                return False
    return True


def generate_minesweeper_logic(grid_size, num_mines, num_hints):
    # Initialize the grid
    grid = [["-" for _ in range(grid_size)] for _ in range(grid_size)]
    mines = set()

    # Place mines randomly
    while len(mines) < num_mines:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            grid[x][y] = "M"

    items = []

    # Add mines to items
    for x, y in mines:
        items.append(
            {
                "coordinates": {"x": x + 1, "y": y + 1},
                "type": "MINE",
                "value": "M",
            }
        )

    hint = f"sum adjacent mine(1,1) = {count_adjacent_mines(grid, 0, 0)}"
    items.append(
        {
            "coordinates": {"x": 1, "y": 1},
            "type": "HINT",
            "value": hint,
            "hint": hint,
        }
    )

    # Generate additional valid FOL hints
    hints_generated = 1  # Initialize hint counter
    hint_types = [
        "no_mines_row",
        "no_mines_col",
        "specific_mine",
        "no_adjacent_mines",
        "adjacent_mine_count",
        "all_diagonal_mines",
    ]
    while hints_generated < num_hints:
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)

        # Skip mine cells and cells where the hint would be about themselves
        if grid[x][y] == "M":
            continue

        hint_type = random.choice(hint_types)

        # Logic for generating hints
        if hint_type == "specific_mine":
            # Avoid giving a hint about the cell itself
            if (x, y) == (0, 0):
                continue
            hint = f"{'-' if not is_mine(grid, x, y) else ''}mine({x + 1},{y + 1})"
        elif hint_type == "no_mines_row" and all(
            grid[row][y] != "M" for row in range(grid_size)
        ):
            hint = f"all x -mine(x,{y + 1})"
        elif hint_type == "no_mines_col" and all(
            grid[x][col] != "M" for col in range(grid_size)
        ):
            hint = f"all y -mine({x + 1},y)"
        elif hint_type == "no_adjacent_mines":
            if any(
                is_mine(grid, x + dx, y + dy)
                for dx in range(-1, 2)
                for dy in range(-1, 2)
                if dx != 0 or dy != 0
            ):
                continue
            hint = f"all dx dy (-mine({x + 1}+dx, {y + 1}+dy) & !(dx = 0 & dy = 0))"
        elif hint_type == "adjacent_mine_count":
            adjacent_mines = count_adjacent_mines(grid, x, y)
            hint = f"sum adjacent mine({x + 1},{y + 1}) = {adjacent_mines}"
        elif hint_type == "all_diagonal_mines":
            if not all_diagonal_mines(grid, x, y):
                continue
            hint = f"all diagonal mine({x + 1},{y + 1})"
        else:
            continue

        items.append(
            {
                "coordinates": {"x": x + 1, "y": y + 1},
                "type": "HINT",
                "value": hint,
                "hint": hint,
            }
        )
        hints_generated += 1

    return items


def save_to_js_file(items, filename="items.js"):
    with open(filename, "w") as file:
        file.write("module.exports = Object.freeze(")
        file.write(json.dumps(items, indent=2))
        file.write(");")


# Example usage
grid_size = 8
num_mines = 3
num_hints = 5  # Adjust based on desired hint frequency
items = generate_minesweeper_logic(grid_size, num_mines, num_hints)
save_to_js_file(items)
