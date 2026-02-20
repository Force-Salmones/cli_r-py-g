import curses
import random
from collections import deque
from gamestate import GameState
from moveenemy import move_enemy
from damageplayer import damage_player
from cprint import c_print
import sys

def main(stdscr):

    curses.curs_set(0)
    stdscr.erase()
    stdscr.keypad(True)
    stdscr.scrollok(False)

    grid = [
    "#########################",
    "#.......................#",
    "#.......................#",
    "#.......................#",
    "#.......................#",
    "#.......................#",
    "#.......................#",
    "#.......................#",
    "#########################"
    ]

    state = GameState(grid)
    GRID_Y_OFFSET = 1

    def move_object(cur_coords,state: GameState):
        new_coords = []
        while True:
            new_coords = (
                random.randint(1,state.grid_size.height), 
                random.randint(1,state.grid_size.width)
            )
            if new_coords != cur_coords:
                if cur_coords in state.occupied_coords:
                    state.occupied_coords.remove(cur_coords)
                state.occupied_coords.append(new_coords)
                return new_coords

    def remove_object(cur_coords,state: GameState):
        if cur_coords in state.occupied_coords:
            state.occupied_coords = [None if x == cur_coords else x for x in state.occupied_coords]

    def handle_input(state: GameState,key):
        
        new_pos = None

        if key == ord('Q'):
            sys.exit()
        elif key == curses.KEY_UP:
            if state.player.pos[0] > 1:
                new_pos = (state.player.pos[0] - 1, state.player.pos[1])
        elif key == curses.KEY_DOWN:
            if state.player.pos[0] < state.grid_size.height:
                new_pos = (state.player.pos[0] + 1, state.player.pos[1])
        elif key == curses.KEY_RIGHT:
            if state.player.pos[1] < state.grid_size.width:
                new_pos = (state.player.pos[0], state.player.pos[1] + 1)
        elif key == curses.KEY_LEFT:
            if state.player.pos[1] > 1:
                new_pos = (state.player.pos[0], state.player.pos[1] - 1)
        else:
            return
        if new_pos == state.spike_pos or not new_pos:
            return
        if new_pos == state.enemy_pos:
            dmg = (state.player.floor * -1 + 1)-5
            damage_player(state, dmg)
            state.enemy_pos = None
            remove_object(state.enemy_pos,state)
            c_print(state,f"The enemy deaks {dmg} damage to you.")
        state.player.pos = new_pos

    def draw_game():
        stdscr.erase()
        for y,row in enumerate(grid):
            #draw grid
            stdscr.addstr(y + GRID_Y_OFFSET,0,row)

            #draw player
            stdscr.addstr(state.player.pos[0] + GRID_Y_OFFSET,state.player.pos[1],state.player.char)

            #draw gold
            stdscr.addstr(state.gold_pos[0] + GRID_Y_OFFSET,state.gold_pos[1], state.gold_char)

            #draw enemy
            if state.enemy_pos:
                stdscr.addstr(state.enemy_pos[0] + GRID_Y_OFFSET,state.enemy_pos[1], state.enemy_char)

            #draw stairs
            if state.player.gold >= state.player.floor * 10:
                stdscr.addstr(state.stairs_pos[0] + GRID_Y_OFFSET,state.stairs_pos[1], state.stairs_char)

            #draw spike
            if state.player.floor > 1:
                stdscr.addstr(state.spike_pos[0] + GRID_Y_OFFSET,state.spike_pos[1], state.spike_char)

            #draw ui
            ui = [
            "-------------------------",
            f"  Lv:{state.player.level}  Gold:{state.player.gold}  Floor:{state.player.floor}",
            "-------------------------",
            f"  Health:{state.player.health}/{state.player.max_health}",
            "-------------------------"
            ]
            
            for i in range(0,len(ui)):
                stdscr.addstr(state.grid_size.height+(i+3),0,ui[i])

            #draw console
            for i, line in enumerate(reversed(state.console)):
                stdscr.addstr(state.grid_size.height+(i+len(ui)+3),0,line)

            stdscr.refresh()
    
    def new_floor(state: GameState):
        state.player.pos = move_object(state.player.pos,state)
        state.gold_pos = move_object(state.gold_pos,state)
        state.enemy_pos = move_object(state.enemy_pos,state)
        remove_object(state.spike_pos,state)
        remove_object(state.stairs_pos,state)
        state.spike_pos = move_object(None,state)

    state.gold_pos = move_object(None,state)
    draw_game()

    while True:
        #input handling
        key = stdscr.getch()
        handle_input(state,key)
        
            #move gold if touched
        if state.player.pos == state.gold_pos:
            state.player.gold += 1
            damage_player(state, 1)
            state.gold_pos = move_object(state.gold_pos,state)

            #spawn stairs conditionally
        if state.player.gold >= state.player.floor * 10 and not state.stairs_pos:
            c_print(state, "The path to the next floor has appeared!")
            state.stairs_pos = move_object(None,state)

            #check for stairs collision
        if state.player.pos == state.stairs_pos:
            state.player.floor += 1
            new_floor(state)
            state.stairs_pos = []

        if state.enemy_pos and random.randint(1,11 - state.player.floor) < 3:
            move_enemy(state)

        draw_game()

curses.wrapper(main)