import pytest
import aws_cdk as cdk
from aws_cdk.assertions import Template, Match
from stacks.microservice_stack import MicroserviceStack


def synthesize_stack(context):
    """
    Helper function to synthesize a CDK stack with a specific, 
    in-memory context. This allows us to test different 
    feature flag combinations.
    """
    app = cdk.App(context=context)
    stack = MicroserviceStack(
        app,
        context["stack_name"]
    )
    return Template.from_stack(stack)


@pytest.fixture
def base_context():
    """
    A 'default' context fixture that all tests can use.
    By default, all optional features are disabled.
    """
    return {
        "service_name": "test-service",
        "stack_name": "TestServiceStack",
        "include_dynamodb": "false",
        "include_sqs": "false"
    }

def test_lambda_created(base_context):
    """
    Tests that the core Lambda function is *always* created,
    regardless of feature flags.
    """
    template = synthesize_stack(base_context)
    
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "FunctionName": "test-service-service",
            "PackageType": "Image",
            "Environment": {
                "Variables": {
                    "SERVICE_NAME": "test-service",
                }
            }
        }
    )

def test_no_resources_by_default(base_context):
    """
    Tests that with the default "all false" context, no
    optional resources (DynamoDB, SQS) are created.
    """
    template = synthesize_stack(base_context)
    
    template.resource_count_is("AWS::DynamoDB::Table", 0)
    template.resource_count_is("AWS::SQS::Queue", 0)
    template.resource_count_is("AWS::Lambda::EventSourceMapping", 0)

def test_dynamodb_created(base_context):
    """
    Tests that DynamoDB resources are created *only when*
    the 'include_dynamodb' context is set to 'true'.
    """
    context = base_context.copy()
    context["include_dynamodb"] = "true"
    
    template = synthesize_stack(context)
    
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "TableName": "test-service-data",
            "BillingMode": "PAY_PER_REQUEST",
            "KeySchema": [
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ]
        }
    )
    
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {
                "Variables": {
                    "SERVICE_NAME": "test-service",
                    "DYNAMO_TABLE_NAME": {"Ref": Match.any_value()}
                }
            }
        }
    )

def test_sqs_created(base_context):
    """
    Tests that SQS resources are created *only when*
    the 'include_sqs' context is set to 'true'.
    """
    context = base_context.copy()
    context["include_sqs"] = "true"
    
    template = synthesize_stack(context)

    template.has_resource_properties(
        "AWS::SQS::Queue",
        {
            "QueueName": "test-service-queue.fifo",
            "FifoQueue": True,
        }
    )
    
    template.resource_count_is("AWS::Lambda::EventSourceMapping", 1)
    
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {
                "Variables": {
                    "SERVICE_NAME": "test-service",
                    "SQS_QUEUE_URL": {"Ref": Match.any_value()}
                }
            }
        }
    )