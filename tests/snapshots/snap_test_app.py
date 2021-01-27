# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_get_root 1"] = [
    {"path": "/openapi.json"},
    {"path": "/docs"},
    {"path": "/docs/oauth2-redirect"},
    {"path": "/redoc"},
    {"path": "/"},
    {"path": "/games/chessdotcom/{username}"},
]
