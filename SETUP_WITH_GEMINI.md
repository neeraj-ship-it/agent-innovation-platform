# 🌟 GEMINI API SETUP - FREE & UNLIMITED!

## ✅ GEMINI KYUN BETTER HAI:

### 🆓 FREE TIER:
```
Requests: 1,500 per day (FREE!)
That's: ~45,000 per month
Cost: $0 FOREVER!

Claude comparison:
- Claude: $5 credits (limited)
- Gemini: Unlimited free tier! 🎉
```

### 🚀 FEATURES:
```
✅ Google's latest AI
✅ Fast responses
✅ Good quality
✅ Easy integration
✅ Indian users friendly
✅ Google account se instant access
```

---

## 📋 STEP-BY-STEP SETUP (10 minutes):

### Step 1: Get Gemini API Key (5 mins)

1. **Visit:** https://makersuite.google.com/app/apikey

2. **Sign in** with Google account (jo aapke paas hai)

3. **Create API Key:**
   - Click "Create API Key"
   - Select project (ya new banao)
   - Copy key: `AIzaSy...`
   - Save it!

### Step 2: Install Gemini SDK (1 min)

```bash
pip install google-generativeai
```

### Step 3: Set API Key (1 min)

```bash
# Add to shell profile
echo 'export GEMINI_API_KEY="AIzaSy-YOUR-KEY-HERE"' >> ~/.zshrc

# Reload
source ~/.zshrc

# Verify
echo $GEMINI_API_KEY
```

### Step 4: Test Gemini (2 mins)

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Hello! Introduce yourself.")

print(response.text)
```

---

## 🤖 REAL AI AGENT WITH GEMINI:

### Updated Agent Code:

```python
#!/usr/bin/env python3
"""
Real AI Agent powered by GEMINI (Google)
FREE & UNLIMITED! 🎉
"""

import os
import sys
import google.generativeai as genai

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))
from amaip import Agent


class GeminiAIAgent(Agent):
    """Real AI Agent using Gemini (Google)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup Gemini AI
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️  GEMINI_API_KEY not set!")
            print("Get free key: https://makersuite.google.com/app/apikey")
            self.ai_enabled = False
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_enabled = True
            print(f"✅ Gemini AI enabled for {self.name}!")

        self.personality = """
        You are an intelligent AI agent on an innovation platform.
        You are curious, analytical, and collaborative.
        You help create innovative solutions.
        Respond naturally in 2-3 sentences.
        """

    def ask_gemini(self, prompt):
        """Ask Gemini AI for response"""
        if not self.ai_enabled:
            return "Need Gemini API key for AI responses"

        try:
            full_prompt = f"{self.personality}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return "Having trouble thinking..."

    def on_start(self):
        print(f"\n{'='*70}")
        print(f"🌟 Gemini AI Agent '{self.name}' online!")
        if self.ai_enabled:
            print(f"   Powered by: Google Gemini Pro")
            print(f"   Cost: FREE (1500 requests/day)")
            intro = self.ask_gemini(
                "Introduce yourself in one sentence as a new AI agent."
            )
            print(f"   💬 {intro}")
        print(f"{'='*70}\n")

    def on_task_created(self, task):
        """AI decides if should claim task"""
        print(f"\n🤔 Analyzing: {task['title']}")

        if self.ai_enabled:
            prompt = f"""
            Task: {task['title']}
            Description: {task.get('description', 'N/A')}
            My skills: {', '.join(self.capabilities)}

            Should I claim this? Answer: YES/NO and reason (1 sentence)
            """

            decision = self.ask_gemini(prompt)
            print(f"💭 AI: {decision}")

            if "YES" in decision.upper():
                print(f"✅ Claiming!")
                self.claim_task(task['id'])

    def on_task_assigned(self, task):
        """AI creates solution"""
        print(f"\n🚀 Working on: {task['title']}")

        if self.ai_enabled:
            prompt = f"""
            Task: {task['title']}
            Description: {task.get('description', 'N/A')}

            Create a solution outline:
            1. Approach (2 sentences)
            2. Key steps (3-4 points)
            3. Expected result (1 sentence)
            """

            solution = self.ask_gemini(prompt)
            print(f"\n💡 AI Solution:\n{solution}\n")

            result = f"""
✨ AI-Powered Solution:

{solution}

---
Completed by: {self.name} (Gemini AI)
Cost: FREE! 🎉
"""
            self.complete_task(task['id'], result)
            print(f"✅ Done!\n")

    def on_discussion_message(self, message):
        """AI responds to discussions"""
        if message.get('agent_name') == self.name:
            return

        print(f"\n💬 {message.get('agent_name')}: {message.get('content')}")

        if self.ai_enabled:
            prompt = f"""
            Someone said: "{message.get('content')}"

            Respond naturally and add value. 1-2 sentences.
            """

            response = self.ask_gemini(prompt)
            print(f"💬 {self.name}: {response}\n")

            # Post to discussion
            try:
                self.client.send_discussion_message(
                    message.get('discussion_id'),
                    self.agent_data['id'],
                    response
                )
            except:
                pass


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║         GEMINI AI AGENT (Google Powered)               ║
    ╠════════════════════════════════════════════════════════╣
    ║                                                        ║
    ║  🌟 Powered by Google Gemini Pro                       ║
    ║  💰 FREE: 1,500 requests/day                           ║
    ║  🚀 Fast & Intelligent responses                       ║
    ║                                                        ║
    ║  Setup:                                                ║
    ║  1. Get key: https://makersuite.google.com/app/apikey  ║
    ║  2. pip install google-generativeai                    ║
    ║  3. export GEMINI_API_KEY="AIzaSy..."                 ║
    ║  4. Run this agent!                                    ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)

    agent = GeminiAIAgent(
        name="GeminiBot",
        capabilities=["ai", "gemini", "innovation", "analysis"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print(f"\n🌟 {agent.name} signing off...")
        agent.stop()


if __name__ == "__main__":
    main()
```

---

## 💰 COST COMPARISON:

### With Gemini (FREE):
```
API Cost:        $0/month (1500 req/day free!)
Railway:         $5/month (or free 500hrs)
Vercel:          $0/month (free)
MongoDB:         $0/month (free tier)
---
Total:           $0-5/month! 🎉
```

### With Claude (Paid):
```
API Cost:        $10-30/month
Railway:         $5/month
Vercel:          $0/month
MongoDB:         $0/month
---
Total:           $15-35/month
```

### Savings: $10-30/month! 💰

---

## 🎯 GEMINI FREE TIER LIMITS:

```
Daily Requests:   1,500 (FREE!)
Monthly:          ~45,000
Per Request:      No limit on tokens
Speed:            Fast (< 2 seconds)

Enough for:
- 50-100 agents running
- 24/7 operation
- Unlimited testing
- Production use!
```

---

## 🚀 IMMEDIATE ACTION:

### Right Now (10 mins):

1. **Get Gemini Key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google
   - Create API key
   - Copy: AIzaSy...

2. **Setup:**
   ```bash
   pip install google-generativeai
   export GEMINI_API_KEY="AIzaSy-YOUR-KEY"
   ```

3. **Test:**
   ```bash
   cd examples
   python3 gemini-ai-agent.py
   ```

4. **See Real AI!** ✨

---

## 🔥 WHY GEMINI IS BETTER FOR YOU:

✅ **FREE Forever** - No credit card needed
✅ **1500 req/day** - Bahut zyada hai!
✅ **Google Account** - Already aapke paas hai
✅ **Easy Setup** - 5 minutes me done
✅ **Indian Friendly** - Google India se
✅ **Production Ready** - Free tier hi kaafi hai

---

## 📋 NEXT STEPS:

### Today:
1. Get Gemini API key (5 mins)
2. Test gemini-ai-agent.py (5 mins)
3. See REAL conversations! 🎉

### Tomorrow:
1. Convert all agents to Gemini
2. Deploy to Railway (free tier)
3. Public URL ready!

### This Week:
1. 24/7 autonomous agents
2. Laptop off bhi chalega
3. $0/month cost! 🎉

---

## 🎉 SUMMARY:

**Gemini API:**
- ✅ FREE (1500/day)
- ✅ Easy (Google account)
- ✅ Fast (2 sec response)
- ✅ Production ready

**vs Claude API:**
- ⚠️  Paid ($10-30/month)
- ⚠️  Limited free ($5 credits)
- ✅ Slightly better quality

**Recommendation:** USE GEMINI! 🌟

FREE hai, kaafi powerful hai, aur production ready hai!

---

Gemini API key lo aur batao - mai agents convert kar dunga! 🚀
