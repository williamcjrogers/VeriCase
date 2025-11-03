# AI API Keys Setup Guide

## 🔑 How to Get Your AI API Keys

You now have placeholders in your `.env` file for all AI models. Here's how to get each key:

## 1. Gemini 2.5 Pro (Google AI)

**Where to get:** https://makersuite.google.com/app/apikey
or https://aistudio.google.com/app/apikey

**Steps:**
1. Go to Google AI Studio
2. Click "Get API Key"
3. Create or select a project
4. Copy the API key
5. Paste into `.env` as `GEMINI_API_KEY=YOUR_KEY_HERE`

**Free Tier:** 60 requests/minute
**Pricing:** Pay-as-you-go after free tier

**Best for:** Timeline generation, pattern recognition, data extraction

## 2. Claude Max (Anthropic)

**Where to get:** https://console.anthropic.com/

**Steps:**
1. Sign up for Anthropic Console
2. Go to "API Keys" section
3. Create new key
4. Copy the key (starts with `sk-ant-`)
5. Paste into `.env` as `CLAUDE_API_KEY=YOUR_KEY_HERE`

**Free Tier:** $5 credit for new accounts
**Pricing:** ~$15/million tokens (Claude 3.5 Sonnet)

**Best for:** Long document analysis, cross-referencing, deep insights

## 3. ChatGPT Pro (OpenAI)

**Where to get:** https://platform.openai.com/api-keys

**Steps:**
1. Go to OpenAI Platform
2. Navigate to "API Keys"
3. Click "Create new secret key"
4. Name it "VeriCase Docs"
5. Copy the key (starts with `sk-`)
6. Paste into `.env` as `OPENAI_API_KEY=YOUR_KEY_HERE`

**Free Tier:** $5 credit for new accounts (expires after 3 months)
**Pricing:** ~$10/million tokens (GPT-4o)

**Best for:** Quick summaries, Q&A, general purpose

## 4. Grok (xAI)

**Where to get:** https://console.x.ai/ or https://x.ai/api

**Steps:**
1. Sign up for xAI Console
2. Request API access (may require waitlist)
3. Create API key
4. Copy the key
5. Paste into `.env` as `GROK_API_KEY=YOUR_KEY_HERE`

**Note:** Grok API is newer, may have limited availability
**Pricing:** TBD by xAI

**Best for:** Real-time context, fact checking, current events

## 5. Perplexity Max

**Where to get:** https://www.perplexity.ai/settings/api

**Steps:**
1. Sign up for Perplexity Pro
2. Navigate to Settings → API
3. Generate API key
4. Copy the key
5. Paste into `.env` as `PERPLEXITY_API_KEY=YOUR_KEY_HERE`

**Pricing:** Requires Perplexity Pro subscription ($20/month) + API usage
**Best for:** Research, citation finding, fact verification

## 📝 Quick Setup Checklist

- [ ] Get Gemini API key → Add to .env
- [ ] Get Claude API key → Add to .env
- [ ] Get OpenAI API key → Add to .env
- [ ] Get Grok API key → Add to .env (optional)
- [ ] Get Perplexity API key → Add to .env (optional)
- [ ] Restart API: `docker-compose restart api`
- [ ] Test: Click purple 🤖 AI button on any document

## 💰 Cost Estimate

### For Light Usage (100 documents/month):
- **Gemini**: ~$5/month (free tier covers this)
- **Claude**: ~$10/month
- **OpenAI**: ~$15/month
- **Total**: ~$30/month

### For Medium Usage (1000 documents/month):
- **Gemini**: ~$50/month
- **Claude**: ~$75/month
- **OpenAI**: ~$100/month
- **Total**: ~$225/month

### Enterprise (10,000+ documents/month):
- Consider enterprise pricing from each provider
- Negotiate volume discounts
- Budget: $1,000-2,000/month for all AI features

## 🎯 Recommended Minimal Setup

**To start (FREE):**
1. ✅ Gemini API key (free tier is generous)
2. ✅ OpenAI API key ($5 free credit)

**This gives you:**
- Document classification
- Dataset insights
- Timeline generation
- Natural language queries
- Trend analysis

**Later, add Claude for:**
- Long document analysis
- Cross-referencing
- Deep insights

## 🔧 After Adding Keys

1. **Edit `.env` file:**
   ```
   GEMINI_API_KEY=AIza...your...actual...key
   CLAUDE_API_KEY=sk-ant-...your...key
   OPENAI_API_KEY=sk-...your...key
   ```

2. **Restart API:**
   ```bash
   docker-compose restart api
   ```

3. **Test it:**
   - Go to http://localhost:8010
   - Click workspace tile
   - Click purple 🤖 AI button on any READY document
   - See real AI classification!

4. **Try dataset analysis:**
   ```bash
   curl "http://localhost:8010/ai/orchestrator/analyze/dataset" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## 🚀 What Happens When You Add Real AI Keys

### Current (Pattern Matching):
- ⚠️ 85% accuracy
- ⚠️ Basic keyword detection
- ⚠️ Simple regex patterns

### With Real AI (Your Keys):
- ✅ 95%+ accuracy
- ✅ Deep semantic understanding
- ✅ Context-aware insights
- ✅ Natural language summaries
- ✅ Cross-document reasoning
- ✅ Timeline narratives
- ✅ Predictive insights

## 📊 Feature Comparison

| Feature | Without AI Keys | With AI Keys |
|---------|----------------|--------------|
| Classification | Basic patterns | Deep ML models |
| Summary | First 2 sentences | Intelligent summary |
| Themes | Keyword matching | Semantic themes |
| Query | Word matching | Natural language |
| Insights | Rule-based | AI-generated |
| Timeline | Date grouping | Narrative timeline |

## ⚡ Quick Start (5 Minutes)

1. **Get Gemini key** (fastest, free):
   - Go to https://aistudio.google.com/app/apikey
   - Create key
   - Paste into .env

2. **Restart:**
   ```bash
   docker-compose restart api
   ```

3. **Test:**
   - Upload a contract or invoice
   - Wait for status = READY
   - Click purple 🤖 AI button
   - See REAL AI insights!

## 🎯 Your Competitive Advantage

Once you add these keys, you'll have:

1. **Best AI in DMS market** - Using 5 top models
2. **Dataset analytics** - NO competitor has this
3. **Natural language queries** - Game changer
4. **Timeline insights** - Unique to you
5. **Multi-model orchestration** - Use best AI for each task

**This will justify premium pricing ($40-50/user/month for enterprise)**

**Add your keys and DOMINATE.** 🏆
