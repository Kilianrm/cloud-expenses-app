import json
import os
import boto3
import uuid
from datetime import datetime
from decimal import Decimal
from utils.dynamodb_utils import get_table
from datetime import datetime, timezone


def create_expense(table, body):
    """
    Core logic to create an expense in DynamoDB.
    Separated from the handler to allow testing with a mock table.
    """
    expense_id = str(uuid.uuid4())
    item = {
        "expense_id": expense_id,
        "user_id": body.get("user_id", "test_user"),
        "amount": Decimal(str(body["amount"])),
        "category": body.get("category", "general"),
        "description": body.get("description", ""),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    table.put_item(Item=item)
    return expense_id

def handler(event, context, table=None):
    """
    Lambda handler. You can optionally pass a table (for testing).
    """
    # Parse body
    body = json.loads(event.get("body", "{}")) if isinstance(event.get("body"), str) else event

    # Use provided table or get the real one
    if table is None:
        table = get_table()

    # Create expense
    expense_id = create_expense(table, body)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Expense created", "expense_id": expense_id})
    }
