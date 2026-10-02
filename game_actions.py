from gamestate import Player, CombatCard, OrderUpgrade, EventCard, EventType


def upgrade_combat_deck(player: Player, purchased_card: CombatCard, card_to_remove: CombatCard):
    if purchased_card not in player.available_combat_upgrades:
        raise ValueError("Combat upgrade not found in upgrade deck.")

    if card_to_remove not in player.combat_deck:
        raise ValueError("Combat card not found in player's combat deck.")

    player.combat_deck.upgrade(card_to_remove, purchased_card)
    player.available_combat_upgrades.remove(purchased_card)
    player.available_combat_upgrades.append(card_to_remove)


def gain_order_upgrade(player: Player, upgrade: OrderUpgrade):
    if upgrade not in player.faction.order_upgrades:
        raise ValueError("Order upgrade not found.")

    if upgrade in player.order_upgrades:
        raise ValueError("Upgrade already purchased.")

    player.order_upgrades.append(upgrade)


def resolve_event(player: Player, event: EventCard):
    if event.type == EventType.TACTIC:
        player.event_deck.return_card(event)

    elif event.type == EventType.SCHEME:
        if player.schemes:
            player.event_deck.return_card(player.schemes.pop())
        player.schemes.append(event)