# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_known_blunders 1"] = [
    {
        "cp_loss": -462.0,
        "pgn": "12... Nc4 { [%clk 0:01:56.1] } 13. Nxd5 { [%clk 0:02:22.5] } ( { Solution (+632) } 13. dxc5 ) ( { Refutation (+170) } 13. Nxd5 Nb6 ) 13... Nb6 { [%clk 0:01:10.1] } 14. Nxb6 { [%clk 0:02:15.4] } 14... axb6 { [%clk 0:01:10.5] } 15. Qb5 { [%clk 0:02:09.8] } 15... Ra5 { [%clk 0:01:05.5] } 16. Qe2 { [%clk 0:01:42.5] } 16... Qxd7 { [%clk 0:01:05.9] } 17. Rd1 { [%clk 0:01:43.9] } 17... cxd4 { [%clk 0:01:01.3] } 18. Rxd4 { [%clk 0:01:42.7] } 18... Qc6 { [%clk 0:00:51.3] } 19. Bd2 { [%clk 0:01:37.6] } 19... Raa8 { [%clk 0:00:48.7] } 20. Rc1 { [%clk 0:01:34.4] } 20... Qe6 { [%clk 0:00:39.8] } 21. a3 { [%clk 0:01:30.6] } 21... Bc5 { [%clk 0:00:34] } 22. Rdc4 { [%clk 0:01:12] } 22... b5 { [%clk 0:00:28.1] } 23. Rxc5 { [%clk 0:01:09.4] } 23... b6 { [%clk 0:00:28] } 24. Rc6 { [%clk 0:01:08.4] } 24... Qa2 { [%clk 0:00:22.9] } 25. Qxb5 { [%clk 0:01:03.6] } 25... Rad8 { [%clk 0:00:18.3] } 26. Bb4 { [%clk 0:01:00.3] } 26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.2623428636014692,
        "starting_fen": "r2q1rk1/pp1Bbppp/8/2pp4/Q1nP4/2N1P3/PP3PPP/R1B2RK1 w - - 1 13",
    },
    {
        "cp_loss": -857.0,
        "pgn": "26... Qxb2 { [%clk 0:00:15.9] } 27. Bxf8 { [%clk 0:01:00.6] } ( { Solution (+773) } 27. Qc4 ) ( { Refutation (-84) } 27. Bxf8 Qxb5 ) 27... Qd2 { [%clk 0:00:10.5] } 28. Bb4 { [%clk 0:00:46.9] } 28... Qd1+ { [%clk 0:00:10.2] } 29. Be1 { [%clk 0:00:40.5] }",
        "probability_loss": -0.5397800931666645,
        "starting_fen": "3r1rk1/5ppp/1pR5/1Q6/1B6/P3P3/1q3PPP/2R3K1 w - - 0 27",
    },
]
