import json
from decimal import Decimal
from lambdas import list_expenses as le


def test_fetch_expenses(mock_dynamodb_table):
    """Test fetching expenses for a user."""

    # First, insert some expenses into the mock table
    for i in range(5):
        item = {
            "expense_id": f"exp{i}",
            "user_id": "test_user",
            "amount": Decimal(str(10 + i)),
            "category": "food" if i % 2 == 0 else "drink",
            "description": f"Item {i}"
        }
        mock_dynamodb_table.put_item(Item=item)

    # Fetch expenses using the core function
    items = le.fetch_expenses(mock_dynamodb_table, user_id="test_user")
    assert len(items) == 5
    for i, item in enumerate(items):
        assert item["user_id"] == "test_user"
        assert item["amount"] == 10 + i  # converted to float by fetch_expenses
        assert item["category"] == ("food" if i % 2 == 0 else "drink")
        assert item["description"] == f"Item {i}"

    # Fetch expenses using the handler
    event = {"body": json.dumps({"user_id": "test_user"})}
    response = le.handler(event, None, table=mock_dynamodb_table)
    body = json.loads(response["body"])
    assert len(body) == 5
    for i, item in enumerate(body):
        assert item["user_id"] == "test_user"
        assert item["amount"] == 10 + i
        assert item["category"] == ("food" if i % 2 == 0 else "drink")
        assert item["description"] == f"Item {i}"
