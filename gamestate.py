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

    player: Player = field(default_factory=Player)

    gold_pos: tuple[int,int] = (1,1)
    gold_char: str = 'o'

    stairs_pos: tuple[int,int] | None = None
    stairs_char: str = '◢'

    def __post_init__(self):
        self.grid_size = GridSize(
            height = len(self.grid) - 2,
            width = len(self.grid[1]) - 2
        )

        if len(self.gold_char) != 1:
            raise ValueError("gold_char must be length 1")
        if len(self.stairs_char) != 1:
            raise ValueError("stairs_char must be length 1")