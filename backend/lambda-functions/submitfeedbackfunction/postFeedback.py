import json
import boto3
import uuid
from datetime import datetime

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Feedback')

def lambda_handler(event, context):
    """
    This function receives feedback data from API Gateway, adds a unique ID and timestamp,
    and saves it to the Feedback DynamoDB table.
    """
    try:
        # API Gateway with Lambda Proxy Integration passes the request body as a JSON string.
        body = json.loads(event['body'])
        
        # Extract data from the request body
        name = body.get('name')
        rating = body.get('rating')
        comments = body.get('comments')
        
        # Basic validation
        if not all([name, rating, comments]):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*', # Required for CORS
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'message': 'Error: Missing required fields (name, rating, comments).'})
            }

        # Generate a unique ID and a timestamp
        feedback_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Create the item to be stored in DynamoDB
        item_to_store = {
            'feedbackId': feedback_id,
            'name': name,
            'rating': int(rating),
            'comments': comments,
            'timestamp': timestamp
        }
        
        # Put the item into the DynamoDB table
        table.put_item(Item=item_to_store)
        
        # Return a success response
        return {
            'statusCode': 201, # 201 Created is more appropriate for a successful POST
             'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'message': 'Feedback submitted successfully!',
                'feedbackId': feedback_id
            })
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
             'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'An internal error occurred.'})
        }