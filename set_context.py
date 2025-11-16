# set_context.py

import json
import sys
import os
from pathlib import Path

CDK_JSON_FILE = Path("cdk.json")
DEFAULT_NAME = "sample-ms"

def read_config():
    """Reads the cdk.json file."""
    if not CDK_JSON_FILE.exists():
        print(f"Error: {CDK_JSON_FILE} not found.")
        print("Please ensure you are in the root of your service directory.")
        sys.exit(1)
    try:
        with open(CDK_JSON_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode {CDK_JSON_FILE}. Is it valid JSON?")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def write_config(data):
    """Writes data back to the cdk.json file with formatting."""
    try:
        with open(CDK_JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing to {CDK_JSON_FILE}: {e}")
        sys.exit(1)

def to_pascal_case(s: str) -> str:
    clean_name = "".join(c for c in s if c.isalnum() or c == '-')
    return "".join(word.capitalize() for word in clean_name.split('-')) + "Stack"

def run_initialization(new_service_name: str):
    """Sets the service_name and stack_name from the provided name."""
    if not new_service_name:
        print("Error: A non-empty service name is required.")
        sys.exit(1)
        
    data = read_config()
    context = data.get("context", {})

    if context.get("service_name") != DEFAULT_NAME:
        print(f"  Service name is already set to '{context.get('service_name')}'.")
        print("   If you want to re-initialize, please reset 'service_name' in cdk.json")
        print("   to 'my-generic-service' first.")
        return

    new_stack_name = to_pascal_case(new_service_name)
    
    context["service_name"] = new_service_name
    context["stack_name"] = new_stack_name
    data["context"] = context
    
    write_config(data)
    print(f" Service initialized: '{new_service_name}'")
    print(f" Updated {CDK_JSON_FILE}:")
    print(f"  - set 'service_name' to '{new_service_name}'")
    print(f"  - set 'stack_name' to '{new_stack_name}'")

def set_value(key, value_str):
    """Sets a value in the 'context' block of cdk.json."""
    data = read_config()
    
    if "context" not in data:
        data["context"] = {}
        
    value = "true" if value_str.lower() in ["true", "1", "yes"] else "false"
    
    if data["context"].get(key) == value:
        print(f"  '{key}' is already set to '{value}'. No change needed.")
        return

    data["context"][key] = value
    write_config(data)
    print(f" Updated {CDK_JSON_FILE}: set '{key}' to '{value}'")

def show_status():
    """Prints the current feature status from cdk.json."""
    data = read_config()
    context = data.get("context", {})
    
    print("\n---")
    print(" Service Configuration Status")
    print(f"  Service Name:  {context.get('service_name', 'Not Set')}")
    print(f"  Stack Name:    {context.get('stack_name', 'Not Set')}")
    print("---")
    print("  Optional Features:")
    
    dynamo = context.get('include_dynamodb', 'false').lower() == 'true'
    print(f"  DynamoDB:    {'ENABLED' if dynamo else 'DISABLED'}")
    
    sqs = context.get('include_sqs', 'false').lower() == 'true'
    print(f"  SQS Queue:     {'ENABLED' if sqs else 'DISABLED'}")
    print("---\n")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == 'init':
        run_initialization(sys.argv[2])
        
    elif len(sys.argv) == 3:
        set_value(sys.argv[1], sys.argv[2])
        
    elif len(sys.argv) == 1:
        show_status()
        
    else:
        print("Usage:")
        print("  python set_context.py                          - Show current status")
        print("  python set_context.py init <service-name>      - Initialize service name")
        print("  python set_context.py <KEY> [true|false]       - Set a context value")
        sys.exit(1)