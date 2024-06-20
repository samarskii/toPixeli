import random
from PIL import Image

# Define specific colors for use when USE_SPECIFIC_COLORS is True
SPECIFIC_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255)   # Cyan
]

# Flags and parameters to control the behavior of the rule
USE_SPECIFIC_COLORS = False  # Flag to switch between specific and random colors
USE_RANDOM_AMOUNT = True  # Flag to switch between random and specific amount of seed pixels
PARTICULAR_AMOUNT = 50  # Specific amount to use if USE_RANDOM_AMOUNT is False

SPECIFIC_SEED = None  # Specific seed value for reproducibility, e.g., 42

BORDER_THICKNESS = 0  # Thickness of the colored border in pixels

def get_colors():
    """Generate a list of colors. Use specific colors if USE_SPECIFIC_COLORS is True, otherwise generate random colors."""
    if USE_SPECIFIC_COLORS:
        return SPECIFIC_COLORS
    else:
        return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(7)]

def get_amount_of_seed_pixels(canvas):
    """Determine the amount of seed pixels to use. Use a random amount if USE_RANDOM_AMOUNT is True, otherwise use PARTICULAR_AMOUNT."""
    if USE_RANDOM_AMOUNT:
        return round((canvas.size[0] * canvas.size[1]) / random.randint(10, 20))
    else:
        return PARTICULAR_AMOUNT

def rule5(canvas):
    """Apply the rule5 pattern to the given canvas."""
    if SPECIFIC_SEED is not None:
        random.seed(SPECIFIC_SEED)
        
    colors = get_colors()
    primary_color = colors[0]
    secondary_color = colors[1]

    amount_of_seed_pixels = get_amount_of_seed_pixels(canvas)
    seed_pixels = set()
    max_attempts = canvas.size[0] * canvas.size[1] * 10  # Safeguard to prevent infinite loops
    attempts = 0
    
    # Place the seed pixels randomly on the canvas
    while len(seed_pixels) < amount_of_seed_pixels and attempts < max_attempts:
        x, y = random.randint(0, canvas.size[0] - 1), random.randint(0, canvas.size[1] - 1)
        seed_pixels.add((x, y))
        canvas.putpixel((x, y), primary_color)
        attempts += 1

    if attempts == max_attempts:
        print("Max attempts reached while placing seed pixels. Some positions might not be placed.")

    # Simulate growth with the secondary color
    num_iterations = random.randint(3, 6)
    for _ in range(num_iterations):
        new_pixels = set()
        for x in range(canvas.size[0]):
            for y in range(canvas.size[1]):
                if (x, y) not in seed_pixels:
                    neighbor_count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if (x + dx, y + dy) in seed_pixels:
                                neighbor_count += 1
                    if neighbor_count >= 2:
                        new_pixels.add((x, y))
                        canvas.putpixel((x, y), secondary_color)
        seed_pixels.update(new_pixels)

    # Add tertiary color based on neighbor conditions
    for x in range(canvas.size[0]):
        for y in range(canvas.size[1]):
            if (x, y) in seed_pixels:
                neighbor_count_primary = 0
                neighbor_count_secondary = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (x + dx, y + dy) in seed_pixels:
                            if canvas.getpixel((x + dx, y + dy)) == primary_color:
                                neighbor_count_primary += 1
                            elif canvas.getpixel((x + dx, y + dy)) == secondary_color:
                                neighbor_count_secondary += 1
                if neighbor_count_primary >= 2 and neighbor_count_secondary >= 2:
                    canvas.putpixel((x, y), random.choice(colors[2:]))

    # Fill remaining white pixels with random colors
    for x in range(canvas.size[0]):
        for y in range(canvas.size[1]):
            if canvas.getpixel((x, y)) == (255, 255, 255):
                canvas.putpixel((x, y), random.choice(colors))

    # Draw border with the seventh color
    border_color = colors[6]
    for t in range(BORDER_THICKNESS):
        for x in range(canvas.size[0]):
            canvas.putpixel((x, t), border_color)
            canvas.putpixel((x, canvas.size[1] - 1 - t), border_color)
        for y in range(canvas.size[1]):
            canvas.putpixel((t, y), border_color)
            canvas.putpixel((canvas.size[0] - 1 - t, y), border_color)
