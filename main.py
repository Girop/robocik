import csv
from math import cos, pi, sin
from os import path
from pynput import keyboard

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

    def rotate(self, angle: float):
        """Rotate vector by given angle in radians, returns Vector"""
        new_x = self.x * cos(angle) - self.y * sin(angle)
        new_y = self.x * sin(angle) - self.y * cos(angle)
        return Vector(new_x, new_y)


class Drone:
    def __init__(self) -> None:
        self.position = Vector(0, 0)
        self.rotation = 0
        self.clear_logs()

        with open(SAVE_PATH, 'w+') as file:
            writer = csv.DictWriter(
                file, fieldnames=self.console_values.keys()
            )
            writer.writeheader()

    def rotate(self, angle: float) -> None:
        self.rotation += angle
        self.console_values['control_rotation'] += angle
        self.console_values['rotation'] = self.rotation

    def update_movement_logs(self, movement: Vector) -> None:
        self.console_values['control_x'] += movement.x
        self.console_values['control_y'] += movement.y
        self.console_values['position_x'] = self.position.x
        self.console_values['position_y'] = self.position.y

    def move_forward(self, distance: float) -> None:
        movement = Vector(distance, 0).rotate(self.rotation)
        self.position += movement
        self.update_movement_logs(movement)

    def move_sideway(self, distance: float) -> None:
        movement = Vector(0, distance).rotate(self.rotation)
        self.position += movement
        self.update_movement_logs(movement)

    def print_logs(self) -> None:
        print(self.console_values)

    def clear_logs(self) -> None:
        self.console_values = {
            'control_x': 0,
            'control_y': 0,
            'control_rotation': 0,
            'rotation': self.rotation,
            'position_x': self.position.x,
            'position_y': self.position.y
        }

    def save_to_csv(self) -> None:
        new_data = [value for (_key, value) in self.console_values.items()]
        with open(SAVE_PATH, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(new_data)


def match_key(key, drone):

    match key.char.lower():
        case 'w':
            drone.move_forward(1.0)
        case 's':
            drone.move_forward(-1.0)
        case 'a':
            drone.move_sideway(1.0)
        case 'd':
            drone.move_sideway(1.0)
        case 'q':
            drone.rotate(pi/4)
        case 'e':
            drone.rotate(-pi/4)
        case _:
            return False

    return True


def handle_press(key: keyboard.KeyCode, drone: Drone):
    if hasattr(key, 'char'):
        if (match_key(key, drone)):
            drone.print_logs()
            drone.save_to_csv()
            drone.clear_logs()


if __name__ == '__main__':
    drone = Drone()
    listener = keyboard.Listener(
        on_press=lambda keyCode: handle_press(keyCode, drone)
    )
    listener.start()
    
    while True:
        pass
