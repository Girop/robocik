from pynput import keyboard
from math import cos, sin
import csv
from os import path

SAVE_PATH = path.join(path.dirname(__file__), 'positions.csv')

d
class Vector:
    def __init__(self, x_start: float, y_start: float) -> None:
        self.x = x_start
        self.y = y_start

    def __str__(self) -> str:
        return f'<Vector({self.x},{self.y})>'

    def __add__(self, other_vector):
        return Vector(self.x + other_vector.x, self.y + other_vector.y)

    def rotate(self, angle: float, starting_pos) -> None:
        new_x = (self.x - starting_pos.x)*cos(angle) - \
            (self.y - starting_pos.y) * sin(angle) + starting_pos.x
        new_y = (self.x - starting_pos.x)*sin(angle) - \
            (self.y - starting_pos.y) * cos(angle) + starting_pos.y

        self.x = new_x
        self.y = new_y


class Drone:

    def __init__(self) -> None:
        self.position = Vector(0, 0)
        self.rotation = 0

    def forward(self):
        self.position += Vector(0, 1)

    def backward(self):
        self.position += Vector(0, -1)

    def leftward(self):
        self.position += Vector(1, 0)

    def rightward(self):
        self.position += Vector(-1, 0)

    def save_to_csv(self) -> None:
        raise NotImplementedError
        field_names = [
            'Control X', 'Control Y', 'Control rotation', 'Rotation', 'Positon X', 'Position Y'
        ]
        with open(SAVE_PATH) as file:
            writer = csv.DictWriter()


if __name__ == '__main__':
    pass
