from __future__ import annotations
from dataclasses import dataclass
import random
from enum import Enum
from PIL import Image, ImageDraw
from collections import deque
from math import pi, sin, cos
from geometry import rotate_vector


class Asset: pass


class Player:
    def __init__(self, name: str, faction: Faction, index: int):
        self.name = name
        self.faction = faction
        self.index = index

        self.units = dict(self.faction.starting_units)
        self.assets = dict(self.faction.starting_assets)
        self.materiel = self.faction.starting_materiel

        self.combat_deck = CombatDeck(self.faction.starting_combat_cards)
        self.event_deck = EventDeck(self.faction.event_cards)

        self.order_upgrades = []


@dataclass(frozen=True)
class Faction:
    name: str
    id: FactionId
    ability: str
    starting_units: dict[UnitTemplate, int]
    total_units: dict[UnitTemplate, int]
    starting_assets: dict[Asset, int]
    starting_materiel: int
    starting_combat_cards: list[CombatCard]
    combat_upgrades: list[CombatCard]
    order_upgrades: list[OrderUpgrade]
    event_cards: list[EventCard]
    home_tile: Tile


class FactionId(Enum):
	SPACE_MARINES = "Space Marines"
	CHAOS = "Chaos Space Marines"
	ORKS = "Orks"
	ELDAR = "Eldar"
	
	
class AreaType(Enum):
    VOID = "void"
    WORLD = "world"


@dataclass(frozen=True)
class UnitTemplate:
    name: str
    long_name: str
    unit_type: UnitType
    command_level: int
    faction: FactionId

    combat_value: int
    health: int
    morale: int

    materiel_cost: int
    requires_forge: bool
    
    image_path: str


class UnitType(Enum):
	GROUND = "ground unit"
	SHIP = "ship"


@dataclass
class UnitState:
    unrouted: int = 0
    routed: int = 0


class StructureType(Enum):
    CITY = "city"
    FACTORY = "factory"
    BASTION = "bastion"


@dataclass(frozen=True)
class StructureTemplate:
    type: StructureType
    name: str

    combat_value: int
    health: int
    morale: int

    materiel_cost: int


@dataclass
class StructureState:
    faction: Faction
    cities: int = 0
    factories: int = 0
    bastions: int = 0


class GameState:
    def __init__(self, players):
        self.players = players
        self.current_round = 0
        self.first_player_index = 0
        self.active_player_index = 0

    def next_player(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.players)


@dataclass
class PlayerSetup:
    name: str
    faction: Faction


class SetupConfig:
    def __init__(self):
        self.players = []

    def add_player(self, player_name: str, faction: Faction):
        self.players.append(PlayerSetup(player_name, faction))


def setup_game(config: SetupConfig) -> GameState:
    player_setups = config.players.copy()
    random.shuffle(player_setups)
    players = []

    for index, ps in enumerate(player_setups):
        player = Player(
            name=ps.name,
            faction=ps.faction,
            index=index
        )
        players.append(player)

    return GameState(players)


class EventDeck:
    def __init__(self, event_cards):
        self.cards = list(event_cards)
        self.shuffle()

    def __iter__(self):
        return iter(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, number_of_cards: int = 1):
        if number_of_cards > len(self.cards):
            raise ValueError("Not enough cards in deck")

        drawn = [self.cards.pop() for _ in range(number_of_cards)]
        return drawn[0] if number_of_cards == 1 else drawn

    def return_card(self, card: EventCard):
        self.cards.append(card)
        self.shuffle()


class CombatDeck:
    def __init__(self, combat_cards):
        self.cards = list(combat_cards)
        self.shuffle()

    def __iter__(self):
        return iter(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, number_of_cards: int):
        if number_of_cards > len(self.cards):
            raise ValueError("Not enough cards in deck")

        drawn = [self.cards.pop() for _ in range(number_of_cards)]
        return drawn

    def upgrade(self, removed_cards, purchased_cards):
        ...


@dataclass
class EventCard:
    name: str
    image_path: str


@dataclass
class CombatCard:
    name: str
    image_path: str


@dataclass
class OrderUpgrade:
    name: str
    image_path: str


@dataclass(frozen=True)
class AreaTemplate:
    name: str
    area_type: AreaType
    capacity: int
    objective_space: bool
    forge: int = 0
    cache: int = 0
    reinforcement: int = 0
    prosperity: int = 0
    origin_offset: tuple[float, float] = (0, 0)
    anchor_radius: float | None = None


class Area:
    def __init__(self, template: AreaTemplate):
        self.template = template

        self.units: dict[UnitTemplate, UnitState] = {}
        self.structures: StructureState | None = None
        self.attacker_units: dict[UnitTemplate, UnitState] = {}
        self.objective_token = None
        self.tile_position = None
        self.local_origin = None
        self.global_origin = None

    @property
    def capacity(self):
        return self.template.capacity

    @property
    def area_type(self):
        return self.template.area_type

    @property
    def friendly_faction(self) -> Faction | None:
        if self.is_contested() or self.is_uncontrolled():
            return None
        if self.units:
            return next(iter(self.units)).faction
        return self.structures.faction

    def add_units(self, unit: UnitTemplate, amount_unrouted: int, amount_routed: int = 0):
        state = self.units.get(unit) or self.attacker_units.get(unit)

        if state is None:
            state = UnitState()
            if not self.units:
                self.units[unit] = state
            elif unit.faction == next(iter(self.units)).faction:
                self.units[unit] = state
            else:
                self.attacker_units[unit] = state

        state.unrouted += amount_unrouted
        state.routed += amount_routed

    def remove_units(self, unit: UnitTemplate, amount_unrouted: int, amount_routed: int = 0):
        if unit in self.units:
            units_dict = self.units
        elif unit in self.attacker_units:
            units_dict = self.attacker_units
        else:
            return

        state = units_dict[unit]

        state.unrouted -= min(state.unrouted, amount_unrouted)
        state.routed -= min(state.routed, amount_routed)

        if state.unrouted == 0 and state.routed == 0:
            del units_dict[unit]
            
    def add_structure(self, structure: StructureType, faction: Faction):
        if self.structures is  None:
            self.structures = StructureState(faction)
        match structure:
            case StructureType.CITY:
                self.structures.cities += 1
            case StructureType.FACTORY:
                self.structures.factories += 1
            case StructureType.BASTION:
                self.structures.bastions += 1

    def remove_structure(self, structure: StructureType):
        if self.structures is None:
            return
        match structure:
            case StructureType.CITY:
                self.structures.cities -= min(self.structures.cities, 1)
            case StructureType.FACTORY:
                self.structures.factories -= min(self.structures.factories, 1)
            case StructureType.BASTION:
                self.structures.bastions -= min(self.structures.bastions, 1)
        if sum(number for number in vars(self.structures).values() if isinstance(number, int)) == 0:
            self.structures = None

    def is_uncontrolled(self) -> bool:
        return not self.units and self.structures is None

    def is_contested(self) -> bool:
        return bool(self.attacker_units)

    def calculate_anchors(self, radius):
        if self.is_uncontrolled():
            return

        if not self.is_contested() and self.units:
            n = len(self.units) # number of unit anchors
            phi = 360 / n
            anchor_offsets = [rotate_vector((0, -radius), i * phi) for i in range(n)]
            return anchor_offsets

        elif self.is_contested():
            n_defender = len(self.units)
            n_attacker = len(self.attacker_units)
            phi_def = 180 / (n_defender + 1)
            phi_att = - 180 / (n_attacker + 1)
            anchor_offsets_defender = [rotate_vector((0, -radius), i * phi_def) for i in range(1, n_defender + 1)]
            anchor_offsets_attacker = [rotate_vector((0, -radius), i * phi_att) for i in range(1, n_attacker + 1)]
            return anchor_offsets_defender, anchor_offsets_attacker


@dataclass(frozen=True)
class TileTemplate:
    id: str
    image_path: str
    area_templates: list[AreaTemplate]
    is_faction_tile: bool


class Tile:
    DEFAULT_LOCAL_ORIGINS = ((0.25, 0.25), (0.75, 0.25), (0.75, 0.75), (0.25, 0.75))

    def __init__(self, template: TileTemplate, rotation: int = 0):
        self.template = template
        self.rotation = rotation

        self.areas = deque([Area(area_template) for area_template in self.template.area_templates])
        ccw_turns = self.rotation // 90
        self.areas.rotate(-ccw_turns)

        for i, area in enumerate(self.areas):
            area.tile = self
            area.tile_position = i
            x0, y0 = self.DEFAULT_LOCAL_ORIGINS[i]
            dx, dy = self._rotate_offset(area.template.origin_offset, self.rotation)
            area.local_origin = (x0 + dx, y0 + dy)

        self.board = None
        self.setup_position = None
        self.position = None
        self.label = None

    @staticmethod
    def _rotate_offset(offset: tuple[float, float], rotation: int) -> tuple[float, float]:
        dx, dy = offset

        if rotation == 0:
            return dx, dy
        elif rotation == 90:
            return dy, -dx
        elif rotation == 180:
            return -dx, -dy
        elif rotation == 270:
            return -dy, dx
        raise ValueError(f"Invalid rotation angle: {rotation} degrees")


class Board:
    COLUMN_LABELS = ('A', 'B', 'C', 'D')
    ROW_LABELS = ('1', '2', '3', '4')

    def __init__(self, player_count: int):
        if player_count == 2:
            self.dimensions = (2, 3)
        elif player_count == 3:
            self.dimensions = (3, 3)
        elif player_count == 4:
            self.dimensions = (3, 4)

        self.tiles: dict[tuple[int, int], Tile] = {}
        self._setup_complete = False

    def add_tile(self, tile: Tile, setup_coords: tuple[int, int]):

        if setup_coords in self.tiles:
            raise ValueError("Tile already exists at this position")

        self.tiles[setup_coords] = tile

        tile.board = self
        tile.setup_position = setup_coords

    def get_tile(self, position: tuple[int, int]) -> Tile | None:
        return self.tiles.get(position)

    def _finalise_layout(self):
        global_cs_origin = min(self.tiles.keys(), key=lambda p: p[0] + p[1]) # new global CS origin (topleft)
        for setup_position, tile in self.tiles.items():
            tile.position = (setup_position[0] - global_cs_origin[0], setup_position[1] - global_cs_origin[1])
            tile.label = f"{self.COLUMN_LABELS[tile.position[0]]}{self.ROW_LABELS[tile.position[1]]}"
            for area in tile.areas:
                area.global_origin = (tile.position[0] + area.local_origin[0],
                                      tile.position[1] + area.local_origin[1])
        self._setup_complete = True


class BoardRenderer:
    TILE_SIZE = 300
    DEFAULT_ANCHOR_RADIUS = TILE_SIZE / 6
    UNIT_OFFSET = 15
    STRUCTURE_OFFSET = 8

    def normalise(self, value):
        return value * self.TILE_SIZE if value else None

    @staticmethod
    def paste_centered(canvas: Image.Image, image: Image.Image, centre: tuple[int, int]) -> None:
        x, y = centre
        canvas.paste(image, (round(x - image.width / 2), round(y - image.height / 2)), image)

    def draw_units(self, area: Area, draw: ImageDraw.Draw):
        anchor_offsets = (
            area.calculate_anchors(radius = self.normalise(area.template.anchor_radius) or self.DEFAULT_ANCHOR_RADIUS))
        area_origin_px, area_origin_py = self.normalise(area.local_origin[0]), self.normalise(area.local_origin[1])
        if anchor_offsets:
            if not area.is_contested():
                for offset, (unit_template, unit_state) in zip(anchor_offsets, area.units.items()):
                    unrouted = unit_state.unrouted
                    routed = unit_state.routed
                    anchor_position = (area_origin_px + offset[0], area_origin_py + offset[1])
                    cursor = anchor_position
                    for i in range(unrouted):
                        draw.circle(cursor, 5, "white")
                        cursor = (cursor[0] + self.UNIT_OFFSET, cursor[1])
                    for i in range(routed):
                        draw.circle(cursor, 5, "black")
                        cursor = (cursor[0] + self.UNIT_OFFSET, cursor[1])
            elif area.is_contested():
                for offset, (unit_template, unit_state) in zip(anchor_offsets[0], area.units.items()):
                    unrouted = unit_state.unrouted
                    routed = unit_state.routed
                    anchor_position = (area_origin_px + offset[0], area_origin_py + offset[1])
                    cursor = anchor_position
                    for i in range(unrouted):
                        draw.circle(cursor, 5, "white")
                        cursor = (cursor[0] + self.UNIT_OFFSET, cursor[1])
                    for i in range(routed):
                        draw.circle(cursor, 5, "black")
                        cursor = (cursor[0] + self.UNIT_OFFSET, cursor[1])

                for offset, (unit_template, unit_state) in zip(anchor_offsets[1], area.attacker_units.items()):
                    unrouted = unit_state.unrouted
                    routed = unit_state.routed
                    anchor_position = (area_origin_px + offset[0], area_origin_py + offset[1])
                    cursor = anchor_position
                    for i in range(unrouted):
                        draw.circle(cursor, 5, "white")
                        cursor = (cursor[0] + self.UNIT_OFFSET, cursor[1])
                    for i in range(routed):
                        draw.circle(cursor, 5, "black")
                        cursor = (cursor[0] + self.UNIT_OFFSET, cursor[1])

    def draw_structures(self, area: Area, tile_img):
        area_origin_px, area_origin_py = self.normalise(area.local_origin[0]), self.normalise(area.local_origin[1])
        structure_mappings = (
        (StructureType.CITY, area.structures.cities, f"assets/city.png"),
        (StructureType.FACTORY, area.structures.factories, f"assets/factory.png"),
        (StructureType.BASTION, area.structures.bastions, f"assets/bastion.png")
        )
        structure_total = sum(count for structure_type, count, img_path in structure_mappings)
        leftmost_offset = (structure_total - 1) * self.STRUCTURE_OFFSET / 2
        starting_position = area_origin_px - leftmost_offset, area_origin_py
        cursor = starting_position
        for structure_type, count, img_path in structure_mappings:
            img = Image.open(img_path).convert("RGBA")
            for _ in range(count):
                self.paste_centered(tile_img, img, cursor)
                cursor = (cursor[0] + self.STRUCTURE_OFFSET, cursor[1])

    def render(self, board: Board, debug=False):
        tiles = board.tiles

        # board dimensions
        min_x = min(x for (x, y) in tiles.keys())
        max_x = max(x for (x, y) in tiles.keys())
        min_y = min(y for (x, y) in tiles.keys())
        max_y = max(y for (x, y) in tiles.keys())
        x_dimension = max_x - min_x + 1
        y_dimension = max_y - min_y + 1

        pixel_width = x_dimension * self.TILE_SIZE
        pixel_height = y_dimension * self.TILE_SIZE

        canvas = Image.new("RGBA", (pixel_width, pixel_height))

        for (x, y), tile in tiles.items():
            img = Image.open(tile.template.image_path)

            if tile.rotation:
                img = img.rotate(tile.rotation)

            px = (x - min_x) * self.TILE_SIZE
            py = (y - min_y) * self.TILE_SIZE

            if debug:
                draw = ImageDraw.Draw(img)
                draw.rectangle((0, 0, self.TILE_SIZE - 1, self.TILE_SIZE - 1), fill=None, outline="black", width=3)
                draw.text((20, 20), text=str(f"id: {tile.template.id}\nrot: {tile.rotation}"), fill="black")
                for area in tile.areas:
                    area_origin_px = self.normalise(area.local_origin[0])
                    area_origin_py = self.normalise(area.local_origin[1])
                    draw.circle((area_origin_px, area_origin_py), 5, "black")
                    draw.circle((area_origin_px, area_origin_py), self.DEFAULT_ANCHOR_RADIUS)
                    self.draw_units(area, draw)
                    if area.structures is not None:
                        self.draw_structures(area, img)


                    draw.text((area_origin_px - 15, area_origin_py - 15), text=str(area.tile_position), fill="black")

            canvas.paste(img, (px, py))

        return canvas





