# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_create_blunder_puzzles[games_loc0-None] 1"] = [
    {
        "cp_loss": -836.0,
        "pgn": "26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } ( { Refutation (-49) } 27. Bxf8 Qxb5 28. Bd6 h5 29. h3 f6 30. Bb4 Rd5 31. Rc8+ Kh7 32. R8c4 Rg5 33. Rf4 Qd5 34. g3 Qe5 35. Rd1 b5 36. Rdd4 Rf5 37. Rxf5 Qxf5 38. h4 ) ( { Solution (787) } 27. a4 ) 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.5076735788072179,
        "starting_fen": "3r1Bk1/5ppp/1pR5/1Q6/8/P3P3/1q3PPP/2R3K1 b - - 0 27",
    }
]

snapshots["test_create_blunder_puzzles[games_loc1-colors1] 1"] = [
    {
        "cp_loss": -670.0,
        "pgn": "29... Bc7 { [%clk 0:01:01.4] } 30. Qxd4 { [%clk 0:00:13.5] } ( { Refutation (193) } 30. Qxd4 Rxf3 ) ( { Solution (863) } 30. Nxd4 Qd6 ) 30... Rxf3 { [%clk 0:00:59.1] } 31. Ra8 { [%clk 0:00:11.4] } 31... Rff8 { [%clk 0:00:55.5] } 32. Rxb8 { [%clk 0:00:10.7] } 32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.2853373539583116,
        "starting_fen": "1r3r1k/1Pb3p1/R1P3qp/8/3Q4/3P1N1P/5PP1/5RK1 b - - 0 30",
    },
    {
        "cp_loss": -1084.0,
        "pgn": "32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } ( { Refutation (-266) } 33. Qa7 Qxc6 34. Rb1 Qc2 35. Re1 Qd2 36. Qe3 Qb4 37. Qe4 Qxb7 38. g3 Qb6 39. Re3 Qd6 40. Qe6 Qxe6 41. Rxe6 Rb2 42. d4 Kg8 43. Re7 Ba5 44. Kg2 Rd2 45. Rd7 ) ( { Solution (818) } 33. Qd7 ) 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.7069098628920365,
        "starting_fen": "1r5k/QPb3p1/2P3qp/8/8/3P3P/5PP1/5RK1 b - - 1 33",
    },
]

snapshots["test_get_root 1"] = [
    {"path": "/"},
    {"path": "/games/chessdotcom/{username}"},
    {"path": "/puzzles/blunders"},
]
