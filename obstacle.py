import math

from polygon import Polygon


class Obstacle(Polygon):

    def __init__(self):
        super().__init__("Obstacle")

        # Position information
        self.w = 30
        self.h = 50
        self.angle = 30

    def get_rectangle_points(self, cx, cy):

        w = self.w
        h = self.h
        theta_deg = self.angle

        rad = math.radians(theta_deg)
        cos_t = math.cos(rad)
        sin_t = math.sin(rad)

        # coins relatifs au centre
        corners = [
            (-w/2, -h/2),  # top-left
            ( w/2, -h/2),  # top-right
            ( w/2,  h/2),  # bottom-right
            (-w/2,  h/2),  # bottom-left
        ]

        # appliquer rotation + translation
        rotated = []
        for px, py in corners:
            x = px * cos_t - py * sin_t + cx
            y = px * sin_t + py * cos_t + cy
            rotated.append((x, y))

        return rotated

