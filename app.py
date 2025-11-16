#!/usr/bin/env python3

import aws_cdk as cdk
import os
from stacks.microservice_stack import MicroserviceStack

app = cdk.App()

service_name = app.node.try_get_context("service_name")
stack_name = app.node.try_get_context("stack_name")

if not service_name or not stack_name:
    raise ValueError("CDK context variables 'service_name' and 'stack_name' are required.")

env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION"),
)

MicroserviceStack(
    app,
    stack_name,
    env=env,
    description=f"Microservice stack for {service_name}"
)

app.synth()