import uuid
import json
import os
import uuid
from datetime import datetime
import boto3
print("Function code updated for deployment! (Attempt 3)") # Add this line
# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
# Use environment variable for table name (good practice) or hardcode 'Feedback'
# Ensure TABLE_NAME exactly matches your DynamoDB table name
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    try:
        # 1. Parse the request body
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in request body.")
            return {
                'statusCode': 400,
                'headers': { "Access-Control-Allow-Origin": "*" },
                'body': json.dumps({"message": "Invalid request body format."})
            }

        # 2. Extract inputs (using .get() to safely handle missing keys)
        name = body.get('name')
        rating = body.get('rating')
        comments = body.get('comments')

        # --- 3. Input Validation Logic ---
        validation_errors = []

        # Validate 'name'
        if not name or not isinstance(name, str) or name.strip() == "":
            validation_errors.append("Name is required and cannot be empty.")
        elif len(name) > 100:
            validation_errors.append("Name cannot exceed 100 characters.")
        else:
            name = name.strip() # Clean leading/trailing whitespace

        # Validate 'rating'
        if rating is None:
            validation_errors.append("Rating is required.")
        elif not isinstance(rating, (int, float)): # Allow float then convert to int
            validation_errors.append("Rating must be a number.")
        else:
            try:
                rating = int(rating) # Convert to integer
                if not (1 <= rating <= 5):
                    validation_errors.append("Rating must be between 1 and 5.")
            except ValueError: # Should not happen if it's already int/float
                validation_errors.append("Rating must be a valid integer.")

        # Validate 'comments'
        if comments is not None and not isinstance(comments, str):
             validation_errors.append("Comments must be a string.")
        elif comments is not None and len(comments) > 500:
            validation_errors.append("Comments cannot exceed 500 characters.")
        else:
            if comments: # Only strip if it's not None or empty
                comments = comments.strip()
            # If comments is None, keep it None. DynamoDB won't store None.


        # 4. If any validation errors, return a 400 Bad Request
        if validation_errors:
            print(f"Validation failed: {validation_errors}")
            return {
                'statusCode': 400,
                'headers': { "Access-Control-Allow-Origin": "*" },
                'body': json.dumps({"message": "Validation failed", "errors": validation_errors})
            }
        # --- End Input Validation ---

        # 5. Process validated data and store in DynamoDB
        feedback_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z' # Add 'Z' for UTC indicator

        item_to_store = {
            'id': feedback_id, # ENSURE THIS MATCHES YOUR DYNAMODB PARTITION KEY EXACTLY (case-sensitive)
            'name': name,
            'rating': rating,
            'comments': comments, # This will be None if no comments, and not stored by DynamoDB
            'timestamp': timestamp
        }

        table.put_item(Item=item_to_store)

        return {
            'statusCode': 200,
            'headers': { "Access-Control-Allow-Origin": "*" },
            'body': json.dumps({"message": "Thanks for your feedback!"})
        }

    except Exception as e:
        # Catch any unexpected errors and log them
        print(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'headers': { "Access-Control-Allow-Origin": "*" },
            'body': json.dumps({"message": "Internal server error. Please try again later.", "details": str(e)})
        }
    #force update