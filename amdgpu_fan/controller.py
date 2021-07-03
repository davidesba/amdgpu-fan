import os
import sys
import time

import yaml

from amdgpu_fan import LOGGER as logger
from amdgpu_fan.lib.amdgpu import Scanner
from amdgpu_fan.lib.curve import Curve


CONFIG_LOCATIONS = [
    '/etc/amdgpu-fan.yml',
]


class FanController:
    def __init__(self, config):
        self.curves = dict()
        self._scanner = Scanner(config.get('cards'))
        if len(self._scanner.cards) < 1:
            logger.error('no compatible cards found, exiting')
            sys.exit(1)
        
        for name, curve in config.get('speed_matrix', {}).items():
            self.curves[name] = Curve(curve)

        self._frequency = 1

    def get_speed(self, card):
        speed = 0
        max_temp = 0
        max_counter = ''
        for name, curve in self.curves.items():
            new_temp = int(getattr(card, f'{name}_temp', 0))
            new_speed = curve.get_speed(new_temp)
            if new_speed > speed:
                speed = new_speed
                if new_temp > max_temp:
                    max_temp = new_temp
                    max_counter = name
        return speed, max_temp, max_counter

    def main(self):
        logger.info(f'starting amdgpu-fan')
        while True:
            for name, card in self._scanner.cards.items():
                speed, max_temp, max_counter = self.get_speed(card)
                if speed < 0:
                    speed = 0

                logger.debug(f'{name}: Temp[{max_counter}] {max_temp}, Setting fan speed to: {speed}, fan speed{card.fan_speed}, min:{card.fan_min}, max:{card.fan_max}')

                card.set_fan_speed(speed)
            time.sleep(self._frequency)


def load_config(path):
    logger.debug(f'loading config from {path}')
    with open(path) as f:
        return yaml.load(f)


def main():

    default_fan_config = '''#Fan Control Matrix. [<Temp in C>,<Fanspeed in %>]
speed_matrix:
  gpu:
    - [0, 0]
    - [30, 33]
    - [45, 50]
    - [60, 66]
    - [65, 69]
    - [70, 75]
    - [75, 89]
    - [80, 100]

# optional
# cards:  # can be any card returned from `ls /sys/class/drm | grep "^card[[:digit:]]$"`
# - card0
'''
    config = None
    for location in CONFIG_LOCATIONS:
        if os.path.isfile(location):
            config = load_config(location)
            break

    if config is None:
        logger.info(f'no config found, creating one in {CONFIG_LOCATIONS[-1]}')
        with open(CONFIG_LOCATIONS[-1], 'w') as f:
            f.write(default_fan_config)
            f.flush()

        config = load_config(CONFIG_LOCATIONS[-1])

    FanController(config).main()


if __name__ == '__main__':
    main()
