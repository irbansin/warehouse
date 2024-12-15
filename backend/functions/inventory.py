import json
import os
import boto3
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
inventory_table = dynamodb.Table(os.environ['INVENTORY_TABLE'])

def handler(event, context):
    """Handle inventory-related operations"""
    http_method = event['httpMethod']
    path = event['path']
    
    try:
        if http_method == 'GET':
            if '/inventory/product' in path:
                product_id = event['pathParameters']['productId']
                return get_product(product_id)
            else:
                return list_inventory()
                
        elif http_method == 'POST':
            body = json.loads(event['body'])
            return add_product(body)
            
        elif http_method == 'PUT':
            body = json.loads(event['body'])
            product_id = event['pathParameters']['productId']
            return update_product(product_id, body)
            
        elif http_method == 'DELETE':
            product_id = event['pathParameters']['productId']
            return delete_product(product_id)
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_product(product_id):
    """Get product details by ID"""
    response = inventory_table.query(
        KeyConditionExpression=Key('productId').eq(product_id)
    )
    
    if response['Items']:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'][0], default=str)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Product not found'})
        }

def list_inventory():
    """List all inventory items"""
    response = inventory_table.scan()
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'], default=str)
    }

def add_product(product_data):
    """Add a new product to inventory"""
    product_data['timestamp'] = datetime.utcnow().isoformat()
    
    inventory_table.put_item(Item=product_data)
    
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Product added successfully'})
    }

def update_product(product_id, updates):
    """Update product details"""
    update_expression = 'SET '
    expression_values = {}
    
    for key, value in updates.items():
        if key != 'productId':  # Don't update the primary key
            update_expression += f'#{key} = :{key}, '
            expression_values[f':{key}'] = value
    
    update_expression = update_expression.rstrip(', ')
    
    inventory_table.update_item(
        Key={'productId': product_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames={f'#{k}': k for k in updates.keys() if k != 'productId'}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Product updated successfully'})
    }

def delete_product(product_id):
    """Delete a product"""
    inventory_table.delete_item(
        Key={'productId': product_id}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Product deleted successfully'})
    }
