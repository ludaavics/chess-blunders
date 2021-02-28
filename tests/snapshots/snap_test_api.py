# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_blunders_worker 1"] = [
    {
        "cp_loss": -100644.0,
        "pgn": "30... Kg8 { [%clk 0:01:21.2] } 31. Rd3 { [%clk 0:00:03.3] } ( { Refutation (-99998) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) ( { Solution (646) } 31. h3 Rf8 ) 31... Ra1+ { [%clk 0:01:21.4] }",
        "probability_loss": -0.9298247211092094,
        "starting_fen": "r5k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/6K1 b - - 5 31",
    }
]

snapshots["test_blunders_worker 2"] = {
    "blunder": {
        "cp_loss": -100644.0,
        "pgn": "30... Kg8 { [%clk 0:01:21.2] } 31. Rd3 { [%clk 0:00:03.3] } ( { Refutation (-99998) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) ( { Solution (646) } 31. h3 Rf8 ) 31... Ra1+ { [%clk 0:01:21.4] }",
        "probability_loss": -0.9298247211092094,
        "starting_fen": "r5k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/6K1 b - - 5 31",
    },
    "job_name": "morning-tree-0821",
}

snapshots["test_blunders_worker 3"] = {
    "connection_id": {"Type": "String", "Value": "None"}
}

snapshots["test_get_blunders 1"] = {
    "body": """[
  {
    "starting_fen": "1r1q1rk1/1b2bppp/1Nnp1n2/pB2p3/1p2P3/4BN2/PPP1RPPP/3Q1RK1 b - - 3 17",
    "pgn": "16... Rb8 { [%clk 0:02:00.3] } 17. Bb5 { [%clk 0:02:38.3] } ( { Refutation (-403) } 17. Bb5 Ba8 ) ( { Solution (35) } 17. c3 bxc3 18. bxc3 Bc8 19. Nxc8 Rxc8 20. Rfe1 h6 21. Qa4 Qc7 22. Rc2 Nd8 23. Bf1 Ne6 ) 17... Ba8 { [%clk 0:01:59] } 18. a3 { [%clk 0:02:27.7] } 18... Ng4 { [%clk 0:01:59.8] } 19. h3 { [%clk 0:02:10.7] } 19... Nxe3 { [%clk 0:02:00.7] } 20. Rxe3 { [%clk 0:02:12.2] } 20... Qxb6 { [%clk 0:01:57.5] } 21. Bc4 { [%clk 0:01:57.7] } 21... bxa3 { [%clk 0:01:45.6] } 22. bxa3 { [%clk 0:01:56.9] } 22... Na7 { [%clk 0:01:27.6] } 23. Rb3 { [%clk 0:01:50.7] } 23... Qc7 { [%clk 0:01:18.2] } 24. Qd2 { [%clk 0:01:43] } 24... Qxc4 { [%clk 0:01:14.9] } 25. Rc3 { [%clk 0:01:41] } 25... Qxe4 { [%clk 0:01:08] } 26. Re3 { [%clk 0:01:38.9] } 26... Qa4 { [%clk 0:01:03] } 27. Ne1 { [%clk 0:01:22.5] } 27... Qc6 { [%clk 0:00:56.5] } 28. Nd3 { [%clk 0:01:20] } 28... Qxg2# { [%clk 0:00:56] }",
    "cp_loss": -438.0,
    "probability_loss": -0.3686
  },
  {
    "starting_fen": "r5k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/6K1 b - - 5 31",
    "pgn": "30... Kg8 { [%clk 0:01:21.2] } 31. Rd3 { [%clk 0:00:03.3] } ( { Refutation (-99998) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) ( { Solution (646) } 31. h3 Rf8 ) 31... Ra1+ { [%clk 0:01:21.4] }",
    "cp_loss": -100644.0,
    "probability_loss": -0.9298
  },
  {
    "starting_fen": "2rq1rk1/nb2bppp/p3pn2/1B1pN3/3P1B2/P1P4P/1P1NQPP1/R3K2R b KQ - 0 14",
    "pgn": "13... Rc8 { [%clk 0:02:48.2] } 14. Bxb5 { [%clk 0:02:39.1] } ( { Refutation (-427) } 14. Bxb5 Nxb5 15. O-O ) ( { Solution (110) } 14. Ng4 Nc6 ) 14... axb5 { [%clk 0:02:41.6] } 15. Ndf3 { [%clk 0:02:33.4] } 15... Ne4 { [%clk 0:02:20.7] } 16. O-O { [%clk 0:02:25.1] } 16... Nc6 { [%clk 0:01:53.4] } 17. Qxb5 { [%clk 0:02:21.6] } 17... Nxe5 { [%clk 0:01:38] } 18. dxe5 { [%clk 0:02:21.7] } 18... Rb8 { [%clk 0:01:37.9] } 19. Qe2 { [%clk 0:02:16.2] } 19... Ra8 { [%clk 0:01:28.2] } 20. Qe3 { [%clk 0:02:08.3] } 20... Bc5 { [%clk 0:01:15.5] } 21. Qc1 { [%clk 0:02:05.2] } 21... f6 { [%clk 0:01:00.4] } 22. exf6 { [%clk 0:01:58.5] } 22... Rxf6 { [%clk 0:00:58] } 23. Nd4 { [%clk 0:01:56.3] } 23... Qd7 { [%clk 0:00:36.4] } 24. Be5 { [%clk 0:01:42] } 24... Rff8 { [%clk 0:00:29.6] } 25. f3 { [%clk 0:01:33.2] } 25... Nf6 { [%clk 0:00:08.3] } 26. Bxf6 { [%clk 0:01:20.9] } 26... Rxf6 { [%clk 0:00:09.3] } 27. Kh1 { [%clk 0:01:16.4] } 27... Rc8 { [%clk 0:00:08.9] } 28. b4 { [%clk 0:01:11.1] } 28... Bxd4 { [%clk 0:00:09.7] } 29. Rb1 { [%clk 0:01:07.9] } 29... Bxc3 { [%clk 0:00:10.2] } 30. Qg5 { [%clk 0:01:04.2] } 30... Be5 { [%clk 0:00:06.5] } 31. f4 { [%clk 0:01:01.6] } 31... Bd4 { [%clk 0:00:06.1] } 32. Rbd1 { [%clk 0:01:00.4] } 32... Ba7 { [%clk 0:00:05.5] } 33. Rf3 { [%clk 0:00:51.7] } 33... Rff8 { [%clk 0:00:06.7] } 34. Rdf1 { [%clk 0:00:52.4] } 34... d4 { [%clk 0:00:07] } 35. Rg3 { [%clk 0:00:52.6] } 35... d3 { [%clk 0:00:07.8] } 36. Rd1 { [%clk 0:00:53.7] } 36... g6 { [%clk 0:00:08] } 37. Rgxd3 { [%clk 0:00:50.6] } 37... Qc6 { [%clk 0:00:09] } 38. R1d2 { [%clk 0:00:42.8] } 38... Qc1+ { [%clk 0:00:09.6] } 39. Rd1 { [%clk 0:00:43.2] } 39... Qc2 { [%clk 0:00:10] } 40. R3d2 { [%clk 0:00:43.8] } 40... Qe4 { [%clk 0:00:10.2] } 41. Rd4 { [%clk 0:00:36.9] } 41... Qxg2+ { [%clk 0:00:10.8] } 42. Qxg2 { [%clk 0:00:37.2] } 42... Bxg2+ { [%clk 0:00:12] } 43. Kxg2 { [%clk 0:00:39.1] } 43... Rc2+ { [%clk 0:00:13.2] } 44. Kg1 { [%clk 0:00:39.8] } 44... Bxd4+ { [%clk 0:00:13.4] } 45. Rxd4 { [%clk 0:00:40.4] } 45... Rc1+ { [%clk 0:00:14.5] } 46. Kh2 { [%clk 0:00:41.8] } 46... Rc2+ { [%clk 0:00:14.7] } 47. Kg3 { [%clk 0:00:43.5] } 47... Ra2 { [%clk 0:00:15.6] } 48. Kh4 { [%clk 0:00:45.4] } 48... Rxa3 { [%clk 0:00:16.7] } 49. Kg5 { [%clk 0:00:46.8] } 49... Ra4 { [%clk 0:00:16.9] } 50. Rd6 { [%clk 0:00:48.3] } 50... Rxb4 { [%clk 0:00:17.7] } 51. Rxe6 { [%clk 0:00:49.5] } 51... Rb5+ { [%clk 0:00:18.8] } 52. Re5 { [%clk 0:00:50.1] } 52... Rxe5+ { [%clk 0:00:19.2] } 53. fxe5 { [%clk 0:00:52] } 53... Rf5+ { [%clk 0:00:20.4] } 54. Kg4 { [%clk 0:00:52.6] } 54... Rxe5 { [%clk 0:00:21.8] } 55. h4 { [%clk 0:00:53.5] } 55... Rg5+ { [%clk 0:00:21.1] } 56. Kf4 { [%clk 0:00:54.1] } 56... Ra5 { [%clk 0:00:22.1] } 57. Kg4 { [%clk 0:00:54.2] } 57... Ra4+ { [%clk 0:00:23.1] } 58. Kg5 { [%clk 0:00:55.7] } 58... Ra5+ { [%clk 0:00:24.4] } 59. Kg4 { [%clk 0:00:56.9] } 59... h5+ { [%clk 0:00:25.8] } 60. Kh3 { [%clk 0:00:56.7] } 60... g5 { [%clk 0:00:26.2] } 61. hxg5 { [%clk 0:00:56.8] } 61... Rxg5 { [%clk 0:00:27.4] } 62. Kh4 { [%clk 0:00:58.5] } 62... Ra5 { [%clk 0:00:27.9] } 63. Kh3 { [%clk 0:00:58.3] } 63... Kf7 { [%clk 0:00:29.4] } 64. Kh4 { [%clk 0:01:00] } 64... Kf6 { [%clk 0:00:30.8] } 65. Kh3 { [%clk 0:01:01.9] } 65... Kg5 { [%clk 0:00:31.4] } 66. Kg3 { [%clk 0:00:59.7] } 66... h4+ { [%clk 0:00:31.2] } 67. Kh3 { [%clk 0:01:01.6] } 67... Ra3+ { [%clk 0:00:29.9] } 68. Kh2 { [%clk 0:01:03.5] } 68... Kg4 { [%clk 0:00:30.7] } 69. Kg2 { [%clk 0:01:05.2] } 69... Rg3+ { [%clk 0:00:28.6] } 70. Kh2 { [%clk 0:01:07.1] } 70... Rh3+ { [%clk 0:00:28.7] } 71. Kg2 { [%clk 0:01:06.2] } 71... Ra3 { [%clk 0:00:27.3] } 72. Kh1 { [%clk 0:01:08.1] } 72... Ra2 { [%clk 0:00:23.7] } 73. Kg1 { [%clk 0:01:06.9] } 73... Kg3 { [%clk 0:00:23.6] } 74. Kh1 { [%clk 0:01:08.8] } 74... Kf3 { [%clk 0:00:18.1] } 75. Kg1 { [%clk 0:01:10.7] } 75... h3 { [%clk 0:00:17.8] } 76. Kh1 { [%clk 0:01:12.6] } 76... Ra1+ { [%clk 0:00:13.1] } 77. Kh2 { [%clk 0:01:13.3] } 77... Kg4 { [%clk 0:00:11.6] }",
    "cp_loss": -537.0,
    "probability_loss": -0.4548
  }
]""",
    "statusCode": 200,
}

snapshots["test_get_blunders 2"] = {
    "body": """[
  {
    "starting_fen": "r5k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/6K1 b - - 5 31",
    "pgn": "30... Kg8 { [%clk 0:01:21.2] } 31. Rd3 { [%clk 0:00:03.3] } ( { Refutation (-99998) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) ( { Solution (646) } 31. h3 Rf8 ) 31... Ra1+ { [%clk 0:01:21.4] }",
    "cp_loss": -100644.0,
    "probability_loss": -0.9298
  }
]""",
    "statusCode": 200,
}

snapshots["test_get_games_chessdotcom_invalid_query_params 1"] = {
    "body": """[
  {
    "loc": [
      "limit"
    ],
    "msg": "ensure this value is greater than 0",
    "type": "value_error.number.not_gt",
    "ctx": {
      "limit_value": 0
    }
  }
]""",
    "statusCode": 400,
}
