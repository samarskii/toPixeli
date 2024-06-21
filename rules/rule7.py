import random
from PIL import Image

# Define specific colors for use when USE_SPECIFIC_COLORS is True
SPECIFIC_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
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
        return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(4)]

def get_amount_of_first_color(canvas):
    """Determine the amount of the first color to use. Use a random amount if USE_RANDOM_AMOUNT is True, otherwise use PARTICULAR_AMOUNT."""
    if USE_RANDOM_AMOUNT:
        return round((canvas.size[0] * canvas.size[1]) / random.randint(5, 8) * random.randint(1, 2))
    else:
        return PARTICULAR_AMOUNT

def rule7(canvas):
    """Apply the rule7 pattern to the given canvas."""
    if SPECIFIC_SEED is not None:
        random.seed(SPECIFIC_SEED)
        
    colors = get_colors()
    first_color = colors[0]
    second_color = colors[1]
    third_color = colors[2]
    fourth_color = colors[3]

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

    # Define adjacent positions for the second color
    above_first_positions = []
    below_first_positions = []
    right_first_positions = []
    left_first_positions = []
    for pos in first_positions:
        x, y = pos
        if y > 0:
            above_pos = (x, y - 1)
            if above_pos not in first_positions:
                above_first_positions.append(above_pos)
        if y < canvas.size[1] - 1:
            below_pos = (x, y + 1)
            if below_pos not in first_positions:
                below_first_positions.append(below_pos)
        if x < canvas.size[0] - 1:
            right_pos = (x + 1, y)
            if right_pos not in first_positions:
                right_first_positions.append(right_pos)
        if x > 0:
            left_pos = (x - 1, y)
            if left_pos not in first_positions:
                left_first_positions.append(left_pos)

    # Apply the second color
    for pos in above_first_positions:
        canvas.putpixel(pos, second_color)
    for pos in below_first_positions:
        canvas.putpixel(pos, second_color)
    for pos in right_first_positions:
        canvas.putpixel(pos, second_color)
    for pos in left_first_positions:
        canvas.putpixel(pos, second_color)

    # Add noise with the third color
    third_positions = set()
    amount_of_third_color = round((canvas.size[0] * canvas.size[1]) / random.randint(4, 6) * random.randint(1, 2))
    max_iterations = canvas.size[0] * canvas.size[1]  # Maximum number of iterations
    iteration_count = 0

    while len(third_positions) < amount_of_third_color and iteration_count < max_iterations:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        if canvas.getpixel((x, y)) == (255, 255, 255):
            third_positions.add((x, y))
            canvas.putpixel((x, y), third_color)
        iteration_count += 1

    # Fill remaining white pixels with the fourth color
    for x in range(canvas.size[0]):
        for y in range(canvas.size[1]):
            if canvas.getpixel((x, y)) == (255, 255, 255):
                canvas.putpixel((x, y), fourth_color)

    # Draw border with the fourth color
    for t in range(BORDER_THICKNESS):
        for x in range(canvas.size[0]):
            canvas.putpixel((x, t), fourth_color)
            canvas.putpixel((x, canvas.size[1] - 1 - t), fourth_color)
        for y in range(canvas.size[1]):
            canvas.putpixel((t, y), fourth_color)
            canvas.putpixel((canvas.size[0] - 1 - t, y), fourth_color)
