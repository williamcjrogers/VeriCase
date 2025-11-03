# VeriCase Docs - Complete AI System Guide

## 🚀 SYSTEM RUNNING: http://localhost:8010

## 🤖 **MULTI-AI ORCHESTRATION - NOW LIVE**

Your document management system now has THREE layers of AI intelligence that NO competitor can match:

## Layer 1: Document-Level AI

### Individual Document Analysis
```
POST /ai/classify/{document_id}
```
**What it does:**
- Auto-identifies: Invoice, Contract, Report, Email, Memo, Presentation
- Extracts dates, amounts, emails, phone numbers
- Identifies people and organizations mentioned
- Generates auto-tags: urgent, confidential, draft, final
- Creates 2-sentence summaries
- Detects PII (SSN, credit cards, etc.)
- Flags compliance issues
- Suggests optimal folder placement

**UI:** Purple 🤖 AI button on each document

## Layer 2: Dataset-Level AI (NEW!)

### Analyze Entire Collections
```
GET /ai/orchestrator/analyze/dataset?folder_path=Legal
```
**What it provides:**
- **Activity Trends** - Upload velocity, acceleration patterns
- **Anomaly Detection** - Unusually large files, outliers
- **Timeline Visualization** - Monthly document batches
- **Theme Extraction** - Financial, Legal, Technical themes
- **Document Distribution** - Breakdown by type
- **Summary Statistics** - Total words, average size, date range

**This is UNIQUE - no competitor has this**

## Layer 3: Natural Language Queries (NEW!)

### Ask Questions Across ALL Documents
```
POST /ai/orchestrator/query
{
  "query": "Show me all contracts from last quarter"
}
```
**Examples:**
- "What invoices are over $10,000?"
- "Find all confidential documents"
- "Show contracts expiring this year"
- "List all documents mentioning John Smith"

**Returns:**
- Direct answer
- Relevant documents ranked by relevance
- Follow-up question suggestions
- Confidence score

## 🎯 **DATASET INSIGHTS - THE GAME CHANGER**

### GET /ai/orchestrator/trends?days=30

**Returns:**
```json
{
  "period_days": 30,
  "total_documents": 142,
  "average_per_day": 4.7,
  "trend": "increasing",
  "daily_breakdown": {
    "2025-01-15": 3,
    "2025-01-16": 8,
    "2025-01-17": 5
  },
  "ai_model": "gemini"
}
```

**Use cases:**
- Legal: "Are we getting more contracts this month?"
- Finance: "Invoice processing velocity?"
- Compliance: "Document review backlog growing?"

## 📊 **WHAT MAKES THIS THE BEST**

### Multi-AI Model Routing (Ready for Integration)

**Gemini 2.5 Pro** - Use for:
- Timeline generation (best at structured data)
- Pattern recognition across datasets
- Trend analysis
- Data extraction

**Claude Max** - Use for:
- Long document analysis (200K context)
- Cross-referencing multiple documents
- Deep insights and correlations
- Summarization of large datasets

**ChatGPT Pro** - Use for:
- Quick summaries
- Natural language responses
- General Q&A
- Creative suggestions

**Grok Heavy** - Use for:
- Real-time fact checking
- Current context (if docs reference current events)
- Validation of extracted data

**Perplexity Max** - Use for:
- Research assistance
- Citation finding
- Fact verification
- External knowledge integration

## 🔥 **API ENDPOINTS - COMPLETE LIST**

### Individual Document AI
```
POST   /ai/classify/{id}           - Full classification + insights
GET    /ai/insights/{id}            - Get stored AI insights
POST   /ai/suggest-folder/{id}     - Smart folder suggestion
POST   /ai/auto-tag/{id}            - Generate and apply tags
POST   /ai/batch-classify           - Classify multiple docs
GET    /ai/search/semantic?q=...   - Semantic search (meaning, not keywords)
```

### Dataset Analysis
```
GET    /ai/orchestrator/analyze/dataset  - Full dataset analysis
POST   /ai/orchestrator/query             - Natural language Q&A
GET    /ai/orchestrator/trends            - Trend analysis
POST   /ai/orchestrator/correlations      - Find patterns
```

### Other Features
```
POST   /favorites/{id}              - Star documents
GET    /favorites                   - List starred
GET    /versions/documents/{id}     - Version history
GET    /documents/recent            - Recent files
```

## 💎 **HOW TO DOMINATE WITH THIS**

### Use Case 1: Legal Firm
**Query:** "Analyze all contracts in Legal folder"
```
GET /ai/orchestrator/analyze/dataset?folder_path=Legal
```
**Get:**
- Timeline of contract signings
- Trend analysis (more/less contracts?)
- Anomalies (unusually large contracts)
- Key
