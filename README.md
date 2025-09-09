#CrowdWisdomTrading AI Agent Sentiment Analyzer



![Python](https://img.shields.io/badge/Pythonwork sentiment across X (Twitter) creators. Built using Python, CrewAI, and LiteLLM, this project delivers structured sentiment insights, market signal extraction, and report automation for 10+ financial influencers.

###🤖 Live Demo

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1528a792-e0b5-4d2c-802b-b1cb3d69e3bb" />


##🚀 Core Functionality


Multi-Agent Pipeline: Modular CrewAI agents handle scraping, sentiment analysis, ticker extraction, and reporting.

Financial Market Focus: Extracts signals specifically from finance Twitter/X users (200+ tweets/creator).

AI-Powered Sentiment: Analyzes and scores sentiment (bullish, bearish, neutral) on every tweet.

Ticker Extraction: Finds and classifies stock symbols and market direction per mention.

Automated Reporting: Generates clean PDF and JSON summaries for decision support.

Guardrails Included: Resilient error handling and validation at every step.

##🛠 Technology Stack


Framework: CrewAI (latest)

LLM Orchestration: LiteLLM + Gemini 2.0 Flash

Report Generation: ReportLab

Schema Validation: Pydantic

Data Source: BrightData MCP, customizable for real/production use

##⚡ Getting Started


Prerequisites
Python 3.10 or newer

API key for Gemini (set as environment variable)

CrewAI, LiteLLM, ReportLab, and dependencies

1. Clone the Repository
bash
git clone https://github.com/your-org/crowdwisdom-ai-agent.git
cd crowdwisdom-ai-agent
2. Install Dependencies
bash
pip install crewai litellm reportlab numpy pydantic
3. Configure Your API Key
Linux/macOS:

bash
export GEMINI_API_KEY="YOUR_API_KEY_HERE"
Windows:

powershell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
(Never commit secrets to code!)

4. Run the AI Pipeline
bash
python main.py
PDF and JSON reports will be generated for each creator in the current directory.

##📦 Project Structure


text
├── main.py                # Main workflow launcher
├── tools.py               # Custom CrewAI tools (collect, analyze, extract, report)
├── agents.py              # Multi-agent definitions and configuration
├── requirements.txt       # Dependency file
├── output/                # Generated PDF and JSON reports
└── README.md              # Documentation
📊 Sample Output
output/@TraderA_report.pdf

output/@TraderA_data.json

Each file contains sentiment statistics, ticker signals, and market direction for each influencer.

##📈 Features & Benefits


Real-time, structured market sentiment from X (Twitter)

Extensible with YouTube, images, and true RAG flows

Robust, production-ready code with clear modularity

Supports reporting and analysis for trading, research, and risk management

##📋 License


Licensed under the MIT License — see the LICENSE file for details.

##🤝 About


Designed and engineered for the CrowdWisdomTrading AI Agent Internship Assessment.
For any questions or feedback, contact gilad@crowdwisdomtrading.com.

Happy trading and analyzing!
