# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

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
