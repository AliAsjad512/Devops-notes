import json
import boto3
import os
from uuid import uuid4
from datetime import datetime
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    method = event['httpMethod']
    path = event['path']
    
    if method == 'GET' and path == '/todos':
        return get_all()
    elif method == 'GET' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        return get_one(todo_id)
    elif method == 'POST' and path == '/todos':
        body = json.loads(event['body'])
        return create(body)
    elif method == 'PUT' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        body = json.loads(event['body'])
        return update(todo_id, body)
    elif method == 'DELETE' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        return delete(todo_id)
    else:
        return response(404, {'error': 'Not found'})
    
    def get_all():
    result = table.scan()
    return response(200, result.get('Items', []))
    
    def get_one(todo_id):
    item = table.get_item(Key={'id': todo_id}).get('Item')
    if not item:
        return response(404, {'error': 'Not found'})
    return response(200, item)
   
   def create(body):
    todo_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    item = {
        'id': todo_id,
        'title': body.get('title'),
        'completed': body.get('completed', False),
        'createdAt': now,
        'updatedAt': now
    }
    table.put_item(Item=item)
    return response(201, item)