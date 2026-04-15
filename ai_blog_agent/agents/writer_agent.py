import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from agents.models import GROQ_LARGE_MODEL
from agents.utils import extract_text

load_dotenv()


class WriterAgent:
    def __init__(self):
        # Using Groq Llama 3.3 70B for detailed roundups and clean section flow.
        self.llm = ChatGroq(model=GROQ_LARGE_MODEL, groq_api_key=os.getenv("GROQ_API_KEY"))

    def _section_input(self, news_sections):
        if not isinstance(news_sections, dict):
            return "No structured sections were provided."

        lines = []
        for section_name in ("National", "International", "Sports", "Headlines"):
            headlines = news_sections.get(section_name, [])
            if headlines:
                section_lines = "\n".join(f"- {headline}" for headline in headlines)
            else:
                section_lines = "- No headlines available."
            lines.append(f"{section_name}:\n{section_lines}")
        return "\n\n".join(lines)

    def _build_placeholder_roundup(self, title, news_sections):
        section_text = self._section_input(news_sections)
        return (
            f"# {title}\n\n"
            "This is today's India and Tamil Nadu news roundup.\n\n"
            "## National\n\n"
            "A short national news summary would appear here.\n\n"
            "## International\n\n"
            "A short international news summary would appear here.\n\n"
            "## Sports\n\n"
            "A short sports update would appear here.\n\n"
            "## Headlines\n\n"
            "A short headline roundup would appear here.\n\n"
            "### Source headlines\n\n"
            f"{section_text}\n"
        )

    def write_blog(self, topic, news_sections=None, category=None):
        if news_sections is None and isinstance(topic, dict):
            news_sections = topic
            topic = "India and Tamil Nadu Daily News Roundup"

        if os.getenv("MOCK_MODE") == "true":
            return self._build_placeholder_roundup(topic, news_sections)

        # Build a category-aware prompt if a category config is provided
        if category:
            prompt_focus = category.get("prompt_focus", "")
            word_count   = category.get("word_count", "700-1000")
            sections     = category.get("sections", ["National", "International", "Sports", "Headlines"])
            section_text = self._section_input_filtered(news_sections, sections)
            prompt_str   = (
                f"{prompt_focus}\n\n"
                "Write a polished Markdown article.\n"
                "Rules:\n"
                f"- Write {word_count} words.\n"
                "- Use H2 headings for each major section.\n"
                "- Be factual and use only the provided headlines as source material.\n"
                "- Do not repeat headlines verbatim; write proper paragraphs.\n\n"
                f"Title for the article: {topic}\n\n"
                f"Lead story: {{lead_story}}\n\n"
                f"Headline inputs:\n{section_text}"
            )
        else:
            section_text = self._section_input(news_sections)
            prompt_str = (
                "You are a newsroom writer creating a daily roundup for readers in India and Tamil Nadu.\n\n"
                "Write a polished Markdown article with the exact section order below:\n"
                "# {title}\n\nIntro paragraph\n\n"
                "## National\n## International\n## Sports\n## Headlines\n\n"
                "Rules:\n"
                "- Keep the order exactly as written.\n"
                "- Use only the supplied headline inputs and reasonable context from them.\n"
                "- Be factual, neutral, and easy to scan.\n"
                "- Write 700-1000 words.\n"
                "- Do not add extra sections.\n\n"
                "Lead story to anchor the intro: {lead_story}\n\n"
                f"Headline inputs:\n{section_text}"
            )

        print(f"[Writer Agent] Writing: {topic}...")
        try:
            prompt = ChatPromptTemplate.from_template(prompt_str)
            chain  = prompt | self.llm
            response = chain.invoke({
                "title":        topic,
                "lead_story":   topic,
            })
            return extract_text(response.content)
        except Exception as exc:
            print(f"[Writer Agent] LLM unavailable ({exc}); falling back to placeholder.")
            return self._build_placeholder_roundup(topic, news_sections)

    def _section_input_filtered(self, news_sections, sections):
        """Build headline input text using only the requested sections."""
        if not isinstance(news_sections, dict):
            return "No structured sections were provided."
        lines = []
        for section_name in sections:
            headlines = news_sections.get(section_name, [])
            section_lines = "\n".join(f"- {h}" for h in headlines) if headlines else "- No headlines available."
            lines.append(f"{section_name}:\n{section_lines}")
        return "\n\n".join(lines)
