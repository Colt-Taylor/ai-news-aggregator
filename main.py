# -*- coding: utf-8 -*-
"""
AI News Aggregator - Main Entry Point

Multi-agent system that collects, summarizes, categorizes,
analyzes and reports the latest news using CrewAI and DeepSeek.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

from crewai import Crew, Process, LLM

from agents import (
    create_scraper_agent,
    create_summarizer_agent,
    create_categorizer_agent,
    create_analyst_agent,
    create_reporter_agent,
)
from tasks import (
    create_scraping_task,
    create_summarization_task,
    create_categorization_task,
    create_analysis_task,
    create_reporting_task,
)
from tools import AINewsScraper


def create_llm():
    """Create and configure the DeepSeek LLM."""
    return LLM(
        model="deepseek/deepseek-flash",
        base_url="https://api.deepseek.com/v1",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7,
    )


def setup_output_directory():
    """Ensure the outputs directory exists."""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def run_news_aggregator():
    """Run the AI News Aggregator crew."""
    print("=" * 60)
    print("     AI NEWS AGGREGATOR")
    print("     Powered by CrewAI + DeepSeek")
    print("=" * 60)
    print()

    # Setup
    setup_output_directory()

    # Create LLM
    llm = create_llm()

    # Create scraper tool
    scraper_tool = AINewsScraper()

    # Create agents
    print("[*] Initializing agents...")
    scraper_agent = create_scraper_agent(llm, tools=[scraper_tool])
    summarizer_agent = create_summarizer_agent(llm)
    categorizer_agent = create_categorizer_agent(llm)
    analyst_agent = create_analyst_agent(llm=llm)
    reporter_agent = create_reporter_agent(llm)
    print("[+] Agents initialized!")
    print()

    # Create tasks (注意顺序！)
    print("[*] Creating tasks...")
    scraping_task = create_scraping_task(scraper_agent)
    summarization_task = create_summarization_task(
        agent=summarizer_agent,
        context=[scraping_task]
    )
    categorization_task = create_categorization_task(
        agent=categorizer_agent,
        context=[summarization_task]
    )
    analysis_task = create_analysis_task(
        agent=analyst_agent,
        context=[categorization_task]
    )
    reporting_task = create_reporting_task(
        agent=reporter_agent,
        context=[categorization_task, analysis_task]
    )
    print("[+] Tasks created!")
    print()

    # Assemble crew
    crew = Crew(
        agents=[
            scraper_agent,
            summarizer_agent,
            categorizer_agent,
            analyst_agent,
            reporter_agent,
        ],
        tasks=[
            scraping_task,
            summarization_task,
            categorization_task,
            analysis_task,
            reporting_task,
        ],
        process=Process.sequential,
        verbose=True,
    )
    print("[+] Crew assembled!")
    print()

    print("=" * 60)
    print("     STARTING NEWS AGGREGATION")
    print(f"     Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    try:
        result = crew.kickoff()

        print()
        print("=" * 60)
        print("     AGGREGATION COMPLETE")
        print("=" * 60)
        print()
        print(f"[+] Report saved to: outputs/daily_report.md")
        print()
        print("---- FINAL REPORT ----")
        print(result)

        return result

    except KeyboardInterrupt:
        print("\n[!] Aggregation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error during aggregation: {e}")
        raise


def main():
    """Main entry point."""
    try:
        run_news_aggregator()
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()