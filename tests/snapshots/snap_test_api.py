# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_blunders_to_db[event0] 1"] = {
    "cp_loss": "-862.0",
    "job_name": "beUJ2csbIAMCLUg=",
    "pgn": "18... Qh4 { [%clk 0:02:50.9] } 19. Qxb7 { [%clk 0:01:03.6] } ( { Refutation (-567) } 19. Qxb7 Rd6 ) ( { Solution (295) } 19. f3 Nf6 ) 19... Ndxf2 { [%clk 0:02:41.3] } 20. Qxa7 { [%clk 0:00:55.8] } 20... Nxh3+ { [%clk 0:02:27.4] } 21. gxh3 { [%clk 0:00:41.8] } 21... Qxh3 { [%clk 0:02:22.5] } 22. Rf2 { [%clk 0:00:35.3] } 22... Nxf2 { [%clk 0:02:09.6] } 23. Qxf2 { [%clk 0:00:32.9] } 23... Qg4+ { [%clk 0:01:54.4] } 24. Qg2 { [%clk 0:00:29] } 24... Qd1+ { [%clk 0:01:51.6] } 25. Qf1 { [%clk 0:00:20.6] } 25... Qg4+ { [%clk 0:01:35.2] } 26. Qg2 { [%clk 0:00:19.6] } 26... Qf4 { [%clk 0:01:30.6] } 27. d4 { [%clk 0:00:16.9] } 27... exd4 { [%clk 0:01:28.4] } 28. cxd4 { [%clk 0:00:15.4] } 28... Rxd4 { [%clk 0:01:26.6] } 29. b5 { [%clk 0:00:14.9] } 29... Rd1+ { [%clk 0:01:24.9] } 30. Qf1 { [%clk 0:00:10.7] } 30... Qxf1# { [%clk 0:01:23.7] }",
    "probability_loss": "-0.6711",
    "starting_fen": "3r1rk1/pQ3ppp/8/4p3/PP2P1nq/2Pn3N/3P1PPP/RN3RK1 b - - 0 19",
}

snapshots["test_blunders_to_db[event0] 2"] = {
    "ConsumedCapacity": {"CapacityUnits": 1, "TableName": "test-blunders-table"},
    "Count": 1,
    "Items": [
        {
            "cp_loss": "-862.0",
            "created_at": "2021-01-27T00:00:00",
            "job_name": "beUJ2csbIAMCLUg=",
            "pgn": "18... Qh4 { [%clk 0:02:50.9] } 19. Qxb7 { [%clk 0:01:03.6] } ( { Refutation (-567) } 19. Qxb7 Rd6 ) ( { Solution (295) } 19. f3 Nf6 ) 19... Ndxf2 { [%clk 0:02:41.3] } 20. Qxa7 { [%clk 0:00:55.8] } 20... Nxh3+ { [%clk 0:02:27.4] } 21. gxh3 { [%clk 0:00:41.8] } 21... Qxh3 { [%clk 0:02:22.5] } 22. Rf2 { [%clk 0:00:35.3] } 22... Nxf2 { [%clk 0:02:09.6] } 23. Qxf2 { [%clk 0:00:32.9] } 23... Qg4+ { [%clk 0:01:54.4] } 24. Qg2 { [%clk 0:00:29] } 24... Qd1+ { [%clk 0:01:51.6] } 25. Qf1 { [%clk 0:00:20.6] } 25... Qg4+ { [%clk 0:01:35.2] } 26. Qg2 { [%clk 0:00:19.6] } 26... Qf4 { [%clk 0:01:30.6] } 27. d4 { [%clk 0:00:16.9] } 27... exd4 { [%clk 0:01:28.4] } 28. cxd4 { [%clk 0:00:15.4] } 28... Rxd4 { [%clk 0:01:26.6] } 29. b5 { [%clk 0:00:14.9] } 29... Rd1+ { [%clk 0:01:24.9] } 30. Qf1 { [%clk 0:00:10.7] } 30... Qxf1# { [%clk 0:01:23.7] }",
            "probability_loss": "-0.6711",
            "starting_fen": "3r1rk1/pQ3ppp/8/4p3/PP2P1nq/2Pn3N/3P1PPP/RN3RK1 b - - 0 19",
        }
    ],
    "ScannedCount": 1,
}

snapshots["test_blunders_to_db[event1] 1"] = {
    "cp_loss": "-533.0",
    "job_name": "beUJ2csbIAMCLUg=",
    "pgn": "9... Qxd4 { [%clk 0:04:20.1] } 10. Nb5 { [%clk 0:04:30.1] } ( { Refutation (-388) } 10. Nb5 Qe5+ ) ( { Solution (145) } 10. f4 e6 ) 10... Qd5 { [%clk 0:04:15.9] } 11. Nxc7+ { [%clk 0:04:28.6] } 11... Kd8 { [%clk 0:04:07.3] } 12. Nxd5 { [%clk 0:04:28.5] } 12... e6 { [%clk 0:03:59.9] } 13. Nf4 { [%clk 0:04:21.2] } 13... Be7 { [%clk 0:03:50.3] } 14. Nxg6 { [%clk 0:04:18.2] } 14... hxg6 { [%clk 0:03:48.6] } 15. Qf3 { [%clk 0:04:11.6] } 15... Rb8 { [%clk 0:03:43.7] } 16. O-O-O { [%clk 0:04:10.4] } 16... Nf6 { [%clk 0:03:37.4] } 17. Ba5+ { [%clk 0:03:35.6] } 17... b6 { [%clk 0:03:33.4] } 18. Bc3 { [%clk 0:03:23.4] } 18... Nd5 { [%clk 0:03:28.5] } 19. Bxg7 { [%clk 0:03:20.4] } 19... Rh7 { [%clk 0:03:24.4] } 20. Be5 { [%clk 0:03:14] } 20... Bg5+ { [%clk 0:03:19.9] } 21. Kb1 { [%clk 0:03:07.6] } 21... Rc8 { [%clk 0:03:15.5] } 22. Qg3 { [%clk 0:02:40.7] } 22... Nb4 { [%clk 0:03:08] } 23. c3 { [%clk 0:02:37.3] } 23... Nc6 { [%clk 0:02:55] } 24. f4 { [%clk 0:02:31.8] } 24... Bh4 { [%clk 0:02:48.8] } 25. Qe3 { [%clk 0:02:24] } 25... g5 { [%clk 0:02:27.1] } 26. f5 { [%clk 0:02:17.4] } 26... Rh6 { [%clk 0:02:16.3] } 27. d4 { [%clk 0:01:51.1] } 27... exf5 { [%clk 0:02:09.9] } 28. d5 { [%clk 0:01:38.7] } 28... Nxe5 { [%clk 0:02:01.7] } 29. Qxe5 { [%clk 0:01:34.9] } 29... fxg4 { [%clk 0:01:56.3] } 30. d6 { [%clk 0:01:21.9] } 30... Rc5 { [%clk 0:01:37.1] } 31. Qe7+ { [%clk 0:01:16.6] } 31... Kc8 { [%clk 0:01:33.6] } 32. d7+ { [%clk 0:01:13] } 32... Kc7 { [%clk 0:01:26.3] } 33. d8=Q+ { [%clk 0:01:07.2] } 33... Kc6 { [%clk 0:01:24.5] } 34. Qde8# { [%clk 0:00:48] }",
    "probability_loss": "-0.4663",
    "starting_fen": "r3kbnr/ppp1pppp/6b1/1N6/3q2P1/3P3P/PPPB1P2/R2QKB1R b KQkq - 1 10",
}

snapshots["test_blunders_to_db[event1] 2"] = {
    "ConsumedCapacity": {"CapacityUnits": 1, "TableName": "test-blunders-table"},
    "Count": 1,
    "Items": [
        {
            "cp_loss": "-533.0",
            "created_at": "2021-01-27T00:00:00",
            "job_name": "beUJ2csbIAMCLUg=",
            "pgn": "9... Qxd4 { [%clk 0:04:20.1] } 10. Nb5 { [%clk 0:04:30.1] } ( { Refutation (-388) } 10. Nb5 Qe5+ ) ( { Solution (145) } 10. f4 e6 ) 10... Qd5 { [%clk 0:04:15.9] } 11. Nxc7+ { [%clk 0:04:28.6] } 11... Kd8 { [%clk 0:04:07.3] } 12. Nxd5 { [%clk 0:04:28.5] } 12... e6 { [%clk 0:03:59.9] } 13. Nf4 { [%clk 0:04:21.2] } 13... Be7 { [%clk 0:03:50.3] } 14. Nxg6 { [%clk 0:04:18.2] } 14... hxg6 { [%clk 0:03:48.6] } 15. Qf3 { [%clk 0:04:11.6] } 15... Rb8 { [%clk 0:03:43.7] } 16. O-O-O { [%clk 0:04:10.4] } 16... Nf6 { [%clk 0:03:37.4] } 17. Ba5+ { [%clk 0:03:35.6] } 17... b6 { [%clk 0:03:33.4] } 18. Bc3 { [%clk 0:03:23.4] } 18... Nd5 { [%clk 0:03:28.5] } 19. Bxg7 { [%clk 0:03:20.4] } 19... Rh7 { [%clk 0:03:24.4] } 20. Be5 { [%clk 0:03:14] } 20... Bg5+ { [%clk 0:03:19.9] } 21. Kb1 { [%clk 0:03:07.6] } 21... Rc8 { [%clk 0:03:15.5] } 22. Qg3 { [%clk 0:02:40.7] } 22... Nb4 { [%clk 0:03:08] } 23. c3 { [%clk 0:02:37.3] } 23... Nc6 { [%clk 0:02:55] } 24. f4 { [%clk 0:02:31.8] } 24... Bh4 { [%clk 0:02:48.8] } 25. Qe3 { [%clk 0:02:24] } 25... g5 { [%clk 0:02:27.1] } 26. f5 { [%clk 0:02:17.4] } 26... Rh6 { [%clk 0:02:16.3] } 27. d4 { [%clk 0:01:51.1] } 27... exf5 { [%clk 0:02:09.9] } 28. d5 { [%clk 0:01:38.7] } 28... Nxe5 { [%clk 0:02:01.7] } 29. Qxe5 { [%clk 0:01:34.9] } 29... fxg4 { [%clk 0:01:56.3] } 30. d6 { [%clk 0:01:21.9] } 30... Rc5 { [%clk 0:01:37.1] } 31. Qe7+ { [%clk 0:01:16.6] } 31... Kc8 { [%clk 0:01:33.6] } 32. d7+ { [%clk 0:01:13] } 32... Kc7 { [%clk 0:01:26.3] } 33. d8=Q+ { [%clk 0:01:07.2] } 33... Kc6 { [%clk 0:01:24.5] } 34. Qde8# { [%clk 0:00:48] }",
            "probability_loss": "-0.4663",
            "starting_fen": "r3kbnr/ppp1pppp/6b1/1N6/3q2P1/3P3P/PPPB1P2/R2QKB1R b KQkq - 1 10",
        }
    ],
    "ScannedCount": 1,
}

snapshots["test_blunders_worker[event0] 1"] = [
    {
        "cp_loss": -100644.0,
        "pgn": "30... Kg8 { [%clk 0:01:21.2] } 31. Rd3 { [%clk 0:00:03.3] } ( { Refutation (-99998) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) ( { Solution (646) } 31. h3 Rf8 ) 31... Ra1+ { [%clk 0:01:21.4] }",
        "probability_loss": -0.9298247211092094,
        "starting_fen": "r5k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/6K1 b - - 5 31",
    }
]

snapshots["test_blunders_worker[event0] 2"] = {
    "blunder": {
        "cp_loss": -100644.0,
        "pgn": "30... Kg8 { [%clk 0:01:21.2] } 31. Rd3 { [%clk 0:00:03.3] } ( { Refutation (-99998) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) ( { Solution (646) } 31. h3 Rf8 ) 31... Ra1+ { [%clk 0:01:21.4] }",
        "probability_loss": -0.9298247211092094,
        "starting_fen": "r5k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/6K1 b - - 5 31",
    },
    "job_name": "morning-tree-0821",
}

snapshots["test_blunders_worker[event0] 3"] = {
    "connection_id": {"Type": "String", "Value": "None"}
}

snapshots["test_get_blunders[event0] 1"] = {
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

snapshots["test_get_blunders[event1] 1"] = {
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
