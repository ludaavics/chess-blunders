from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Player(BaseModel):
    username: str
    url: str
    rating: int


class PlayerPlaying(Player):
    result: str


class SideEnum(str, Enum):
    white = "white"
    black = "back"


class Game(BaseModel):
    url: Optional[str]
    white: PlayerPlaying
    black: PlayerPlaying
    pgn: str
    fen: str
    start_time: Optional[int]
    end_time: int
    time_control: str
    rules: str
    eco_url: Optional[str]
    tournament_url: Optional[str]
    match_url: Optional[str]


class BlunderThreshold(BaseModel):
    threshold: float = Field(
        0.1,
        gt=0,
        lt=1,
        description=(
            "The threshold for a blunder must be a probability between 0 and 1."
        ),
    )


class Line(BaseModel):
    starting_fen: str
    pgn: str


class Blunder(Line):
    cp_loss: float = Field(
        ..., gt=0, description="The centipawn loss must be greater than 0."
    )
    probability_loss: float = Field(
        ...,
        gt=0,
        lt=1,
        description="The winning probability loss must be between 0 and 1.",
    )
