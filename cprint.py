from gamestate import GameState

def c_print(state: GameState, msg: str):
    state.console.append(msg)