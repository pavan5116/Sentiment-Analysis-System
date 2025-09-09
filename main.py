import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool, BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import numpy as np
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import dotenv
# Set environment variable for API key
API=os.getdotenv
os.environ["GEMINI_API_KEY"] = API

# Mock TwitterScraper if brightdata_mcp is unavailable
def get_user_tweets(handle, limit):
    sample_tweets = [
        {"id": "1", "text": "$AAPL looking bullish after strong earnings report! Price target $200 #stocks",
         "timestamp": "2025-08-30T10:00:00Z"},
        {"id": "2", "text": "Bearish on $TSLA - production concerns mounting. Might see a pullback to $180",
         "timestamp": "2025-08-30T11:00:00Z"},
        {"id": "3", "text": "Market volatility increasing. $SPY showing resistance at current levels",
         "timestamp": "2025-08-30T12:00:00Z"},
        {"id": "4", "text": "Great opportunity in $NVDA - AI sector expansion continues",
         "timestamp": "2025-08-30T13:00:00Z"},
        {"id": "5", "text": "Economic data release tomorrow could impact $QQQ significantly",
         "timestamp": "2025-08-30T14:00:00Z"}
    ]
    return sample_tweets[:min(limit, len(sample_tweets))]

# --------------- Input Schemas ---------------
class CollectTweetsInput(BaseModel):
    handle: str = Field(..., description="Twitter handle to collect tweets from")
    count: int = Field(default=5, description="Number of tweets to collect")

class AnalyzeSentimentInput(BaseModel):
    tweet_data: str = Field(..., description="JSON string containing tweet data")

class ExtractTickersInput(BaseModel):
    sentiment_data: str = Field(..., description="JSON string containing sentiment data")

class GenerateReportInput(BaseModel):
    final_data: str = Field(..., description="JSON string containing final processed data")

# --------------- Custom Tools ---------------
class CollectTweetsTool(BaseTool):
    name: str = "collect_tweets"
    description: str = "Scrape tweets from mock"
    args_schema: Type[BaseModel] = CollectTweetsInput
    def _run(self, handle: str, count: int = 5) -> str:
        tweets = get_user_tweets(handle, limit=count)
        result = {"creator_handle": handle, "tweets": tweets}
        return json.dumps(result)

class AnalyzeSentimentTool(BaseTool):
    name: str = "analyze_sentiment"
    description: str = "Classify sentiment as positive, negative, or neutral (prompt handled by LLM)"
    args_schema: Type[BaseModel] = AnalyzeSentimentInput
    def _run(self, tweet_data: str) -> str:
        data = json.loads(tweet_data)
        tweets = data.get("tweets", [])
        enriched = []
        for t in tweets:
            text = t["text"].lower()
            if any(word in text for word in ['bullish', 'buy', 'strong', 'up', 'positive', 'great', 'opportunity']):
                score = 0.7
                subject = "bullish"
            elif any(word in text for word in ['bearish', 'sell', 'weak', 'down', 'negative', 'concerns', 'pullback']):
                score = -0.7
                subject = "bearish"
            else:
                score = 0.0
                subject = "neutral"
            t_new = {**t, "sentiment_score": score, "subject": subject}
            enriched.append(t_new)
        return json.dumps({"creator_handle": data["creator_handle"], "tweets": enriched})

class ExtractTickersTool(BaseTool):
    name: str = "extract_tickers"
    description: str = "Extract potential tickers and label direction"
    args_schema: Type[BaseModel] = ExtractTickersInput
    def _run(self, sentiment_data: str) -> str:
        data = json.loads(sentiment_data)
        tweets = data.get("tweets", [])
        final = []
        for t in tweets:
            tickers = re.findall(r'\\$([A-Z]{1,5})', t["text"])
            score = t.get("sentiment_score", 0)
            if score > 0.1:
                direction = "bullish"
            elif score < -0.1:
                direction = "bearish"
            else:
                direction = "neutral"
            t_full = {**t, "tickers": tickers, "direction": direction}
            final.append(t_full)
        return json.dumps({"creator_handle": data["creator_handle"], "tweets": final})

class GenerateReportTool(BaseTool):
    name: str = "generate_report"
    description: str = "Create PDF report from processed data."
    args_schema: Type[BaseModel] = GenerateReportInput
    def _run(self, final_data: str) -> str:
        data = json.loads(final_data)
        creator_handle = data.get("creator_handle", "Unknown")
        tweets = data.get("tweets", [])
        sentiment_scores = [t.get('sentiment_score', 0) for t in tweets]
        directions = [t.get('direction', 'neutral') for t in tweets]
        all_tickers = []
        for t in tweets:
            all_tickers.extend(t.get('tickers', []))
        summary = {
            "creator_handle": creator_handle,
            "total_tweets": len(tweets),
            "average_sentiment": float(np.mean(sentiment_scores)) if sentiment_scores else 0.0,
            "tickers_mentioned": list(set(all_tickers)),
            "bullish_count": directions.count("bullish"),
            "bearish_count": directions.count("bearish"),
            "neutral_count": directions.count("neutral")
        }
        pdf_filename = f"{creator_handle.replace('@', '')}_report.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, f"Sentiment Analysis Report for {creator_handle}")
        c.setFont("Helvetica", 12)
        y = 720
        for key, val in summary.items():
            if key != "creator_handle":
                c.drawString(50, y, f"{key}: {val}")
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 750
        c.save()
        json_filename = f"{creator_handle.replace('@', '')}_data.json"
        with open(json_filename, 'w') as f:
            json.dump(data, f, indent=2)
        return f"Report generated: {pdf_filename} | Data saved: {json_filename}"

# --------------- Tool Instances ---------------
collect_tweets_tool = CollectTweetsTool()
analyze_sentiment_tool = AnalyzeSentimentTool()
extract_tickers_tool = ExtractTickersTool()
generate_report_tool = GenerateReportTool()

# --------------- LLM Instance ---------------
llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=os.environ["GEMINI_API_KEY"],
    temperature=0.1
)

# --------------- Agent Definitions ---------------
data_agent = Agent(
    role="X Data Collector",
    goal="Scrape tweets for a given creator and return structured data",
    backstory="An expert at gathering social media data for sentiment analysis projects.",
    tools=[collect_tweets_tool],
    llm=llm,
    verbose=True
)

sentiment_agent = Agent(
    role="Sentiment Analyzer",
    goal="Analyze tweet sentiment and identify main topics",
    backstory="A data scientist who specializes in understanding online opinions and market sentiment.",
    tools=[analyze_sentiment_tool],
    llm=llm,
    verbose=True
)

ticker_agent = Agent(
    role="Ticker Extractor",
    goal="Identify stock tickers and determine market direction from tweets",
    backstory="A financial analyst with expertise in extracting trading signals from social media.",
    tools=[extract_tickers_tool],
    llm=llm,
    verbose=True
)

report_agent = Agent(
    role="Report Generator",
    goal="Compile analysis results and create comprehensive PDF reports",
    backstory="A professional report writer specializing in financial analysis documentation.",
    tools=[generate_report_tool],
    llm=llm,
    verbose=True
)

# --------------- Task Definitions ---------------
task_collect = Task(
    description="Collect tweets from the specified creator handle: {handle}.",
    agent=data_agent,
    expected_output="JSON string containing creator handle and list of tweets with metadata"
)

task_sentiment = Task(
    description="Analyze sentiment scores and extract subjects from the collected tweet data.",
    agent=sentiment_agent,
    context=[task_collect],
    expected_output="JSON string with tweets enriched with sentiment_score and subject fields"
)

task_ticker = Task(
    description="Extract financial tickers and determine bullish/bearish direction from analyzed tweets.",
    agent=ticker_agent,
    context=[task_sentiment],
    expected_output="JSON string with tweets enriched with tickers and direction fields"
)

task_report = Task(
    description="Generate a comprehensive PDF report summarizing all analysis results.",
    agent=report_agent,
    context=[task_ticker],
    expected_output="Confirmation message with PDF filename and data file location"
)

def main():
    creators = ["@TraderA", "@TraderB", "@TraderC", "@TraderD", "@TraderE"]
    print("🚀 Starting CrowdWisdomTrading AI Agent Analysis")
    print(f"📊 Processing {len(creators)} creators")
    for handle in creators:
        print(f"\n=== Processing {handle} ===")
        try:
            crew = Crew(
                agents=[data_agent, sentiment_agent, ticker_agent, report_agent],
                tasks=[task_collect, task_sentiment, task_ticker, task_report],
                process=Process.sequential,
                verbose=True
            )
            result = crew.kickoff(inputs={"handle": handle})
            print(f"✅ Completed processing for {handle}")
            print(f"📄 Result: {result}")
        except Exception as e:
            print(f"❌ Error processing {handle}: {str(e)}")
            continue
    print(f"\n🎉 Analysis completed! Check the generated PDF reports and JSON data files.")

if __name__ == "__main__":
    main()

