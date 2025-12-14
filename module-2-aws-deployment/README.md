# Module 2: AWS Deployment - Making Your Agent Publicly Accessible

## Overview
In Module 1, you built a stateful research agent that works on your laptop. Now we're going to deploy it to AWS so anyone can use it through a public API. This is where you transition from "works on my machine" to "works for real users."

## What You'll Deploy

A production-accessible AI agent with:
- **AWS Lambda**: Serverless function to run your agent
- **API Gateway**: Public HTTP endpoint for users to call
- **S3**: State storage between invocations
- **Environment Variables**: Secure API key management
- **CloudFormation/SAM**: Infrastructure as Code for reproducible deployments

## The Architecture

```
User Request → API Gateway → Lambda Function → Agent Logic
                                ↓                    ↑
                           S3 (State Storage) ←──────┘
```

This is a **workshop architecture** - simplified to get you deploying quickly. It works, but it's not production-grade. We'll discuss what's missing at the end.

## What You'll Learn

1. **Packaging Python Lambda Functions**: Dependencies, layers, and deployment packages
2. **API Gateway Configuration**: Creating public endpoints for your agent
3. **S3 State Management**: Persisting state between Lambda invocations
4. **Environment Variables**: Managing secrets in AWS
5. **SAM/CloudFormation**: Declarative infrastructure deployment
6. **Testing Deployed Agents**: Making requests to your live API

## Prerequisites

- Completed Module 1 (stateful agent)
- AWS Account with admin access
- AWS CLI installed and configured
- SAM CLI installed (for deployment)

## Setup Instructions

### 1. Install AWS SAM CLI

**macOS:**
```bash
brew tap aws/tap
brew install aws-sam-cli
```

**Windows/Linux:** Follow [AWS SAM Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

### 2. Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1 (or your preferred region)
# Default output format: json
```

### 3. Install Dependencies

```bash
cd module-2-aws-deployment
pip install -r requirements.txt
```

### 4. Set Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Project Structure

```
module-2-aws-deployment/
├── lambda_function/
│   ├── app.py                 # Lambda handler (main entry point)
│   ├── agent.py               # Stateful agent from Module 1
│   └── requirements.txt       # Lambda dependencies
├── template.yaml              # SAM template (infrastructure as code)
├── deploy.sh                  # Deployment script
├── test_local.py              # Test Lambda locally before deploying
├── test_deployed.py           # Test deployed API
├── README.md                  # This file
└── TEACHING_GUIDE.md          # Workshop teaching notes
```

## Deployment Steps

### Step 1: Test Locally First

```bash
python test_local.py
```

This simulates Lambda locally to catch issues before deploying.

### Step 2: Deploy to AWS

```bash
chmod +x deploy.sh
./deploy.sh
```

This will:
1. Build the Lambda package
2. Upload to S3
3. Deploy via CloudFormation
4. Output your API endpoint URL

### Step 3: Test Your Deployed API

```bash
python test_deployed.py --url <your-api-gateway-url>
```

## Using Your Deployed Agent

Once deployed, anyone can make requests to your API:

```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "Latest developments in quantum computing"}'
```

## What This Architecture Gets Right

✅ **Serverless**: No servers to manage, pay only for what you use  
✅ **Scalable**: Lambda auto-scales with demand  
✅ **Public Access**: Anyone can call your API  
✅ **State Persistence**: Uses S3 for basic state storage  
✅ **Reproducible**: Infrastructure as Code with SAM  

## What This Architecture Is Missing (Production Gaps)

This is where your workshop creates appetite for deeper learning. This simplified deployment works, but here are the production problems we're NOT solving:

### 🚨 Problem 1: No Async Processing
**The Issue**: Lambda has a 15-minute timeout. If your agent takes longer, it fails.

**Workshop Solution**: We're using synchronous Lambda invokes - simple but limited.

**Production Solution**: Async invokes with Step Functions, SQS queues, or ECS Fargate for long-running tasks.

**Where to Learn**: Your course Project 2 covers async architectures.

### 🚨 Problem 2: State Management is Naive
**The Issue**: We're using S3 with simple file reads/writes. No handling for concurrent users accessing the same state.

**Workshop Solution**: One S3 file per request - works but causes race conditions.

**Production Solution**: DynamoDB with atomic updates, Redis for session state, or RDS for complex queries.

**Where to Learn**: Your course Project 1 covers production state management.

### 🚨 Problem 3: No Monitoring or Observability
**The Issue**: When this breaks in production, you have no idea why.

**Workshop Solution**: Basic CloudWatch logs - you have to dig through text.

**Production Solution**: Structured logging, tracing with X-Ray, custom metrics, dashboards, alerts.

**Where to Learn**: Your course Project 3 covers observability patterns.

### 🚨 Problem 4: No Cost Controls
**The Issue**: A DDoS attack or bug could run up massive AWS bills.

**Workshop Solution**: None - you're exposed to unlimited costs.

**Production Solution**: API throttling, rate limiting, budget alerts, usage plans.

**Where to Learn**: Your course Project 4 covers cost optimization.

### 🚨 Problem 5: Minimal Security
**The Issue**: Anyone can call your API. No authentication, authorization, or input validation.

**Workshop Solution**: Public API with no auth - fine for demos, dangerous for production.

**Production Solution**: API keys, JWT tokens, Cognito, WAF, input sanitization.

**Where to Learn**: Covered across all course projects.

### 🚨 Problem 6: Cold Start Performance
**The Issue**: Lambda cold starts can take 3-10 seconds, causing poor user experience.

**Workshop Solution**: We accept cold starts - users wait.

**Production Solution**: Provisioned concurrency, warm-up strategies, or always-on ECS.

**Where to Learn**: Your course optimization modules.

## Cost Estimate

This workshop deployment will cost approximately:
- **Lambda**: ~$0.20 per 1M requests (within free tier: 1M requests/month)
- **API Gateway**: ~$3.50 per 1M requests (within free tier: 1M requests/month)
- **S3**: ~$0.023 per GB storage (negligible for state files)

**Expected workshop cost**: $0-$1 (within free tier limits)

**Production Reality**: At scale, you'll optimize architecture to reduce costs significantly.

## Troubleshooting

### Lambda Deployment Fails
- Check AWS credentials: `aws sts get-caller-identity`
- Verify region in template.yaml matches your AWS CLI region
- Ensure SAM CLI is installed: `sam --version`

### API Returns 500 Errors
- Check CloudWatch Logs: AWS Console → Lambda → Functions → Your function → Monitor → View logs
- Verify environment variables are set in Lambda configuration
- Test locally first with `test_local.py`

### Agent Times Out
- Increase Lambda timeout in `template.yaml` (max: 900 seconds / 15 minutes)
- Consider async processing for longer tasks (production pattern)

## Next Steps

After completing this module, you'll have:
- ✅ A deployed, publicly accessible AI agent
- ✅ Understanding of AWS Lambda and API Gateway
- ✅ Basic infrastructure-as-code experience
- ✅ A portfolio project to show employers

But you'll also recognize the production gaps. The questions you'll be asking:
- How do I handle long-running tasks?
- How do I make this more reliable?
- How do I monitor and debug production issues?
- How do I control costs at scale?
- How do I secure this properly?

These questions lead naturally to comprehensive production engineering training - which is exactly what the full course provides across 4 complete projects.

## Workshop Outcome

By the end of this module, you should be able to:
1. Package and deploy Python Lambda functions
2. Create public API endpoints with API Gateway
3. Manage state between Lambda invocations
4. Test and debug deployed serverless applications
5. Understand the gaps between "it works" and "production-ready"

The gap between these two is the value proposition of your full course.
