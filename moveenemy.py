from gamestate import GameState

def move_enemy(state: GameState):
    py, px = state.player.pos
    ey, ex = state.enemy_pos
    spike_pos = state.spike_pos

    def move():
        if new_pos == (py, px):
            state.enemy_pos = None
            state.player.health -= 5
            return
        
        if new_pos == spike_pos:
            state.enemy_pos = None
            state.player.level += 1
            return
        
        if new_pos in state.occupied_coords:
            return
        
        state.enemy_pos = new_pos

    if abs(py - ey) >= abs(px - ex):
        if py > ey:
            new_pos = (ey + 1, ex)
            move()
        else:
            new_pos = (ey - 1, ex)
            move()
    else:
        if px > ex:
            new_pos = (ey, ex + 1)
            move()
        else:
            new_pos = (ey, ex - 1)
            move()