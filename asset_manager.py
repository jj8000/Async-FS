from pathlib import Path
from PIL import Image

from unit_templates import *


class AssetManager:
    def __init__(self, asset_directory: str | Path) -> None:
        self.asset_directory = Path(asset_directory)
        self._image_cache: dict[Path, Image.Image] = {}

    def image(self, relative_path: str | Path) -> Image.Image:
        relative_path = Path(relative_path)

        if relative_path not in self._image_cache:
            full_path = self.asset_directory / relative_path
            self._image_cache[relative_path] = Image.open(full_path).convert("RGBA")

        return self._image_cache[relative_path]


assets = AssetManager("assets")

img = assets.image(SCOUT.image_path)

print(img)
print(img.size)

# img.show()

img2 = assets.image(SCOUT.image_path)

print(img is img2)

MAX_UNIT_SIZE = (100, 100)
PADDING = 10

unit_images = []

for unit in ALL_UNITS:
    image = assets.image(unit.image_path).copy()
    image.thumbnail(MAX_UNIT_SIZE)

    unit_images.append(image)

width = sum(image.width for image in unit_images) + PADDING * (len(unit_images) - 1)
height = max(image.height for image in unit_images)

canvas = Image.new("RGBA", (width, height), (255, 255, 255, 255))

x = 0

for image in unit_images:
    y = (height - image.height) // 2
    canvas.paste(image, (x, y), image)

    x += image.width + PADDING

canvas.show()