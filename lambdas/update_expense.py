import json
import os
import boto3
from decimal import Decimal

from utils.dynamodb_utils import get_table

def update_expense(table, expense_data):
    """
    Core logic to update an expense in DynamoDB.
    Separated from the handler for easier testing with a mock.
    """
    expense_id = expense_data["expense_id"]
    update_expr = "SET "
    expr_attr_vals = {}

    for k, v in expense_data.items():
        if k != "expense_id":
            update_expr += f"{k} = :{k}, "
            expr_attr_vals[f":{k}"] = Decimal(str(v)) if k == "amount" else v

    update_expr = update_expr.rstrip(", ")

    table.update_item(
        Key={"expense_id": expense_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_vals
    )
    return expense_id

def handler(event, context, table=None):
    """
    Lambda handler. You can optionally pass a table (for testing).
    """
    body_str = event.get("body", "{}")
    body = json.loads(body_str) if isinstance(body_str, str) else body_str

    if table is None:
        table = get_table()

    expense_id = update_expense(table, body)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Expense updated", "expense_id": expense_id})
    }
