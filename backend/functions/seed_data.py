import boto3
import uuid
import random
from datetime import datetime, timedelta
import json

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
inventory_table = dynamodb.Table('InventoryTable')
orders_table = dynamodb.Table('OrdersTable')

# Sample data for generating realistic entries
PRODUCT_CATEGORIES = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Books']
WAREHOUSE_IDS = ['WH001', 'WH002', 'WH003']
ORDER_STATUSES = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
PRODUCT_NAMES = {
    'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes'],
    'Food': ['Coffee', 'Tea', 'Snacks', 'Pasta', 'Cereal'],
    'Furniture': ['Chair', 'Table', 'Desk', 'Sofa', 'Bed'],
    'Books': ['Novel', 'Textbook', 'Comic', 'Magazine', 'Dictionary']
}

def generate_product():
    category = random.choice(PRODUCT_CATEGORIES)
    name = random.choice(PRODUCT_NAMES[category])
    return {
        'productId': str(uuid.uuid4()),
        'name': f'{name} {random.randint(1000, 9999)}',
        'description': f'Description for {name}',
        'category': category,
        'quantity': random.randint(0, 1000),
        'unitPrice': round(random.uniform(10, 1000), 2),
        'warehouseId': random.choice(WAREHOUSE_IDS),
        'location': f'Aisle {random.randint(1, 20)}-Shelf {random.randint(1, 50)}',
        'sku': f'SKU{random.randint(10000, 99999)}',
        'lastUpdated': datetime.now().isoformat()
    }

def generate_order(products):
    order_items = []
    total_amount = 0
    num_items = random.randint(1, 5)
    
    # Randomly select products for the order
    selected_products = random.sample(products, num_items)
    
    for product in selected_products:
        quantity = random.randint(1, 5)
        subtotal = quantity * product['unitPrice']
        total_amount += subtotal
        
        order_items.append({
            'productId': product['productId'],
            'productName': product['name'],
            'quantity': quantity,
            'unitPrice': product['unitPrice'],
            'subtotal': subtotal
        })

    # Generate a random date within the last 30 days
    days_ago = random.randint(0, 30)
    order_date = (datetime.now() - timedelta(days=days_ago)).isoformat()

    return {
        'orderId': str(uuid.uuid4()),
        'customerName': f'Customer {random.randint(1000, 9999)}',
        'customerEmail': f'customer{random.randint(1000, 9999)}@example.com',
        'shippingAddress': {
            'street': f'{random.randint(100, 999)} Main St',
            'city': 'Sample City',
            'state': 'ST',
            'zipCode': f'{random.randint(10000, 99999)}',
            'country': 'USA'
        },
        'items': order_items,
        'status': random.choice(ORDER_STATUSES),
        'totalAmount': round(total_amount, 2),
        'createdAt': order_date,
        'updatedAt': order_date,
        'trackingNumber': f'TRK{random.randint(1000000, 9999999)}',
        'notes': 'Sample order notes',
        'warehouseId': random.choice(WAREHOUSE_IDS)
    }

def seed_data(num_products=50, num_orders=100):
    # Generate and insert products
    products = []
    print(f"Generating {num_products} products...")
    
    for _ in range(num_products):
        product = generate_product()
        try:
            inventory_table.put_item(Item=product)
            products.append(product)
            print(f"Added product: {product['name']}")
        except Exception as e:
            print(f"Error adding product: {str(e)}")

    # Generate and insert orders
    print(f"\nGenerating {num_orders} orders...")
    
    for _ in range(num_orders):
        order = generate_order(products)
        try:
            orders_table.put_item(Item=order)
            print(f"Added order: {order['orderId']}")
        except Exception as e:
            print(f"Error adding order: {str(e)}")

def handler(event, context):
    try:
        num_products = event.get('numProducts', 50)
        num_orders = event.get('numOrders', 100)
        
        seed_data(num_products, num_orders)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully seeded {num_products} products and {num_orders} orders'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

if __name__ == '__main__':
    # For local testing
    handler({'numProducts': 50, 'numOrders': 100}, None)
