from dataclasses import dataclass

@dataclass
class Player:

    level: int = 1
    health: int = 10
    max_health: int = 10
    gold: int = 9
    floor: int = 1
    pos: tuple[int] = (1,1)
    char: str = '@'

    def __post_init__(self):
        if self.pos is None:
            self.pos = [1,1]

        if len(self.char) != 1:
            raise ValueError("player.char must be length 1")