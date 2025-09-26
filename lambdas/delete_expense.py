import json
import os
import boto3

from utils.dynamodb_utils import get_table

def delete_expense(table, expense_id):
    """
    Core logic to delete an expense in DynamoDB.
    Separated from the handler to allow testing with a mock table.
    """
    table.delete_item(Key={"expense_id": expense_id})
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

    # Delete expense
    expense_id = body["expense_id"]
    delete_expense(table, expense_id)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Expense deleted", "expense_id": expense_id})
    }
