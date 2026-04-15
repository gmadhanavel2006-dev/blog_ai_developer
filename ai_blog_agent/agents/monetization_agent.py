from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from agents.utils import extract_text
from agents.models import GROQ_SMALL_MODEL

load_dotenv()


class MonetizationAgent:
    def __init__(self):
        # Using Llama 3 8B via Groq - Fast and efficient for simple tasks
        self.llm = ChatGroq(model=GROQ_SMALL_MODEL, groq_api_key=os.getenv("GROQ_API_KEY"))

    def add_affiliate_links(self, blog_content):
        if os.getenv("MOCK_MODE") == "true":
            return (
                blog_content
                + "\n\n---\n\n### Related Reading\n"
                "- Government press releases\n"
                "- Tamil Nadu state updates\n"
                "- India-wide reporting on the same story"
            )

        print("[Monetization Agent] Adding related reading and source suggestions...")
        try:
            prompt = ChatPromptTemplate.from_template(
                "You are a newsroom editor. Analyze the following India and Tamil Nadu news blog post and suggest 3 neutral, "
                "non-promotional references or source ideas that readers might find useful. Avoid affiliate language and sales pitches.\n\n"
                "Format the output as a Markdown section titled '### Related Reading'.\n\n"
                "Blog Content:\n{content}"
            )

            chain = prompt | self.llm
            response = chain.invoke({"content": blog_content})

            related_section = extract_text(response.content)

            # Append the related-reading section to the end of the blog
            updated_blog = f"{blog_content}\n\n---\n\n{related_section}"
            return updated_blog
        except Exception:
            print("[Monetization Agent] LLM unavailable; adding a simple related-reading section.")
            return (
                blog_content
                + "\n\n---\n\n### Related Reading\n"
                "- Government press releases\n"
                "- Tamil Nadu state updates\n"
                "- India-wide reporting on the same story"
            )
