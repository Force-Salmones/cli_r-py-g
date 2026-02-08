import curses
import random
from gamestate import GameState
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
            if new_coords != cur_coords and new_coords != state.player.pos:
                return new_coords

    def handle_input(state,key):
        if key == ord('Q'):
            sys.exit()
        elif key == curses.KEY_UP:
            if state.player.pos[0] > 1:
                state.player.pos = (state.player.pos[0] - 1, state.player.pos[1])
        elif key == curses.KEY_DOWN:
            if state.player.pos[0] < state.grid_size.height:
                state.player.pos = (state.player.pos[0] + 1, state.player.pos[1])
        elif key == curses.KEY_RIGHT:
            if state.player.pos[1] < state.grid_size.width:
                state.player.pos = (state.player.pos[0], state.player.pos[1] + 1)
        elif key == curses.KEY_LEFT:
            if state.player.pos[1] > 1:
                state.player.pos = (state.player.pos[0], state.player.pos[1] - 1)


    def draw_game():
        stdscr.erase()
        for y,row in enumerate(grid):
            #draw grid
            stdscr.addstr(y + GRID_Y_OFFSET,0,row)

            #draw player
            stdscr.addstr(state.player.pos[0] + GRID_Y_OFFSET,state.player.pos[1],state.player.char)

            #draw gold
            stdscr.addstr(state.gold_pos[0] + GRID_Y_OFFSET,state.gold_pos[1], state.gold_char)

            #draw stairs
            if state.player.gold >= state.player.floor * 10:
                stdscr.addstr(state.stairs_pos[0] + GRID_Y_OFFSET,state.stairs_pos[1], state.stairs_char)

            #draw ui
            ui = [
            "-------------------------",
            f"  Lv:{state.player.level}  Gold:{state.player.gold}  Floor:{state.player.floor}",
            "-------------------------"
            ]
            stdscr.addstr(state.grid_size.height+3,0,ui[0])
            stdscr.addstr(state.grid_size.height+4,0,ui[1])
            stdscr.addstr(state.grid_size.height+5,0,ui[2])

            stdscr.refresh()
    
    def new_floor(state: GameState):
        state.player.pos = move_object([],state)
        state.gold_pos = move_object([],state)

    state.gold_pos = move_object(None,state)
    draw_game()

    while True:
        #input handling
        key = stdscr.getch()
        handle_input(state,key)
        
            #move gold if touched
        if state.player.pos == state.gold_pos:
            state.player.gold += 1
            state.gold_pos = move_object(state.gold_pos,state)

            #spawn stairs conditionally
        if state.player.gold >= state.player.floor * 10 and not state.stairs_pos:
            state.stairs_pos = move_object([],state)

            #check for stairs collision
        if state.player.pos == state.stairs_pos:
            state.player.floor += 1
            new_floor(state)
            state.stairs_pos = []

        draw_game()

curses.wrapper(main)