"""
Test Lambda function locally before deploying to AWS

This simulates how Lambda will call your handler function,
allowing you to catch errors before deploying.

Usage:
    python test_local.py
"""

import sys
import os
import json
from datetime import datetime

# Add lambda_function to path so we can import it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lambda_function'))

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Now import the Lambda handler
from lambda_function.app import lambda_handler


class MockContext:
    """Mock Lambda context object for local testing"""
    def __init__(self):
        self.aws_request_id = f"local-test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.request_id = self.aws_request_id  # Alias for compatibility
        self.function_name = "research-agent-local-test"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = "arn:aws:lambda:local:123456789012:function:research-agent-local-test"
        
    def get_remaining_time_in_millis(self):
        return 300000  # 5 minutes


def create_api_gateway_event(topic):
    """
    Create a mock API Gateway event
    
    This matches the structure Lambda receives from API Gateway
    """
    return {
        "body": json.dumps({"topic": topic}),
        "resource": "/research",
        "path": "/research",
        "httpMethod": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "queryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "local-test",
            "protocol": "HTTP/1.1",
            "httpMethod": "POST",
            "path": "/research",
            "stage": "test",
            "requestId": "local-test-request",
            "requestTime": datetime.now().isoformat(),
            "requestTimeEpoch": int(datetime.now().timestamp() * 1000)
        },
        "isBase64Encoded": False
    }


def test_lambda_locally():
    """Test the Lambda handler locally"""
    
    print("\n" + "="*60)
    print("🧪 LOCAL LAMBDA TESTING")
    print("="*60 + "\n")
    
    # Check environment variables
    print("Checking environment variables...")
    openai_key = os.environ.get('OPENAI_API_KEY')
    tavily_key = os.environ.get('TAVILY_API_KEY')
    
    if not openai_key:
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("Make sure you have a .env file with your API keys")
        return False
    
    if not tavily_key:
        print("❌ Error: TAVILY_API_KEY not found in environment")
        print("Make sure you have a .env file with your API keys")
        return False
    
    print("✅ Environment variables loaded")
    print()
    
    # Create test event
    topic = "Latest developments in quantum computing"
    print(f"Creating test event for topic: {topic}")
    event = create_api_gateway_event(topic)
    
    # Create mock context
    context = MockContext()
    print(f"Request ID: {context.request_id}")
    print()
    
    # Call the handler
    print("Invoking Lambda handler...")
    print("-" * 60)
    
    try:
        response = lambda_handler(event, context)
        
        print("-" * 60)
        print()
        
        # Parse response
        status_code = response.get('statusCode')
        body = json.loads(response.get('body', '{}'))
        
        print(f"Status Code: {status_code}")
        print()
        
        if status_code == 200:
            print("✅ Lambda execution successful!")
            print()
            print("Response:")
            print(json.dumps(body, indent=2))
            print()
            print("="*60)
            print("✅ LOCAL TEST PASSED")
            print("="*60)
            print()
            print("Next steps:")
            print("1. Review the output above")
            print("2. If everything looks good, deploy to AWS:")
            print("   ./deploy.sh")
            print()
            return True
        else:
            print("❌ Lambda execution failed")
            print()
            print("Error response:")
            print(json.dumps(body, indent=2))
            return False
            
    except Exception as e:
        print()
        print("❌ Exception during Lambda execution:")
        print(str(e))
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_lambda_locally()
    sys.exit(0 if success else 1)
