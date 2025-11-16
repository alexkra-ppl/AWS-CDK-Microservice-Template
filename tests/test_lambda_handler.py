import pytest
import json

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import handler


@pytest.fixture
def direct_invoke_event():
    """A sample event for a direct invocation (e.g., test console)."""
    return {}

@pytest.fixture
def sqs_event():
    """A sample SQS event payload with one message."""
    return {
        "Records": [
            {
                "messageId": "059f36b4-87a3-44ab-83d2-661975413000",
                "body": "{\"message\": \"Hello from SQS!\"}",
                "eventSource": "aws:sqs",
            }
        ]
    }


def test_handler_direct_invoke(direct_invoke_event, monkeypatch):
    """
    Tests the handler with a simple, direct invocation.
    """
    monkeypatch.delenv("SERVICE_NAME", raising=False)
    monkeypatch.setenv("SERVICE_NAME", "test-service")
    
    monkeypatch.delenv("DYNAMO_TABLE_NAME", raising=False)
    monkeypatch.setenv("DYNAMO_TABLE_NAME", "test-table")
    
    monkeypatch.delenv("SQS_QUEUE_URL", raising=False)
    monkeypatch.setenv("SQS_QUEUE_URL", "test-queue-url")

    response = handler(direct_invoke_event, {})
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    
    assert body["message"] == "Hello from the test-service!"
    assert body["configured_dynamo_table"] == "test-table"
    assert body["configured_sqs_queue"] == "test-queue-url"

def test_handler_sqs_event(sqs_event, monkeypatch):
    """
    Tests the handler's SQS processing logic.
    """
    monkeypatch.delenv("SERVICE_NAME", raising=False)
    monkeypatch.setenv("SERVICE_NAME", "test-service")

    response = handler(sqs_event, {})

    assert response == {"status": "sqs_processed"}

def test_handler_sqs_error(sqs_event, monkeypatch):
    """
    Tests that if an error occurs during SQS processing,
    the function re-raises the exception.
    """
    monkeypatch.delenv("SERVICE_NAME", raising=False)
    monkeypatch.setenv("SERVICE_NAME", "test-service")

    sqs_event["Records"][0]["body"] = "this is not json"

    with pytest.raises(Exception):
        handler(sqs_event, {})

def test_handler_no_env_vars(direct_invoke_event, monkeypatch):
    """
    Tests that the handler runs safely even if no
    environment variables are set.
    """
    monkeypatch.delenv("SERVICE_NAME", raising=False)
    monkeypatch.delenv("DYNAMO_TABLE_NAME", raising=False)
    monkeypatch.delenv("SQS_QUEUE_URL", raising=False)
    
    response = handler(direct_invoke_event, {})
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    
    assert body["message"] == "Hello from the default-service!"
    assert body["configured_dynamo_table"] == "Not configured"
    assert body["configured_sqs_queue"] == "Not configured"