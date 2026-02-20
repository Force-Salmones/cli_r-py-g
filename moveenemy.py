from gamestate import GameState
from damageplayer import damage_player
from cprint import c_print

def move_enemy(state: GameState):
    py, px = state.player.pos
    ey, ex = state.enemy_pos
    spike_pos = state.spike_pos

    def move():
        if new_pos == (py, px):
            dmg = (state.player.floor * -1 + 1)-5
            state.enemy_pos = None
            damage_player(state, dmg)
            c_print(state,f"The enemy deaks {dmg} damage to you.")
            return
        
        if new_pos == spike_pos:
            state.enemy_pos = None
            state.player.level += 1
            state.player.max_health += 5
            c_print(state, "Level up! Max health increased.")
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