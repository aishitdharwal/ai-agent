# Deploy Your First AI Agent on AWS - Workshop

Complete workshop materials for teaching production AI agent deployment.

## Workshop Overview

**Duration**: 2.5-3 hours  
**Level**: Intermediate (some Python and basic AWS knowledge helpful)  
**Outcome**: Participants deploy a working, stateful AI agent to AWS with public API access

## What Participants Will Build

A production-accessible Research Assistant Agent that:
- Takes a research topic via HTTP API
- Searches the web for information
- Extracts key findings
- Generates comprehensive summary
- Maintains state throughout the process
- Runs on AWS serverless infrastructure

## Workshop Structure

### Module 1: Building Your First Stateful Agent (45 minutes)
**Location**: `module-1-stateful-agent/`

Learn why state management is critical by building the same agent twice:
1. Naive approach (stateless) - shows the problems
2. LangGraph approach (stateful) - shows the solution

**Key Learning**: Understanding state management in multi-step AI workflows

[→ Module 1 README](./module-1-stateful-agent/README.md)

### Module 2: AWS Deployment (50 minutes)
**Location**: `module-2-aws-deployment/`

Deploy the stateful agent to AWS using:
- AWS Lambda (serverless compute)
- API Gateway (public HTTP endpoint)
- S3 (state storage)
- CloudFormation/SAM (infrastructure as code)

**Key Learning**: Deploying AI agents to production infrastructure

[→ Module 2 README](./module-2-aws-deployment/README.md)

### Module 3: Production Reality Check (15 minutes)

Discussion of production gaps and what's needed for real production systems:
- Async processing for long-running tasks
- Proper state management at scale
- Monitoring and observability
- Cost controls and optimization
- Security and authentication
- Performance and reliability

**Key Learning**: Understanding the gap between "working" and "production-grade"

## Prerequisites

### Required Knowledge
- Python programming (intermediate level)
- Basic understanding of APIs and HTTP
- Familiarity with command line/terminal
- Basic Git knowledge

### Required Accounts
- OpenAI API account ([platform.openai.com](https://platform.openai.com))
- Tavily API account ([tavily.com](https://tavily.com)) - free tier available
- AWS account with admin access ([aws.amazon.com](https://aws.amazon.com))

### Required Software
- Python 3.11 or higher
- pip (Python package manager)
- Git
- AWS CLI configured
- AWS SAM CLI installed

### Setup Instructions

1. **Clone this repository**
```bash
git clone <repository-url>
cd ai-agent
```

2. **Get API Keys**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com (free tier: 1000 searches/month)

3. **Configure AWS**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Region: us-east-1 (or your preferred region)
```

4. **Install SAM CLI**
- macOS: `brew tap aws/tap && brew install aws-sam-cli`
- Windows/Linux: [Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Running the Workshop

### For Participants

**Module 1 Setup:**
```bash
cd module-1-stateful-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python run_agent.py --agent both --topic "Your topic"
```

**Module 2 Setup:**
```bash
cd module-2-aws-deployment
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python test_local.py  # Test locally first
./deploy.sh  # Deploy to AWS
```

### For Instructors

- **Module 1 Teaching Guide**: [module-1-stateful-agent/TEACHING_GUIDE.md](./module-1-stateful-agent/TEACHING_GUIDE.md)
- **Module 2 Teaching Guide**: [module-2-aws-deployment/TEACHING_GUIDE.md](./module-2-aws-deployment/TEACHING_GUIDE.md)

Each teaching guide includes:
- Detailed lesson plan with timing
- Key teaching moments
- Common questions and answers
- Workshop setup checklist
- Connection to course upsell

## Workshop Outcomes

By the end of this workshop, participants will be able to:

✅ **Build stateful AI agents** using LangGraph  
✅ **Deploy to AWS** using Lambda, API Gateway, and S3  
✅ **Create public APIs** that anyone can access  
✅ **Manage infrastructure** using CloudFormation/SAM  
✅ **Debug deployed applications** using CloudWatch  
✅ **Understand production gaps** and what's needed for real systems

## What's NOT Covered (Course Content)

This workshop intentionally uses simplified patterns to enable quick deployment. Production systems require:

🔴 **Async Processing**: Handling long-running tasks beyond Lambda limits  
🔴 **Production State Management**: DynamoDB, Redis, proper transaction handling  
🔴 **Observability**: Structured logging, tracing, metrics, alerts  
🔴 **Cost Optimization**: Profiling, caching, right-sizing resources  
🔴 **Security**: Authentication, authorization, input validation  
🔴 **Reliability**: Error handling, retries, circuit breakers  

These topics are covered in depth across four production-grade projects in the full course.

## Workshop Resources

### Code
- Complete, working implementations of both modules
- Deployment templates ready to use
- Test scripts for validation

### Documentation
- README files for each module
- Teaching guides for instructors
- Troubleshooting guides

### Support Materials
- Architecture diagrams
- Production gap analysis
- Cost estimation worksheets

## Cost Expectations

**Workshop Costs** (staying within AWS free tier):
- Lambda: Free tier covers 1M requests/month
- API Gateway: Free tier covers 1M requests/month
- S3: Negligible storage costs
- **Expected**: $0-$1 for the workshop

**Cleanup Instructions** (to avoid ongoing costs):
```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name <your-stack-name>

# Empty and delete S3 bucket
aws s3 rb s3://<bucket-name> --force
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError" when running agents**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**"AWS credentials not configured"**
- Run `aws configure` and enter your credentials
- Test with `aws sts get-caller-identity`

**"SAM CLI not found"**
- Install SAM CLI following [official guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Verify with `sam --version`

**"Lambda deployment fails"**
- Check AWS credentials are valid
- Ensure you have permissions to create CloudFormation stacks
- Verify region consistency across CLI and template

**"API returns 500 errors"**
- Check CloudWatch Logs in AWS Console
- Verify environment variables are set
- Test locally first with `test_local.py`

### Getting Help

For workshop-specific questions:
1. Check the module README files
2. Review teaching guides for common issues
3. Check CloudWatch logs for deployment issues

## Next Steps After Workshop

**For Participants:**
1. Experiment with the deployed API
2. Modify the agent to research different topics
3. Try deploying variations of the architecture
4. Review the production gaps document
5. Consider enrolling in the full course for production patterns

**For Instructors:**
1. Collect feedback on workshop timing
2. Note questions that came up (add to teaching guides)
3. Track conversion to full course
4. Iterate on content based on participant success

## Course Connection

This workshop demonstrates foundational deployment skills and reveals production complexity. The full course builds on this foundation with four complete projects covering:

**Project 1: Production State & Memory**
- DynamoDB for structured state
- Redis for session management
- Conversation history and context

**Project 2: Async Agent Workflows**
- SQS for job queues
- Step Functions for orchestration
- ECS Fargate for long-running tasks

**Project 3: Observability & Debugging**
- Structured logging patterns
- Distributed tracing with X-Ray
- Custom metrics and dashboards

**Project 4: Optimization & Scaling**
- Performance profiling
- Caching strategies
- Cost optimization

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Acknowledgments

Built for AI Classroom by Aishit Dharwal

---

**Ready to get started?** Jump into [Module 1](./module-1-stateful-agent/README.md) and build your first stateful agent!
