import csv
from math import cos, pi, sin, degrees
from os import path
from pynput import keyboard
import pygame as pg
from pygame import freetype
from screeninfo import get_monitors
import argparse

monitor = get_monitors()[0]
SAVE_PATH = path.join(path.dirname(__file__), 'positions.csv')
SUBMARINE_IMG = path.join(path.dirname(__file__), 'submarine.png')
WIDTH, HEIGHT = (monitor.width, monitor.height)


class Vector:
    """Object representing position or movment"""

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
    """Main class for managing positons and motions"""

    def __init__(self, start_x=0, start_y=0, print_flag=True, save_flag=True) -> None:
        self.position = Vector(start_x, start_y)
        self.rotation = 0
        self.clear_logs()
        self.print_flag = print_flag
        self.save_flag = save_flag

        with open(SAVE_PATH, 'w+') as file:
            writer = csv.DictWriter(
                file, fieldnames=self.console_values.keys()
            )
            writer.writeheader()

    def update_movement_logs(self, movement: Vector) -> None:
        self.console_values['control_x'] += movement.x
        self.console_values['control_y'] += movement.y
        self.console_values['position_x'] = self.position.x
        self.console_values['position_y'] = self.position.y

    def rotate(self, angle: float) -> None:
        self.rotation += angle
        self.rotation %= 2 * pi
        self.console_values['control_rotation'] += angle
        self.console_values['rotation'] = self.rotation

    def move_forward(self, distance: float) -> None:
        movement = Vector(distance, 0).rotate(-self.rotation)
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

    def match_key(self, key) -> bool:
        """Handles drone movement, returns True when action was made"""
        match key.char.lower():
            case 'w':
                self.move_sideway(1.0)
            case 's':
                self.move_sideway(-1.0)
            case 'a':
                self.move_forward(-1.0)
            case 'd':
                self.move_forward(1.0)
            case 'q':
                self.rotate(pi/36)  # 5 degrees
            case 'e':
                self.rotate(-pi/36)  # -5 degrees
            case _:
                return False

        return True

    def manage_logs(self) -> None:
        if self.print_flag:
            self.print_logs()
        if self.save_flag:
            self.save_to_csv()
        self.clear_logs()


def handle_press(key: keyboard.KeyCode, drone: Drone):
    if hasattr(key, 'char'):
        if (drone.match_key(key)):
            drone.manage_logs()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simulate simple underwater drone movement'
    )
    parser.add_argument(
        '-p', '--print', action='store_true', help='Prints drone postions to console'
    )
    parser.add_argument(
        '-s', '--save', action='store_true', help='Saves drone positions to `positions.csv`'
    )
    args = parser.parse_args()

    drone = Drone(
        WIDTH / 2, HEIGHT / 2, print_flag=args.print, save_flag=args.save
    )

    listener = keyboard.Listener(
        on_press=lambda keyCode: handle_press(keyCode, drone)
    )
    listener.start()

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
    sub_img = pg.image.load(SUBMARINE_IMG)
    font = freetype.SysFont(name=freetype.get_default_font(), size=18)
    deegree_sym = u"\u00b0"
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((174, 198, 207))

        # Degrees subtitle render
        dg_val = int(degrees(drone.rotation))
        y_text = drone.position.y + sub_img.get_height() + 5
        x_text = drone.position.x + sub_img.get_width() / 3
        font.render_to(
            screen, (x_text, y_text), f'{dg_val}' + deegree_sym, (0, 0, 0)
        )
        #
        rotated_img = pg.transform.rotate(sub_img, degrees(drone.rotation))

        screen.blit(rotated_img, (drone.position.x, drone.position.y))
        pg.display.flip()
