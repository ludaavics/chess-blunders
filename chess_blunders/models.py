from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ------------------------------------------------------------------------------------ #
#                                         Games                                        #
# ------------------------------------------------------------------------------------ #
class Source(str, Enum):
    chessdotcom = "chess.com"


class Color(str, Enum):
    white = "white"
    black = "black"


class Player(BaseModel):
    name: str
    url: str


class PlayerInGame(Player):
    rating: int
    result: str


class Game(BaseModel):
    url: Optional[str]
    white: PlayerInGame
    black: PlayerInGame
    pgn: str
    fen: str
    start_time: Optional[int]
    end_time: int
    time_control: str
    rules: str
    eco_url: Optional[str]
    tournament_url: Optional[str]
    match_url: Optional[str]


# ------------------------------------------------------------------------------------ #
#                                        Puzzles                                       #
# ------------------------------------------------------------------------------------ #
class Puzzle(BaseModel):
    starting_fen: str
    pgn: str


class Blunder(Puzzle):
    cp_loss: float = Field(
        ..., lt=0, description="The centipawn loss must be greater than 0."
    )
    probability_loss: float = Field(
        ...,
        gt=-1,
        lt=0,
        description="The probability-of-winning loss must be between -1 and 0.",
    )
