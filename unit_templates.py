from gamestate import UnitTemplate, UnitType, FactionId

# Space Marines

SCOUT = UnitTemplate(
	name = "Scout",
    long_name = "Scout",
    unit_type = UnitType.GROUND,
    command_level = 0,
    faction = FactionId.SPACE_MARINES,
    combat_value = 1,
    health = 2,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/space_marines/scout.png"
    )

STRIKE_CRUISER = UnitTemplate(
	name = "Strike Cruiser",
    long_name = "Strike Cruiser",
    unit_type = UnitType.SHIP,
    command_level = 0,
    faction = FactionId.SPACE_MARINES,
    combat_value = 2,
    health = 2,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/space_marines/strike_cruiser.png"
    )

SPACE_MARINE = UnitTemplate(
	name = "Space Marine",
    long_name = "Space Marine",
    unit_type = UnitType.GROUND,
    command_level = 1,
    faction = FactionId.SPACE_MARINES,
    combat_value = 2,
    health = 3,
    morale = 3,
    materiel_cost = 3,
    requires_forge = False,
    image_path="units/space_marines/space_marine.png"
    )
    
LAND_RAIDER = UnitTemplate(
	name = "Land Raider",
    long_name = "Land Raider",
    unit_type = UnitType.GROUND,
    command_level = 2,
    faction = FactionId.SPACE_MARINES,
    combat_value = 3,
    health = 4,
    morale = 3,
    materiel_cost = 4,
    requires_forge = False,
    image_path="units/space_marines/land_raider.png"
    )
    
BATTLE_BARGE = UnitTemplate(
	name = "Battle Barge",
    long_name = "Battle Barge",
    unit_type = UnitType.SHIP,
    command_level = 2,
    faction = FactionId.SPACE_MARINES,
    combat_value = 4,
    health = 5,
    morale = 4,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/space_marines/battle_barge.png"
    )    
    
WARLORD_TITAN = UnitTemplate(
	name = "Warlord Titan",
    long_name = "Warlord Titan",
    unit_type = UnitType.GROUND,
    command_level = 3,
    faction = FactionId.SPACE_MARINES,
    combat_value = 3,
    health = 5,
    morale = 4,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/space_marines/warlord_titan.png"
    )    
    
    
# Chaos Space Marines
    
CULTIST = UnitTemplate(
	name = "Cultist",
    long_name = "Cultist",
    unit_type = UnitType.GROUND,
    command_level = 0,
    faction = FactionId.CHAOS,
    combat_value = 1,
    health = 2,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/chaos/cultist.png"
    )

ICONOCLAST_DESTROYER = UnitTemplate(
	name = "Iconoclast",
    long_name = "Iconoclast Destroyer",
    unit_type = UnitType.SHIP,
    command_level = 0,
    faction = FactionId.CHAOS,
    combat_value = 2,
    health = 2,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/chaos/iconoclast.png"
    )

CHAOS_SPACE_MARINE = UnitTemplate(
	name = "Chaos Space Marine",
    long_name = "Chaos Space Marine",
    unit_type = UnitType.GROUND,
    command_level = 1,
    faction = FactionId.CHAOS,
    combat_value = 3,
    health = 3,
    morale = 2,
    materiel_cost = 3,
    requires_forge = False,
    image_path="units/chaos/chaos_space_marine.png"
    )
    
HELBRUTE = UnitTemplate(
	name = "Helbrute",
    long_name = "Helbrute",
    unit_type = UnitType.GROUND,
    command_level = 2,
    faction = FactionId.CHAOS,
    combat_value = 3,
    health = 4,
    morale = 3,
    materiel_cost = 4,
    requires_forge = False,
    image_path="units/chaos/helbrute.png"
    )
    
REPULSIVE_GRAND_CRUISER = UnitTemplate(
	name = "Grand Cruiser",
    long_name = "Repulsive Grand Cruiser",
    unit_type = UnitType.SHIP,
    command_level = 2,
    faction = FactionId.CHAOS,
    combat_value = 4,
    health = 5,
    morale = 4,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/chaos/grand_cruiser.png"
    )    
    
CHAOS_REAVER_TITAN = UnitTemplate(
	name = "Chaos Titan",
    long_name = "Chaos Reaver Titan",
    unit_type = UnitType.GROUND,
    command_level = 3,
    faction = FactionId.CHAOS,
    combat_value = 4,
    health = 5,
    morale = 3,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/chaos/chaos_titan.png"
    )    
    
    
# ORKS
    
ORK_BOYZ = UnitTemplate(
	name = "Ork Boyz",
    long_name = "Ork Boyz",
    unit_type = UnitType.GROUND,
    command_level = 0,
    faction = FactionId.ORKS,
    combat_value = 2,
    health = 2,
    morale = 1,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/orks/ork_boyz.png"
    )

ONSLAUGHT_ATTACK_SHIP = UnitTemplate(
	name = "Onslaught",
    long_name = "Onslaught Attack Ship",
    unit_type = UnitType.SHIP,
    command_level = 0,
    faction = FactionId.ORKS,
    combat_value = 2,
    health = 2,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/orks/onslaught.png"
    )

NOB = UnitTemplate(
	name = "Nob",
    long_name = "Nob",
    unit_type = UnitType.GROUND,
    command_level = 1,
    faction = FactionId.ORKS,
    combat_value = 2,
    health = 4,
    morale = 2,
    materiel_cost = 3,
    requires_forge = False,
    image_path="units/orks/nob.png"
    )
    
BATTLEWAGON = UnitTemplate(
	name = "Battlewagon",
    long_name = "Battlewagon",
    unit_type = UnitType.GROUND,
    command_level = 2,
    faction = FactionId.ORKS,
    combat_value = 3,
    health = 5,
    morale = 2,
    materiel_cost = 4,
    requires_forge = False,
    image_path="units/orks/battlewagon.png"
    )
    
KILL_KROOZER = UnitTemplate(
	name = "Kill Kroozer",
    long_name = "Kill Kroozer",
    unit_type = UnitType.SHIP,
    command_level = 2,
    faction = FactionId.ORKS,
    combat_value = 3,
    health = 6,
    morale = 4,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/orks/kill_kroozer.png"
    )    
    
GARGANT = UnitTemplate(
	name = "Gargant",
    long_name = "Gargant",
    unit_type = UnitType.GROUND,
    command_level = 3,
    faction = FactionId.ORKS,
    combat_value = 3,
    health = 6,
    morale = 3,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/orks/gargant.png"
    )    
    
    
 # ELDAR
    
ASPECT_WARRIOR = UnitTemplate(
	name = "Aspect Warrior",
    long_name = "Aspect Warrior",
    unit_type = UnitType.GROUND,
    command_level = 0,
    faction = FactionId.ELDAR,
    combat_value = 2,
    health = 1,
    morale = 2,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/eldar/aspect_warrior.png"
    )

HELLEBORE_FRIGATE = UnitTemplate(
	name = "Frigate",
    long_name = "Hellebore Frigate",
    unit_type = UnitType.SHIP,
    command_level = 0,
    faction = FactionId.ELDAR,
    combat_value = 3,
    health = 2,
    morale = 1,
    materiel_cost = 2,
    requires_forge = False,
    image_path="units/eldar/frigate.png"
    )

WRAITHGUARD = UnitTemplate(
	name = "Wraithguard",
    long_name = "Wraithguard",
    unit_type = UnitType.GROUND,
    command_level = 1,
    faction = FactionId.ELDAR,
    combat_value = 2,
    health = 4,
    morale = 2,
    materiel_cost = 3,
    requires_forge = False,
    image_path="units/eldar/wraithguard.png"
    )
    
FALCON = UnitTemplate(
	name = "Falcon",
    long_name = "Falcon",
    unit_type = UnitType.GROUND,
    command_level = 2,
    faction = FactionId.ELDAR,
    combat_value = 3,
    health = 4,
    morale = 3,
    materiel_cost = 4,
    requires_forge = False,
    image_path="units/eldar/falcon.png"
    )
    
VOID_STALKER = UnitTemplate(
	name = "Void Stalker",
    long_name = "Void Stalker",
    unit_type = UnitType.SHIP,
    command_level = 2,
    faction = FactionId.ELDAR,
    combat_value = 4,
    health = 5,
    morale = 4,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/eldar/void_stalker.png"
    )    
    
WARLOCK_BATTLE_TITAN = UnitTemplate(
	name = "Warlock Titan",
    long_name = "Warlock Battle Titan",
    unit_type = UnitType.GROUND,
    command_level = 3,
    faction = FactionId.ELDAR,
    combat_value = 4,
    health = 5,
    morale = 3,
    materiel_cost = 5,
    requires_forge = True,
    image_path="units/eldar/warlock_titan.png"
    )    


ALL_UNITS = [SCOUT, STRIKE_CRUISER, SPACE_MARINE, LAND_RAIDER, BATTLE_BARGE, WARLORD_TITAN,
             CULTIST, ICONOCLAST_DESTROYER, CHAOS_SPACE_MARINE, HELBRUTE, REPULSIVE_GRAND_CRUISER, CHAOS_REAVER_TITAN,
             ORK_BOYZ, ONSLAUGHT_ATTACK_SHIP, NOB, BATTLEWAGON, KILL_KROOZER, GARGANT,
             ASPECT_WARRIOR, HELLEBORE_FRIGATE, WRAITHGUARD, FALCON, VOID_STALKER, WARLOCK_BATTLE_TITAN]