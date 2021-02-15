import json


def _jsonify(status_code, data, message):
    body = {"data": data, "message": message}
    return {"statusCode": status_code, "body": json.dumps(body, indent=2)}


def get_games_chessdotcom(event, context):
    """
    Get all the games from a chess.com user.
    """
    username = event["pathParameters"]["username"]
    return _jsonify(200, "", f"Get chess.com games from {username}")


def blunders(event, context):
    """
    Create puzzles from blunders in a list of games.
    """
    data = json.loads(event.get("body", "{}"))
    return _jsonify(200, data, "Create puzzles from data.")
