import json
import os
import boto3
from decimal import Decimal
from utils.dynamodb_utils import get_table

def fetch_expenses(table, user_id="test_user"):
    """
    Core logic to fetch expenses from DynamoDB.
    Separated from the handler for easier testing with a mock.
    """
    response = table.scan(
        FilterExpression="user_id = :uid",
        ExpressionAttributeValues={":uid": user_id}
    )

    items = response.get("Items", [])
    # Convert Decimals to float for JSON serialization
    for item in items:
        if "amount" in item and isinstance(item["amount"], Decimal):
            item["amount"] = float(item["amount"])
    return items

def handler(event, context, table=None):
    """
    Lambda handler. You can optionally pass a table (for testing).
    """
    # Parse body
    body = json.loads(event.get("body", "{}")) if isinstance(event.get("body"), str) else event
    user_id = body.get("user_id", "test_user")

    # Use provided table or get the real one
    if table is None:
        table = get_table()

    items = fetch_expenses(table, user_id)

    return {
        "statusCode": 200,
        "body": json.dumps(items)
    }
