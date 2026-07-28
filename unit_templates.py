# Space Marines

SCOUT = UnitTemplate(name = "Scout",
    long_name = "Scout",
    unit_type = UnitType.GROUND,
    command_level = 0,
    faction = FactionId.SPACE_MARINES,
    combat_value = 1,
    health = 2,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False
    )

STRIKE_CRUISER = UnitTemplate(name = "Strike Cruiser",
    long_name = "Strike Cruiser",
    unit_type = UnitType.SHIP,
    command_level = 0,
    faction = FactionId.SPACE_MARINES,
    combat_value = 2,
    health = 2,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False
    )

SPACE_MARINE = UnitTemplate(name = "Space Marine",
    long_name = "Space Marine",
    unit_type = UnitType.GROUND,
    command_level = 1,
    faction = FactionId.SPACE_MARINES,
    combat_value = 2,
    health = 3,
    morale = 3,
    materiel_cost = 3,
    requires_forge = False
    )
    
LAND_RAIDER = UnitTemplate(name = "Land Raider",
    long_name = "Land Raider",
    unit_type = UnitType.GROUND,
    command_level = 2,
    faction = FactionId.SPACE_MARINES,
    combat_value = 3,
    health = 4,
    morale = 3,
    materiel_cost = 4,
    requires_forge = False
    )
    
BATTLE_BARGE = UnitTemplate(name = "Battle Barge",
    long_name = "Battle Barge",
    unit_type = UnitType.SHIP,
    command_level = 2,
    faction = FactionId.SPACE_MARINES,
    combat_value = 4,
    health = 5,
    morale = 4,
    materiel_cost = 5,
    requires_forge = True
    )    
    
WARLORD_TITAN = UnitTemplate(name = "Warlord Titan",
    long_name = "Warlord Titan",
    unit_type = UnitType.GROUND,
    command_level = 3,
    faction = FactionId.SPACE_MARINES,
    combat_value = 3,
    health = 5,
    morale = 4,
    materiel_cost = 5,
    requires_forge = True
    )    
    
    
# Chaos Space Marines
    
