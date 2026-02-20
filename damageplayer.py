from gamestate import GameState

def damage_player(state: GameState, amount: int):
    result = state.player.health + amount
    state.player.health = max(0, min(result, state.player.max_health))