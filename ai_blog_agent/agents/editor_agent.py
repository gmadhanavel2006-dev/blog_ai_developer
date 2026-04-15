from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from agents.utils import extract_text
from agents.models import GROQ_LARGE_MODEL

load_dotenv()

class EditorAgent:
    def __init__(self):
        # Using Llama 3 70B via Groq for senior-level editing
        self.llm = ChatGroq(model=GROQ_LARGE_MODEL, groq_api_key=os.getenv("GROQ_API_KEY"))

    def edit_blog(self, draft):
        if os.getenv("MOCK_MODE") == "true":
            return draft + "\n\n(Mock SEO Polish Applied)"

        print("[Editor Agent] Improving and SEO optimizing the blog...")
        try:
            prompt = ChatPromptTemplate.from_template(
                "You are a professional blog editor. Review the following blog post and improve it.\n\n"
                "Tasks:\n"
                "- Fix any grammar or spelling issues.\n"
                "- Improve sentence flow and readability.\n"
                "- Ensure the SEO keywords are naturally integrated.\n"
                "- Make sure the headings are descriptive.\n"
                "- Preserve the section order National, International, Sports, and Headlines if present.\n"
                "- Do not remove or reorder Markdown headings unless needed for clarity.\n\n"
                "Original Blog:\n{draft}"
            )
            chain = prompt | self.llm
            response = chain.invoke({"draft": draft})
            return extract_text(response.content)
        except Exception as e:
            print("[Editor Agent] LLM unavailable; keeping the original draft.")
            return draft
