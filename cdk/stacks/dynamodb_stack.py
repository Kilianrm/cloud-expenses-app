from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy
)
from constructs import Construct

class DynamoDBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the Expenses table
        self.expenses_table = dynamodb.Table(
            self, "ExpensesTable",
            table_name="Expenses",
            partition_key=dynamodb.Attribute(
                name="expense_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # Use RETAIN in production
        )

        # Global Secondary Index for user + category (filter by category)
        self.expenses_table.add_global_secondary_index(
            index_name="user_category_index",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="category",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        # Global Secondary Index for user + date (filter by month/year)
        self.expenses_table.add_global_secondary_index(
            index_name="user_date_index",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="date",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        # Optionally, you could define additional attributes like:
        # - amount (Number)
        # - currency (String)
        # - description (String)
        # - created_at / updated_at (String)
