from typing import List, Optional

from fastapi import Body

from ..models import Color


class BlunderParameters:
    def __init__(
        self,
        colors: Optional[List[Color]] = None,
        threshold: float = Body(
            0.25,
            gt=0,
            lt=1,
            description=(
                "The threshold for a blunder must be a probability between 0 and 1."
            ),
        ),
        nodes: int = Body(1_000_000),
        max_variation_plies: Optional[int] = Body(None),
        logistic_scale: float = Body(0.004),
        engine_options: Optional[dict] = {"Hash": 256, "Threads": 1},
    ):

        self.threshold = threshold
        self.colors = colors
        self.nodes = nodes
        self.max_variation_plies = max_variation_plies
        self.logistic_scale = logistic_scale
        self.engine_options = engine_options
