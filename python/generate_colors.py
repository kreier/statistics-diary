import colorsys
import json

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        int(round(rgb[0] * 255)),
        int(round(rgb[1] * 255)),
        int(round(rgb[2] * 255))
    )

def get_shades(name, hex_val):
    rgb = hex_to_rgb(hex_val)
    h, l, s = colorsys.rgb_to_hls(*rgb)

    shades = {}
    # Percentages: 100%, 75%, 50%, 25%
    # 100% is pure (L = l)
    # 0% is white (L = 1.0)
    # 75% shade is 25% towards white: L = l + (1.0 - l) * 0.25

    for pct in [100, 75, 50, 25]:
        # factor is how much of the "whiteness" we add.
        # 100% shade = 0% whiteness
        # 25% shade = 75% whiteness
        factor = (100 - pct) / 100.0
        new_l = l + (1.0 - l) * factor

        new_rgb = colorsys.hls_to_rgb(h, new_l, s)
        hex_out = rgb_to_hex(new_rgb)

        key = f"{name}_{pct}"
        shades[key] = hex_out
        if pct == 100:
            shades[name] = hex_out

    return shades

base_colors = {
    "red": "#FF0000",
    "orange": "#FFA500",
    "yellow": "#FFFF00",
    "green": "#008000",
    "blue": "#0000FF",
    "purple": "#800080",
    "brown": "#A52A2A",
    "black": "#000000"
}

all_colors = {}
for name, hex_val in base_colors.items():
    all_colors.update(get_shades(name, hex_val))

# Sort keys for better readability if desired, though dict order is fine in Python 3.7+
# Let's keep them grouped by color
final_json = {}
for name in base_colors:
    final_json[name] = all_colors[name]
    for pct in [100, 75, 50, 25]:
        key = f"{name}_{pct}"
        final_json[key] = all_colors[key]

print(json.dumps(final_json, indent=2))
