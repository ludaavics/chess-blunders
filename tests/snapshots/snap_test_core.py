# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_known_blunders[0-False] 1"] = [
    {
        "cp_loss": -821.0,
        "pgn": "26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } ( { Refutation (-47) } 27. Bxf8 Qxb5 ) ( { Solution (774) } 27. Qc4 ) 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.5035895039665865,
        "starting_fen": "3r1Bk1/5ppp/1pR5/1Q6/8/P3P3/1q3PPP/2R3K1 b - - 0 27",
    }
]

snapshots["test_known_blunders[games_loc1-True] 1"] = [
    {
        "cp_loss": -507.0,
        "pgn": "22... exd4 { [%clk 0:01:43.8] } 23. Nf3 { [%clk 0:01:28.4] } ( { Refutation (69) } 23. Nf3 Rxf3 ) ( { Solution (576) } 23. g3 ) 23... Bf4 { [%clk 0:01:30.9] } 24. bxa6 { [%clk 0:01:15.3] } 24... bxa6 { [%clk 0:01:27.7] } 25. h3 { [%clk 0:01:15.7] } 25... Rfe8 { [%clk 0:01:22.4] } 26. Qc4 { [%clk 0:00:46.3] } 26... Rf8 { [%clk 0:01:10.1] } 27. c6 { [%clk 0:00:44.4] } 27... Qg6 { [%clk 0:01:07.7] } 28. b7 { [%clk 0:00:35.6] } 28... Rab8 { [%clk 0:01:03] } 29. Rxa6 { [%clk 0:00:34.5] } 29... Bc7 { [%clk 0:01:01.4] } 30. Qxd4 { [%clk 0:00:13.5] } 30... Rxf3 { [%clk 0:00:59.1] } 31. Ra8 { [%clk 0:00:11.4] } 31... Rff8 { [%clk 0:00:55.5] } 32. Rxb8 { [%clk 0:00:10.7] } 32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.3406424768115154,
        "starting_fen": "rb3r1k/1p4p1/pP2Q2p/1PP4q/3p4/3P1N2/5PPP/R4RK1 b - - 1 23",
    },
    {
        "cp_loss": -536.0,
        "pgn": "29... Bc7 { [%clk 0:01:01.4] } 30. Qxd4 { [%clk 0:00:13.5] } ( { Refutation (187) } 30. Qxd4 Rxf3 ) ( { Solution (723) } 30. Nxd4 ) 30... Rxf3 { [%clk 0:00:59.1] } 31. Ra8 { [%clk 0:00:11.4] } 31... Rff8 { [%clk 0:00:55.5] } 32. Rxb8 { [%clk 0:00:10.7] } 32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.2687067954177095,
        "starting_fen": "1r3r1k/1Pb3p1/R1P3qp/8/3Q4/3P1N1P/5PP1/5RK1 b - - 0 30",
    },
    {
        "cp_loss": -874.0,
        "pgn": "32... Rxb8 { [%clk 0:00:56] } 33. Qa7 { [%clk 0:00:10] } ( { Refutation (-224) } 33. Qa7 Qxc6 ) ( { Solution (650) } 33. Qd7 ) 33... Qxc6 { [%clk 0:00:55.6] } 34. Qa8 { [%clk 0:00:09.6] } 34... Qxb7 { [%clk 0:00:52.5] } 35. Qxb7 { [%clk 0:00:08.6] } 35... Rxb7 { [%clk 0:00:53.5] } 36. Re1 { [%clk 0:00:09.1] } 36... Ba5 { [%clk 0:00:51.2] } 37. Re8+ { [%clk 0:00:09.6] } 37... Kh7 { [%clk 0:00:50.9] } 38. d4 { [%clk 0:00:09.7] } 38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.6409883879613829,
        "starting_fen": "1r5k/QPb3p1/2P3qp/8/8/3P3P/5PP1/5RK1 b - - 1 33",
    },
    {
        "cp_loss": -99754.0,
        "pgn": "38... Bc7 { [%clk 0:00:50.1] } 39. d5 { [%clk 0:00:10.1] } ( { Refutation (-99998) } 39. d5 Rb1+ ) ( { Solution (-244) } 39. g3 ) 39... Rb1+ { [%clk 0:00:50.5] } 40. Re1 { [%clk 0:00:05.7] } 40... Rxe1# { [%clk 0:00:51.3] }",
        "probability_loss": -0.273686191698313,
        "starting_fen": "4R3/1rb3pk/7p/3P4/8/7P/5PP1/6K1 b - - 0 39",
    },
    {
        "cp_loss": -278.0,
        "pgn": "15... Qxd6 { [%clk 0:02:23.2] } 16. Bg5 { [%clk 0:02:06.7] } ( { Refutation (-282) } 16. Bg5 Bxg5 ) ( { Solution (-4) } 16. Ng3 ) 16... Bxg5 { [%clk 0:02:06.5] } 17. Nxg5 { [%clk 0:02:05.3] } 17... Qd5 { [%clk 0:02:06.2] } 18. Qd2 { [%clk 0:01:52.3] } 18... Nxd4 { [%clk 0:01:53.4] } 19. Nxd4 { [%clk 0:01:46.5] } 19... Qxg2# { [%clk 0:01:53.3] }",
        "probability_loss": -0.2514697026803494,
        "starting_fen": "r4rk1/1b2bp1p/p1nqp1p1/6Bn/1p1P4/3B1N2/PPQ1NPPP/R4RK1 b - - 1 16",
    },
    {
        "cp_loss": -99827.0,
        "pgn": "18... Nxd4 { [%clk 0:01:53.4] } 19. Nxd4 { [%clk 0:01:46.5] } ( { Refutation (-99999) } 19. Nxd4 Qxg2# ) ( { Solution (-172) } 19. Be4 ) 19... Qxg2# { [%clk 0:01:53.3] }",
        "probability_loss": -0.33447813078794053,
        "starting_fen": "r4rk1/1b3p1p/p3p1p1/3q2Nn/1p1N4/3B4/PP1Q1PPP/R4RK1 b - - 0 19",
    },
]
