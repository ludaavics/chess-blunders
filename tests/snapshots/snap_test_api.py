# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_blunders_to_db[event0] 1"] = {
    "cp_loss": "-1058.0",
    "job_name": "bh2R9cS1IAMCJ_Q=",
    "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2020.07.02"]
[Round "-"]
[White "E_Jaime"]
[Black "ludavics"]
[Result "0-1"]
[BlackElo "936"]
[CurrentPosition "r4rk1/p2p1p1p/1p2pbp1/8/4qP2/1P4R1/P2BK2P/8 w - -"]
[ECO "B21"]
[ECOUrl "https://www.chess.com/openings/Sicilian-Defense-Smith-Morra-Gambit-2...cxd4-3.Qxd4-Nc6"]
[EndDate "2020.07.02"]
[EndTime "21:48:28"]
[FEN "r4rk1/p1qp1p1p/1p2pbp1/8/4bP2/1P1QB1R1/P1B1K2P/8 w - - 0 25"]
[Link "https://www.chess.com/live/game/5091644286"]
[SetUp "1"]
[StartTime "21:41:38"]
[Termination "ludavics won by resignation"]
[TimeControl "300"]
[Timezone "UTC"]
[UTCDate "2020.07.02"]
[UTCTime "21:41:38"]
[WhiteElo "958"]

25. Qxe4 d5 ( { Refutation (-260 vs. 798 in solution) } 25... Qxc2+ 26. Qxc2 ) 26. Qd3 e5 27. fxe5 Qxe5 28. Kf1 Rac8 29. Bd1 Rfe8 30. Bd4 Qe1+ 31. Kg2 Rc1 32. Bxf6 Rxd1 33. Bc3 Qh1+ 34. Kh3 0-1""",
    "probability_loss": "-0.6994",
    "refutations": None,
    "solution": [
        ("d7", "d5"),
        ("e4", "d3"),
        ("e6", "e5"),
        ("f4", "e5"),
        ("c7", "e5"),
        ("e2", "f1"),
        ("a8", "c8"),
        ("c2", "d1"),
        ("f8", "e8"),
        ("e3", "d4"),
        ("e5", "e1"),
        ("f1", "g2"),
        ("c8", "c1"),
        ("d4", "f6"),
        ("c1", "d1"),
        ("f6", "c3"),
        ("e1", "h1"),
        ("g2", "h3"),
    ],
    "starting_fen": "r4rk1/p1qp1p1p/1p2pbp1/8/4bP2/1P1QB1R1/P1B1K2P/8 w - - 0 25",
}

snapshots["test_blunders_to_db[event0] 2"] = {
    "ConsumedCapacity": {"CapacityUnits": 1, "TableName": "test-blunders-table"},
    "Count": 1,
    "Items": [
        {
            "cp_loss": "-1058.0",
            "created_at": "2021-01-27T00:00:00",
            "job_name": "bh2R9cS1IAMCJ_Q=",
            "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2020.07.02"]
[Round "-"]
[White "E_Jaime"]
[Black "ludavics"]
[Result "0-1"]
[BlackElo "936"]
[CurrentPosition "r4rk1/p2p1p1p/1p2pbp1/8/4qP2/1P4R1/P2BK2P/8 w - -"]
[ECO "B21"]
[ECOUrl "https://www.chess.com/openings/Sicilian-Defense-Smith-Morra-Gambit-2...cxd4-3.Qxd4-Nc6"]
[EndDate "2020.07.02"]
[EndTime "21:48:28"]
[FEN "r4rk1/p1qp1p1p/1p2pbp1/8/4bP2/1P1QB1R1/P1B1K2P/8 w - - 0 25"]
[Link "https://www.chess.com/live/game/5091644286"]
[SetUp "1"]
[StartTime "21:41:38"]
[Termination "ludavics won by resignation"]
[TimeControl "300"]
[Timezone "UTC"]
[UTCDate "2020.07.02"]
[UTCTime "21:41:38"]
[WhiteElo "958"]

25. Qxe4 d5 ( { Refutation (-260 vs. 798 in solution) } 25... Qxc2+ 26. Qxc2 ) 26. Qd3 e5 27. fxe5 Qxe5 28. Kf1 Rac8 29. Bd1 Rfe8 30. Bd4 Qe1+ 31. Kg2 Rc1 32. Bxf6 Rxd1 33. Bc3 Qh1+ 34. Kh3 0-1""",
            "probability_loss": "-0.6994",
            "refutations": None,
            "solution": [
                ["d7", "d5"],
                ["e4", "d3"],
                ["e6", "e5"],
                ["f4", "e5"],
                ["c7", "e5"],
                ["e2", "f1"],
                ["a8", "c8"],
                ["c2", "d1"],
                ["f8", "e8"],
                ["e3", "d4"],
                ["e5", "e1"],
                ["f1", "g2"],
                ["c8", "c1"],
                ["d4", "f6"],
                ["c1", "d1"],
                ["f6", "c3"],
                ["e1", "h1"],
                ["g2", "h3"],
            ],
            "starting_fen": "r4rk1/p1qp1p1p/1p2pbp1/8/4bP2/1P1QB1R1/P1B1K2P/8 w - - 0 25",
        }
    ],
    "ScannedCount": 1,
}

snapshots["test_blunders_worker[event0] 1"] = [
    {
        "cp_loss": -509.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.02.02"]
[Round "-"]
[White "ludavics"]
[Black "CloakerBoi"]
[Result "0-1"]
[BlackElo "1183"]
[CurrentPosition "6k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/r5K1 w - -"]
[ECO "C57"]
[ECOUrl "https://www.chess.com/openings/Italian-Game-Traxler-Bishop-Sacrifice-Line-5...Ke7"]
[EndDate "2021.02.02"]
[EndTime "01:31:39"]
[FEN "r2q3r/p5pp/2pk4/1pb1p3/1n2Q3/PBP5/1PP2PPP/R1B2RK1 b - - 0 15"]
[Link "https://www.chess.com/live/game/6421841712"]
[SetUp "1"]
[StartTime "01:24:40"]
[Termination "CloakerBoi won on time"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.02.02"]
[UTCTime "01:24:40"]
[WhiteElo "1047"]

15... Nd5 16. Rd1 ( { Refutation (1.62 vs. 6.71 in solution) } 16. Be3 Nxe3 ) 0-1""",
        "probability_loss": -0.2795162669459942,
        "refutations": [[("c1", "e3"), ("d5", "e3")]],
        "solution": [("f1", "d1")],
        "starting_fen": "r2q3r/p5pp/2pk4/1pb1p3/1n2Q3/PBP5/1PP2PPP/R1B2RK1 b - - 0 15",
    },
    {
        "cp_loss": -100674.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.02.02"]
[Round "-"]
[White "ludavics"]
[Black "CloakerBoi"]
[Result "0-1"]
[BlackElo "1183"]
[CurrentPosition "6k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/r5K1 w - -"]
[ECO "C57"]
[ECOUrl "https://www.chess.com/openings/Italian-Game-Traxler-Bishop-Sacrifice-Line-5...Ke7"]
[EndDate "2021.02.02"]
[EndTime "01:31:39"]
[FEN "r6k/6p1/2p3Q1/1pqnp2p/8/1BP5/1PP2PPP/3R2K1 b - - 3 30"]
[Link "https://www.chess.com/live/game/6421841712"]
[SetUp "1"]
[StartTime "01:24:40"]
[Termination "CloakerBoi won on time"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.02.02"]
[UTCTime "01:24:40"]
[WhiteElo "1047"]

30... Kg8 31. Qe6+ ( { Refutation (-999.98 vs. 6.76 in solution) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) 31... Kh7 0-1""",
        "probability_loss": -0.937262262592271,
        "refutations": [[("d1", "d3"), ("a8", "a1"), ("d3", "d1"), ("a1", "d1")]],
        "solution": [("g6", "e6"), ("g8", "h7")],
        "starting_fen": "r6k/6p1/2p3Q1/1pqnp2p/8/1BP5/1PP2PPP/3R2K1 b - - 3 30",
    },
]

snapshots["test_blunders_worker[event0] 2"] = {
    "blunder": {
        "cp_loss": -509.0,
        "pgn": """[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.02.02"]
[Round "-"]
[White "ludavics"]
[Black "CloakerBoi"]
[Result "0-1"]
[BlackElo "1183"]
[CurrentPosition "6k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/r5K1 w - -"]
[ECO "C57"]
[ECOUrl "https://www.chess.com/openings/Italian-Game-Traxler-Bishop-Sacrifice-Line-5...Ke7"]
[EndDate "2021.02.02"]
[EndTime "01:31:39"]
[FEN "r2q3r/p5pp/2pk4/1pb1p3/1n2Q3/PBP5/1PP2PPP/R1B2RK1 b - - 0 15"]
[Link "https://www.chess.com/live/game/6421841712"]
[SetUp "1"]
[StartTime "01:24:40"]
[Termination "CloakerBoi won on time"]
[TimeControl "180+2"]
[Timezone "UTC"]
[UTCDate "2021.02.02"]
[UTCTime "01:24:40"]
[WhiteElo "1047"]

15... Nd5 16. Rd1 ( { Refutation (1.62 vs. 6.71 in solution) } 16. Be3 Nxe3 ) 0-1""",
        "probability_loss": -0.2795162669459942,
        "refutations": [[["c1", "e3"], ["d5", "e3"]]],
        "solution": [["f1", "d1"]],
        "starting_fen": "r2q3r/p5pp/2pk4/1pb1p3/1n2Q3/PBP5/1PP2PPP/R1B2RK1 b - - 0 15",
    },
    "job_name": "morning-tree-0821",
}

snapshots["test_blunders_worker[event0] 3"] = {}

snapshots["test_blunders_worker[event1] 1"] = [
    {
        "cp_loss": -417.0,
        "pgn": """[Event "Let\'s Play!"]
[Site "Chess.com"]
[Date "2018.05.23"]
[Round "-"]
[White "FlashCP3"]
[Black "ludavics"]
[Result "1-0"]
[BlackElo "1165"]
[CurrentPosition "r1b2rk1/ppNp1ppp/5n2/3Ppq2/2PP4/8/PP1QNPPP/R3KB1R b KQ - 0 11"]
[ECO "A40"]
[ECOUrl "https://www.chess.com/openings/Queens-Pawn-Opening-Mikenas-Defense-2.c4-e5-3.d5"]
[EndDate "2018.05.24"]
[EndTime "01:09:28"]
[FEN "r1bqk1nr/pppp1ppp/8/3Pp3/2Pn4/8/PP1QPPPP/RN2KBNR w KQkq - 1 6"]
[Link "https://www.chess.com/game/daily/195452148"]
[SetUp "1"]
[StartTime "21:40:36"]
[Termination "FlashCP3 won by resignation"]
[TimeControl "1/86400"]
[Timezone "UTC"]
[UTCDate "2018.05.23"]
[UTCTime "21:40:36"]
[WhiteElo "1397"]

6. e3 Nf5 ( { Refutation (-5.1 vs. -0.93 in solution) } 6... Qh4 7. exd4 ) 1-0""",
        "probability_loss": -0.29299110755486085,
        "refutations": [[("d8", "h4"), ("e3", "d4")]],
        "solution": [("d4", "f5")],
        "starting_fen": "r1bqk1nr/pppp1ppp/8/3Pp3/2Pn4/8/PP1QPPPP/RN2KBNR w KQkq - 1 6",
    }
]

snapshots["test_blunders_worker[event1] 2"] = {
    "blunder": {
        "cp_loss": -417.0,
        "pgn": """[Event "Let\'s Play!"]
[Site "Chess.com"]
[Date "2018.05.23"]
[Round "-"]
[White "FlashCP3"]
[Black "ludavics"]
[Result "1-0"]
[BlackElo "1165"]
[CurrentPosition "r1b2rk1/ppNp1ppp/5n2/3Ppq2/2PP4/8/PP1QNPPP/R3KB1R b KQ - 0 11"]
[ECO "A40"]
[ECOUrl "https://www.chess.com/openings/Queens-Pawn-Opening-Mikenas-Defense-2.c4-e5-3.d5"]
[EndDate "2018.05.24"]
[EndTime "01:09:28"]
[FEN "r1bqk1nr/pppp1ppp/8/3Pp3/2Pn4/8/PP1QPPPP/RN2KBNR w KQkq - 1 6"]
[Link "https://www.chess.com/game/daily/195452148"]
[SetUp "1"]
[StartTime "21:40:36"]
[Termination "FlashCP3 won by resignation"]
[TimeControl "1/86400"]
[Timezone "UTC"]
[UTCDate "2018.05.23"]
[UTCTime "21:40:36"]
[WhiteElo "1397"]

6. e3 Nf5 ( { Refutation (-5.1 vs. -0.93 in solution) } 6... Qh4 7. exd4 ) 1-0""",
        "probability_loss": -0.29299110755486085,
        "refutations": [[["d8", "h4"], ["e3", "d4"]]],
        "solution": [["d4", "f5"]],
        "starting_fen": "r1bqk1nr/pppp1ppp/8/3Pp3/2Pn4/8/PP1QPPPP/RN2KBNR w KQkq - 1 6",
    },
    "job_name": "bg3excLCIAMCFkw=",
}

snapshots["test_blunders_worker[event1] 3"] = {
    "connection_id": {"Type": "String", "Value": "bg3excLCIAMCFkw="}
}

snapshots["test_get_blunders[event0] 1"] = {
    "body": """[
  {
    "starting_fen": "3r2k1/7p/4rp2/8/1PR2P2/8/3p1KPP/3R4 w - - 0 28",
    "pgn": "[Event \\"Let\'s Play!\\"]\\n[Site \\"Chess.com\\"]\\n[Date \\"2019.01.28\\"]\\n[Round \\"-\\"]\\n[White \\"Paul6336\\"]\\n[Black \\"ludavics\\"]\\n[Result \\"1-0\\"]\\n[BlackElo \\"1378\\"]\\n[CurrentPosition \\"3r2k1/7p/5p2/5P2/1P2R3/8/3p1KPP/3R4 b - - 0 29\\"]\\n[ECO \\"D30\\"]\\n[ECOUrl \\"https://www.chess.com/openings/Queens-Gambit-Declined\\"]\\n[EndDate \\"2019.02.12\\"]\\n[EndTime \\"21:16:58\\"]\\n[FEN \\"3r2k1/7p/4rp2/8/1PR2P2/8/3p1KPP/3R4 w - - 0 28\\"]\\n[Link \\"https://www.chess.com/game/daily/217107360\\"]\\n[SetUp \\"1\\"]\\n[StartTime \\"16:38:57\\"]\\n[Termination \\"Paul6336 won by resignation\\"]\\n[TimeControl \\"1/259200\\"]\\n[Timezone \\"UTC\\"]\\n[UTCDate \\"2019.01.28\\"]\\n[UTCTime \\"16:38:57\\"]\\n[WhiteElo \\"1464\\"]\\n\\n28. f5 Re5 ( { Refutation (-8.81 vs. 0.0 in solution) } 28... Re4 29. Rxe4 Rd5 30. Rg4+ Kf7 31. Rf4 Rd3 32. Ke2 Rb3 33. Rxd2 Kg7 34. Kd1 Kh6 35. Kc2 Kg5 36. Kxb3 Kxf4 37. Rd5 Ke4 38. Kc4 h5 39. b5 Ke3 ) 29. Rc2 Rxf5+ 30. Ke3 Re5+ 31. Kf3 Rd3+ 32. Kf2 Rd4 33. Rb2 Rb5 34. Kg3 Rd3+ 35. Kf2 1-0",
    "solution": [
      [
        "e6",
        "e5"
      ],
      [
        "c4",
        "c2"
      ],
      [
        "e5",
        "f5"
      ],
      [
        "f2",
        "e3"
      ],
      [
        "f5",
        "e5"
      ],
      [
        "e3",
        "f3"
      ],
      [
        "d8",
        "d3"
      ],
      [
        "f3",
        "f2"
      ],
      [
        "d3",
        "d4"
      ],
      [
        "c2",
        "b2"
      ],
      [
        "e5",
        "b5"
      ],
      [
        "f2",
        "g3"
      ],
      [
        "d4",
        "d3"
      ],
      [
        "g3",
        "f2"
      ]
    ],
    "refutations": [
      [
        [
          "e6",
          "e4"
        ],
        [
          "c4",
          "e4"
        ],
        [
          "d8",
          "d5"
        ],
        [
          "e4",
          "g4"
        ],
        [
          "g8",
          "f7"
        ],
        [
          "g4",
          "f4"
        ],
        [
          "d5",
          "d3"
        ],
        [
          "f2",
          "e2"
        ],
        [
          "d3",
          "b3"
        ],
        [
          "d1",
          "d2"
        ],
        [
          "f7",
          "g7"
        ],
        [
          "e2",
          "d1"
        ],
        [
          "g7",
          "h6"
        ],
        [
          "d1",
          "c2"
        ],
        [
          "h6",
          "g5"
        ],
        [
          "c2",
          "b3"
        ],
        [
          "g5",
          "f4"
        ],
        [
          "d2",
          "d5"
        ],
        [
          "f4",
          "e4"
        ],
        [
          "b3",
          "c4"
        ],
        [
          "h7",
          "h5"
        ],
        [
          "b4",
          "b5"
        ],
        [
          "e4",
          "e3"
        ]
      ]
    ],
    "cp_loss": -881.0,
    "probability_loss": -0.4714
  }
]""",
    "statusCode": 200,
}

snapshots["test_get_blunders[event1] 1"] = {
    "body": """[
  {
    "starting_fen": "r4rk1/4bpp1/1nq4p/pp1p4/2pP4/P1N1PB1P/1P3PP1/R2Q1RK1 w - - 0 19",
    "pgn": "[Event \\"Live Chess\\"]\\n[Site \\"Chess.com\\"]\\n[Date \\"2020.08.26\\"]\\n[Round \\"-\\"]\\n[White \\"abel79\\"]\\n[Black \\"ludavics\\"]\\n[Result \\"0-1\\"]\\n[BlackElo \\"984\\"]\\n[CurrentPosition \\"8/5k2/6pp/3P4/7P/1K4P1/5P2/3q4 w - -\\"]\\n[ECO \\"D30\\"]\\n[ECOUrl \\"https://www.chess.com/openings/Queens-Gambit-Declined\\"]\\n[EndDate \\"2020.08.26\\"]\\n[EndTime \\"22:35:19\\"]\\n[FEN \\"r4rk1/4bpp1/1nq4p/pp1p4/2pP4/P1N1PB1P/1P3PP1/R2Q1RK1 w - - 0 19\\"]\\n[Link \\"https://www.chess.com/live/game/5355534259\\"]\\n[SetUp \\"1\\"]\\n[StartTime \\"22:25:13\\"]\\n[Termination \\"ludavics won on time\\"]\\n[TimeControl \\"300\\"]\\n[Timezone \\"UTC\\"]\\n[UTCDate \\"2020.08.26\\"]\\n[UTCTime \\"22:25:13\\"]\\n[WhiteElo \\"949\\"]\\n\\n19. e4 Qd7 ( { Refutation (-2.97 vs. -0.02 in solution) } 19... dxe4 20. Bxe4 ) 0-1",
    "solution": [
      [
        "c6",
        "d7"
      ]
    ],
    "refutations": [
      [
        [
          "d5",
          "e4"
        ],
        [
          "f3",
          "e4"
        ]
      ]
    ],
    "cp_loss": -295.0,
    "probability_loss": -0.2644
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

snapshots["test_http_validation_error[event0] 1"] = {
    "body": """[
  {
    "loc": [
      "job_name"
    ],
    "msg": "field required",
    "type": "value_error.missing"
  }
]""",
    "statusCode": 400,
}
