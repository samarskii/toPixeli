import random
from PIL import Image

# Define specific colors for use when USE_SPECIFIC_COLORS is True
SPECIFIC_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0)   # Orange
]

# Flags and parameters to control the behavior of the rule
USE_SPECIFIC_COLORS = False  # Flag to switch between specific and random colors
USE_RANDOM_AMOUNT = True  # Flag to switch between random and specific amount of first color
PARTICULAR_AMOUNT = 50  # Specific amount to use if USE_RANDOM_AMOUNT is False

SPECIFIC_SEED = None  # Specific seed value for reproducibility, e.g., 42

BORDER_THICKNESS = 1  # Thickness of the colored border in pixels

def get_colors():
    """Generate a list of colors. Use specific colors if USE_SPECIFIC_COLORS is True, otherwise generate random colors."""
    if USE_SPECIFIC_COLORS:
        return SPECIFIC_COLORS
    else:
        return [(random.randint(0, 1) * 255, random.randint(0, 1) * 255, random.randint(0, 1) * 255) for _ in range(5)]

def get_amount_of_first_color(canvas):
    """Determine the amount of the first color to use. Use a random amount if USE_RANDOM_AMOUNT is True, otherwise use PARTICULAR_AMOUNT."""
    if USE_RANDOM_AMOUNT:
        return round((canvas.size[0] * canvas.size[1]) / random.randint(5, 8) * random.randint(1, 2))
    else:
        return PARTICULAR_AMOUNT

def rule6(canvas):
    """Apply the rule6 pattern to the given canvas."""
    if SPECIFIC_SEED is not None:
        random.seed(SPECIFIC_SEED)
        
    colors = get_colors()
    first_color = colors[0]
    second_color = colors[1]
    third_color = colors[2]
    fourth_color = colors[3]
    border_color = colors[4]

    amount_of_first_color = get_amount_of_first_color(canvas)
    first_positions = set()
    max_attempts = canvas.size[0] * canvas.size[1] * 10  # Safeguard to prevent infinite loops
    attempts = 0
    
    # Place the first color randomly on the canvas
    while len(first_positions) < amount_of_first_color and attempts < max_attempts:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        first_positions.add((x, y))
        canvas.putpixel((x, y), first_color)
        attempts += 1

    if attempts == max_attempts:
        print("Max attempts reached while placing first color. Some positions might not be placed.")

    list_of_first_positions = list(first_positions)

    # Define subrules for how the pattern should expand
    submodes = ["DIAGONAL_UP_RIGHT", "DIAGONAL_UP_LEFT", "DIAGONAL_DOWN_RIGHT", "DIAGONAL_DOWN_LEFT", "CROSS", "SQUARE"]
    chosen_submode = random.choice(submodes)

    # Apply the chosen submode to expand the pattern with the second color
    list_of_second_positions = list()
    if chosen_submode == "DIAGONAL_UP_RIGHT":
        for pos in list_of_first_positions:
            x, y = pos
            if x < canvas.size[0] - 1 and y > 0:
                diagonal_pos = (x + 1, y - 1)
                if diagonal_pos not in first_positions:
                    list_of_second_positions.append(diagonal_pos)

    elif chosen_submode == "DIAGONAL_UP_LEFT":
        for pos in list_of_first_positions:
            x, y = pos
            if x > 0 and y > 0:
                diagonal_pos = (x - 1, y - 1)
                if diagonal_pos not in first_positions:
                    list_of_second_positions.append(diagonal_pos)

    elif chosen_submode == "DIAGONAL_DOWN_RIGHT":
        for pos in list_of_first_positions:
            x, y = pos
            if x < canvas.size[0] - 1 and y < canvas.size[1] - 1:
                diagonal_pos = (x + 1, y + 1)
                if diagonal_pos not in first_positions:
                    list_of_second_positions.append(diagonal_pos)

    elif chosen_submode == "DIAGONAL_DOWN_LEFT":
        for pos in list_of_first_positions:
            x, y = pos
            if x > 0 and y < canvas.size[1] - 1:
                diagonal_pos = (x - 1, y + 1)
                if diagonal_pos not in first_positions:
                    list_of_second_positions.append(diagonal_pos)

    elif chosen_submode == "CROSS":
        for pos in list_of_first_positions:
            x, y = pos
            cross_positions = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
            for cross_pos in cross_positions:
                if (0 <= cross_pos[0] < canvas.size[0] and
                        0 <= cross_pos[1] < canvas.size[1] and
                        cross_pos not in first_positions):
                    list_of_second_positions.append(cross_pos)

    elif chosen_submode == "SQUARE":
        for pos in list_of_first_positions:
            x, y = pos
            square_positions = [
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
            ]
            for square_pos in square_positions:
                if (0 <= square_pos[0] < canvas.size[0] and
                        0 <= square_pos[1] < canvas.size[1] and
                        square_pos not in first_positions):
                    list_of_second_positions.append(square_pos)

    for pos in list_of_second_positions:
                canvas.putpixel(pos, second_color)

    # Add noise with the third color, ensuring no overlap with the first or second colors
    noise_positions = set()
    noise_amount = round((canvas.size[0] * canvas.size[1]) * 0.4)  # Use 40% of the remaining space for noise
    attempts = 0
    while len(noise_positions) < noise_amount and attempts < max_attempts:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        if (x, y) not in first_positions and (x, y) not in list_of_second_positions:
            noise_positions.add((x, y))
            canvas.putpixel((x, y), third_color)
        attempts += 1

    if attempts == max_attempts:
        print("Max attempts reached while adding noise. Some noise positions might not be placed.")

    # Fill remaining white pixels with the fourth color
    for x in range(canvas.size[0]):
        for y in range(canvas.size[1]):
            if canvas.getpixel((x, y)) == (255, 255, 255):
                canvas.putpixel((x, y), fourth_color)

    # Draw border with the fifth color
    for t in range(BORDER_THICKNESS):
        for x in range(canvas.size[0]):
            canvas.putpixel((x, t), border_color)
            canvas.putpixel((x, canvas.size[1] - 1 - t), border_color)
        for y in range(canvas.size[1]):
            canvas.putpixel((t, y), border_color)
            canvas.putpixel((canvas.size[0] - 1 - t, y), border_color)
