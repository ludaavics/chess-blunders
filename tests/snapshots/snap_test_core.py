# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_known_blunders[0] 1"] = [
    {
        "cp_loss": -822.0,
        "pgn": "26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } ( { Refutation (-56) } 27. Bxf8 Qxb5 ) ( { Solution (766) } 27. a4 ) 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.5111501270440948,
        "starting_fen": "3r1Bk1/5ppp/1pR5/1Q6/8/P3P3/1q3PPP/2R3K1 b - - 0 27",
    }
]

snapshots["test_known_blunders[games_loc1] 1"] = [
    {
        "cp_loss": -655.0,
        "pgn": "29... Bc7 { [%clk 0:01:01.4] } 30. Qxd4 { [%clk 0:00:13.5] } ( { Refutation (220) } 30. Qxd4 Rxf3 ) ( { Solution (875) } 30. Nxd4 ) 30... Rxf3 { [%clk 0:00:59.1] } 31. Ra8 { [%clk 0:00:11.4] } 31... Rff8 { [%clk 0:00:55.5] } 32. Rxb8 { [%clk 0:00:10.7] } 32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.263865548155076,
        "starting_fen": "1r3r1k/1Pb3p1/R1P3qp/8/3Q4/3P1N1P/5PP1/5RK1 b - - 0 30",
    },
    {
        "cp_loss": -1015.0,
        "pgn": "32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } ( { Refutation (-263) } 33. Qa7 Qxc6 ) ( { Solution (752) } 33. Qd7 ) 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.6940930034743776,
        "starting_fen": "1r5k/QPb3p1/2P3qp/8/8/3P3P/5PP1/5RK1 b - - 1 33",
    },
    {
        "cp_loss": -99740.0,
        "pgn": "38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } ( { Refutation (-99998) } 39. d5 Rb1+ ) ( { Solution (-258) } 39. g3 ) 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.26269654621644073,
        "starting_fen": "4R3/1rb3pk/7p/3P4/8/7P/5PP1/6K1 b - - 0 39",
    },
    {
        "cp_loss": -99807.0,
        "pgn": "18... Nxd4 { [%clk 0:01:53.4] } 19. Nxd4 { [%clk 0:01:46.5] } ( { Refutation (-99999) } 19. Nxd4 Qxg2# ) ( { Solution (-192) } 19. Be4 ) 19... Qxg2# { [%clk 0:01:53.3] }",
        "probability_loss": -0.3169119051378149,
        "starting_fen": "r4rk1/1b3p1p/p3p1p1/3q2Nn/1p1N4/3B4/PP1Q1PPP/R4RK1 b - - 0 19",
    },
]
