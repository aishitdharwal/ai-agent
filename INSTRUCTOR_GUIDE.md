# Workshop Instructor Quick Reference

Essential information for running the "Deploy Your First AI Agent on AWS" workshop.

## Pre-Workshop Checklist (1 Week Before)

### Technical Prep
- [ ] Test complete workshop flow on your own machine
- [ ] Deploy your own version to AWS as backup demo
- [ ] Verify all API keys work (OpenAI, Tavily)
- [ ] Check AWS account limits (Lambda concurrency, etc.)
- [ ] Prepare alternative examples if default topics fail
- [ ] Test with 2-3 different research topics
- [ ] Ensure you can access CloudWatch logs quickly

### Materials Prep
- [ ] Share GitHub repo link with participants
- [ ] Send prerequisites email (API keys, AWS account, installations)
- [ ] Prepare whiteboard/slides for architecture diagrams
- [ ] Have production gaps diagram ready to show
- [ ] Print reference cards (optional but helpful)

### Environment Prep
- [ ] Test screen sharing/projection
- [ ] Verify stable internet connection
- [ ] Have backup 4G/5G hotspot ready
- [ ] Open all necessary AWS Console tabs in advance
- [ ] Bookmark CloudWatch Logs for quick access

---

## Workshop Timeline (Total: 2.5-3 hours)

### Module 1: Stateful Agents (45 min)
- 0:00-0:05 → Introduction & setup verification
- 0:05-0:20 → Build naive agent (live coding)
- 0:20-0:35 → Build stateful agent (live coding)
- 0:35-0:45 → Compare both, discuss state management

**Key Moments:**
- 0:15 → Show naive agent breaking (the "aha moment")
- 0:30 → Explain `ResearchState` TypedDict (critical concept)
- 0:40 → Connect to production needs

### Break (10 min)
- 0:45-0:55 → Bathroom break, troubleshooting help

### Module 2: AWS Deployment (50 min)
- 0:55-1:05 → Architecture overview & component explanation
- 1:05-1:10 → Local testing walkthrough
- 1:10-1:25 → Deploy to AWS (includes wait time)
- 1:25-1:35 → Test deployed API
- 1:35-1:45 → Production gaps discussion (upsell setup)

**Key Moments:**
- 1:00 → Draw architecture diagram (visual learning)
- 1:15-1:25 → Use deployment wait time for discussion
- 1:30 → Show cold vs warm start difference
- 1:40 → Bridge to course with production gaps

### Wrap-up & Course Intro (15 min)
- 1:45-1:50 → Recap what was built
- 1:50-2:00 → Course overview and enrollment info
- 2:00-2:10 → Q&A

---

## Critical Teaching Moments

### The "State Management Aha Moment" (Module 1, ~0:15)
**Setup:** Run naive agent with a query that requires multiple steps

**What to Show:**
- Agent works for simple cases
- Gets confused with complex queries
- No way to track progress
- Difficult to debug

**The Pivot:**
"This works... sometimes. But notice we have NO idea what's happening inside. Let me show you what proper state management looks like."

**Why This Works:**
Participants see the problem firsthand before you present the solution.

---

### The "Infrastructure as Code" Moment (Module 2, ~1:00)
**Setup:** Open template.yaml side-by-side with AWS Console

**What to Show:**
```yaml
ResearchAgentFunction:
  Type: AWS::Serverless::Function
  Properties:
    Timeout: 300
    MemorySize: 512
```

**Then show in Console:** Same values appear in Lambda configuration

**The Teaching Point:**
"This YAML file IS your infrastructure. Change timeout to 600? Just edit this file and redeploy. No clicking through console. This is version-controlled, reviewable, reproducible infrastructure."

---

### The "Cold Start Reality" Moment (Module 2, ~1:30)
**Setup:** Make two API calls back-to-back

**What to Show:**
- First call: 8 seconds
- Second call: 2 seconds

**The Teaching Point:**
"Same code, 4x performance difference. This is the Lambda cold start tax. For demos, fine. For production UX, unacceptable. Production requires either provisioned concurrency or different architecture."

---

### The "Production Gap Bridge" (Module 2, ~1:40)
**Setup:** Pull up PRODUCTION_GAPS.md, walk through each gap

**What to Say:**
"What you built today WORKS. It's real. It's on AWS. You should feel proud. But getting from 'works' to 'production-grade' means solving these six problems systematically. That's what the course teaches."

**Why This Works:**
You've established credibility by helping them succeed. Now you're showing them the path forward.

---

## Common Failure Points & Solutions

### Problem: Participants stuck on Python setup
**Solution:** Have a working environment ready to share screen
**Prevention:** Send detailed setup instructions 3 days before

### Problem: API keys don't work
**Solution:** Have backup keys ready (your own testing accounts)
**Prevention:** Test all keys morning of workshop

### Problem: AWS deployment fails
**Solution:** Show your pre-deployed version as backup
**Prevention:** Document common error messages and solutions

### Problem: Internet connection issues during deployment
**Solution:** Pre-deploy and walk through using existing deployment
**Prevention:** Have cellular hotspot as backup

### Problem: Participants fall behind
**Solution:** Have "catch-up points" where fast folks can help slow folks
**Prevention:** Share complete working code at start

### Problem: Different Python versions cause errors
**Solution:** Emphasize virtual environments, have requirements.txt tested
**Prevention:** Specify exact Python version in prerequisites

---

## Handling Different Experience Levels

### For Beginners (Struggling with Concepts):
- Slow down on state management explanation
- Use more analogies (state = memory, Lambda = function that runs on request)
- Pair them with more experienced participants
- Focus on getting ONE thing working, skip optimizations

### For Advanced Users (Bored or Ahead):
- Challenge them: "How would you add X feature?"
- Ask them to help others
- Discuss production tradeoffs in more depth
- Point them to advanced course content

### For Mixed Groups:
- Use "fast track" and "thorough track" approach
- Fast track: Skip explanations, just build
- Thorough track: Detailed explanations
- Reconvene at key milestones

---

## Timing Adjustments

### Running Behind Schedule:
**Module 1 Cuts:**
- Skip running naive agent multiple times (just once)
- Show stateful agent code instead of live coding it
- Reduce comparison discussion time

**Module 2 Cuts:**
- Pre-deploy and just demonstrate (skip live deployment)
- Skip local testing (go straight to deployed version)
- Shorten production gaps discussion

**Minimum Workshop:** Can compress to 2 hours by showing instead of doing

### Running Ahead of Schedule:
**Module 1 Extensions:**
- Add additional agent node (e.g., fact-checking step)
- Discuss LangGraph conditional edges
- Show graph visualization

**Module 2 Extensions:**
- Demonstrate API with different tools (Postman, curl, Python)
- Show CloudWatch metrics/dashboards
- Live modify and redeploy

---

## Upsell Strategy

### The Psychology:
1. **Make them successful** (they deployed something real!)
2. **Show them the gap** (production is different)
3. **Position course as bridge** (from success to mastery)

### What NOT to Do:
- ❌ Don't be pushy or salesy
- ❌ Don't diminish what they built
- ❌ Don't make course sound mandatory
- ❌ Don't oversell or promise too much

### What TO Do:
- ✅ Be genuinely helpful
- ✅ Show enthusiasm for production engineering
- ✅ Share real war stories from production
- ✅ Frame course as natural next step
- ✅ Offer clear value proposition

### The Bridge Statement:
"You've taken the first step - you can build and deploy AI agents. The course is about taking that foundation and building production-grade systems. It's not more of the same - it's solving the problems you encountered today at production scale across four complete projects."

---

## Course Transition Framing

### Position Workshop as "Chapter 1"
"Today was Chapter 1: Getting Started. The course is Chapters 2-5: Production Mastery."

### Highlight Project-Based Learning
"Not more lectures. Four complete projects you build from scratch:
1. Build a conversational agent with memory (DynamoDB + Redis)
2. Build an async research system (SQS + Step Functions)
3. Build a monitored production API (CloudWatch + X-Ray)
4. Optimize and scale it (reduce costs 70%)"

### Emphasize Hands-On Approach
"Same format as today - you build, I guide, we debug together. By the end you have four portfolio projects."

### Address ROI
"The course pays for itself if you:
- Land one job because you can answer 'deployed to production' in interviews
- Avoid one AWS bill surprise by understanding cost optimization
- Save your team one week of debugging with proper observability"

---

## Q&A Preparation

### Technical Questions

**Q: "Why Lambda instead of EC2/ECS?"**
A: "Lambda is fastest path to deployment. ECS gives more control but more complexity. Course covers when to choose each."

**Q: "How do I add authentication?"**
A: "API Gateway supports API keys, Lambda authorizers, Cognito. We covered the basics today; course covers production auth patterns."

**Q: "What about other LLM providers (Anthropic, local models)?"**
A: "Same patterns apply. Swap OpenAI for Anthropic/local model - the architecture stays the same. Agent code changes, deployment doesn't."

**Q: "Can this handle real production load?"**
A: "Today's architecture works for demos and prototypes. Production needs the six improvements we discussed - that's the course content."

### Business Questions

**Q: "How much does production deployment cost?"**
A: "Workshop setup: <$1/month. Production: $30-70/month optimized, $200-500/month unoptimized. Course teaches optimization."

**Q: "How long to go from workshop to production?"**
A: "Depends on requirements. With course knowledge: 2-4 weeks for typical agent. Without: 2-3 months of trial and error."

**Q: "Is this enough to get a job?"**
A: "Workshop shows you CAN deploy. Jobs want you to deploy WELL. Course gives you production stories to tell in interviews."

---

## Post-Workshop Follow-Up

### Immediately After (Same Day):
- [ ] Share workshop recording (if recorded)
- [ ] Send link to complete code repository
- [ ] Share PRODUCTION_GAPS.md reference
- [ ] Provide course enrollment link

### Next Day:
- [ ] Send thank you email
- [ ] Share additional resources (blog posts, docs)
- [ ] Offer office hours for questions
- [ ] Course early-bird discount (if applicable)

### One Week Later:
- [ ] Follow up on course enrollment
- [ ] Share success stories from other students
- [ ] Answer any lingering questions
- [ ] Final course reminder

---

## Success Metrics

### Workshop Success:
- ✅ 80%+ participants deploy working agent
- ✅ All participants understand state management concept
- ✅ Positive feedback on teaching quality
- ✅ Questions indicate genuine interest in learning more

### Upsell Success:
- 🎯 Target: 15-25% conversion to course
- 🎯 Metric: Participants request course info
- 🎯 Indicator: Questions about production patterns

### Long-term Success:
- 📈 Workshop completers stay engaged with content
- 📈 Students share workshop experience
- 📈 Organic referrals from participants

---

## Emergency Protocols

### If Live Demo Fails:
1. Stay calm (participants understand tech fails)
2. Switch to pre-deployed backup
3. Explain what would have happened
4. Show CloudWatch logs to diagnose
5. Use as teaching moment: "This is why we need monitoring!"

### If AWS Has Outage:
1. Check status.aws.amazon.com
2. Pivot to Module 1 deep dive
3. Show architecture and code walkthrough
4. Promise to share deployed version later
5. Extend Q&A and production discussions

### If You Run Out of Time:
1. Prioritize deployment over explanation
2. Share detailed README for self-study
3. Offer follow-up office hours
4. Focus on production gaps discussion (upsell)

---

## Final Reminders

### Before Workshop Starts:
- Deep breath. You know this material.
- Remember: teaching is performance + knowledge
- Engage participants, don't lecture at them
- Mistakes are okay - model debugging mindset

### During Workshop:
- Check understanding frequently
- Adjust pace based on room
- Celebrate small wins
- Stay enthusiastic

### After Workshop:
- Collect feedback immediately
- Note what worked / didn't work
- Update materials for next time
- Follow up on promises

**You've got this!** 🚀
