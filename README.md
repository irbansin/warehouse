# Warehouse Management System

A serverless warehouse management system built using AWS CDK v2, Lambda, DynamoDB, S3, and API Gateway.

## Architecture

The system uses a serverless architecture with the following AWS services:

- **AWS Lambda**: Handles business logic for inventory management
- **Amazon DynamoDB**: NoSQL database for storing inventory and orders
- **Amazon S3**: Storage for documents and images
- **Amazon API Gateway**: RESTful API endpoints
- **Amazon Cognito**: User authentication and authorization

## Prerequisites

- Python 3.9 or higher
- Node.js 18.x or higher (for AWS CDK)
- AWS CLI configured with appropriate credentials
- pipenv (Python package manager)

## Project Structure

```
warehouse/
├── infrastructure/     # CDK infrastructure code
│   └── app.py         # Main CDK stack definition
├── lambda/            # Lambda function code
│   └── inventory.py   # Inventory management handler
└── backend/          # Backend configuration
    └── requirements.txt
```

## Setup Instructions

1. **Install Dependencies**

```bash
# Install Node.js (if not installed)
brew install node

# Install AWS CDK CLI
npm install -g aws-cdk

# Install Python dependencies
pipenv install
```

2. **Configure AWS Credentials**

Ensure your AWS credentials are configured with appropriate permissions. The IAM user needs permissions for:
- CloudFormation
- Lambda
- DynamoDB
- S3
- API Gateway
- Cognito

3. **Deploy the Stack**

```bash
# Activate virtual environment
pipenv shell

# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy the stack
cdk deploy
```

## API Endpoints

Base URL: `https://l7sv7v0wg4.execute-api.ap-south-1.amazonaws.com/prod/`

### Inventory Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | List all inventory items |
| POST | `/inventory` | Add a new product |
| GET | `/inventory/{productId}` | Get details of a specific product |
| PUT | `/inventory/{productId}` | Update a product |
| DELETE | `/inventory/{productId}` | Delete a product |

### Database Schema

#### Inventory Table
- `productId` (Partition Key): String
- `warehouseId` (Sort Key): String
- Additional attributes as needed

#### Orders Table
- `orderId` (Partition Key): String
- `timestamp` (Sort Key): String
- Additional attributes as needed

## Security

- Authentication is handled by Amazon Cognito
- User Pool configured with email verification
- API endpoints are secured with Cognito authorizers
- S3 bucket configured with auto-delete for proper cleanup
- DynamoDB tables use encryption at rest

## Development

To make changes to the infrastructure:

1. Modify the CDK stack in `infrastructure/app.py`
2. Update Lambda functions in `lambda/` directory
3. Deploy changes using `cdk deploy`

## Testing

You can test the API endpoints using any HTTP client (e.g., curl, Postman):

```bash
# Example: List all inventory items
curl -X GET https://l7sv7v0wg4.execute-api.ap-south-1.amazonaws.com/prod/inventory

# Example: Add a new product
curl -X POST https://l7sv7v0wg4.execute-api.ap-south-1.amazonaws.com/prod/inventory \
  -H "Content-Type: application/json" \
  -d '{"productId": "123", "name": "Example Product", "quantity": 100}'
```

## Cleanup

To avoid incurring charges, delete the stack when no longer needed:

```bash
cdk destroy
```

This will remove all resources created by the stack.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
