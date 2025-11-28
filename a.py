Core Architecture
Tender PDF / Portal Feed
   ↓
[Tender Understanding Agent]
   ↓
[Tender Intelligence Hub (Crew.AI Orchestrator)]
   ├── Product Matching Agent
   ├── Competitor Analysis Agent
   ├── Price & Risk Agent
   ├── Approval Agent
   ├── Business Impact Agent
   ├── Document Generator Agent
   ├── RFP Question Assistant
   ├── Salesforce Connector Agent
   └── Translation Agent (multi-language)
   ↓
Salesforce Tender__c, Tender_Line_Item__c
   ↓
Final PDF + Notification to Sales / Regulatory / Supply Teams

🤖 3. Agent List and Descriptions
Agent Name	Role	Description	Input	Output
🧠 Tender Understanding Agent	Core Extractor	Reads tender (PDF/Word/Excel) and extracts key fields — tender ID, authority, drugs, quantity, delivery terms, deadlines	Tender document	JSON with structured tender fields
🧬 Product & Molecule Matching Agent	Match products	Maps tender drugs to internal product catalog and identifies equivalent molecules	Extracted tender data + product master	Mapped list of SKUs, formulations, strengths
⚔️ Competitor Analysis Agent	Market insights	Fetches competitor pricing and win/loss data from Salesforce or external APIs	Product and region	Competitor summary + score
💰 Pricing Optimization Agent	Predict optimal bid	Uses historical data and pricing elasticity models to suggest best bid range	Tender + historical tender data	Suggested bid price, confidence score
⚖️ Risk & Compliance Agent	Approve / reject logic	Classifies tenders by probability of success and regulatory eligibility	Tender + product data	Risk score, recommendation (Go / No-Go)
📄 Document Generator Agent	Auto-generate tender response	Builds proposal document (Word/PDF) using templates	Tender + pricing + approval	Ready-to-submit file
💬 RFP Question Assistant	Q&A on tenders	Allows team to ask questions like “What are the eligibility criteria?”	Tender context	Textual answers
🌐 Translation Agent	Multi-language support	Translates tenders/responses into required languages (e.g., English ↔ French, Arabic)	Tender text	Translated versions
🔗 Salesforce Connector Agent	Sync with CRM	Creates/updates Tender__c and related records, attaches generated files	All agent outputs	Salesforce records updated
🌍 Business Impact (Nalya) Agent	Impact projection	Predicts business outcomes: “Will we win?”, “Which region benefits?”, “Revenue forecast”	Tender summary + pricing data + history	Region impact map, probability of new business
