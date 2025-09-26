from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, expenses_table: dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda to create an expense
        create_expense_lambda = _lambda.Function(
            self, "CreateExpenseLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="create_expense.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"EXPENSES_TABLE": expenses_table.table_name}
        )

        # Lambda to list expenses
        list_expenses_lambda = _lambda.Function(
            self, "ListExpensesLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="list_expenses.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"EXPENSES_TABLE": expenses_table.table_name}
        )

        # Lambda to update an expense
        update_expense_lambda = _lambda.Function(
            self, "UpdateExpenseLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="update_expense.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"EXPENSES_TABLE": expenses_table.table_name}
        )

        # Lambda to delete an expense
        delete_expense_lambda = _lambda.Function(
            self, "DeleteExpenseLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="delete_expense.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"EXPENSES_TABLE": expenses_table.table_name}
        )

        # Permissions for accessing the table
        expenses_table.grant_read_write_data(create_expense_lambda)
        expenses_table.grant_read_data(list_expenses_lambda)
        expenses_table.grant_read_write_data(update_expense_lambda)
        expenses_table.grant_read_write_data(delete_expense_lambda)

        # API Gateway REST
        api = apigateway.RestApi(
            self, "ExpensesApi",
            rest_api_name="Expenses Service",
            description="API to manage expenses"
        )

        expenses = api.root.add_resource("expenses")
        expenses.add_method("POST", apigateway.LambdaIntegration(create_expense_lambda))
        expenses.add_method("GET", apigateway.LambdaIntegration(list_expenses_lambda))
        expenses.add_method("PUT", apigateway.LambdaIntegration(update_expense_lambda))
        expenses.add_method("DELETE", apigateway.LambdaIntegration(delete_expense_lambda))
