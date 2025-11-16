
-----

# AWS CDK Microservice Boilerplate (Python)

This is a template for creating new, container-based, Python Lambda microservices on AWS.

It provides a clean, configurable, and testable starting point. You can create a new, deployable service in minutes by cloning this repo and running a few  commands.

## ✨ Features

  * **AWS CDK in Python:** All infrastructure is defined in Python using the AWS CDK.
  * **Container-Based Lambda:** Uses a `Dockerfile` for maximum flexibility and consistency.
  * **Simple CLI:** A `Makefile` provides simple commands like `make deploy` and `make test`.
  * **Configurable Features:** Easily enable or disable optional AWS resources (DynamoDB, SQS) from the command line.
  * **Built-in Testing:**
      * **Infrastructure Tests:** `pytest` tests for your CDK stack (in `tests/test_stack.py`).
      * **Application Tests:** `pytest` tests for your Lambda's business logic (in `tests/test_lambda_handler.py`).

-----

## 🚀 Getting Started: New Service

Follow these steps to turn this template into your new microservice.

### Step 1: Clone This Repository

Clone this repo into a new directory with your service's name.

```bash
# Replace "my-new-service" with your actual service name
git clone https://github.com/your-org/cdk-microservice-boilerplate.git my-new-service
cd my-new-service
```

### Step 2: Reset Git History

Wipe the template's git history and start your own.

```bash
rm -rf .git
git init -b main
git add .
git commit -m "Initial commit from boilerplate"
```

### Step 3: Configure Your Service Name

Open `cdk.json` and set your unique `service_name` and `stack_name`. This is the **only file** you need to edit manually.

```json
{
  "app": "poetry run python app.py",
  ...
  "context": {
    "service_name": "my-payment-processor",  <-- SET THIS
    "stack_name": "MyPaymentProcessorStack", <-- SET THIS
    "include_dynamodb": "false",
    "include_sqs": "false"
  }
}
```

### Step 4: Install Dependencies

This installs all CDK and Python dependencies for your new service using Poetry.

```bash
make install
```

### Step 5: Enable Optional Features (Optional)

Use the built-in `make` commands to enable the AWS resources your service needs.

```bash
# See the current configuration
make status

# Example: Enable DynamoDB
make enable-dynamo

# Example: Enable SQS (as a Lambda trigger)
make enable-sqs
```

### Step 6: Run Tests

Before deploying, run the built-in tests to make sure everything is configured correctly. This runs both infrastructure and application tests.

```bash
make test
```

### Step 7: Deploy to AWS

First, bootstrap your AWS account/region (you only need to do this once per environment). Then, deploy.

> **Prerequisites:**
>
>   * You must have your AWS credentials configured (e.g., via `aws sso login` or environment variables).
>   * You must have Docker running on your machine (for building the Lambda container).

```bash
# Run this once per account/region
make bootstrap

# Deploy your service
make deploy
```

That's it\! Your new microservice is live.

-----

## 💻 How to Develop

1.  **Write Your Business Logic:**
    All your Python code goes in `src/app.py`. Modify the `handler` function to add your logic.
2.  **Write Application Tests:**
    As you add logic to `src/app.py`, add corresponding tests to `tests/test_lambda_handler.py`.
3.  **Add Python Dependencies:**
    To add a new library (like `requests`), run `poetry add requests`. The `Dockerfile` will install it automatically during deployment.
4.  **Redeploy:**
    Run `make deploy` to deploy your changes.

-----

## 🛠️ CLI Commands (Makefile)

All common tasks are run via `make`.

### Configuration

  * `make status`
    Show the current feature status (SQS, DynamoDB).
  * `make enable-sqs` / `make disable-sqs`
    Enable or disable SQS queue creation.
  * `make enable-dynamo` / `make disable-dynamo`
    Enable or disable DynamoDB table creation.

### Deployment

  * `make install`
    Install all Python dependencies with Poetry.
  * `make bootstrap`
    Bootstrap the AWS environment for CDK (first-time use only).
  * `make deploy`
    Synthesize and deploy the service to your AWS account.
  * `make destroy`
    Tear down all resources in the stack.

### Development

  * `make test`
    Run all automated tests (both infrastructure and application logic).

-----

## 📂 Project Structure

```
.
├── .dockerignore
├── .gitignore
├── app.py                     # CDK App entrypoint (loads context)
├── cdk.json                   # Main config file for your service
├── Dockerfile                 # Defines your Lambda's container
├── Makefile                   # The CLI for developers
├── poetry.lock
├── pyproject.toml             # Python dependencies (managed by Poetry)
├── README.md                  # This file
├── set_context.py             # Helper script used by `make`
├── src/                       # Your Lambda's application code
│   └── app.py                 # The Lambda handler (your business logic)
├── stacks/                    # Your CDK Infrastructure code
│   └── microservice_stack.py  # The main CDK Stack class
└── tests/                     # Automated tests
    ├── test_lambda_handler.py # Tests for your Lambda's logic (src/app.py)
    └── test_stack.py          # Tests for your CDK stack (stacks/microservice_stack.py)
```