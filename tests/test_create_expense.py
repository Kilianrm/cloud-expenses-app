import json
from decimal import Decimal
import pytest
from lambdas import create_expense as ce



def test_create_expense_core(mock_dynamodb_table):
    body = {
        "user_id": "user123",
        "amount": 42.5,
        "category": "food",
        "description": "Lunch"
    }

    expense_id = ce.create_expense(mock_dynamodb_table, body)

    # Check that the item exists in the mocked table
    item = mock_dynamodb_table.get_item(Key={"expense_id": expense_id})["Item"]
    assert item["expense_id"] == expense_id
    assert item["user_id"] == "user123"
    assert item["amount"] == 42.5 or item["amount"] == Decimal("42.5")
    assert item["category"] == "food"
    assert item["description"] == "Lunch"

    

def test_create_multiple_expenses(mock_dynamodb_table):
    """Insert multiple expenses and check they are all stored correctly."""

    # Generar 10 eventos con datos ligeramente diferentes
    for i in range(10):
        event = {
            "body": json.dumps({
                "user_id": f"user{i}",
                "amount": 10 + i,  # amounts: 10, 11, ..., 19
                "category": "food" if i % 2 == 0 else "drink",
                "description": f"Item {i}"
            })
        }

        response = ce.handler(event, None, table=mock_dynamodb_table)
        body = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert "expense_id" in body

        # Check the item exists in the mock table
        item = mock_dynamodb_table.get_item(Key={"expense_id": body["expense_id"]})["Item"]
        assert item["user_id"] == f"user{i}"
        assert item["amount"] == 10 + i or item["amount"] == Decimal(str(10 + i))
        assert item["category"] == ("food" if i % 2 == 0 else "drink")
        assert item["description"] == f"Item {i}"