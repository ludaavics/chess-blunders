# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_create_blunder_puzzles[0] 1"] = [
    {
        "cp_loss": -836.0,
        "pgn": "26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } ( { Solution (787) } 27. a4 ) ( { Refutation (-49) } 27. Bxf8 Qxb5 28. Bd6 h5 29. h3 f6 30. Bb4 Rd5 31. Rc8+ Kh7 32. R8c4 Rg5 33. Rf4 Qd5 34. g3 Qe5 35. Rd1 b5 36. Rdd4 Rf5 37. Rxf5 Qxf5 38. h4 ) 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.51,
        "starting_fen": "3r1rk1/5ppp/1pR5/1Q6/1B6/P3P3/1q3PPP/2R3K1 w - - 0 27",
    }
]

snapshots["test_create_blunder_puzzles[games_loc1] 1"] = [
    {
        "cp_loss": -670.0,
        "pgn": "29... Bc7 { [%clk 0:01:01.4] } 30. Qxd4 { [%clk 0:00:13.5] } ( { Solution (863) } 30. Nxd4 Qd6 ) ( { Refutation (193) } 30. Qxd4 Rxf3 ) 30... Rxf3 { [%clk 0:00:59.1] } 31. Ra8 { [%clk 0:00:11.4] } 31... Rff8 { [%clk 0:00:55.5] } 32. Rxb8 { [%clk 0:00:10.7] } 32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.29,
        "starting_fen": "1r3r1k/1Pb3p1/R1P3qp/8/2Qp4/3P1N1P/5PP1/5RK1 w - - 1 30",
    },
    {
        "cp_loss": -1084.0,
        "pgn": "32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } ( { Solution (818) } 33. Qd7 ) ( { Refutation (-266) } 33. Qa7 Qxc6 34. Rb1 Qc2 35. Re1 Qd2 36. Qe3 Qb4 37. Qe4 Qxb7 38. g3 Qb6 39. Re3 Qd6 40. Qe6 Qxe6 41. Rxe6 Rb2 42. d4 Kg8 43. Re7 Ba5 44. Kg2 Rd2 45. Rd7 ) 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.71,
        "starting_fen": "1r5k/1Pb3p1/2P3qp/8/3Q4/3P3P/5PP1/5RK1 w - - 0 33",
    },
    {
        "cp_loss": -99812.0,
        "pgn": "18... Nxd4 { [%clk 0:01:53.4] } 19. Nxd4 { [%clk 0:01:46.5] } ( { Solution (-187) } 19. Be4 Nxe2+ ) ( { Refutation (-99999) } 19. Nxd4 Qxg2# ) 19... Qxg2# { [%clk 0:01:53.3] }",
        "probability_loss": -0.32,
        "starting_fen": "r4rk1/1b3p1p/p3p1p1/3q2Nn/1p1n4/3B4/PP1QNPPP/R4RK1 w - - 0 19",
    },
]

snapshots["test_get_root 1"] = [
    {"path": "/"},
    {"path": "/games/chessdotcom/{username}"},
    {"path": "/puzzles/blunders"},
]
