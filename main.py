import curses
import random


def main(stdscr):

    def move_gold(cur_coords,grid_y,grid_x):
        new_coords = []
        while True:
            new_coords = [
                random.randint(1,grid_y), 
                random.randint(1,grid_x)
                ]
            if new_coords != cur_coords:
                return new_coords

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

    player_level = 1
    player_gold = 0
    player_floor = 1
    player_char = '@'
    player_pos = [1,1] #y, x
    grid_height = len(grid) - 2
    grid_width = len(grid[1]) - 2
    GRID_Y_OFFSET = 1
    gold_char = 'o'
    gold_pos = move_gold(None,grid_height,grid_width)

    while True:
        for y,row in enumerate(grid):
            #grid
            stdscr.addstr(y + GRID_Y_OFFSET,0,row)

            #player
            stdscr.addstr(player_pos[0] + GRID_Y_OFFSET,player_pos[1],player_char)

            #gold
            stdscr.addstr(gold_pos[0] + GRID_Y_OFFSET,gold_pos[1], gold_char)

            #ui
            ui = [
        "-------------------------",
        f"  Lv:{player_level}  Gold:{player_gold}  Floor:{player_floor}",
        "-------------------------"
    ]
            stdscr.addstr(grid_height+3,0,ui[0])
            stdscr.addstr(grid_height+4,0,ui[1])
            stdscr.addstr(grid_height+5,0,ui[2])

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('Q'):
            break
        elif key == curses.KEY_UP:
            if player_pos[0] > 1:
                player_pos[0] -= 1
        elif key == curses.KEY_DOWN:
            if player_pos[0] < grid_height:
                player_pos[0] += 1
        elif key == curses.KEY_RIGHT:
            if player_pos[1] < grid_width:
                player_pos[1] += 1
        elif key == curses.KEY_LEFT:
            if player_pos[1] > 1:
                player_pos[1] -= 1

        if player_pos == gold_pos:
            player_gold += 1
            gold_pos = move_gold(gold_pos,grid_height,grid_width)

curses.wrapper(main)