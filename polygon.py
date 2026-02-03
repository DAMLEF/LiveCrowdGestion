class Polygon:
    def __init__(self, t: str):
        self.points = []    # Points are considered in World Space (in meters)

        self.polygon_type = t

    def confirm_position(self, converted_points: list):
        self.points = converted_points