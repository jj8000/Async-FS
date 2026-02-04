from __future__ import annotations
from dataclasses import dataclass

class Asset: pass
class CombatDeck: pass
class CombatCard: pass
class OrderUpgrade: pass
class EventDeck: pass
class EventCard: pass
class Tile: pass

@dataclass
class Player:
    name: str
    faction: Faction
    index: int

@dataclass
class Faction:
    name: str
    ability: str
    starting_units: dict[UnitTemplate, int]
    available_units: dict[UnitTemplate, int]
    starting_assets: dict[Asset, int]
    starting_materiel: int
    starting_combat_deck: CombatDeck
    combat_upgrades: list[CombatCard]
    order_upgrades: list[OrderUpgrade]
    event_deck: EventDeck
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
    def __init__(self, players, turn_order): pass





