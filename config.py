"""
Global configuration for the pygame Minesweeper game.

This module centralizes all tunable settings used by both the logic layer
(only grid sizes and counts) and the presentation layer (colors, fonts,
layout metrics). Keeping these in one place helps tweak gameplay and visuals
without touching logic or rendering code.

Groups:
- Grid and display: board dimensions, cell size, margins, derived window size
- Colors: palette for cells, numbers, flags, overlays
- Text/UI: font sizes for body, header, and result
- Input: mouse button mappings
- Behavior: highlight duration, overlay alpha
"""

# Display settings
fps = 60

# Difficulty presets
DIFFICULTY_PRESETS = {
    1: {"cols": 10, "rows": 10, "mines": 10, "name": "초급"},
    2: {"cols": 15, "rows": 15, "mines": 40, "name": "중급"},
    3: {"cols": 20, "rows": 20, "mines": 80, "name": "고급"},
}

# Current difficulty (default: 중급)
current_difficulty = 2

# Grid settings (initialized from current difficulty)
def get_difficulty_settings(level):
    preset = DIFFICULTY_PRESETS.get(level, DIFFICULTY_PRESETS[2])
    return preset["cols"], preset["rows"], preset["mines"]

cols, rows, num_mines = get_difficulty_settings(current_difficulty)

# Cell size and margins
cell_size = 32
margin_left = 20
margin_top = 60
margin_right = 20
margin_bottom = 20

# Derived display dimension
width = margin_left + cols * cell_size + margin_right
height = margin_top + rows * cell_size + margin_bottom

display_dimension = (width, height)

# Colors
color_bg = (24, 26, 27)
color_grid = (60, 64, 67)
color_cell_hidden = (40, 44, 52)
color_cell_revealed = (225, 228, 232)
color_cell_mine = (220, 0, 0)
color_flag = (255, 215, 0)
color_text = (20, 20, 20)
color_text_inv = (240, 240, 240)
color_header_text = (240, 240, 240)
color_header = (32, 34, 36)
color_highlight = (70, 130, 180)
color_result = (242, 242, 0)

# Number colors 1~8
number_colors = {
    1: (25, 118, 210),   # blue
    2: (56, 142, 60),    # green
    3: (211, 47, 47),    # red
    4: (123, 31, 162),   # purple
    5: (123, 31, 162),   # purple
    6: (123, 31, 162),   # purple
    7: (123, 31, 162),   # purple
    8: (123, 31, 162),   # purple
}

# Text / UI
font_name = None  # default pygame font
font_size = 22
header_font_size = 24
result_font_size = 64

# Input
mouse_left = 1
mouse_middle = 2
mouse_right = 3

# Highlight behavior (milliseconds)
highlight_duration_ms = 600

# Overlay alpha for result background (0~255)
result_overlay_alpha = 120

# Misc
title = "Minesweeper"

