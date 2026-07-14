"""
Renderer playground / regression test for the current Forbidden Stars prototype.

Run from the project root:
    python tests/forbidden_stars_renderer_test.py

The script writes PNG snapshots into:
    tests/test_outputs/
"""

from pathlib import Path
import os

print("cwd:", os.getcwd())

for i in range(1, 7):
    p = Path(f"assets/testtile{i}.png")
    print(i, p.exists(), p.resolve())

from pathlib import Path

from gamestate import (
    AreaTemplate,
    AreaType,
    Board,
    BoardRenderer,
    Tile,
    TileTemplate,
    UnitTemplate,
)


OUTPUT_DIR = Path("tests/test_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def check(condition: bool, description: str) -> None:
    if not condition:
        raise AssertionError(description)
    print(f"[PASS] {description}")


def render_step(renderer: BoardRenderer, board: Board, filename: str) -> None:
    output_path = OUTPUT_DIR / f"{filename}.png"
    image = renderer.render(board, debug=True)
    image.save(output_path)
    print(f"[RENDER] {output_path}")


def get_area(board: Board, setup_coords: tuple[int, int], area_index: int):
    tile = board.get_tile(setup_coords)
    if tile is None:
        raise KeyError(f"No tile at setup coordinates {setup_coords}")
    return tile.areas[area_index]


# ---------------------------------------------------------------------------
# Area templates
# ---------------------------------------------------------------------------

world_a = AreaTemplate(
    name="World A",
    area_type=AreaType.WORLD,
    capacity=5,
    objective_space=True,
)

world_b = AreaTemplate(
    name="World B",
    area_type=AreaType.WORLD,
    capacity=3,
    objective_space=False,
    anchor_radius=0.12,
)

world_c = AreaTemplate(
    name="World C",
    area_type=AreaType.WORLD,
    capacity=4,
    objective_space=True,
    origin_offset=(0.02, -0.015),
)

void_a = AreaTemplate(
    name="Void A",
    area_type=AreaType.VOID,
    capacity=3,
    objective_space=False,
)

void_b = AreaTemplate(
    name="Void B",
    area_type=AreaType.VOID,
    capacity=3,
    objective_space=False,
)


# ---------------------------------------------------------------------------
# Unit templates
# ---------------------------------------------------------------------------

scout = UnitTemplate(
    "Scout", "Scout", "ground_unit", 0, "spacemarines",
    1, 2, 2, 2, False
)

space_marine = UnitTemplate(
    "Space Marine", "Space Marine", "ground_unit", 1, "spacemarines",
    2, 3, 3, 3, False
)

land_raider = UnitTemplate(
    "Land Raider", "Land Raider", "ground_unit", 2, "spacemarines",
    3, 3, 4, 4, False
)

titan = UnitTemplate(
    "Warlord Titan", "Warlord Titan", "ground_unit", 3, "spacemarines",
    4, 4, 5, 6, True
)

boyz = UnitTemplate(
    "Boyz", "Ork Boyz", "ground_unit", 0, "orks",
    1, 2, 2, 2, False
)

nobz = UnitTemplate(
    "Nobz", "Ork Nobz", "ground_unit", 1, "orks",
    2, 3, 3, 3, False
)

battlewagon = UnitTemplate(
    "Battlewagon", "Ork Battlewagon", "ground_unit", 2, "orks",
    3, 3, 4, 4, False
)


# ---------------------------------------------------------------------------
# Board and tiles
# ---------------------------------------------------------------------------

tile_templates = [
    TileTemplate(
        id=str(i),
        image_path=f"assets/testtile{i}.png",
        area_templates=[world_a, void_a, void_b, world_c],
        is_faction_tile=False,
    )
    for i in range(1, 7)
]

rotations = (0, 90, 180, 270, 90, 180)
tiles = [
    Tile(template, rotation=rotation)
    for template, rotation in zip(tile_templates, rotations)
]

board = Board(player_count=2)
renderer = BoardRenderer()

placements = (
    ((-1, -1), tiles[0]),
    ((0, -1), tiles[1]),
    ((-1, 0), tiles[2]),
    ((0, 0), tiles[3]),
    ((-1, 1), tiles[4]),
    ((0, 1), tiles[5]),
)

for setup_coords, tile in placements:
    board.add_tile(tile=tile, setup_coords=setup_coords)

board._finalise_layout()

check(board._setup_complete, "Board layout finalised")
check(board.get_tile((-1, -1)).position == (0, 0), "Top-left tile normalised")
check(board.get_tile((-1, -1)).label == "A1", "Top-left tile labelled A1")
check(board.get_tile((0, 1)).label == "B3", "Bottom-right tile labelled B3")

render_step(renderer, board, "01_empty_board")


# ---------------------------------------------------------------------------
# Uncontested layouts
# ---------------------------------------------------------------------------

one_stack = get_area(board, (-1, -1), 0)
one_stack.add_units(scout, 1)

check(len(one_stack.units) == 1, "First stack added")
check(not one_stack.is_contested(), "Single-faction area uncontested")
render_step(renderer, board, "02_one_stack")


two_stacks = get_area(board, (0, -1), 1)
two_stacks.add_units(scout, 2)
two_stacks.add_units(space_marine, 1, 1)

check(len(two_stacks.units) == 2, "Two friendly stacks added")
check(two_stacks.units[space_marine].routed == 1, "Routed count stored")
render_step(renderer, board, "03_two_stacks")


three_stacks = get_area(board, (-1, 0), 2)
three_stacks.add_units(scout, 1)
three_stacks.add_units(space_marine, 2)
three_stacks.add_units(land_raider, 1, 1)

check(
    len(three_stacks.calculate_anchors(renderer.DEFAULT_ANCHOR_RADIUS)) == 3,
    "Three anchors calculated",
)
render_step(renderer, board, "04_three_stacks")


four_stacks = get_area(board, (0, 0), 3)
four_stacks.add_units(scout, 2)
four_stacks.add_units(space_marine, 1)
four_stacks.add_units(land_raider, 1, 1)
four_stacks.add_units(titan, 0, 1)

check(len(four_stacks.units) == 4, "Four stacks added")
render_step(renderer, board, "05_four_stacks")


# ---------------------------------------------------------------------------
# Contested layouts
# ---------------------------------------------------------------------------

combat_area = get_area(board, (-1, 1), 0)

combat_area.add_units(scout, 2)
combat_area.add_units(space_marine, 1)
combat_area.add_units(boyz, 3)

check(len(combat_area.units) == 2, "Defenders remain in units")
check(len(combat_area.attacker_units) == 1, "Attacker added separately")
check(combat_area.is_contested(), "Area reports contested")
render_step(renderer, board, "06_combat_two_vs_one")


combat_area.add_units(nobz, 1, 1)
combat_area.add_units(battlewagon, 1)

check(len(combat_area.attacker_units) == 3, "Attacker reinforcements added")
render_step(renderer, board, "07_combat_two_vs_three")


combat_area.add_units(scout, 2)
combat_area.add_units(boyz, 1)

check(combat_area.units[scout].unrouted == 4, "Defender reinforced")
check(combat_area.attacker_units[boyz].unrouted == 4, "Attacker reinforced")
render_step(renderer, board, "08_reinforced")


# ---------------------------------------------------------------------------
# Removals
# ---------------------------------------------------------------------------

combat_area.remove_units(scout, 1)
check(combat_area.units[scout].unrouted == 3, "Partial defender removal")
render_step(renderer, board, "09_partial_defender_removal")


combat_area.remove_units(nobz, 1, 1)
check(nobz not in combat_area.attacker_units, "Attacker stack deleted")
render_step(renderer, board, "10_remove_attacker_stack")


combat_area.remove_units(space_marine, 1)
check(space_marine not in combat_area.units, "Defender stack deleted")
render_step(renderer, board, "11_remove_defender_stack")


combat_area.remove_units(boyz, 4)
combat_area.remove_units(battlewagon, 1)

check(not combat_area.attacker_units, "All attackers removed")
check(not combat_area.is_contested(), "Area returns to uncontested")
render_step(renderer, board, "12_attackers_cleared")


combat_area.remove_units(titan, 99)
check(titan not in combat_area.units, "Removing missing stack is harmless")


print()
print("All assertions passed.")
print(f"Open rendered images in: {OUTPUT_DIR.resolve()}")
