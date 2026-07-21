from PIL import Image, ImageDraw

# Create a blank 600x400 image
board = Image.new("RGBA", (600, 400), "black")

# Create first tile
tile1 = Image.new("RGBA", (200, 200), "darkgreen")
draw1 = ImageDraw.Draw(tile1)
draw1.text((20, 20), "Tile A", fill="white")

# Create second tile
tile2 = Image.new("RGBA", (200, 200), "darkred")
draw2 = ImageDraw.Draw(tile2)
draw2.text((20, 20), "Tile B", fill="white")

# Rotate second tile
tile2 = tile2.rotate(90, expand=True)

# Paste tiles onto board
board.paste(tile1, (0, 0))
board.paste(tile2, (200, 0))

# Save result
board.save("map_test.png")

# Open image automatically (debug helper)
board.show()

print("Saved map_test.png")