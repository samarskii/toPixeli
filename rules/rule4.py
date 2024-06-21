import random
import math
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

USE_SPECIFIC_SUBRULE = False  # Flag to use a specific subrule
SPECIFIC_SUBRULE = 'EXPLOSION'  # Specific subrule to use if USE_SPECIFIC_SUBRULE is True

SPECIFIC_SEED = None  # Specific seed value for reproducibility, e.g., 42

BORDER_THICKNESS = 1  # Thickness of the colored border in pixels

def get_colors():
    """Generate a list of colors. Use specific colors if USE_SPECIFIC_COLORS is True, otherwise generate random colors."""
    if USE_SPECIFIC_COLORS:
        return SPECIFIC_COLORS
    else:
        return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(5)]

def get_amount_of_first_color(canvas):
    """Determine the amount of the first color to use. Use a random amount if USE_RANDOM_AMOUNT is True, otherwise use PARTICULAR_AMOUNT."""
    if USE_RANDOM_AMOUNT:
        return round((canvas.size[0] * canvas.size[1]) / random.randint(3, 5) * random.randint(1, 2))
    else:
        return PARTICULAR_AMOUNT

def rule4(canvas):
    """Apply the rule4 pattern to the given canvas."""
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
    subrules = ["EXPLOSION", "SPIRAL", "RIPPLE", "GALAXY"]
    chosen_subrule = SPECIFIC_SUBRULE if USE_SPECIFIC_SUBRULE else random.choice(subrules)

    # Apply the chosen subrule to expand the pattern with the second color
    list_of_second_positions = list()
    if chosen_subrule == 'EXPLOSION':
        for pos in list_of_first_positions:
            x, y = pos
            for i in range(1, random.randint(2, 5)):
                explosion_pos = (x + random.randint(-i, i), y + random.randint(-i, i))
                if (explosion_pos[0] >= 0 and explosion_pos[0] < canvas.size[0] and
                        explosion_pos[1] >= 0 and explosion_pos[1] < canvas.size[1] and
                        explosion_pos not in first_positions):
                    list_of_second_positions.append(explosion_pos)

    if chosen_subrule == 'SPIRAL':
        for pos in list_of_first_positions:
            x, y = pos
            for i in range(1, random.randint(2, 5)):
                spiral_pos = (x + i * math.cos(i * math.pi / 4), y + i * math.sin(i * math.pi / 4))
                if (0 <= spiral_pos[0] < canvas.size[0] and 0 <= spiral_pos[1] < canvas.size[1] and
                        spiral_pos not in first_positions):
                    list_of_second_positions.append(spiral_pos)

    if chosen_subrule == 'RIPPLE':
        for pos in list_of_first_positions:
            x, y = pos
            for i in range(1, random.randint(2, 5)):
                ripple_pos = (x + i * math.cos(i * math.pi / 2), y + i * math.sin(i * math.pi / 2))
                if (0 <= ripple_pos[0] < canvas.size[0] and 0 <= ripple_pos[1] < canvas.size[1] and
                        ripple_pos not in first_positions):
                    list_of_second_positions.append(ripple_pos)

    if chosen_subrule == 'GALAXY':
        for pos in list_of_first_positions:
            x, y = pos
            for i in range(1, random.randint(2, 5)):
                galaxy_pos = (x + i * math.cos(i * math.pi / 3), y + i * math.sin(i * math.pi / 3))
                if (0 <= galaxy_pos[0] < canvas.size[0] and 0 <= galaxy_pos[1] < canvas.size[1] and
                        galaxy_pos not in first_positions):
                    list_of_second_positions.append(galaxy_pos)

    for i in list_of_second_positions:
        canvas.putpixel((int(i[0]), int(i[1])), second_color)

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
