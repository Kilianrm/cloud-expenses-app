#!/usr/bin/env python3
from aws_cdk import App
from stacks.dynamodb_stack import DynamoDBStack
from stacks.backend_stack import BackendStack  # tu stack de Lambdas + API

app = App()

# Crear la tabla DynamoDB
dynamo_stack = DynamoDBStack(app, "DynamoDBStack")

# Crear el stack de Lambdas + API Gateway, pasándole la tabla
backend_stack = BackendStack(app, "BackendStack", expenses_table=dynamo_stack.expenses_table)

app.synth()
