import os
import boto3

def get_table(dynamodb_resource=None):
    """
    Returns the DynamoDB table instance.
    If dynamodb_resource is provided, it uses that (mock in tests).
    Otherwise, it uses the real DynamoDB from boto3.
    """
    if not dynamodb_resource:
        dynamodb_resource = boto3.resource("dynamodb")
    return dynamodb_resource.Table(os.environ["EXPENSES_TABLE"])
