#!/bin/bash

# Deploy script for Research Agent
# This automates the SAM deployment process

set -e  # Exit on any error

echo "🚀 Starting deployment of Research Agent to AWS..."
echo ""

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ Error: AWS SAM CLI is not installed."
    echo "Install it from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Error: AWS CLI is not configured."
    echo "Run: aws configure"
    exit 1
fi

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Loaded environment variables from .env"
else
    echo "❌ Error: .env file not found"
    echo "Copy .env.example to .env and add your API keys"
    exit 1
fi

# Check required environment variables
if [ -z "$OPENAI_API_KEY" ] || [ -z "$TAVILY_API_KEY" ]; then
    echo "❌ Error: Missing API keys in .env file"
    echo "Please set OPENAI_API_KEY and TAVILY_API_KEY"
    exit 1
fi

echo "✅ Environment variables loaded"
echo ""

# Build the Lambda package
echo "📦 Building Lambda package..."
sam build
echo "✅ Build complete"
echo ""

# Deploy to AWS
echo "🌩️  Deploying to AWS..."
echo "This will:"
echo "  1. Create an S3 bucket for deployment artifacts"
echo "  2. Upload your Lambda code"
echo "  3. Create CloudFormation stack with all resources"
echo "  4. Set up API Gateway and Lambda function"
echo ""

sam deploy \
    --guided \
    --parameter-overrides \
        "OpenAIApiKey=$OPENAI_API_KEY" \
        "TavilyApiKey=$TAVILY_API_KEY" \
    --capabilities CAPABILITY_IAM

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy the API URL from the output above"
echo "2. Test your API:"
echo "   python test_deployed.py --url <your-api-url>"
echo ""
echo "To view logs:"
echo "   aws logs tail /aws/lambda/research-agent-workshop --follow"
echo ""
