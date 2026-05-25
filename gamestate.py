from __future__ import annotations
from dataclasses import dataclass
import random
from enum import Enum
from PIL import Image, ImageDraw
from collections import deque


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


@dataclass
class Faction:
    name: str
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

class AreaType(Enum):
    VOID = "void"
    WORLD = "world"

@dataclass(frozen=True)
class UnitTemplate:
    name: str
    long_name: str
    unit_type: str
    command_level: int

    combat_value: int
    health: int
    morale: int

    materiel_cost: int
    requires_forge: bool

@dataclass
class UnitState:
    unrouted: int = 0
    routed: int = 0

class GameState:
    def __init__(self, players):
        self.players = players
        self.current_round = 0
        self.first_player_index = 0

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
        pass

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


class Area:
    def __init__(self, template: AreaTemplate):
        self.template = template

        self.units: dict[UnitTemplate, UnitState] = {}
        self.structures = {}
        self.objective_token = None
        self.position = None
        self.anchor_origin = None

    @property
    def capacity(self):
        return self.template.capacity

    @property
    def area_type(self):
        return self.template.area_type

    def add_units(self, unit: UnitTemplate, amount_unrouted: int, amount_routed: int = 0):
        state = self.units.get(unit)

        if state is None:
            state = UnitState()
            self.units[unit] = state

        state.unrouted += amount_unrouted
        state.routed += amount_routed

    def remove_units(self, unit: UnitTemplate, amount_unrouted: int, amount_routed: int = 0):
        state = self.units.get(unit)
        if state is None:
            return

        state.unrouted -= min(state.unrouted, amount_unrouted)

        state.routed -= min(state.routed, amount_routed)

        if state.unrouted == 0 and state.routed == 0:
            del self.units[unit]

    def is_empty(self) -> bool:
        return len(self.units) == 0

@dataclass(frozen=True)
class TileTemplate:
    id: str
    image_path: str
    area_templates: list[AreaTemplate]
    is_faction_tile: bool

class Tile:
    ANCHOR_ORIGINS = {0: (0.25, 0.25), 1: (0.75, 0.25), 2: (0.75, 0.75), 3: (0.25, 0.75)}

    def __init__(self, template: TileTemplate, rotation: int = 0):
        self.template = template
        self.rotation = rotation

        self.areas = deque([Area(area_template) for area_template in self.template.area_templates])
        ccw_turns = self.rotation // 90
        self.areas.rotate(-ccw_turns)

        for i, area in enumerate(self.areas):
            area.tile = self
            area.position = i
            area.anchor_origin = self.ANCHOR_ORIGINS[area.position]

        self.board = None
        self.position = None

class Board:
    def __init__(self, player_count: int):
        if player_count == 2:
            self.dimensions = (2, 3)
        elif player_count == 3:
            self.dimensions = (3, 3)
        elif player_count == 4:
            self.dimensions = (3, 4)

        self.tiles: dict[tuple[int, int], Tile] = {}

    def add_tile(self, tile: Tile, position: tuple[int, int]):

        if position in self.tiles:
            raise ValueError("Tile already exists at this position")

        self.tiles[position] = tile

        tile.board = self
        tile.position = position

    def get_tile(self, position: tuple[int, int]) -> Tile | None:
        return self.tiles.get(position)

class BoardRenderer:
    TILE_SIZE = 300
    ANCHOR_RADIUS = 50

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
                    area_origin_px = area.anchor_origin[0] * self.TILE_SIZE
                    area_origin_py = area.anchor_origin[1] * self.TILE_SIZE
                    draw.circle((area_origin_px, area_origin_py), 5, "black")
                    draw.circle((area_origin_px, area_origin_py), self.ANCHOR_RADIUS)
                    draw.text((area_origin_px - 15, area_origin_py - 15), text=str(area.position), fill="black")
            canvas.paste(img, (px, py))

        return canvas





