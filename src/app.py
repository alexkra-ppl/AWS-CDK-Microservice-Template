import os
import json

def handler(event, context):
    """
    Main Lambda handler
    """
    
    print(f"Event received: {json.dumps(event)}")
    
    service_name = os.environ.get("SERVICE_NAME", "default-service")
    table_name = os.environ.get("DYNAMO_TABLE_NAME")
    queue_url = os.environ.get("SQS_QUEUE_URL")

    if "Records" in event and event["Records"] and "eventSource" in event["Records"][0]:
        if event["Records"][0]["eventSource"] == "aws:sqs":
            print(f"Processing SQS event from queue: {queue_url}...")
            
            try:
                for record in event["Records"]:
                    message_body = record.get("body")
                    print(f"Processing message ID: {record.get('messageId')}")
                    print(f"Message body: {message_body}")
                    
                    if message_body:
                        _ = json.loads(message_body) 

                print("Successfully processed SQS messages.")
                return {"status": "sqs_processed"}

            except Exception as e:
                print(f"Error processing SQS message: {e}")
                raise e

    print("Processing standard invocation.")
    
    response_body = {
        "message": f"Hello from the {service_name}!",
        "configured_dynamo_table": table_name if table_name else "Not configured",
        "configured_sqs_queue": queue_url if queue_url else "Not configured",
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }