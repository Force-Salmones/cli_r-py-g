import curses

def main(stdscr):

    curses.curs_set(0)
    stdscr.erase()
    stdscr.keypad(True)
    stdscr.scrollok(False)

    grid = [
        "#######",
        "#.....#",
        "#.....#",
        "#.....#",
        "#.....#",
        "#.....#",
        "#######"
    ]

    player_char = '@'
    player_pos = [1,1]
    grid_height = 5
    grid_width = 5
    GRID_Y_OFFSET = 1

    while True:
        for y,row in enumerate(grid):
            stdscr.addstr(y + GRID_Y_OFFSET,0,row)
            stdscr.addstr(player_pos[1] + GRID_Y_OFFSET,player_pos[0],player_char)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('Q'):
            break
        elif key == curses.KEY_UP:
            if player_pos[1] > 1:
                player_pos[1] -= 1
        elif key == curses.KEY_DOWN:
            if player_pos[1] < grid_height:
                player_pos[1] += 1
        elif key == curses.KEY_RIGHT:
            if player_pos[0] < grid_width:
                player_pos[0] += 1
        elif key == curses.KEY_LEFT:
            if player_pos[0] > 1:
                player_pos[0] -= 1

curses.wrapper(main)