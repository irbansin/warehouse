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
)
from constructs import Construct

class WarehouseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB tables
        inventory_table = dynamodb.Table(
            self,
            "InventoryTable",
            partition_key=dynamodb.Attribute(
                name="productId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="warehouseId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        orders_table = dynamodb.Table(
            self,
            "OrdersTable",
            partition_key=dynamodb.Attribute(
                name="orderId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
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

        # Create API Gateway
        api = apigateway.RestApi(
            self,
            "WarehouseApi",
            rest_api_name="Warehouse Management API",
            description="API for Warehouse Management System",
        )

        # Create Lambda functions
        inventory_lambda = lambda_.Function(
            self,
            "InventoryHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambda"),
            handler="inventory.handler",
            environment={
                "INVENTORY_TABLE": inventory_table.table_name,
                "ORDERS_TABLE": orders_table.table_name,
            },
        )

        # Grant permissions
        inventory_table.grant_read_write_data(inventory_lambda)
        orders_table.grant_read_write_data(inventory_lambda)
        documents_bucket.grant_read_write(inventory_lambda)

        # Add API Gateway endpoints
        inventory_integration = apigateway.LambdaIntegration(inventory_lambda)
        
        inventory = api.root.add_resource("inventory")
        inventory.add_method("GET", inventory_integration)  # GET /inventory
        inventory.add_method("POST", inventory_integration)  # POST /inventory
        
        product = inventory.add_resource("{productId}")
        product.add_method("GET", inventory_integration)    # GET /inventory/{productId}
        product.add_method("PUT", inventory_integration)    # PUT /inventory/{productId}
        product.add_method("DELETE", inventory_integration) # DELETE /inventory/{productId}

app = App()
WarehouseStack(app, "WarehouseStack")
app.synth()
