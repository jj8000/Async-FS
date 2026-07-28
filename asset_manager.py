from pathlib import Path

from PIL import Image


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
