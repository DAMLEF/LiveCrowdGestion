class Camera:
    def __init__(self, start_offset: tuple = (0, 0)):
        # Camera offsets are expressed in window space (in pixels)
        self.x_offset = start_offset[0]
        self.y_offset = start_offset[1]

        self.camera_speed = 2.0   # In pixel

    def move(self, vector: tuple):
        self.x_offset +=  vector[0] * self.camera_speed
        self.y_offset += vector[1] * self.camera_speed

    def change_camera_speed(self, new_speed: float):
        self.camera_speed = new_speed

    def apply_offset(self, pos: tuple):
        return pos[0] - self.x_offset, pos[1] - self.y_offset