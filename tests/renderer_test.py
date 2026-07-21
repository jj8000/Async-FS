from gamestate import AreaType, AreaTemplate, Area, TileTemplate, Tile, Board, BoardRenderer, UnitTemplate, UnitState
import random

WorldTemplate1 = AreaTemplate('foo', AreaType.WORLD, 3, objective_space=True)
WorldTemplate2 = AreaTemplate('qoo', AreaType.WORLD, 1, objective_space=True)
WorldTemplate3 = AreaTemplate('moo', AreaType.WORLD, 1, objective_space=True)
WorldTemplate4 = AreaTemplate('woo', AreaType.WORLD, 5, objective_space=True)
WorldTemplate5 = AreaTemplate('koo', AreaType.WORLD, 2, objective_space=True)

VoidTemplate1 = AreaTemplate('ook', AreaType.VOID, 3, objective_space=False)
VoidTemplate2 = AreaTemplate('oop', AreaType.VOID, 3, objective_space=False)
VoidTemplate3 = AreaTemplate('oot', AreaType.VOID, 3, objective_space=False)
VoidTemplate4 = AreaTemplate('ooj', AreaType.VOID, 3, objective_space=False)
VoidTemplate5 = AreaTemplate('ooh', AreaType.VOID, 3, objective_space=False)

World1 = Area(WorldTemplate1)
World2 = Area(WorldTemplate2)
Void1 = Area(VoidTemplate1)
Void2 = Area(VoidTemplate2)

scout = UnitTemplate("Scout", "Scout", "ground_unit", 0, "spacemarines", 1, 2, 2, 2, False)
space_marine = UnitTemplate("Space Marine", "Space Marine", "ground_unit", 1, "spacemarines", 2, 3, 3, 3, False)
land_raider = UnitTemplate("Land Raider", "Land Raider", "ground_unit", 2, "spacemarines", 3, 3, 4, 4, False)
titan = UnitTemplate("Warlord Titan", "Warlord Titan", "ground_unit", 3, "spacemarines", 4, 4, 5, 6, True)


tile_templates = [TileTemplate(id=str(i), image_path=f"assets/testtile{i}.png",
                               area_templates=[WorldTemplate5, VoidTemplate5, VoidTemplate2, WorldTemplate3],
                               is_faction_tile=False) for i in range(1, 7)]

tiles = [Tile(template, rotation=random.choice([0, 90, 180, 270])) for template in tile_templates]

board = Board(player_count=2)

renderer = BoardRenderer()

random.shuffle(tiles)

tile_iterator = iter(tiles)

board.add_tile(tile=next(tile_iterator), setup_coords=(0, 0))
img = renderer.render(board, debug=True)
img.save("test_output1.png")

board.add_tile(tile=next(tile_iterator), setup_coords=(-1, 0))
img = renderer.render(board, debug=True)
img.save("test_output2.png")

board.add_tile(tile=next(tile_iterator), setup_coords=(0, 1))
img = renderer.render(board, debug=True)
img.save("test_output3.png")

board.add_tile(tile=next(tile_iterator), setup_coords=(0, -1))
img = renderer.render(board, debug=True)
img.save("test_output4.png")

board.add_tile(tile=next(tile_iterator), setup_coords=(-1, -1))
img = renderer.render(board, debug=True)
img.save("test_output5.png")

board.tiles.get((0, 0)).areas[0].add_units(scout, 1)
board.tiles.get((0, 1)).areas[3].add_units(scout, 1, 1)

img = renderer.render(board, debug=True)
img.save("test_output6.png")

board.tiles.get((0, 1)).areas[3].add_units(space_marine, 1, 0)
board.tiles.get((0, 1)).areas[3].add_units(land_raider, 1)
board.tiles.get((-1, -1)).areas[0].add_units(scout, 3, 1)
board.tiles.get((0, 1)).areas[0].add_units(titan, 0, 1)
board.tiles.get((0, 1)).areas[1].add_units(titan, 1)
board.tiles.get((0, 1)).areas[1].add_units(space_marine, 0, 1)
board.tiles.get((0, 1)).areas[1].add_units(land_raider, 1)
board.tiles.get((0, 1)).areas[1].add_units(scout, 2)

img = renderer.render(board, debug=True)
img.save("test_output7.png")