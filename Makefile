.PHONY: help install bootstrap deploy test destroy

init:
	@if [ -z "$(name)" ]; then \
		echo "Error: Please provide a name."; \
		echo "Usage: make init name=my-new-service"; \
		exit 1; \
	fi
	@echo " Initializing service as: $(name)..."
	@poetry run python set_context.py init $(name)

install:
	@echo "Installing Poetry dependencies..."
	@poetry install --no-root

bootstrap: install
	@echo "Bootstrapping AWS environment..."
	@poetry run cdk bootstrap

deploy: install
	@echo "Deploying service..."
	@poetry run cdk deploy --all --require-approval never

test: install
	@echo "Running tests..."
	@poetry run pytest

destroy:
	@echo "Destroying service..."
	@poetry run cdk destroy --all --force

status:
	@poetry run python set_context.py

# Enable SQS
enable-sqs:
	@poetry run python set_context.py include_sqs true

# Disable SQS
disable-sqs:
	@poetry run python set_context.py include_sqs false

# Enable DynamoDB
enable-dynamo:
	@poetry run python set_context.py include_dynamodb true

# Disable DynamoDB
disable-dynamo:
	@poetry run python set_context.py include_dynamodb false

help:
	@echo "Available commands:"
	@echo ""
	@echo "  Deployment:"
	@echo "    make install    - Installs Python dependencies"
	@echo "    make bootstrap  - Bootstrap the CDK environment in your target AWS account/region"
	@echo "    make deploy     - Deploy the service to AWS"
	@echo "    make test       - Run the CDK unit tests"
	@echo "    make destroy    - Destroy the deployed service"
	@echo ""
	@echo "  Configuration:"
	@echo "    make init           - Initialize new service and set service name (example usage: make init name=my-new-service)"
	@echo "    make status         - Show current feature status (SQS, DynamoDB)"
	@echo "    make enable-sqs     - Enable SQS queue creation"
	@echo "    make disable-sqs    - Disable SQS queue creation"
	@echo "    make enable-dynamo  - Enable DynamoDB table creation"
	@echo "    make disable-dynamo - Disable DynamoDB table creation"