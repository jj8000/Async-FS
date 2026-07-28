from pathlib import Path

from PIL import Image


class AssetManager:
    def __init__(self, asset_directory: str | Path) -> None:
        self.asset_directory = Path(asset_directory)

    def load_image(self, relative_path: str | Path) -> Image.Image:
        full_path = self.asset_directory / relative_path

        return Image.open(full_path).convert("RGBA")
