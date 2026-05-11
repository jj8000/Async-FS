from __future__ import annotations
from dataclasses import dataclass
import random
from enum import Enum


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

        self.units = {}
        self.structures = {}
        self.objective_token = None

    @property
    def capacity(self):
        return self.template.capacity

    @property
    def area_type(self):
        return self.template.area_type

@dataclass(frozen=True)
class TileTemplate:
    id: str
    image_path: str
    areas: list[AreaTemplate]
    is_faction_tile: bool

class Tile:
    def __init__(self, template: TileTemplate, rotation: int = 0):
        self.template = template
        self.rotation = rotation

        self.areas = [Area(t) for t in self.template.areas]

        for area in self.areas:
            area.tile = self



