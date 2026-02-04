import math

from tools.colors import *

class Polygon:
    def __init__(self, t: str, color: tuple):
        self.points = []    # Points are considered in World Space (in meters)

        self.polygon_type = t

        # Position information
        self.w = 30
        self.h = 50
        self.angle = 0

        self.color = color

    def get_rectangle_points(self, cx, cy):
        w = self.w
        h = self.h
        theta_deg = self.angle

        rad = math.radians(theta_deg)
        cos_t = math.cos(rad)
        sin_t = math.sin(rad)

        # coins relatifs au centre
        corners = [
            (-w / 2, -h / 2),  # top-left
            (w / 2, -h / 2),  # top-right
            (w / 2, h / 2),  # bottom-right
            (-w / 2, h / 2),  # bottom-left
        ]

        # appliquer rotation + translation
        rotated = []
        for px, py in corners:
            x = px * cos_t - py * sin_t + cx
            y = px * sin_t + py * cos_t + cy
            rotated.append((x, y))

        return rotated

    def confirm_position(self, converted_points: list):
        self.points = converted_points