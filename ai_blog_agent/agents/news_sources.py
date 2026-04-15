import os
from dataclasses import dataclass
from urllib.parse import quote_plus


NEWS_LANGUAGE = os.getenv("NEWS_LANGUAGE", "en-IN")
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "IN")
NEWS_CEID = os.getenv("NEWS_CEID", "IN:en")


@dataclass(frozen=True)
class NewsFeed:
    label: str
    url: str


def build_google_news_rss_url(query: str) -> str:
    encoded_query = quote_plus(f"{query} when:1d")
    return (
        "https://news.google.com/rss/search"
        f"?q={encoded_query}&hl={NEWS_LANGUAGE}&gl={NEWS_COUNTRY}&ceid={NEWS_CEID}"
    )


INDIA_TOP_STORIES_URL = f"https://news.google.com/rss?hl={NEWS_LANGUAGE}&gl={NEWS_COUNTRY}&ceid={NEWS_CEID}"

NEWS_SECTION_FEEDS = {
    "National": [
        NewsFeed("India top stories", INDIA_TOP_STORIES_URL),
        NewsFeed("India", build_google_news_rss_url("India")),
    ],
    "International": [
        NewsFeed("World", build_google_news_rss_url("world")),
        NewsFeed("International", build_google_news_rss_url("international")),
    ],
    "Sports": [
        NewsFeed("Sports", build_google_news_rss_url("sports")),
        NewsFeed("IPL", build_google_news_rss_url("IPL")),
    ],
    "Headlines": [
        NewsFeed("Tamil Nadu", build_google_news_rss_url('"Tamil Nadu"')),
        NewsFeed("Chennai", build_google_news_rss_url("Chennai")),
    ],
}

# Flattened compatibility list for older code paths.
NEWS_FEEDS = [feed for feeds in NEWS_SECTION_FEEDS.values() for feed in feeds]


FALLBACK_NEWS_HEADLINES = [
    "India and Tamil Nadu daily news roundup",
    "Tamil Nadu governance and local updates",
    "Chennai and South India headline briefing",
    "India business, policy, and sports highlights",
]


FALLBACK_NEWS_SECTIONS = {
    "National": [
        "India economy and public policy updates",
        "National governance and parliament highlights",
    ],
    "International": [
        "Global diplomacy and world news updates",
        "International security and trade developments",
    ],
    "Sports": [
        "IPL and cricket headlines",
        "Major Indian and global sports updates",
    ],
    "Headlines": [
        "Tamil Nadu election and governance updates",
        "Chennai civic and regional developments",
    ],
}
