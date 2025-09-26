import json
from decimal import Decimal
from lambdas import delete_expense as de

def test_delete_expense(mock_dynamodb_table):
    """Test deleting an existing expense."""

    # First, insert an expense into the mock table
    initial_item = {
        "expense_id": "exp1",
        "user_id": "test_user",
        "amount": Decimal("20.0"),
        "category": "food",
        "description": "Lunch"
    }
    mock_dynamodb_table.put_item(Item=initial_item)

    # Verify the item exists
    item = mock_dynamodb_table.get_item(Key={"expense_id": "exp1"})["Item"]
    assert item["expense_id"] == "exp1"

    # Call the core delete function directly
    deleted_id = de.delete_expense(mock_dynamodb_table, "exp1")
    assert deleted_id == "exp1"

    # Check that the item no longer exists
    response = mock_dynamodb_table.get_item(Key={"expense_id": "exp1"})
    assert "Item" not in response or response["Item"] is None

    # Now test the handler
    event = {"body": json.dumps({"expense_id": "exp1"})}

    # First, re-insert the item to test the handler
    mock_dynamodb_table.put_item(Item=initial_item)
    response = de.handler(event, None, table=mock_dynamodb_table)
    body = json.loads(response["body"])
    assert response["statusCode"] == 200
    assert body["message"] == "Expense deleted"
    assert body["expense_id"] == "exp1"

    # Verify it was deleted by the handler
    response = mock_dynamodb_table.get_item(Key={"expense_id": "exp1"})
    assert "Item" not in response or response["Item"] is None
