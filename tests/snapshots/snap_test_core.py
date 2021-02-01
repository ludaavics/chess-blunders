# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_known_blunders 1"] = [
    {
        "cp_loss": -836.0,
        "pgn": "26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } ( { Solution (787) } 27. a4 ) ( { Refutation (-49) } 27. Bxf8 Qxb5 ) 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.51,
        "starting_fen": "3r1rk1/5ppp/1pR5/1Q6/1B6/P3P3/1q3PPP/2R3K1 w - - 0 27",
    }
]
