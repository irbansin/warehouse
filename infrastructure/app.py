from aws_cdk import (
    Stack,
    RemovalPolicy,
    App,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_s3 as s3,
    aws_rds as rds,
    aws_iam as iam,
    Duration,
)
from constructs import Construct

class WarehouseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB tables
        inventory_table = dynamodb.Table(
            self, 'InventoryTable',
            partition_key=dynamodb.Attribute(
                name='productId',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='warehouseId',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,  # For development only
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        orders_table = dynamodb.Table(
            self, 'OrdersTable',
            partition_key=dynamodb.Attribute(
                name='orderId',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='timestamp',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,  # For development only
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Create S3 bucket for documents/images
        documents_bucket = s3.Bucket(
            self,
            "DocumentsBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Create Cognito User Pool
        user_pool = cognito.UserPool(
            self,
            "WarehouseUserPool",
            self_sign_up_enabled=True,
            user_verification=cognito.UserVerificationConfig(
                email_subject="Verify your email for Warehouse Management System",
                email_style=cognito.VerificationEmailStyle.CODE,
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True)
            ),
        )

        # Create Lambda functions
        inventory_lambda = lambda_.Function(
            self,
            "InventoryHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("backend/functions"),
            handler="inventory.handler",
            environment={
                "INVENTORY_TABLE": inventory_table.table_name,
                "ORDERS_TABLE": orders_table.table_name,
            },
        )

        # Add seed data Lambda function
        seed_data_function = lambda_.Function(
            self, 'SeedDataFunction',
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler='seed_data.handler',
            code=lambda_.Code.from_asset('backend/functions'),
            environment={
                'INVENTORY_TABLE': inventory_table.table_name,
                'ORDERS_TABLE': orders_table.table_name,
            },
            timeout=Duration.seconds(300),  # 5 minutes timeout for seeding data
            memory_size=512,  # Increase memory for better performance
        )

        # Grant permissions
        inventory_table.grant_read_write_data(inventory_lambda)
        orders_table.grant_read_write_data(inventory_lambda)
        inventory_table.grant_read_write_data(seed_data_function)
        orders_table.grant_read_write_data(seed_data_function)
        documents_bucket.grant_read_write(inventory_lambda)

        # Create API Gateway
        api = apigateway.RestApi(
            self, 'WarehouseApi',
            rest_api_name='Warehouse Management API',
            description='API for Warehouse Management System',
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            )
        )

        # Add inventory endpoints
        inventory_resource = api.root.add_resource('inventory')
        inventory_resource.add_method(
            'GET',
            apigateway.LambdaIntegration(inventory_lambda)
        )
        inventory_resource.add_method(
            'POST',
            apigateway.LambdaIntegration(inventory_lambda)
        )

        inventory_item = inventory_resource.add_resource('{productId}')
        inventory_item.add_method(
            'GET',
            apigateway.LambdaIntegration(inventory_lambda)
        )
        inventory_item.add_method(
            'PUT',
            apigateway.LambdaIntegration(inventory_lambda)
        )
        inventory_item.add_method(
            'DELETE',
            apigateway.LambdaIntegration(inventory_lambda)
        )

        # Add seed-data endpoint
        seed_resource = api.root.add_resource('seed-data')
        seed_resource.add_method(
            'POST',
            apigateway.LambdaIntegration(seed_data_function)
        )

app = App()
WarehouseStack(app, "WarehouseStack")
app.synth()
