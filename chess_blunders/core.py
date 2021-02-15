import asyncio
import io
import logging
import multiprocessing
import os
from math import exp
from typing import List, Optional, Union

import chess
import chess.engine
import chess.pgn
from pydantic import confloat, validate_arguments
from pydantic.types import PositiveFloat, PositiveInt

from .models import Blunder, Color, Game

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
DEFAULT_ENGINE = os.environ["CHESS_BLUNDERS_ENGINE"]
MATE_SCORE = 100_000


async def analyse_position(
    fen: str,
    color: Color,
    engine: chess.engine.Protocol,
    *,
    nodes: int,
    logistic_scale: float = 0.004,
    clear_hash: bool = True,
) -> chess.engine.InfoDict:
    """
    Return the centi-pawn score and probability of winning at a given FEN position.

    Args:
        fen: FEN position.
        color: `white` or `black`. Point of view used to score.
        engine: UCI or XBoard engine.
        nodes: number of nodes to explore.
        logisitic_scale: scaling factor of the logistic transform.
        clear_hash: ``True`` to clear the engine's hash table before running
            the analysis. This helps make results more deterministic.

    Notes:
        default logistic scale from
        https://lichess.org/blog/WFvLpiQAACMA8e9D/learn-from-your-mistakes

    Returns:
        a dictionary of information on the position returned by the engine, augmented
        with the ``win_probability`` and ``pov_score`` keys.
    """
    if clear_hash:  # pragma: no branch
        engine._ucinewgame()
    board = chess.Board(fen)
    solution = await engine.analyse(
        board,
        chess.engine.Limit(nodes=nodes),
        info=(chess.engine.INFO_SCORE | chess.engine.INFO_PV),
    )
    solution["pov_score"] = getattr(solution["score"], color)().score(
        mate_score=MATE_SCORE
    )
    solution["win_probability"] = 1 / (1 + exp(-logistic_scale * solution["pov_score"]))

    return solution


@validate_arguments
async def blunders(
    games: Union[Game, List[Game]],
    *,
    threshold: confloat(gt=0, lt=1) = 0.25,  # type: ignore
    colors: Union[Color, List[Color]] = Color.white,
    nodes: PositiveInt = 500_000,
    max_variation_plies: Optional[PositiveInt] = None,
    logistic_scale: PositiveFloat = 0.004,
    engine_options: Optional[dict] = {"Hash": 256, "Threads": 1},
    engine_path: Optional[str] = None,
    n_engines: int = 1,
) -> List[Blunder]:
    """
    Return all the blunders in a list of games.

    Args:
        games: list of chess game data model.
        threshold: threshold of probability-of-winning loss to be considered a blunder.
        colors: for each game, the color we monitor for blunders. `white` or `black`.
        nodes: number of nodes to explore.
        max_variation_plies: maximum number of plies in the refutations and solutions.
        logistic_scale: scale (a.k.a growth rate) of the logistic curve used to convert
            centi-pawn scores to probabilities-of-winning.
        engine_options: options passed to the UCI or XBoard engine.
        engine_path: path to the UCI or XBoard engine.
        n_engines: number of concurrent engines to use to analyze the position.
            Use -1 to use create as many engines are there as CPUs, -2 to use all but
            one CPUs, ...

    Returns:
        list of blunders data models.
    """
    if isinstance(games, Game):
        games = [games]
    if isinstance(colors, Color):
        colors = [colors] * len(games)
    if len(colors) != len(games):
        msg = "`games` and `colors` must have the same length."
        raise ValueError(msg)
    if n_engines < 0:
        n_engines = multiprocessing.cpu_count() + (n_engines + 1)
    engine_path = engine_path or DEFAULT_ENGINE

    scores: dict = {i: {} for i in range(len(games))}

    async def scorer(queue: asyncio.Queue) -> None:
        """
        Worker that scores positions.
        """
        try:
            _, engine = await chess.engine.popen_uci(engine_path)
            await engine.configure(engine_options)
            while True:
                game_iloc, ply, position = await queue.get()
                scores[game_iloc][ply] = await analyse_position(
                    position,
                    colors[game_iloc],  # type: ignore
                    engine,
                    nodes=nodes,
                    logistic_scale=logistic_scale,
                    clear_hash=True,
                )
                queue.task_done()
        finally:
            await engine.quit()

    # create the fen of each position and push it in the work queue
    positions: asyncio.Queue = asyncio.Queue()
    roots: List[chess.pgn.Game] = []
    for game_iloc, game in enumerate(games):
        board = chess.Board()
        root = chess.pgn.read_game(io.StringIO(game.pgn))
        roots.append(root)
        positions.put_nowait((game_iloc, board.ply(), chess.STARTING_FEN))
        for move in root.mainline_moves():
            board.push(move)
            positions.put_nowait((game_iloc, board.ply(), board.fen()))

    # calculate the score at each position
    workers = [
        asyncio.create_task(scorer(positions))
        for _ in range(min(n_engines, positions.qsize()))
    ]
    await positions.join()
    [worker.cancel() for worker in workers]
    await asyncio.gather(*workers, return_exceptions=True)

    blunders = []

    async def annotate_blunders(queue: asyncio.Queue) -> None:
        """
        Worker that creates blunder objects with solution and refutation lines.
        """
        try:
            _, engine = await chess.engine.popen_uci(engine_path)
            await engine.configure(engine_options)
            while True:
                game_iloc, node = await queue.get()

                ply = node.ply()
                refutation = scores[game_iloc][ply]
                solution = scores[game_iloc][ply - 1]

                solution_score = solution["pov_score"]
                refutation_score = refutation["pov_score"]
                cp_loss = refutation_score - solution_score

                probability_loss = (
                    refutation["win_probability"] - solution["win_probability"]
                )
                node.parent.add_line(
                    [node.move] + refutation["pv"][:max_variation_plies],
                    starting_comment=f"Refutation ({refutation_score})",
                )
                node.parent.add_line(
                    solution["pv"][:max_variation_plies],
                    starting_comment=f"Solution ({solution_score})",
                )
                blunder = Blunder(
                    **{
                        "starting_fen": node.board().fen(),
                        "cp_loss": cp_loss,
                        "probability_loss": probability_loss,
                        "pgn": str(node.parent),
                    }
                )
                blunders.append(blunder)
                queue.task_done()
        finally:
            await engine.quit()

    # look for blunders by the player we're interested in
    blunder_nodes: asyncio.Queue = asyncio.Queue()
    for game_iloc in scores:
        game_scores = scores[game_iloc]
        color = colors[game_iloc]
        color_is_white = color == "white"
        root = roots[game_iloc]
        for ply in range(len(game_scores)):
            if ply == 0:
                continue
            white_is_playing = ply % 2
            is_blunder = (
                game_scores[ply]["win_probability"]
                - game_scores[ply - 1]["win_probability"]
            ) <= -threshold
            if (white_is_playing == color_is_white) and is_blunder:
                node = root
                for _ in range(ply):
                    node = node.next()
                assert node.parent.turn() == {"white": True, "black": False}[color]
                assert node.ply() == ply
                blunder_nodes.put_nowait((game_iloc, node))

    workers = [
        asyncio.create_task(annotate_blunders(blunder_nodes))
        for _ in range(min(n_engines, blunder_nodes.qsize()))
    ]
    await blunder_nodes.join()
    [worker.cancel() for worker in workers]
    await asyncio.gather(*workers, return_exceptions=True)

    return blunders
