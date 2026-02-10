class World:
    def __init__(self):
        self.meter = 15

        self.agent_radius = 0.65        # In m

        self.world_width = 30           # In m
        self.world_height = 20          # In m

        self.contact_tolerance = 0.02    # In m

    def pixel_to_world(self, pixel: int) -> float:
        return pixel / self.meter

    def world_to_pixel(self, length: float) -> float:
        return length * self.meter

    def get_world_size(self):
        return self.world_width, self.world_height

    def worldVector_to_pixelVector(self, vector: tuple):
        return self.world_to_pixel(vector[0]), self.world_to_pixel(vector[1])

    def pixelVector_to_worldVector(self, vector: tuple):
        return self.pixel_to_world(vector[0]), self.pixel_to_world(vector[1])