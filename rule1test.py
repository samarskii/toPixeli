import random
from PIL import Image

# Define specific colors
SPECIFIC_COLORS = [
    (255, 255, 0),    # Yellow
    (255, 165, 0),    # Orange
    (206, 70, 118),   # Pink
    (0, 128, 0)       # Green
]

USE_SPECIFIC_COLORS = False  # Change this flag to switch between specific and random colors
USE_RANDOM_AMOUNT = True  # Change this flag to switch between random and specific amount
PARTICULAR_AMOUNT = 40  # Set a particular amount if USE_RANDOM_AMOUNT is False

USE_SPECIFIC_SUBRULE = True  # Change this flag to use a specific subrule
SPECIFIC_SUBRULE = 'ABOVE'   # Set the specific subrule to be used if USE_SPECIFIC_SUBRULE is True

SPECIFIC_SEED = None  # Set a specific seed value for reproducibility, e.g., 42

def get_colors():
    if USE_SPECIFIC_COLORS:
        return SPECIFIC_COLORS
    else:
        return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(4)]

def get_amount_of_first_color(canvas):
    if USE_RANDOM_AMOUNT:
        return round((canvas.size[0] * canvas.size[1]) / random.randint(5, 8) * random.randint(1, 2))
    else:
        return PARTICULAR_AMOUNT

def rule1(canvas):
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

    subrules = ["LEFT", "RIGHT", "ABOVE", "BELOW"]
    chosen_subrule = SPECIFIC_SUBRULE if USE_SPECIFIC_SUBRULE else random.choice(subrules)

    if chosen_subrule == 'ABOVE':
        list_of_above_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if y > 0:
                above_pos = (x, y - 1)
                if above_pos[1] >= 0 and above_pos not in list_of_first_positions:
                    list_of_above_positions.append(above_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        left_pos = (x - i, y - 1)
                        right_pos = (x + i, y - 1)
                        if (left_pos[0] >= 0 and left_pos[0] < canvas.size[0] and
                                left_pos[1] >= 0 and left_pos[1] < canvas.size[1] and
                                left_pos not in list_of_first_positions):
                            list_of_above_positions.append(left_pos)
                        if (right_pos[0] >= 0 and right_pos[0] < canvas.size[0] and
                                right_pos[1] >= 0 and right_pos[1] < canvas.size[1] and
                                right_pos not in list_of_first_positions):
                            list_of_above_positions.append(right_pos)

        for i in list_of_above_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'BELOW':
        list_of_below_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if y < canvas.size[1] - 1:
                below_pos = (x, y + 1)
                if below_pos[1] < canvas.size[1] and below_pos not in list_of_first_positions:
                    list_of_below_positions.append(below_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        left_pos = (x - i, y + 1)
                        right_pos = (x + i, y + 1)
                        if (left_pos[0] >= 0 and left_pos[0] < canvas.size[0] and
                                left_pos[1] >= 0 and left_pos[1] < canvas.size[1] and
                                left_pos not in list_of_first_positions):
                            list_of_below_positions.append(left_pos)
                        if (right_pos[0] >= 0 and right_pos[0] < canvas.size[0] and
                                right_pos[1] >= 0 and right_pos[1] < canvas.size[1] and
                                right_pos not in list_of_first_positions):
                            list_of_below_positions.append(right_pos)

        for i in list_of_below_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'RIGHT':
        list_of_right_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x < canvas.size[0] - 1:
                right_pos = (x + 1, y)
                if right_pos[0] < canvas.size[0] and right_pos not in list_of_first_positions:
                    list_of_right_positions.append(right_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        above_pos = (x + 1, y - i)
                        below_pos = (x + 1, y + i)
                        if (above_pos[0] < canvas.size[0] and above_pos[0] >= 0 and
                                above_pos[1] < canvas.size[1] and above_pos[1] >= 0 and
                                above_pos not in list_of_first_positions):
                            list_of_right_positions.append(above_pos)
                        if (below_pos[0] < canvas.size[0] and below_pos[0] >= 0 and
                                below_pos[1] < canvas.size[1] and below_pos[1] >= 0 and
                                below_pos not in list_of_first_positions):
                            list_of_right_positions.append(below_pos)

        for i in list_of_right_positions:
            canvas.putpixel(i, colors[0])

    if chosen_subrule == 'LEFT':
        list_of_left_positions = list()
        for pos in list_of_first_positions:
            x, y = pos
            if x > 0:
                left_pos = (x - 1, y)
                if left_pos[0] >= 0 and left_pos not in list_of_first_positions:
                    list_of_left_positions.append(left_pos)

                    random_distance = random.randint(1, 2)

                    for i in range(1, random_distance + 1):
                        above_pos = (x - 1, y - i)
                        below_pos = (x - 1, y + i)
                        if (above_pos[0] >= 0 and above_pos[0] < canvas.size[0] and
                                above_pos[1] >= 0 and above_pos[1] < canvas.size[1] and
                                above_pos not in list_of_first_positions):
                            list_of_left_positions.append(above_pos)
                        if (below_pos[0] >= 0 and below_pos[0] < canvas.size[0] and
                                below_pos[1] >= 0 and below_pos[1] < canvas.size[1] and
                                below_pos not in list_of_first_positions):
                            list_of_left_positions.append(below_pos)

        for i in list_of_left_positions:
            canvas.putpixel(i, colors[0])

    amount_of_third_color = round((canvas.size[0] * canvas.size[1]) / random.randint(4, 6) * random.randint(1, 2))
    third_positions = set()
    max_iterations = canvas.size[0] * canvas.size[1]  # Maximum number of iterations
    iteration_count = 0

    while len(third_positions) < amount_of_third_color and iteration_count < max_iterations:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        if canvas.getpixel((x, y)) == (255, 255, 255):
            third_positions.add((x, y))
            canvas.putpixel((x, y), colors[1])
        iteration_count += 1

    try:
        for x in range(canvas.size[0]):
            for y in range(canvas.size[1]):
                if canvas.getpixel((x, y)) == (255, 255, 255):
                    canvas.putpixel((x, y), colors[2])
                    
    except KeyboardInterrupt:
        print("Program interrupted by the user.")