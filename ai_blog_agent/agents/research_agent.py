import os
import xml.etree.ElementTree as ET

import requests
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from agents.models import GROQ_SMALL_MODEL
from agents.news_sources import (
    FALLBACK_NEWS_HEADLINES,
    FALLBACK_NEWS_SECTIONS,
    NEWS_SECTION_FEEDS,
)
from agents.utils import extract_text

load_dotenv()


class ResearchAgent:
    def __init__(self):
        # Using Llama 3.1 8B on Groq for modern speed and reliability
        self.llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=os.getenv("GROQ_API_KEY"))

    def _parse_feed_headlines(self, xml_payload):
        root = ET.fromstring(xml_payload)
        headlines = []
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            if title:
                headlines.append(title)
        return headlines

    def _dedupe(self, headlines):
        seen = set()
        unique = []
        for headline in headlines:
            cleaned = " ".join(headline.split()).strip()
            key = cleaned.lower()
            if cleaned and key not in seen:
                seen.add(key)
                unique.append(cleaned)
        return unique

    def get_daily_sections(self):
        """Pull daily headlines for the roundup sections in the requested order."""
        print("[Research Agent] Finding India, international, sports, and Tamil Nadu headlines...")
        if os.getenv("MOCK_MODE") == "true":
            return {key: list(value) for key, value in FALLBACK_NEWS_SECTIONS.items()}

        headers = {"User-Agent": "Mozilla/5.0"}
        sections = {}
        for section_name, feeds in NEWS_SECTION_FEEDS.items():
            section_topics = []
            for feed in feeds:
                try:
                    response = requests.get(feed.url, timeout=15, headers=headers)
                    response.raise_for_status()
                    feed_topics = self._parse_feed_headlines(response.content)
                    print(
                        f"[Research Agent] Collected {len(feed_topics)} headlines from {feed.label} for {section_name}."
                    )
                    section_topics.extend(feed_topics[:5])
                except Exception:
                    print(
                        f"[Research Agent] Could not fetch {feed.label}; continuing with the remaining feeds."
                    )

            unique_topics = self._dedupe(section_topics)
            sections[section_name] = unique_topics[:4] or list(FALLBACK_NEWS_SECTIONS[section_name])

        return sections

    def get_trending_topics(self):
        """Compatibility helper that returns the flattened headline list."""
        sections = self.get_daily_sections()
        flattened = []
        for section_name in ("National", "International", "Sports", "Headlines"):
            flattened.extend(sections.get(section_name, []))
        return self._dedupe(flattened) or list(FALLBACK_NEWS_HEADLINES)

    def select_best_topic(self, topics):
        """Pick the best lead story for the roundup, preferring national news first."""
        if isinstance(topics, dict):
            topic_list = []
            for section_name in ("National", "International", "Sports", "Headlines"):
                topic_list.extend(topics.get(section_name, []))
        else:
            topic_list = list(topics)

        if os.getenv("MOCK_MODE") == "true":
            return topic_list[0] if topic_list else FALLBACK_NEWS_HEADLINES[0]

        print(f"[Research Agent] Analyzing {len(topic_list)} headlines...")
        try:
            prompt = ChatPromptTemplate.from_template(
                "Given the following current news headlines for a daily roundup, "
                "select the single best lead story for an India and Tamil Nadu blog post. "
                "Prefer the strongest national headline first, then other broadly relevant items. "
                "Return ONLY the headline title text. Do not return a list, do not use numbering, and do not include the source name.\n\n"
                "Headlines:\n{topics}"
            )
            chain = prompt | self.llm
            response = chain.invoke({"topics": "\n".join(topic_list)})
            return extract_text(response.content).strip().split('\n')[0].replace('"', '')
        except Exception:
            print("[Research Agent] LLM unavailable; falling back to the first headline.")
            return topic_list[0] if topic_list else FALLBACK_NEWS_HEADLINES[0]


if __name__ == "__main__":
    agent = ResearchAgent()
    sections = agent.get_daily_sections()
    best = agent.select_best_topic(sections)
    print(f"Best Topic: {best}")
