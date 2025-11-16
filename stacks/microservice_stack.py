# microservice_stack.py

from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_sqs as sqs,
    aws_lambda_event_sources as lambda_events,
    aws_iam as iam,
)
from constructs import Construct
import os

class MicroserviceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        service_name = self.node.try_get_context("service_name")
        include_dynamodb = self.node.try_get_context("include_dynamodb").lower() == 'true'
        include_sqs = self.node.try_get_context("include_sqs").lower() == 'true'

        if not service_name:
            raise ValueError("service_name must be set in cdk.json context")

        self.lambda_function = _lambda.DockerImageFunction(
            self,
            "ServiceLambda",
            function_name=f"{service_name}-service",
            code=_lambda.DockerImageCode.from_image_asset(
                directory=os.path.join(os.getcwd(), "src")
            ),
            memory_size=1024,
            timeout=Duration.seconds(10),
            environment={
                "SERVICE_NAME": service_name,
            },
        )

        if include_dynamodb:
            self.dynamo_table = dynamodb.Table(
                self,
                "ServiceTable",
                table_name=f"{service_name}-data",
                partition_key=dynamodb.Attribute(
                    name="pk", type=dynamodb.AttributeType.STRING
                ),
                sort_key=dynamodb.Attribute(
                    name="sk", type=dynamodb.AttributeType.STRING
                ),
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                removal_policy=RemovalPolicy.DESTROY,
            )
            self.dynamo_table.grant_read_write_data(self.lambda_function)
            self.lambda_function.add_environment(
                "DYNAMO_TABLE_NAME", self.dynamo_table.table_name
            )

        if include_sqs:
            self.sqs_queue = sqs.Queue(
                self,
                "ServiceQueue",
                queue_name=f"{service_name}-queue.fifo",
                fifo=True,
                content_based_deduplication=True,
                visibility_timeout=Duration.seconds(30),
                retention_period=Duration.days(4),
            )
            self.lambda_function.add_event_source(
                lambda_events.SqsEventSource(
                    self.sqs_queue,
                    batch_size=10
                )
            )
            self.sqs_queue.grant_consume_messages(self.lambda_function)
            self.lambda_function.add_environment(
                "SQS_QUEUE_URL", self.sqs_queue.queue_url
            )