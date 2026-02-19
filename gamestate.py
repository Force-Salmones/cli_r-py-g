from player import Player
from dataclasses import dataclass,field

@dataclass
class GridSize:
    height: int
    width: int

@dataclass
class GameState:

    grid: list[str]
    grid_size: GridSize = field(init=False)

    occupied_coords: list[tuple[int,int]] = field(default_factory=list)

    player: Player = field(default_factory=Player)

    gold_pos: tuple[int,int] = (1,2)
    gold_char: str = 'o'

    stairs_pos: tuple[int,int] | None = None
    stairs_char: str = '◢'

    spike_pos: tuple[int,int] | None = None
    spike_char: str = '^'

    enemy_pos: tuple[int,int] | None = None
    enemy_char: str = '¤'

    def __post_init__(self):
        self.grid_size = GridSize(
            height = len(self.grid) - 2,
            width = len(self.grid[1]) - 2
        )

        self.occupied_coords.append(self.player.pos)
        self.occupied_coords.append(self.gold_pos)

        if len(self.gold_char) != 1:
            raise ValueError("gold_char must be length 1")
        if len(self.stairs_char) != 1:
            raise ValueError("stairs_char must be length 1")
        if len(self.spike_char) != 1:
            raise ValueError("spike_char must be length 1")
        if len(self.enemy_char) != 1:
            raise ValueError("enemy_char must be length 1")