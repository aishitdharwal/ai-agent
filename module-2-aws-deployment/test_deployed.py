"""
Test the deployed API endpoint

Usage:
    python test_deployed.py --url <your-api-gateway-url>

Example:
    python test_deployed.py --url https://abc123.execute-api.us-east-1.amazonaws.com/prod/research
"""

import requests
import argparse
import json
import time


def test_api(api_url, topic):
    """Test the deployed API with a research request"""
    
    print(f"\n{'='*60}")
    print(f"Testing API: {api_url}")
    print(f"Topic: {topic}")
    print(f"{'='*60}\n")
    
    # Prepare request
    payload = {
        "topic": topic
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("📤 Sending request...")
    start_time = time.time()
    
    try:
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=300  # 5 minute timeout
        )
        
        elapsed = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("✅ Success!")
            print()
            
            # Parse and display results
            result = response.json()
            
            print(f"📌 Request ID: {result.get('request_id', 'N/A')}")
            print(f"📝 Topic: {result.get('topic', 'N/A')}")
            print()
            
            if 'result' in result:
                research_result = result['result']
                
                print("🔍 Search Queries:")
                for i, query in enumerate(research_result.get('search_queries', []), 1):
                    print(f"   {i}. {query}")
                print()
                
                print(f"📈 Results Analyzed: {research_result.get('num_results', 0)}")
                print()
                
                print("🎯 Key Findings:")
                for i, finding in enumerate(research_result.get('key_findings', []), 1):
                    print(f"   {i}. {finding}")
                print()
                
                print("📄 Summary:")
                print(research_result.get('summary', 'No summary'))
                print()
            
            print(f"{'='*60}")
            print("✅ API is working correctly!")
            print(f"{'='*60}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print()
            print("Response:")
            print(json.dumps(response.json(), indent=2))
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>5 minutes)")
        print("This might indicate:")
        print("  - Lambda timeout (check CloudFormation template)")
        print("  - Slow LLM responses")
        print("  - Network issues")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Test deployed Research Agent API"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="API Gateway URL (from SAM deployment output)"
    )
    parser.add_argument(
        "--topic",
        default="Latest developments in quantum computing",
        help="Research topic to test"
    )
    
    args = parser.parse_args()
    
    # Ensure URL ends with /research
    api_url = args.url
    if not api_url.endswith('/research'):
        if api_url.endswith('/'):
            api_url = api_url + 'research'
        else:
            api_url = api_url + '/research'
    
    test_api(api_url, args.topic)


if __name__ == "__main__":
    main()
