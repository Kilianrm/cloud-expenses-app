import json
from decimal import Decimal
from lambdas import update_expense as ue

def test_update_expense(mock_dynamodb_table):
    """Test updating an existing expense."""

    # First, insert an expense into the mock table
    initial_item = {
        "expense_id": "exp1",
        "user_id": "test_user",
        "amount": Decimal("20.0"),
        "category": "food",
        "description": "Lunch"
    }
    mock_dynamodb_table.put_item(Item=initial_item)

    # Prepare update data
    update_data = {
        "expense_id": "exp1",
        "amount": 25.5,
        "description": "Updated Lunch"
    }

    # Call the core function directly
    expense_id = ue.update_expense(mock_dynamodb_table, update_data)
    assert expense_id == "exp1"

    # Check that the item was updated in the table
    item = mock_dynamodb_table.get_item(Key={"expense_id": "exp1"})["Item"]
    assert item["amount"] == Decimal("25.5")
    assert item["description"] == "Updated Lunch"
    assert item["user_id"] == "test_user"  # unchanged
    assert item["category"] == "food"      # unchanged

    # Now test the handler
    event = {"body": json.dumps(update_data)}
    response = ue.handler(event, None, table=mock_dynamodb_table)
    body = json.loads(response["body"])
    assert response["statusCode"] == 200
    assert body["message"] == "Expense updated"
    assert body["expense_id"] == "exp1"
