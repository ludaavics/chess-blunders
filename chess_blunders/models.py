from typing import Optional

from pydantic import BaseModel, Field


class Player(BaseModel):
    name: str
    rating: int
    url: str


class PlayerPlaying(Player):
    result: str


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
        0.25,
        gt=0,
        lt=1,
        description=(
            "The threshold for a blunder must be a probability between 0 and 1."
        ),
    )


class Tactic(BaseModel):
    starting_fen: str
    pgn: str


class Blunder(Tactic):
    cp_loss: float = Field(
        ..., lt=0, description="The centipawn loss must be greater than 0."
    )
    probability_loss: float = Field(
        ...,
        gt=-1,
        lt=0,
        description="The probability-of-winning loss must be between -1 and 0.",
    )
