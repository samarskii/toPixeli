import random
import colorsys

def generate_color(hue_range, saturation_range, brightness_range):
    hue = random.randint(*hue_range)
    saturation = random.randint(*saturation_range)
    brightness = random.randint(*brightness_range)
    
    h = hue / 360
    s = saturation / 100
    v = brightness / 100
    
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    return f'#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}'

def generate_acidic_color():
    return generate_color((120, 240), (60, 100), (30, 70))

def generate_pastel_color():
    return generate_color((0, 360), (15, 30), (85, 95))

def generate_vibrant_color():
    return generate_color((0, 360), (80, 100), (80, 100))

def generate_earthy_color():
    return generate_color((20, 50), (30, 60), (20, 60))

def generate_monochromatic_color(base_hue):
    return generate_color((base_hue, base_hue), (30, 100), (20, 80))

def generate_psychedelic_color():
    return generate_color((0, 360), (70, 100), (50, 100))

def generate_dark_color():
    return generate_color((0, 360), (50, 100), (0, 30))

def generate_acidic_vibrant_color():
    return generate_color((120, 240), (80, 100), (60, 100))

def generate_gradient_colors(num_colors):
    start_hue = random.randint(0, 360)
    end_hue = (start_hue + random.randint(30, 330)) % 360
    hue_step = (end_hue - start_hue) / (num_colors - 1)
    
    return [generate_color((int(start_hue + i * hue_step), int(start_hue + i * hue_step)),
                           (70, 100), (50, 100)) for i in range(num_colors)]

def generate_palette(palette_type, num_colors=4):
    if palette_type == 'acidic':
        return tuple(generate_acidic_color() for _ in range(num_colors))
    elif palette_type == 'pastel':
        return tuple(generate_pastel_color() for _ in range(num_colors))
    elif palette_type == 'vibrant':
        return tuple(generate_vibrant_color() for _ in range(num_colors))
    elif palette_type == 'earthy':
        return tuple(generate_earthy_color() for _ in range(num_colors))
    elif palette_type == 'monochromatic':
        base_hue = random.randint(0, 360)
        return tuple(generate_monochromatic_color(base_hue) for _ in range(num_colors))
    elif palette_type == 'psychedelic':
        return tuple(generate_psychedelic_color() for _ in range(num_colors))
    elif palette_type == 'dark':
        return tuple(generate_dark_color() for _ in range(num_colors))
    elif palette_type == 'acidic-vibrant':
        return tuple(generate_acidic_vibrant_color() for _ in range(num_colors))
    elif palette_type == 'gradient':
        return tuple(generate_gradient_colors(num_colors))
    else:
        raise ValueError("Invalid palette type. Choose from 'acidic', 'pastel', 'vibrant', 'earthy', 'monochromatic', 'psychedelic', 'dark', 'acidic-vibrant', or 'gradient'.")
