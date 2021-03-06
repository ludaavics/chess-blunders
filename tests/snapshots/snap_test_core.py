# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_known_blunders[0-False] 1"] = [
    {
        "cp_loss": -821.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.01.03"]
[Round "-"]
[White "Cuervo_Ingenuo"]
[Black "ludavics"]
[Result "1-0"]
[BlackElo "1093"]
[CurrentPosition "3r2k1/5ppp/1pR5/1Q6/8/P3P3/5PPP/2RqB1K1 b - -"]
[ECO "D32"]
[ECOUrl "https://www.chess.com/openings/Tarrasch-Defense-4.e3"]
[EndDate "2021.01.03"]
[EndTime "01:13:31"]
[FEN "3r1rk1/5ppp/1pR5/1Q6/1B6/P3P3/qP3PPP/2R3K1 b - - 2 26"]
[Link "https://www.chess.com/live/game/6127697792"]
[SetUp "1"]
[StartTime "01:06:03"]
[Termination "Cuervo_Ingenuo won on time"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.01.03"]
[UTCTime "01:06:03"]
[WhiteElo "1114"]

26... Qxb2 27. Qc4 ( { Refutation (-0.47 vs. 7.74 in solution) } 27. Bxf8 Qxb5 ) 1-0""",
        "probability_loss": -0.5035895039665865,
        "refutations": [[("b4", "f8"), ("b2", "b5")]],
        "solution": [("b5", "c4")],
        "starting_fen": "3r1rk1/5ppp/1pR5/1Q6/1B6/P3P3/qP3PPP/2R3K1 b - - 2 26",
    }
]

snapshots["test_known_blunders[games_loc1-True] 1"] = [
    {
        "cp_loss": -507.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.01.03"]
[Round "-"]
[White "ludavics"]
[Black "fabio_srj"]
[Result "0-1"]
[BlackElo "1176"]
[CurrentPosition "8/2b3pk/7p/3P4/8/7P/5PP1/4r1K1 w - -"]
[ECO "C40"]
[ECOUrl "https://www.chess.com/openings/Kings-Pawn-Opening-Kings-Knight-Busch-Gass-Gambit"]
[EndDate "2021.01.03"]
[EndTime "01:21:41"]
[FEN "rb3r1k/1p4p1/pP2Q2p/1PP1p2q/3N4/3P4/3N1PPP/R4RK1 b - - 0 22"]
[Link "https://www.chess.com/live/game/6127740086"]
[SetUp "1"]
[StartTime "01:13:38"]
[Termination "fabio_srj won by checkmate"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.01.03"]
[UTCTime "01:13:38"]
[WhiteElo "1087"]

22... exd4 23. g3 ( { Refutation (0.69 vs. 5.76 in solution) } 23. Nf3 Rxf3 ) 0-1""",
        "probability_loss": -0.3406424768115154,
        "refutations": [[("d2", "f3"), ("f8", "f3")]],
        "solution": [("g2", "g3")],
        "starting_fen": "rb3r1k/1p4p1/pP2Q2p/1PP1p2q/3N4/3P4/3N1PPP/R4RK1 b - - 0 22",
    },
    {
        "cp_loss": -536.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.01.03"]
[Round "-"]
[White "ludavics"]
[Black "fabio_srj"]
[Result "0-1"]
[BlackElo "1176"]
[CurrentPosition "8/2b3pk/7p/3P4/8/7P/5PP1/4r1K1 w - -"]
[ECO "C40"]
[ECOUrl "https://www.chess.com/openings/Kings-Pawn-Opening-Kings-Knight-Busch-Gass-Gambit"]
[EndDate "2021.01.03"]
[EndTime "01:21:41"]
[FEN "1r3r1k/1P4p1/R1P3qp/8/2Qp1b2/3P1N1P/5PP1/5RK1 b - - 0 29"]
[Link "https://www.chess.com/live/game/6127740086"]
[SetUp "1"]
[StartTime "01:13:38"]
[Termination "fabio_srj won by checkmate"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.01.03"]
[UTCTime "01:13:38"]
[WhiteElo "1087"]

29... Bc7 30. Nxd4 ( { Refutation (1.87 vs. 7.23 in solution) } 30. Qxd4 Rxf3 ) 0-1""",
        "probability_loss": -0.2687067954177095,
        "refutations": [[("c4", "d4"), ("f8", "f3")]],
        "solution": [("f3", "d4")],
        "starting_fen": "1r3r1k/1P4p1/R1P3qp/8/2Qp1b2/3P1N1P/5PP1/5RK1 b - - 0 29",
    },
    {
        "cp_loss": -874.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.01.03"]
[Round "-"]
[White "ludavics"]
[Black "fabio_srj"]
[Result "0-1"]
[BlackElo "1176"]
[CurrentPosition "8/2b3pk/7p/3P4/8/7P/5PP1/4r1K1 w - -"]
[ECO "C40"]
[ECOUrl "https://www.chess.com/openings/Kings-Pawn-Opening-Kings-Knight-Busch-Gass-Gambit"]
[EndDate "2021.01.03"]
[EndTime "01:21:41"]
[FEN "1R3r1k/1Pb3p1/2P3qp/8/3Q4/3P3P/5PP1/5RK1 b - - 0 32"]
[Link "https://www.chess.com/live/game/6127740086"]
[SetUp "1"]
[StartTime "01:13:38"]
[Termination "fabio_srj won by checkmate"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.01.03"]
[UTCTime "01:13:38"]
[WhiteElo "1087"]

32... Rxb8 33. Qd7 ( { Refutation (-2.24 vs. 6.5 in solution) } 33. Qa7 Qxc6 ) 0-1""",
        "probability_loss": -0.6409883879613829,
        "refutations": [[("d4", "a7"), ("g6", "c6")]],
        "solution": [("d4", "d7")],
        "starting_fen": "1R3r1k/1Pb3p1/2P3qp/8/3Q4/3P3P/5PP1/5RK1 b - - 0 32",
    },
    {
        "cp_loss": -99754.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.01.03"]
[Round "-"]
[White "ludavics"]
[Black "fabio_srj"]
[Result "0-1"]
[BlackElo "1176"]
[CurrentPosition "8/2b3pk/7p/3P4/8/7P/5PP1/4r1K1 w - -"]
[ECO "C40"]
[ECOUrl "https://www.chess.com/openings/Kings-Pawn-Opening-Kings-Knight-Busch-Gass-Gambit"]
[EndDate "2021.01.03"]
[EndTime "01:21:41"]
[FEN "4R3/1r4pk/7p/b7/3P4/7P/5PP1/6K1 b - - 0 38"]
[Link "https://www.chess.com/live/game/6127740086"]
[SetUp "1"]
[StartTime "01:13:38"]
[Termination "fabio_srj won by checkmate"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.01.03"]
[UTCTime "01:13:38"]
[WhiteElo "1087"]

38... Bc7 39. g3 ( { Refutation (-999.98 vs. -2.44 in solution) } 39. d5 Rb1+ ) 0-1""",
        "probability_loss": -0.273686191698313,
        "refutations": [[("d4", "d5"), ("b7", "b1")]],
        "solution": [("g2", "g3")],
        "starting_fen": "4R3/1r4pk/7p/b7/3P4/7P/5PP1/6K1 b - - 0 38",
    },
    {
        "cp_loss": -278.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.01.03"]
[Round "-"]
[White "mhughes127"]
[Black "ludavics"]
[Result "0-1"]
[BlackElo "1096"]
[CurrentPosition "r4rk1/1b3p1p/p3p1p1/6Nn/1p1N4/3B4/PP1Q1PqP/R4RK1 w - -"]
[ECO "B50"]
[ECOUrl "https://www.chess.com/openings/Sicilian-Defense-Delayed-Alapin-Variation"]
[EndDate "2021.01.03"]
[EndTime "01:25:35"]
[FEN "r2q1rk1/1b2bp1p/p1nPp1p1/7n/1p1P4/3BBN2/PPQ1NPPP/R4RK1 b - - 0 15"]
[Link "https://www.chess.com/live/game/6127785617"]
[SetUp "1"]
[StartTime "01:21:49"]
[Termination "ludavics won by checkmate"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.01.03"]
[UTCTime "01:21:49"]
[WhiteElo "1100"]

15... Qxd6 16. Ng3 ( { Refutation (-2.82 vs. -0.04 in solution) } 16. Bg5 Bxg5 ) 0-1""",
        "probability_loss": -0.2514697026803494,
        "refutations": [[("e3", "g5"), ("e7", "g5")]],
        "solution": [("e2", "g3")],
        "starting_fen": "r2q1rk1/1b2bp1p/p1nPp1p1/7n/1p1P4/3BBN2/PPQ1NPPP/R4RK1 b - - 0 15",
    },
    {
        "cp_loss": -99827.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.01.03"]
[Round "-"]
[White "mhughes127"]
[Black "ludavics"]
[Result "0-1"]
[BlackElo "1096"]
[CurrentPosition "r4rk1/1b3p1p/p3p1p1/6Nn/1p1N4/3B4/PP1Q1PqP/R4RK1 w - -"]
[ECO "B50"]
[ECOUrl "https://www.chess.com/openings/Sicilian-Defense-Delayed-Alapin-Variation"]
[EndDate "2021.01.03"]
[EndTime "01:25:35"]
[FEN "r4rk1/1b3p1p/p1n1p1p1/3q2Nn/1p1P4/3B4/PP1QNPPP/R4RK1 b - - 2 18"]
[Link "https://www.chess.com/live/game/6127785617"]
[SetUp "1"]
[StartTime "01:21:49"]
[Termination "ludavics won by checkmate"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.01.03"]
[UTCTime "01:21:49"]
[WhiteElo "1100"]

18... Nxd4 19. Be4 ( { Refutation (-999.99 vs. -1.72 in solution) } 19. Nxd4 Qxg2# ) 0-1""",
        "probability_loss": -0.33447813078794053,
        "refutations": [[("e2", "d4"), ("d5", "g2")]],
        "solution": [("d3", "e4")],
        "starting_fen": "r4rk1/1b3p1p/p1n1p1p1/3q2Nn/1p1P4/3B4/PP1QNPPP/R4RK1 b - - 2 18",
    },
]
