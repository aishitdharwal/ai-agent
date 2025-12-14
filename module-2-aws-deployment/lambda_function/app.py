"""
AWS Lambda Handler for Research Agent

This is the entry point that AWS Lambda calls when your API receives a request.
It handles the HTTP request/response cycle and calls your agent.
"""

import json
import os
import boto3
from datetime import datetime
from agent import ResearchAgent

# Initialize S3 client for state persistence
s3_client = boto3.client('s3')
STATE_BUCKET = os.environ.get('STATE_BUCKET', 'ai-agent-state-bucket')

# Initialize the agent once (outside handler for reuse across invocations)
agent = ResearchAgent()


def lambda_handler(event, context):
    """
    AWS Lambda handler function
    
    Event structure from API Gateway:
    {
        "body": '{"topic": "research topic"}',
        "headers": {...},
        "httpMethod": "POST",
        ...
    }
    
    Returns API Gateway response format:
    {
        "statusCode": 200,
        "headers": {...},
        "body": '{"result": ...}'
    }
    """
    
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        topic = body.get('topic')
        
        if not topic:
            return create_response(400, {
                'error': 'Missing required field: topic'
            })
        
        # Generate unique request ID for state tracking
        request_id = context.request_id
        
        print(f"Processing research request for topic: {topic}")
        print(f"Request ID: {request_id}")
        
        # Run the agent
        result = agent.research(topic)
        
        # Save state to S3 (for demonstration of state persistence)
        save_state_to_s3(request_id, result)
        
        # Return successful response
        return create_response(200, {
            'request_id': request_id,
            'topic': topic,
            'result': result
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return create_response(500, {
            'error': 'Internal server error',
            'message': str(e)
        })


def create_response(status_code, body):
    """
    Create properly formatted API Gateway response
    
    IMPORTANT: API Gateway requires specific response format.
    This helper ensures we always return the correct structure.
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Enable CORS
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps(body, indent=2)
    }


def save_state_to_s3(request_id, state):
    """
    Save agent state to S3
    
    This is a SIMPLIFIED state persistence approach for the workshop.
    
    PRODUCTION ISSUES with this approach:
    1. No handling for concurrent writes (race conditions)
    2. No versioning or conflict resolution
    3. Slow for high-frequency updates
    4. No indexing or querying capabilities
    
    Production alternatives:
    - DynamoDB for structured state with atomic updates
    - Redis/ElastiCache for session state
    - RDS for complex queries
    """
    try:
        key = f"states/{request_id}.json"
        
        state_with_metadata = {
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'state': state
        }
        
        s3_client.put_object(
            Bucket=STATE_BUCKET,
            Key=key,
            Body=json.dumps(state_with_metadata),
            ContentType='application/json'
        )
        
        print(f"State saved to s3://{STATE_BUCKET}/{key}")
        
    except Exception as e:
        # Don't fail the request if state saving fails
        print(f"Warning: Failed to save state to S3: {str(e)}")


def get_state_from_s3(request_id):
    """
    Retrieve agent state from S3
    
    This would be used if we wanted to resume a previous conversation
    or continue a multi-step workflow across multiple Lambda invocations.
    """
    try:
        key = f"states/{request_id}.json"
        
        response = s3_client.get_object(
            Bucket=STATE_BUCKET,
            Key=key
        )
        
        state_data = json.loads(response['Body'].read())
        return state_data['state']
        
    except s3_client.exceptions.NoSuchKey:
        print(f"No state found for request_id: {request_id}")
        return None
    except Exception as e:
        print(f"Error retrieving state from S3: {str(e)}")
        return None
