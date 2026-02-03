class Camera:
    def __init__(self, start_offset: tuple = (0, 0)):
        # Camera offsets are expressed in window space (in pixels)
        self.x_offset = start_offset[0]
        self.y_offset = start_offset[1]

        self.camera_speed = 300.0   # In pixel / sec

    def move(self, vector: tuple, dt: float):
        self.x_offset +=  vector[0] * (self.camera_speed * dt)
        self.y_offset += vector[1] * (self.camera_speed * dt)

    def change_camera_speed(self, new_speed: float):
        self.camera_speed = new_speed

    def apply_offset(self, pos: tuple):
        return pos[0] + self.x_offset, pos[1] + self.y_offset