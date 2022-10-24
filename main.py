from pynput import keyboard
from math import cos, sin, pi
import csv
from os import path

SAVE_PATH = path.join(path.dirname(__file__), 'positions.csv')

# TODO:
# Saving to csv on change
# Visualisation
# Documentation


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

    def rotate(self, angle: float):
        self.rotation += angle

    def move_forward(self, distance: float) -> None:
        self.position += Vector(distance,
                                0).rotate(self.rotation, self.position)

    def move_sideway(self, distance: float) -> None:
        self.position += Vector(0,
                                distance).rotate(self.rotation, self.position)

    def save_to_csv(self) -> None:
        raise NotImplementedError
        field_names = [
            'Control X', 'Control Y', 'Control rotation', 'Rotation', 'Positon X', 'Position Y'
        ]
        with open(SAVE_PATH) as file:
            writer = csv.DictWriter()


def handle_press(key: keyboard.KeyCode, drone: Drone):
    match key.char.lower():
        case 'w':
            drone.move_forward(1)
        case 's':
            drone.move_forward(-1)
        case 'a':
            drone.move_sideway(1)
        case 'd':
            drone.move_sideway(1)
        case 'q':
            drone.rotate(pi/4)
        case 'e':
            drone.rotate(-pi/4)
        case _:
            pass


if __name__ == '__main__':

    drone = Drone()
    keyboard.Listener(
        on_press=lambda keyCode: handle_press(keyCode, drone)
    ).start()

    while True:
        pass
