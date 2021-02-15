# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_post_blunders[post_blunders_event0] 1"] = {
    "body": """[
  {
    "starting_fen": "r5k1/6p1/2p3Q1/1pqnp2p/8/1BPR4/1PP2PPP/6K1 b - - 5 31",
    "pgn": "30... Kg8 { [%clk 0:01:21.2] } 31. Rd3 { [%clk 0:00:03.3] } ( { Refutation (-99998) } 31. Rd3 Ra1+ 32. Rd1 Rxd1# ) ( { Solution (646) } 31. h3 Rf8 ) 31... Ra1+ { [%clk 0:01:21.4] }",
    "cp_loss": -100644.0,
    "probability_loss": -0.9298247211092094
  }
]""",
    "statusCode": 200,
}
