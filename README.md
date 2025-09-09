CrowdWisdomTrading AI Agent
![Python](https://img.shields.io/badge/PythonILL AI-driven sentiment analysis and reporting on financial social media, built with CrewAI, LiteLLM, and the latest multi-agent orchestration workflows.

🤖 Live Demo
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/66a1b3dc-2e04-4536-8876-224956c4e771" />


🚀 Core Functionality
Automated Data Collection: Scrape 200+ tweets each from 10 X (Twitter) creators

Sentiment Analysis: Assigns sentiment scores (-1 = bearish, +1 = bullish), detects subjects, and market mood

Ticker Extraction: Identifies stock symbols in text with AI and regex backup

Comprehensive Reporting: Generates both PDF and machine-readable JSON outputs

Agentic Pipeline: Extensible multi-agent flow for robust AI automation via CrewAI

🛠️ Technology Stack
Orchestration Framework: CrewAI (latest)

LLM Provider: LiteLLM & Gemini 2.0 Flash

PDF Generation: ReportLab

Schema Validation: Pydantic

Analytics: numpy, regex

Python Version: 3.10+

🏁 Getting Started
Prerequisites
Python 3.10 or newer

(Optional) Access to Gemini LLM (API key)

1. Clone the Repository
bash
git clone https://github.com/your-org/crowdwisdom-ai-agent.git
cd crowdwisdom-ai-agent
2. Install Dependencies
bash
pip install crewai litellm reportlab numpy pydantic
3. Configure Your API Key
Set your Gemini API key as an environment variable.
On macOS/Linux:

bash
export GEMINI_API_KEY="YOUR_API_KEY_HERE"
On Windows:

powershell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
Do not hard-code your keys into the script.

4. Run the Application
Execute the main pipeline script:

bash
python main.py
The system will loop through the X creators, collect tweet data, analyze sentiment, extract financial intelligence, and generate reports.

📊 Output
PDF Reports: e.g., TraderA_report.pdf for human analysis and presentation

JSON Files: e.g., TraderA_data.json for data science and further processing

📁 Project Structure
text
├── main.py                  # Main execution script
├── requirements.txt         # Dependency list
└── README.md                # Project documentation
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🤝 About
Created by the CrowdWisdomTrading team as part of the AI Agent Internship Assessment.

🌟For any questions, please contact Gilad, CEO: gilad@crowdwisdomtrading.com
