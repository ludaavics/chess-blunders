import asyncio
import json

import wrapt


# ------------------------------------------------------------------------------------ #
#                                        Helpers                                       #
# ------------------------------------------------------------------------------------ #
def jsonify(status_code, data, message):
    body = {"data": data, "message": message}
    return {"statusCode": status_code, "body": json.dumps(body, indent=2)}


@wrapt.decorator
def async_handler(handler, instance, args, kwargs):
    return asyncio.run(handler(*args, **kwargs))


# ------------------------------------------------------------------------------------ #
#                                       Handlers                                       #
# ------------------------------------------------------------------------------------ #
@async_handler
async def get_games_chessdotcom(event, context):
    """
    Get all the games from a chess.com user.
    """
    username = event["pathParameters"]["username"]
    return jsonify(200, "", f"Get chess.com games from {username}")


@async_handler
async def blunders(event, context):
    """
    Create puzzles from blunders in a list of games.
    """
    data = json.loads(event.get("body", "{}"))
    return jsonify(200, data, "Create puzzles from data.")
