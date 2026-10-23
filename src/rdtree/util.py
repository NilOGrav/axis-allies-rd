"""Small helpers shared by several modules."""

import sys


def darken_color(hex_color, factor=0.82):
    """Return a darkened version of a hex colour.

    Multiplies each RGB channel by factor. Used to make cluster
    background fills visibly darker than the node fill in the
    simple renderer, while keeping them in the same colour family.
    """
    hex_color = hex_color.lstrip("#")
    r = int(int(hex_color[0:2], 16) * factor)
    g = int(int(hex_color[2:4], 16) * factor)
    b = int(int(hex_color[4:6], 16) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def blend_to_white(hex_color, factor=0.2):
    """Blend a hex colour toward white.

    factor controls how much of the original colour survives:
    0.0 = pure white, 1.0 = original colour unchanged.
    Used for 'fade' dim mode to wash out non-highlighted nodes
    while keeping them recognisably in their domain colour family.
    """

    hex_color = hex_color.lstrip("#")
    r = int(int(hex_color[0:2], 16) * factor + 255 * (1 - factor))
    g = int(int(hex_color[2:4], 16) * factor + 255 * (1 - factor))
    b = int(int(hex_color[4:6], 16) * factor + 255 * (1 - factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def warn(message):
    """Print a warning to stderr without stopping the run."""

    print(f"WARNING: {message}", file=sys.stderr)
