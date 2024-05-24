import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('items')

def create_item(event, context):
    item_data = json.loads(event['body'])
    table.put_item(Item=item_data)
    response = {
        "statusCode": 200,
        "body": json.dumps("Item created successfully")
    }
    return response

def get_item(event, context):
    item_id = event['pathParameters']['id']
    response = table.get_item(Key={'itemId': item_id})
    item = response.get('Item')
    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps("Item not found")
        }
    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }

def update_item(event, context):
    item_id = event['pathParameters']['id']
    item_data = json.loads(event['body'])
    response = table.update_item(
        Key={'itemId': item_id},
        UpdateExpression='SET #attr = :val',
        ExpressionAttributeNames={'#attr': 'attribute'},
        ExpressionAttributeValues={':val': item_data['attribute']}
    )
    return {
        "statusCode": 200,
        "body": json.dumps("Item updated successfully")
    }

def delete_item(event, context):
    item_id = event['pathParameters']['id']
    table.delete_item(Key={'itemId'
