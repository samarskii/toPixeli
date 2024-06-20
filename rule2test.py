import random
from PIL import Image

# Define specific colors
SPECIFIC_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0)   # Orange
]

USE_SPECIFIC_COLORS = False  # Change this flag to switch between specific and random colors
USE_RANDOM_AMOUNT = True  # Change this flag to switch between random and specific amount
PARTICULAR_AMOUNT = 50  # Set a particular amount if USE_RANDOM_AMOUNT is False

USE_SPECIFIC_SUBRULE = False  # Change this flag to use a specific subrule
SPECIFIC_SUBRULE = 'DIAGONAL_UP_RIGHT'  # Set the specific subrule to be used if USE_SPECIFIC_SUBRULE is True

SPECIFIC_SEED = None  # Set a specific seed value for reproducibility, e.g., 42

BORDER_THICKNESS = 2  # Thickness of the colored border in pixels

def get_colors():
    if USE_SPECIFIC_COLORS:
        return SPECIFIC_COLORS
    else:
        return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(5)]

def get_amount_of_first_color(canvas):
    if USE_RANDOM_AMOUNT:
        return round((canvas.size[0] * canvas.size[1]) / random.randint(4, 7) * random.randint(1, 3))
    else:
        return PARTICULAR_AMOUNT

def rule2(canvas):
    if SPECIFIC_SEED is not None:
        random.seed(SPECIFIC_SEED)
        
    colors = get_colors()
    first_color, *colors = colors

    amount_of_first_color = get_amount_of_first_color(canvas)
    first_positions = set()
    while len(first_positions) < amount_of_first_color:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        first_positions.add((x, y))
        canvas.putpixel((x, y), first_color)

    list_of_first_positions = list(first_positions)

    subrules = ["DIAGONAL_UP_RIGHT", "DIAGONAL_UP_LEFT", "DIAGONAL_DOWN_RIGHT", "DIAGONAL_DOWN_LEFT"]
    chosen_subrule = SPECIFIC_SUBRULE if USE_SPECIFIC_SUBRULE else random.choice(subrules)

    if chosen_subrule == 'DIAGONAL_UP_RIGHT':
        list_of_diagonal_up_right_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x < canvas.size[0] - 1 and y > 0:
                diagonal_pos = (x + 1, y - 1)
                if diagonal_pos[0] < canvas.size[0] and diagonal_pos[1] >= 0 and diagonal_pos not in list_of_first_positions:
                    list_of_diagonal_up_right_positions.append(diagonal_pos)

        for i in list_of_diagonal_up_right_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'DIAGONAL_UP_LEFT':
        list_of_diagonal_up_left_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x > 0 and y > 0:
                diagonal_pos = (x - 1, y - 1)
                if diagonal_pos[0] >= 0 and diagonal_pos[1] >= 0 and diagonal_pos not in list_of_first_positions:
                    list_of_diagonal_up_left_positions.append(diagonal_pos)

        for i in list_of_diagonal_up_left_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'DIAGONAL_DOWN_RIGHT':
        list_of_diagonal_down_right_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x < canvas.size[0] - 1 and y < canvas.size[1] - 1:
                diagonal_pos = (x + 1, y + 1)
                if diagonal_pos[0] < canvas.size[0] and diagonal_pos[1] < canvas.size[1] and diagonal_pos not in list_of_first_positions:
                    list_of_diagonal_down_right_positions.append(diagonal_pos)

        for i in list_of_diagonal_down_right_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'DIAGONAL_DOWN_LEFT':
        list_of_diagonal_down_left_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x > 0 and y < canvas.size[1] - 1:
                diagonal_pos = (x - 1, y + 1)
                if diagonal_pos[0] >= 0 and diagonal_pos[1] < canvas.size[1] and diagonal_pos not in list_of_first_positions:
                    list_of_diagonal_down_left_positions.append(diagonal_pos)

        for i in list_of_diagonal_down_left_positions:
            canvas.putpixel(i, colors[0])

    # Fill remaining white pixels with second color
    for x in range(canvas.size[0]):
        for y in range(canvas.size[1]):
            if canvas.getpixel((x, y)) == (255, 255, 255):
                canvas.putpixel((x, y), colors[1])

    # Add noise with third color
    noise_positions = set()
    max_noise_iterations = round((canvas.size[0] * canvas.size[1]) / random.randint(10, 20))
    while len(noise_positions) < max_noise_iterations:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        if (x, y) not in noise_positions:
            noise_positions.add((x, y))
            canvas.putpixel((x, y), colors[2])

    # Draw border with fourth color
    border_color = colors[3]
    for t in range(BORDER_THICKNESS):
        for x in range(canvas.size[0]):
            canvas.putpixel((x, t), border_color)
            canvas.putpixel((x, canvas.size[1] - 1 - t), border_color)
        for y in range(canvas.size[1]):
            canvas.putpixel((t, y), border_color)
            canvas.putpixel((canvas.size[0] - 1 - t, y), border_color)