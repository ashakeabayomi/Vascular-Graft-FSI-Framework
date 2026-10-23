"""
cell_stretch_demo.py

A simple 2D visualisation of a cell boundary stretching along a
micro-patterned surface with 2 micrometre (um) grating lines.

The cell is modelled as an ellipse with constant area. As it elongates
along the grating direction (x-axis), it also narrows in y. The aspect
ratio (major axis / minor axis) is calculated at each stage, the same
kind of morphometric used later in the Fiji -> Python pipeline.

This is a conceptual demo, not a biophysical simulation.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 1. Parameters (all lengths in micrometres, um)
# ----------------------------------------------------------------------
GRID_SPACING_UM = 2.0        # spacing between grating lines
CELL_RADIUS_UM = 8.0         # radius of the initial, round cell
STRETCH_FACTORS = [1.0, 1.5, 2.2]   # how much the cell elongates at each stage
N_POINTS = 200               # number of points that trace the cell boundary
PLOT_LIMIT_UM = 24.0         # plots span -24 to +24 um in x and y


# ----------------------------------------------------------------------
# 2. Helper functions
# ----------------------------------------------------------------------
def make_cell_boundary(stretch, radius=CELL_RADIUS_UM, n_points=N_POINTS):
    """
    Return the (x, y) coordinates of an elliptical cell boundary.

    The semi-axes are radius*stretch (along x) and radius/stretch (along y),
    so the area (pi * a * b) stays the same for any stretch value.
    """
    theta = np.linspace(0, 2 * np.pi, n_points)   # angles around the cell
    a = radius * stretch                          # semi-axis along the gratings (x)
    b = radius / stretch                          # semi-axis across the gratings (y)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    return x, y


def calculate_aspect_ratio(x, y):
    """
    Estimate the aspect ratio from boundary coordinates.

    Uses the bounding extent in x and y: longer side / shorter side.
    """
    width = x.max() - x.min()
    height = y.max() - y.min()
    return max(width, height) / min(width, height)


def draw_gratings(ax, spacing=GRID_SPACING_UM, limit=PLOT_LIMIT_UM):
    """
    Draw horizontal grating lines every `spacing` um as the background.
    """
    # np.arange creates evenly spaced y-positions for the lines
    for y_pos in np.arange(-limit, limit + spacing, spacing):
        ax.axhline(y_pos, color="lightgray", linewidth=0.6, zorder=1)


# ----------------------------------------------------------------------
# 3. Build the figure: one panel per stretch stage
# ----------------------------------------------------------------------
fig, axes = plt.subplots(1, len(STRETCH_FACTORS), figsize=(13, 4.5), sharey=True)

for ax, stretch in zip(axes, STRETCH_FACTORS):
    # Background: the 2 um grating lines
    draw_gratings(ax)

    # Foreground: the cell boundary at this stretch level
    x, y = make_cell_boundary(stretch)
    ax.fill(x, y, color="tab:blue", alpha=0.25, zorder=2)        # cell body
    ax.plot(x, y, color="tab:blue", linewidth=2, zorder=3)       # cell outline

    # Quantify elongation and show it in the panel title
    ar = calculate_aspect_ratio(x, y)
    ax.set_title(f"Stretch = {stretch:.1f}  |  Aspect ratio = {ar:.2f}")

    # Formatting
    ax.set_xlim(-PLOT_LIMIT_UM, PLOT_LIMIT_UM)
    ax.set_ylim(-PLOT_LIMIT_UM, PLOT_LIMIT_UM)
    ax.set_aspect("equal")               # equal scaling so the cell is not distorted
    ax.set_xlabel("x (µm)")

axes[0].set_ylabel("y (µm)")

fig.suptitle(
    f"Simulated cell elongation on {GRID_SPACING_UM:.0f} µm linear gratings",
    fontsize=13,
)
plt.tight_layout()
plt.show()   # to save instead, use: plt.savefig("cell_stretch_demo.png", dpi=300)