"""
CreateFunction
"""


import json
import os
from typing import List, Optional, Union, Set
import boto3
from boto3.dynamodb.types import TypeDeserializer
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.logging.logger import Logger
from ecom.apigateway import iam_user_id, response # pylint: disable=import-error


ENVIRONMENT = os.environ["ENVIRONMENT"]
TABLE_NAME = os.environ["TABLE_NAME"]


dyn_resource = boto3.resource("dynamodb") # pylint: disable=invalid-name
logger = Logger() # pylint: disable=invalid-name
tracer = Tracer() # pylint: disable=invalid-name
type_deserializer = TypeDeserializer() # pylint: disable=invalid-name


@tracer.capture_method
def create(product: dict) -> dict:
    table = dyn_resource.Table(TABLE_NAME)
    table.put_item(Item=product)
    return {}


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, _):
    """
    Lambda function handler for /backend/create
    """

    try:
        body = json.loads(event["body"])
    except Exception as exc: # pylint: disable=broad-except
        logger.warning("Exception caught: %s", exc)
        return response("Failed to parse JSON body", 400)

    create(body)

    return response({'success': True})
