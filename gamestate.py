from __future__ import annotations
from dataclasses import dataclass
import random


class Asset: pass
class CombatDeck: pass
class Tile: pass

class Player:
    def __init__(self, name: str, faction: Faction, index: int):
        self.name = name
        self.faction = faction
        self.index = index

        self.starting_units = dict(self.faction.starting_units)
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

@dataclass(frozen=True)
class UnitTemplate:
    name: str
    long_name: str
    unit_type: str
    command_level: int
    offence: int
    health: int
    morale: int

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
        drawn_cards = [self.cards.pop() for _ in range(number_of_cards)]
        return drawn_cards

    def return_card(self, card: EventCard):
        self.cards.append(card)
        self.shuffle()

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
