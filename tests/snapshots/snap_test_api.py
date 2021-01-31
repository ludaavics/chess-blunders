# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_create_blunder_puzzles[0] 1"] = [
    {
        "cp_loss": -462.0,
        "pgn": "12... Nc4 { [%clk 0:01:56.1] } 13. Nxd5 { [%clk 0:02:22.5] } ( { Solution (632) } 13. dxc5 ) ( { Refutation (170) } 13. Nxd5 Nb6 14. Qb5 ) 13... Nb6 { [%clk 0:01:10.1] } 14. Nxb6 { [%clk 0:02:15.4] } 14... axb6 { [%clk 0:01:10.5] } 15. Qb5 { [%clk 0:02:09.8] } 15... Ra5 { [%clk 0:01:05.5] } 16. Qe2 { [%clk 0:01:42.5] } 16... Qxd7 { [%clk 0:01:05.9] } 17. Rd1 { [%clk 0:01:43.9] } 17... cxd4 { [%clk 0:01:01.3] } 18. Rxd4 { [%clk 0:01:42.7] } 18... Qc6 { [%clk 0:00:51.3] } 19. Bd2 { [%clk 0:01:37.6] } 19... Raa8 { [%clk 0:00:48.7] } 20. Rc1 { [%clk 0:01:34.4] } 20... Qe6 { [%clk 0:00:39.8] } 21. a3 { [%clk 0:01:30.6] } 21... Bc5 { [%clk 0:00:34] } 22. Rdc4 { [%clk 0:01:12] } 22... b5 { [%clk 0:00:28.1] } 23. Rxc5 { [%clk 0:01:09.4] } 23... b6 { [%clk 0:00:28] } 24. Rc6 { [%clk 0:01:08.4] } 24... Qa2 { [%clk 0:00:22.9] } 25. Qxb5 { [%clk 0:01:03.6] } 25... Rad8 { [%clk 0:00:18.3] } 26. Bb4 { [%clk 0:01:00.3] } 26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.26,
        "starting_fen": "r2q1rk1/pp1Bbppp/8/2pp4/Q1nP4/2N1P3/PP3PPP/R1B2RK1 w - - 1 13",
    },
    {
        "cp_loss": -857.0,
        "pgn": "26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } ( { Solution (773) } 27. Qc4 Rfe8 ) ( { Refutation (-84) } 27. Bxf8 Qxb5 28. Bd6 f6 29. h3 Rd7 30. Bb4 Kf7 31. Rc8 Kg6 32. Bc3 Rd3 33. Bb4 h6 34. R8c7 Rd7 35. Rxd7 Qxd7 36. f3 h5 37. Kf2 Kf7 38. Rc2 h4 39. Rd2 Qc7 ) 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.54,
        "starting_fen": "3r1rk1/5ppp/1pR5/1Q6/1B6/P3P3/1q3PPP/2R3K1 w - - 0 27",
    },
]

snapshots["test_create_blunder_puzzles[games_loc1] 1"] = [
    {
        "cp_loss": -690.0,
        "pgn": "29... Bc7 { [%clk 0:01:01.4] } 30. Qxd4 { [%clk 0:00:13.5] } ( { Solution (927) } 30. Nxd4 ) ( { Refutation (237) } 30. Qxd4 Rxf3 31. Ra8 ) 30... Rxf3 { [%clk 0:00:59.1] } 31. Ra8 { [%clk 0:00:11.4] } 31... Rff8 { [%clk 0:00:55.5] } 32. Rxb8 { [%clk 0:00:10.7] } 32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.26,
        "starting_fen": "1r3r1k/1Pb3p1/R1P3qp/8/2Qp4/3P1N1P/5PP1/5RK1 w - - 1 30",
    },
    {
        "cp_loss": -1015.0,
        "pgn": "32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } ( { Solution (796) } 33. Qd7 Qd6 34. Qxd6 Bxd6 35. Re1 Kh7 36. d4 Rd8 37. Re7 Bxe7 38. c7 Rxd4 39. b8=Q Rd1+ 40. Kh2 Bd6+ 41. g3 Bxc7 42. Qxc7 Rd2 43. Kg2 Ra2 44. h4 Ra6 45. Qc2+ g6 46. h5 Rf6 ) ( { Refutation (-219) } 33. Qa7 Qxc6 34. Rb1 ) 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.67,
        "starting_fen": "1r5k/1Pb3p1/2P3qp/8/3Q4/3P3P/5PP1/5RK1 w - - 0 33",
    },
    {
        "cp_loss": -959.0,
        "pgn": "33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } ( { Solution (-213) } 34. Rb1 Qc2 ) ( { Refutation (-1172) } 34. Qa8 Rxa8 35. bxa8=Q+ Qxa8 36. Re1 Bb6 37. d4 Qa4 38. g3 Qxd4 39. Re8+ Kh7 40. Rf8 Qd1+ 41. Kg2 Qd5+ 42. Kg1 g5 43. Rb8 Qc5 44. Rxb6 Qxb6 45. Kg2 Kg8 ) 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.29,
        "starting_fen": "1r5k/QPb3p1/2q4p/8/8/3P3P/5PP1/5RK1 w - - 0 34",
    },
    {
        "cp_loss": -99754.0,
        "pgn": "38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } ( { Solution (-244) } 39. g4 Rb2 40. Kg2 Rd2 41. Re4 Bb6 42. Kf3 Bxd4 43. Re2 Rd1 44. h4 Kg6 45. Re6+ Bf6 46. Ra6 Rc1 47. Kf4 Rc4+ 48. Kg3 Rc2 49. f4 Rc3+ 50. Kh2 Rc4 51. h5+ Kf7 ) ( { Refutation (-99998) } 39. d5 Rb1+ 40. Re1 Rxe1# ) 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.27,
        "starting_fen": "4R3/1rb3pk/7p/8/3P4/7P/5PP1/6K1 w - - 1 39",
    },
    {
        "cp_loss": -99846.0,
        "pgn": "18... Nxd4 { [%clk 0:01:53.4] } 19. Nxd4 { [%clk 0:01:46.5] } ( { Solution (-153) } 19. Be4 ) ( { Refutation (-99999) } 19. Nxd4 Qxg2# ) 19... Qxg2# { [%clk 0:01:53.3] }",
        "probability_loss": -0.35,
        "starting_fen": "r4rk1/1b3p1p/p3p1p1/3q2Nn/1p1n4/3B4/PP1QNPPP/R4RK1 w - - 0 19",
    },
]

snapshots["test_get_root 1"] = [
    {"path": "/"},
    {"path": "/games/chessdotcom/{username}"},
    {"path": "/puzzles/blunders"},
]
