"""Script to parse data from a vacuum map."""

import logging

from tuya_vacuum import Map
from tuya_vacuum.map.layout import Layout
from tuya_vacuum.map.path import Path


logging.basicConfig(level=logging.DEBUG)


def main():
    """Parse data from a vacuum map."""

    with open("path.bin", "rb") as path_file:
        with open("layout.bin", "rb") as layout_file:
            layout = Layout(layout_file.read())
            path = Path(path_file.read())

            vacuum_map = Map(layout, path)
            map_image = vacuum_map.to_image()
            map_image.save("combined.png")


if __name__ == "__main__":
    main()
